"""Exploratory analysis and leakage-conscious attrition model comparison."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, RocCurveDisplay
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUT = ROOT / "outputs"

def main():
    if not DATA.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA}\nDownload the IBM HR Attrition sample CSV (see README) and place it in data/.")
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    if "Attrition" not in df:
        raise ValueError("Expected target column 'Attrition' was not found.")
    df = df.drop_duplicates()
    df["AttritionFlag"] = df["Attrition"].map({"Yes":1,"No":0})
    if df["AttritionFlag"].isna().any():
        raise ValueError("Attrition values should be Yes/No.")
    df["AttritionFlag"].value_counts().rename_axis("attrition").to_frame("employees").to_csv(OUT/"class_balance.csv")
    df.groupby("Attrition")["Age","MonthlyIncome"] if False else None
    numeric = df.select_dtypes(include="number").columns.tolist()
    df.groupby("Attrition")[numeric].mean().T.to_csv(OUT/"numeric_profile_by_attrition.csv")
    df.groupby("Attrition").size().rename("employees").to_csv(OUT/"attrition_counts.csv")

    X = df.drop(columns=["Attrition","AttritionFlag"])
    y = df["AttritionFlag"]
    cat = X.select_dtypes(include=["object","category"]).columns.tolist()
    num = X.select_dtypes(include="number").columns.tolist()
    pre = ColumnTransformer([
        ("numeric",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),num),
        ("categorical",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),
                                 ("encode",OneHotEncoder(handle_unknown="ignore"))]),cat)
    ])
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    models = {
        "logistic_regression": LogisticRegression(max_iter=2000,class_weight="balanced",random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=400,min_samples_leaf=3,
             class_weight="balanced",random_state=42,n_jobs=-1)
    }
    metrics=[]
    best_auc=-1
    for name, estimator in models.items():
        pipe=Pipeline([("preprocess",pre),("model",estimator)])
        pipe.fit(X_train,y_train)
        pred=pipe.predict(X_test)
        prob=pipe.predict_proba(X_test)[:,1]
        auc=roc_auc_score(y_test,prob)
        metrics.append({"model":name,"roc_auc":auc})
        (OUT/f"{name}_classification_report.txt").write_text(classification_report(y_test,pred,digits=3),encoding="utf-8")
        pd.DataFrame(confusion_matrix(y_test,pred),index=["actual_no","actual_yes"],
                     columns=["predicted_no","predicted_yes"]).to_csv(OUT/f"{name}_confusion_matrix.csv")
        RocCurveDisplay.from_predictions(y_test,prob)
        plt.title(f"ROC curve — {name}")
        plt.tight_layout()
        plt.savefig(OUT/f"{name}_roc_curve.png",dpi=150)
        plt.close()
        if auc>best_auc:
            best_auc=auc
            joblib.dump(pipe,OUT/"best_model.joblib")
    pd.DataFrame(metrics).to_csv(OUT/"model_comparison.csv",index=False)
    print("Attrition analysis complete. Review outputs/ for metrics and reports.")
    print(pd.DataFrame(metrics).to_string(index=False))

if __name__=="__main__":
    main()
