# NIPT Timing and Fetal Anomaly Analysis

This repository presents a 2025 mathematical modeling project on non-invasive prenatal testing (NIPT). It studies the relationship between gestational age, maternal BMI, and the Y-chromosome fraction; estimates testing times for BMI groups; and explores anomaly classification for female-fetus records. This is a research exercise, not a clinical decision tool.

## Files

All files are at the repository root so the project can be uploaded together through GitHub's web interface.

| File | Purpose |
| --- | --- |
| `nipt-timing-and-anomaly-analysis-report.pdf` | Full original report (Chinese) |
| `01_male_regression.ipynb` | Correlation and regression for the Y-chromosome fraction |
| `02_bmi_timing.ipynb` | BMI grouping and risk-based testing time |
| `02_bmi_bootstrap.ipynb` | Bootstrap uncertainty for group timings |
| `03_multifactor_timing.ipynb` | Timing with multiple factors and longitudinal records |
| `04_female_logistic.ipynb` | Logistic anomaly model and calibration check |
| `prepare_inputs.py` | Builds local notebook inputs from the original competition workbook |
| `female_anomaly_model.py` | Optional MLP, LightGBM, or XGBoost classifier |
| `*.csv` | Selected aggregate result tables |

The notebooks retain the competition dataset's original Chinese field names and a few Chinese labels so that the calculations are traceable. The repository guide and file names are in English.

## Data and privacy

The source project contained row-level pregnancy and testing records, including subject codes, dates, and health outcomes. These records are not included in this public version. Only aggregate tables and the report are provided. Do not upload real patient records or generated row-level predictions to a public repository.

For a full rerun, obtain the 2025 C-problem NIPT workbook from an authorized source and save it as `data/raw/attachment.xlsx`. It needs sheets named `男胎检测数据` and `女胎检测数据` with the original Chinese field names.

## Run locally

Use Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python prepare_inputs.py --input data/raw/attachment.xlsx
jupyter lab
```

The preparation command creates five local workbooks in `data/processed/`: `male_filtered.xlsx`, `bmi_first_threshold.xlsx`, `male_first_threshold.xlsx`, `male_longitudinal.xlsx`, and `female_filtered.xlsx`. Run the numbered notebooks with Jupyter's working directory set to the repository root. Keep the raw and processed data outside Git when publishing your own work.

For the female-fetus classifier:

```bash
python female_anomaly_model.py \
  --input data/processed/female_filtered.xlsx \
  --pred outputs/female_predictions.csv \
  --report outputs/female_model_report.txt
```

The default model is an MLP. To use `--model lgbm` or `--model xgb`, install `requirements-optional.txt`. Run `python female_anomaly_model.py --help` for additional options.

## Approach and limits

The analysis filters low-GC records, converts gestational week/day notation to days, examines male-fetus Y-fraction relationships, and searches candidate weeks using chosen costs for an early failed test and delayed testing. Bootstrap resampling describes variability. Female-fetus records are studied with a logistic model and an optional classifier based on recorded aneuploidy labels.

Results depend on the original competition data, preprocessing, and chosen loss weights. Repeated measurements from the same subject require subject-level validation for predictive claims. The recommended weeks and scores have not been clinically validated; see the original report for assumptions and interpretation.
