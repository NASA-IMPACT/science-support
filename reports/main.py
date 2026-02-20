#!/usr/bin/env python3
"""
Query GitHub API for commits to repositories in parallel.
"""

from github import Github, Auth
from datetime import datetime
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pandas as pd
from config import (
    get_time_range,
    get_current_pi,
    get_contributors_for_pi,
    get_repos_x_contributors_for_pi,
)
from settings import TOKEN_ENV_VAR


def get_commits_for_repo_author(
    g: Github,
    owner: str,
    repo: str,
    author: str,
    start_date: datetime,
    end_date: datetime,
) -> List[dict]:
    """
    Query GitHub API for commits by a specific author in a repo.

    Returns list of commit detail dicts (not commit objects) to avoid
    thread safety issues with PyGithub objects.
    """
    try:
        repository = g.get_repo(f"{owner}/{repo}")
        commits = repository.get_commits(
            author=author, since=start_date, until=end_date
        )

        # Group commits by PR
        prs = []
        pr_commits = []
        standalone_commits = []

        for commit in commits:
            pulls = commit.get_pulls()
            if pulls.totalCount == 1:
                if (number := pulls[0].number) not in prs:
                    pr_commits.append(commit)
                    prs.append(number)
            elif pulls.totalCount == 0:
                standalone_commits.append(commit)

        # Extract details immediately (avoid returning PyGithub objects)
        results = []
        for commit in pr_commits + standalone_commits:
            results.append(
                {
                    "sha": commit.sha,
                    "message": commit.commit.message.split("\n")[0],
                    "author": commit.commit.author.name,
                    "committer": commit.commit.committer.name,
                    "url": commit.html_url,
                    "total_changes": commit.stats.total if commit.stats else 0,
                    "organization": owner,
                    "repository": repo,
                }
            )
        return results
    except Exception as e:
        print(f"  Error processing {owner}/{repo} for {author}: {e}")
        return []


def get_resolved_for_contributor(
    g: Github,
    tasks: List[tuple],
    contributor: str,
    start_date: datetime,
    end_date: datetime,
) -> List[dict]:
    """
    Query GitHub API for closed issues and PRs that a contributor was involved with across repos.

    "Involved" means the contributor was the author, assignee, mentioned, or commented.
    Uses the GitHub search API with the `involves:` qualifier and multiple `repo:` filters
    in a single query, then returns only results matching the configured repos.

    Returns list of issue/PR detail dicts (not PyGithub objects) to avoid
    thread safety issues.
    """
    try:
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")
        repo_filters = " ".join(f"repo:{owner}/{repo}" for owner, repo, _ in tasks)
        base_query = (
            f"{repo_filters} "
            f"involves:{contributor} "
            f"closed:{start_str}..{end_str}"
        )

        issues = g.search_issues(f"is:issue {base_query}")
        prs = g.search_issues(f"is:pr {base_query} -author:{contributor}")

        results = []
        for item in [*issues, *prs]:
            # item.repository is a Repository object with owner.login and name
            item_owner = item.repository.owner.login
            item_repo = item.repository.name
            if (item_owner, item_repo, contributor) not in tasks:
                continue
            is_pr = item.pull_request is not None
            results.append(
                {
                    "number": item.number,
                    "title": item.title,
                    "type": "PR" if is_pr else "Issue",
                    "state": item.state,
                    "author": item.user.login if item.user else None,
                    "url": item.html_url,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                    "organization": item_owner,
                    "repository": item_repo,
                    "contributor": contributor,
                }
            )
        return results
    except Exception as e:
        print(f"  Error fetching issues/PRs for {contributor}: {e}")
        return []


def main(token: str = None, pi: str = None, max_workers: int = 10):
    """
    Query GitHub for commits using parallel requests.

    Args:
        token: GitHub personal access token
        pi: Optional PI to filter repos/contributors (e.g., "pi-26.1").
            If None, uses current PI based on today's date.
        max_workers: Number of parallel threads (default 10)
    """
    # Default to current PI if not specified
    if pi is None:
        pi = get_current_pi()

    time_range = get_time_range(pi)
    if not time_range:
        raise ValueError(f"No date range found for PI: {pi}")

    time_start = datetime.strptime(time_range[0], "%Y%m%d")
    time_end = datetime.strptime(time_range[1], "%Y%m%d")

    # Get repos tasks for the PI
    contributors = get_contributors_for_pi(pi)
    tasks = get_repos_x_contributors_for_pi(pi)
    print(
        f"PI: {pi} ({time_start.strftime('%Y-%m-%d')} to {time_end.strftime('%Y-%m-%d')})"
    )
    print(f"  {len(tasks)} repos x contributors")

    if len(tasks) < 1:
        raise ValueError("No repos x contributors found in config.")

    print(
        f"Querying {len(tasks)} repo×contributor combinations with {max_workers} workers..."
    )

    all_commits = []
    all_resolved = []

    # Use thread pool for parallel API calls
    # Each thread gets its own Github client to avoid rate limit issues
    def make_client():
        if token:
            return Github(auth=Auth.Token(token))
        return Github()

    def process_commits_task(task):
        owner, repo, username = task
        g = make_client()
        try:
            return get_commits_for_repo_author(
                g, owner, repo, username, time_start, time_end
            )
        finally:
            g.close()

    def process_resolved_task(username):
        g = make_client()
        try:
            return get_resolved_for_contributor(
                g, tasks, username, time_start, time_end
            )
        finally:
            g.close()

    completed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        commits_futures = {executor.submit(process_commits_task, task): task for task in tasks}
        resolved_issues_futures = {executor.submit(process_resolved_task, username): username for _, username in contributors}

        for future in as_completed(commits_futures):
            completed += 1
            print(f"  Progress: {completed}/{len(tasks) + len(contributors)}")
            commits = future.result()
            all_commits.extend(commits)
        
        for future in as_completed(resolved_issues_futures):
            completed += 1
            print(f"  Progress: {completed}/{len(tasks)+ len(contributors)}")
            resolved_issues = future.result()
            all_resolved.extend(resolved_issues)

    print(f"Found {len(all_commits)} authored commits")
    print(f"Found {len(all_resolved)} resolved issues/PRs")

    df = pd.DataFrame(all_commits)
    csv_filename = f"output/{pi}-authored-commits.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Saved to {csv_filename}")

    df_resolved = pd.DataFrame(all_resolved).drop_duplicates(subset=["number", "organization", "repository"])
    resolved_filename = f"output/{pi}-resolved-issues-prs.csv"
    df_resolved.to_csv(resolved_filename, index=False)
    print(f"Saved to {resolved_filename}")


if __name__ == "__main__":
    token = os.environ.get(TOKEN_ENV_VAR) or os.environ.get("GITHUB_TOKEN")
    main(token=token)
