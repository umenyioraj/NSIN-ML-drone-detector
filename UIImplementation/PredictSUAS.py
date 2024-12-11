import sklearn
import xgboost as xgb
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRFClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import make_scorer, r2_score
from sklearn.feature_selection import SelectKBest, f_classif,chi2
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder


def PredictSUAS(target, data, model, imputer, scaler, X_train):

    row = data[data["ThreatId"] == target]
    
    current_row = row.drop(columns=["Drone", "ThreatId", "SourceSystem", "ThreatName", "Tracks.Lob.OriginPosition.DataCase", "Countermeasures.State"])

    current_row = current_row[X_train.columns]

    current_row_imputed = imputer.transform(current_row)
    current_row_scaled = scaler.transform(current_row_imputed)

    prediction = model.predict(current_row_scaled)

    print(f"The prediction for ThreatId {target} is: {prediction[0]}")
