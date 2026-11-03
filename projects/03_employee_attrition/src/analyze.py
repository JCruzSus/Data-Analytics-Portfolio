"""Analyze the synthetic employee sample and compare attrition classifiers."""
from pathlib import Path
import subprocess,sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,roc_auc_score,RocCurveDisplay
from sklearn.inspection import permutation_importance
import joblib
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=ROOT/"data"/"synthetic_hr_attrition.csv"
    subprocess.run([sys.executable,str(ROOT/"src"/"generate_synthetic_data.py")],check=True)
    out=ROOT/"outputs"; img=ROOT/"visualizations"; out.mkdir(exist_ok=True); img.mkdir(exist_ok=True)
    df=pd.read_csv(data); df["AttritionFlag"]=(df.Attrition=="Yes").astype(int)
    df.Attrition.value_counts().rename_axis("attrition").to_frame("employees").to_csv(out/"class_balance.csv")
    df.groupby("Attrition")[["Age","MonthlyIncome","YearsAtCompany","JobSatisfaction","WorkLifeBalance"]].mean().T.to_csv(out/"profile_by_attrition.csv")
    overtime=df.groupby("OverTime").agg(employees=("Attrition","size"),attrition_rate=("AttritionFlag","mean")).reset_index()
    overtime["attrition_rate_pct"]=100*overtime.attrition_rate; overtime.to_csv(out/"attrition_by_overtime.csv",index=False)
    dept=df.groupby("Department").agg(employees=("Attrition","size"),attrition_rate=("AttritionFlag","mean")).reset_index()
    dept["attrition_rate_pct"]=100*dept.attrition_rate; dept.to_csv(out/"attrition_by_department.csv",index=False)
    X=df.drop(columns=["Attrition","AttritionFlag"]); y=df.AttritionFlag
    cat=X.select_dtypes(include="object").columns.tolist(); num=X.select_dtypes(include="number").columns.tolist()
    prep=ColumnTransformer([("num",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),num),
      ("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),("encode",OneHotEncoder(handle_unknown="ignore"))]),cat)])
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    models={"Logistic Regression":LogisticRegression(max_iter=2000,class_weight="balanced",random_state=42),
      "Random Forest":RandomForestClassifier(n_estimators=350,min_samples_leaf=3,class_weight="balanced",random_state=42,n_jobs=1)}
    results=[]; fitted={}
    for name,estimator in models.items():
        pipe=Pipeline([("preprocess",prep),("model",estimator)]); pipe.fit(X_train,y_train)
        pred=pipe.predict(X_test); prob=pipe.predict_proba(X_test)[:,1]
        report=classification_report(y_test,pred,output_dict=True,zero_division=0)
        results.append({"model":name,"roc_auc":roc_auc_score(y_test,prob),"precision_attrition":report["1"]["precision"],
          "recall_attrition":report["1"]["recall"],"f1_attrition":report["1"]["f1-score"],"accuracy":report["accuracy"]})
        key=name.lower().replace(" ","_")
        (out/f"{key}_classification_report.txt").write_text(classification_report(y_test,pred,zero_division=0))
        pd.DataFrame(confusion_matrix(y_test,pred),index=["actual_stayed","actual_left"],columns=["predicted_stayed","predicted_left"]).to_csv(out/f"{key}_confusion_matrix.csv")
        RocCurveDisplay.from_predictions(y_test,prob); plt.title(f"ROC Curve — {name}"); plt.tight_layout(); plt.savefig(img/f"{key}_roc_curve.png",dpi=150); plt.close()
        fitted[name]=pipe
    metrics=pd.DataFrame(results).sort_values("roc_auc",ascending=False); metrics.to_csv(out/"model_comparison.csv",index=False)
    best=fitted[metrics.iloc[0]["model"]]; joblib.dump(best,out/"best_model.joblib")
    importance=permutation_importance(best,X_test,y_test,n_repeats=5,random_state=42,scoring="roc_auc",n_jobs=1)
    pd.DataFrame({"feature":X_test.columns,"importance_mean":importance.importances_mean,"importance_std":importance.importances_std}).sort_values("importance_mean",ascending=False).to_csv(out/"permutation_importance.csv",index=False)
    plt.figure(figsize=(7,4)); df.Attrition.value_counts().plot(kind="bar"); plt.title("Synthetic Employee Attrition Class Balance"); plt.ylabel("Employees"); plt.tight_layout(); plt.savefig(img/"class_balance.png",dpi=150); plt.close()
    plt.figure(figsize=(7,4)); plt.bar(overtime.OverTime,overtime.attrition_rate_pct); plt.title("Attrition Rate by Overtime"); plt.ylabel("Attrition rate (%)"); plt.tight_layout(); plt.savefig(img/"attrition_by_overtime.png",dpi=150); plt.close()
    print(metrics.to_string(index=False))
if __name__=="__main__": main()
