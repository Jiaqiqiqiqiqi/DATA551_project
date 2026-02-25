# Mercedes-Benz Sales Insights Dashboard (2020-2025)

Deployed app link: **to be updated after render deployment**

This project is an interactive dashboard for Mercedes-Benz sales data from 2020 to 2025.

## Why this project
We are a student data consulting team.
Our main users are regional dealership managers.
They need simple evidence for inventory and display decisions.

## What users can do
- check fuel type trend by year
- check top-selling models
- compare price and horsepower patterns
- check top color choices
- filter data by year, model, fuel type, turbo, price, and horsepower
- use one reset button to clear all filters

## Dashboard layout
Main panels in the app:
- fuel type sales trend
- top models by sales
- price vs horsepower
- top colors

## Local setup
### 1) create environment (optional)
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) install packages
```bash
pip install -r requirements.txt
```

### 3) run app
```bash
python src/app.py
```

Before running, put the raw dataset at:
`data/raw/mercedes_benz_sales_2020_2025.csv`

Then open the local link in your browser.

## Project structure
```text
DATA551_Project_G11_SUN_YAO_ZHAO/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── reports/
├── doc/
├── requirements.txt
├── Procfile
└── README.md
```

## For contributors
Please read `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` first.
You can open an issue for bugs, ideas, or feature requests.
If you want to help, open a pull request to `main`.

## Team files
- proposal: `proposal.md`
- team contract: `team-contract.md`
- milestone submission link: `canvas-submission.md`
