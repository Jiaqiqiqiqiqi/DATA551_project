# Contributing Guidelines

Thank you for helping this project.

## Scope
This project builds an interactive dashboard for Mercedes-Benz sales insights.

## Team members
- ZHAO ZIHAO
- JI HAOZHONG
- YAO JIAQI

## Code of conduct
Please read and follow [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## Before you start
1. Pull the newest `main` branch.
2. Check open issues and pick one task.
3. Create a branch from `main`.

Branch name examples:
- `feature/fuel-trend-widget`
- `fix/filter-reset-bug`
- `docs/update-readme`

## How to open an issue
Please include:
- clear title
- short background
- expected behavior
- current behavior
- steps to reproduce (for bugs)
- screenshot or log (if needed)

## How to open a pull request
1. Push your branch.
2. Open a PR to `main`.
3. Add a short PR description with:
   - what changed
   - why it changed
   - how to test
4. Request at least one review before merge.

## Commit style
Use short and clear commit messages.

Examples:
- `add fuel trend chart callback`
- `fix year slider range bug`
- `update milestone2 reflection text`

## Review checklist
- app runs locally
- no sensitive data added
- raw large data is not committed
- docs are updated if behavior changed

## Large file rule
Do not commit large raw data files to GitHub.
Keep local raw csv in `data/raw/`.
