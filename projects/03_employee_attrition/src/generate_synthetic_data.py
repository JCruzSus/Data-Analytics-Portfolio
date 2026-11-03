"""Generate seeded synthetic employee records for an attrition-modeling demo.
This is not IBM HR data and does not represent real employees.
"""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"synthetic_hr_attrition.csv"
def main():
    rng=np.random.default_rng(29); n=1470
    age=rng.integers(18,61,n); tenure=np.clip(np.round(rng.gamma(2.2,4,n)),0,40).astype(int)
    income=np.clip((age*105+tenure*175+rng.normal(0,1100,n)).astype(int),1200,20000)
    overtime=rng.choice(["Yes","No"],n,p=[.28,.72]); satisfaction=rng.integers(1,5,n); worklife=rng.integers(1,5,n)
    travel=rng.choice(["Travel_Rarely","Travel_Frequently","Non-Travel"],n,p=[.72,.18,.10])
    department=rng.choice(["Research & Development","Sales","Human Resources"],n,p=[.65,.30,.05])
    roles=["Research Scientist","Laboratory Technician","Sales Executive","Sales Representative","Manufacturing Director","Healthcare Representative","Manager","Research Director","Human Resources"]
    role=rng.choice(roles,n); marital=rng.choice(["Married","Single","Divorced"],n,p=[.46,.32,.22])
    years_role=np.minimum(tenure,np.maximum(0,tenure-rng.integers(0,6,n)))
    years_manager=np.minimum(tenure,np.maximum(0,tenure-rng.integers(0,5,n)))
    signal=1.5*(overtime=="Yes")+.65*(satisfaction==1)+.40*(worklife==1)+.45*(travel=="Travel_Frequently")+.035*(30-age)+.075*(4-np.minimum(tenure,4))+.00005*(7000-income)
    lo,hi=-8,2
    for _ in range(100):
        mid=(lo+hi)/2
        if (1/(1+np.exp(-(mid+signal)))).mean()>.16: hi=mid
        else: lo=mid
    probability=1/(1+np.exp(-((lo+hi)/2+signal))); attrition=(rng.random(n)<probability).astype(int)
    df=pd.DataFrame({"Age":age,"Attrition":np.where(attrition==1,"Yes","No"),"BusinessTravel":travel,"Department":department,
    "DistanceFromHome":rng.integers(1,30,n),"Education":rng.integers(1,6,n),"EnvironmentSatisfaction":rng.integers(1,5,n),
    "Gender":rng.choice(["Female","Male"],n),"JobInvolvement":rng.integers(1,5,n),"JobLevel":rng.integers(1,6,n),
    "JobRole":role,"JobSatisfaction":satisfaction,"MaritalStatus":marital,"MonthlyIncome":income,
    "NumCompaniesWorked":rng.integers(0,10,n),"OverTime":overtime,"PerformanceRating":rng.choice([3,4],n,p=[.85,.15]),
    "RelationshipSatisfaction":rng.integers(1,5,n),"StockOptionLevel":rng.integers(0,4,n),"TotalWorkingYears":np.maximum(tenure,rng.integers(0,30,n)),
    "TrainingTimesLastYear":rng.integers(0,7,n),"WorkLifeBalance":worklife,"YearsAtCompany":tenure,
    "YearsInCurrentRole":years_role,"YearsSinceLastPromotion":np.minimum(tenure,rng.integers(0,16,n)),"YearsWithCurrManager":years_manager})
    OUT.parent.mkdir(parents=True,exist_ok=True); df.to_csv(OUT,index=False)
    print(f"Generated {len(df)} synthetic employee records at {OUT}")
if __name__=="__main__": main()
