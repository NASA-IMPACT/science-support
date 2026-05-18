"""Team-specific settings for the VEDA Science Support reporting system."""

from dse_oss_reports.settings import TeamSettings

TOKEN_ENV_VAR = "GH_PAT"

TEAM_SETTINGS = TeamSettings(
    team_name="Science Support",
    team_display_name="VEDA/EODC Science Support",
    github_org="NASA-IMPACT",
    github_repo="science-support",
    site_url="nasa-impact.github.io/science-support",
    objectives_page_url="https://nasa-impact.github.io/science-support/objectives",
    token_env_var=TOKEN_ENV_VAR,
)
