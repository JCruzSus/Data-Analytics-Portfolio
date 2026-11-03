# Employee Attrition — Run Results

**Data:** 1,470 seeded synthetic employee records. This is not IBM's dataset or actual employee information.

- Attrition rate: 16.9% (248 of 1,470).
- Overtime = Yes attrition rate: 34.2%.
- Overtime = No attrition rate: 10.1%.
- Best held-out ROC-AUC: 0.745 (Random Forest).

## Model comparison

| Model | ROC-AUC | Attrition precision | Attrition recall | Attrition F1 | Accuracy |
|---|---:|---:|---:|---:|---:|
| Random Forest | 0.745 | 0.464 | 0.210 | 0.289 | 0.826 |
| Logistic Regression | 0.745 | 0.302 | 0.726 | 0.427 | 0.671 |

Logistic regression identifies a larger share of positive cases but produces more false positives. Random forest is more conservative at the default threshold. These are educational results from generated data, not evidence about real workplaces.
