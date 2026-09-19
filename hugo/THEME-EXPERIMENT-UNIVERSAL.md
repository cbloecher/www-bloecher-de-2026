# Universal theme experiment

Branch: `theme-universal`

The baseline implementation remains available as `themes/bloecher-custom`.

## Setup

```bash
cd hugo
bash tools/setup-universal-theme.sh
hugo server
```

Universal is intentionally not vendored into this repository. The setup script checks out the upstream theme into the ignored directory `themes/hugo-universal-theme`.

Blöcher-specific visual overrides are in `static/css/custom.css`.

The existing content is reused unchanged so the comparison focuses on theme/layout behavior.
