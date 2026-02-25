# Sample data method

To support deployment on free hosting, we include a smaller raw sample file.

## raw sample
- file: `data/raw/mb_sales_sample_stratified.csv`
- method: stratified random sampling
- strata: `year × fuel type`
- target size: about 120,000 rows
- random seed: `551`

This keeps trend balance across years and fuel categories.

## processed sample tables
The script also builds these processed files in `data/processed/`:
- `sample_sales_by_year_fuel.csv`
- `sample_top_models.csv`
- `sample_color_by_year.csv`
- `sample_price_hp_grid.csv`
- `sample_strata_summary.csv`

## reproduce
If full raw data exists at `data/raw/mercedes_benz_sales_2020_2025.csv`, run:

```bash
python src/build_samples.py
```
