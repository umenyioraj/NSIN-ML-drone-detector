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

def Train(data):

    #label encoder for object type features
    label_encoder = LabelEncoder()

    object_columns = data.select_dtypes(include=['object']).columns

    for col in object_columns:
        data[col] = label_encoder.fit_transform(data[col])


    correlation = data.corr(numeric_only=False)["Drone"].sort_values(ascending=False)

    threat_ids = data['ThreatId']

    X = data.drop(columns=["Drone", "ThreatId", "SourceSystem", "ThreatName", "Tracks.Lob.OriginPosition.DataCase", "Countermeasures.State"])
    y = data["Drone"]

    X = X.dropna(axis=1, how='all')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    priority_features = ["Signal Persistence", "Altitude Consistent", "Speed"]

    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)
    X_test_imputed = imputer.transform(X_test)


    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_imputed)
    X_test_scaled = scaler.transform(X_test_imputed)

    # Select k best features to use
    selector = SelectKBest(score_func=f_classif, k=30)
    X_train_selected = selector.fit_transform(X_train_scaled, y_train)
    X_test_selected = selector.transform(X_test_scaled)

    # Get selected feature names
    selected_features_mask = selector.get_support()
    selected_feature_names = X.columns[selected_features_mask].tolist()

    # Ensure priority features are included
    final_selected_features = list(set(selected_feature_names + priority_features))

    # Create final datasets with selected features
    X_train_final = X_train[final_selected_features]
    X_test_final = X_test[final_selected_features]

    #print("Selected features:", X_train_final.columns.tolist())

    models = {
        "dt_clf": DecisionTreeClassifier(random_state=42),
        "xgb_clas" : XGBRFClassifier(),
        "rnd_forest": RandomForestClassifier()

    }

    for name, model in models.items():
        model.fit(X_train_final, y_train)
        y_pred = model.predict(X_test_final)
        r2 = r2_score(y_pred,y_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"{name}: Accuracy = {accuracy}")
        print(f"{name}: R2 score = {r2}")

    model = RandomForestClassifier(random_state=42)

    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    return model, imputer, scaler, X_train, X_train_final, X_test_final, y_train, y_test, threat_ids
