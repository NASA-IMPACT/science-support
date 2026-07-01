- Ovals - Sources
- Rectangles - Docker Container images
- Green Rectangles - Images deployed on MAAP or VEDA

```mermaid
---
config:
  theme: redux
  layout: dagre
---
flowchart LR
    n1["Conda-Forge"] --> n6["Pangeo"] & n16["Pangeo Tensorflow"] & n17["Pangeo PyTorch"] & n11["Upstream Fixes"] & n18["Repo2docker"]
    n2["POSIT R Binary Mirror"] --> n7["Rocker"] & n18
    n7 --> n8["py-rocket"] & n13["VEDA R*<br>(TBD replaced by MAAP R)"]
    n6 --> n8 & n9["VEDA Pangeo"] & n14["ISCE3"]
    n9 --> n10["MAAP Pangeo"]
    n11 --> n9
    n4["pypi"] --> n10 & n20["Geotrees/lasR"]
    n8 --> n12["MAAP R"]
    n5["R Universe"] --> n12
    n3["CRAN"] --> n12
    n19["Ubuntu"] --> n18
    n18 --> n20

    n1@{ shape: rounded}
    n11@{ shape: hex}
    n18@{ shape: lean-r}
    n2@{ shape: rounded}
    n4@{ shape: rounded}
    n20@{ shape: rect}
    n5@{ shape: rounded}
    n3@{ shape: rounded}
    n19@{ shape: rect}
    style n16 fill:#C8E6C9
    style n17 fill:#C8E6C9
    style n9 fill:#C8E6C9
    style n14 fill:#C8E6C9
    style n10 fill:#C8E6C9
    style n20 fill:#C8E6C9
    style n12 fill:#C8E6C9
    click n9 "https://github.com/NASA-IMPACT/pangeo-notebook-veda-image"
    click n10 "https://github.com/MAAP-Project/maap-workspaces/tree/main/base_images/2i2c/pangeo"
    click n12 "https://github.com/MAAP-Project/maap-workspaces/tree/main/base_images/2i2c/r"
    click n14 "https://github.com/MAAP-Project/maap-workspaces/tree/main/base_images/2i2c/isce3"
    click n16 "https://github.com/MAAP-Project/maap-workspaces/tree/main/base_images/2i2c/tensorflow2"
    click n17 "https://github.com/MAAP-Project/maap-workspaces/tree/main/base_images/2i2c/pytorch"
    click n20 "https://github.com/GEO-TREES/workspace_images/tree/lasR"
```
