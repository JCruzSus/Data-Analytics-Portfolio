# 03 — Employee Attrition Analysis & Prediction

## Business scenario

An HR analytics team wants to understand employee attrition patterns and evaluate whether a classification model can identify records associated with elevated attrition risk.

## Dataset

Use the IBM HR Analytics Employee Attrition & Performance sample dataset, commonly distributed as `WA_Fn-UseC_-HR-Employee-Attrition.csv`. It contains 1,470 employee records and a binary `Attrition` field in the commonly circulated version.

Download the CSV from the Kaggle dataset page: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset  
Place the file at `data/WA_Fn-UseC_-HR-Employee-Attrition.csv`.

This dataset is a public educational sample, not a representative sample of the current labor market or any specific employer.

## Questions

1. What is the overall attrition rate in the sample?
2. How does attrition vary across tenure, overtime, role, and satisfaction measures?
3. Which features are useful for prediction on held-out data?
4. How do precision, recall, ROC-AUC, and confusion matrices compare across models?

## Run

```bash
pip install -r ../../requirements.txt
python src/analyze.py
```

The script checks for the dataset, performs exploratory summaries, trains baseline logistic regression and random forest models, and writes evaluation outputs under `outputs/`.

## Methodology

- Separate target from predictors.
- Split train/test data with stratification.
- Preprocess numeric and categorical columns within a scikit-learn pipeline to avoid leakage.
- Compare logistic regression and random forest on the same held-out split.
- Report class-aware metrics because attrition is the minority class in this sample.

## Responsible use

This is an educational modeling exercise. Attrition labels may reflect organizational context, measurement choices, and historical inequities. Feature importance is associational, not causal. Do not use this model to screen, rank, discipline, or make employment decisions about individuals. Any real-world HR application would require legal review, fairness testing, transparency, consent, and human oversight.
