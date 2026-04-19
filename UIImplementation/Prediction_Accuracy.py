import sklearn
import pandas as pd
import xgboost as xgb
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import make_scorer, r2_score
from sklearn.impute import SimpleImputer
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def Accuracy(X_train_final, X_test_final, y_train, y_test, threat_ids):
    model = RandomForestClassifier(random_state=42)

    model.fit(X_train_final, y_train)

    y_pred = model.predict(X_test_final)



    # Generating a Confusion Matrix for the Decision Tree
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score

    from sklearn import metrics
    X_test_copy = X_test_final.copy()
    X_test_copy['ThreatId'] = threat_ids.loc[X_test_copy.index]

    y_pred = model.predict(X_test_copy.drop(columns=['ThreatId']))  # Ensure ThreatId isn't used for prediction

    # Add ThreatId and predictions to test_data DataFrame
    test_data = pd.DataFrame({
        'y_true': y_test,
        'y_pred': y_pred,
        'ThreatId': X_test_copy['ThreatId']
    })


    aggregated_data = test_data.groupby('ThreatId').agg({
        'y_true': 'max',
        'y_pred': 'max'
    }).reset_index()

    # Calculate Confusion Matrix
    confusion_matrix = metrics.confusion_matrix(aggregated_data['y_true'], aggregated_data['y_pred'])

    # Display the confusion matrix
    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[0, 1])

    params = {
    # Calculate precision, recall, F1 score
    "precision": metrics.precision_score(aggregated_data['y_true'], aggregated_data['y_pred']),
    "recall": metrics.recall_score(aggregated_data['y_true'], aggregated_data['y_pred']),
    "F1_score": metrics.f1_score(aggregated_data['y_true'], aggregated_data['y_pred'])
    }

    metric_dict = {
        "accuracy": metrics.accuracy_score(aggregated_data['y_true'], aggregated_data['y_pred'])
    }

    # Print important stats
    print({"Precision": params["precision"], "Recall": params["recall"], "F1_score": params["F1_score"]})
    print({"Accuracy": metric_dict["accuracy"]})

    false_positives = aggregated_data[(aggregated_data['y_pred'] == 1) & (aggregated_data['y_true'] == 0)]

    false_negatives = aggregated_data[(aggregated_data['y_pred'] == 0) & (aggregated_data['y_true'] == 1)]


    # Plot confusion matrix
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(bottom=0.2, left=0.2)
    cm_display.plot(ax=ax)
    plt.title('Confusion Matrix of Drone Detection Decision Tree', fontweight='bold')
    ax.set_xlabel(f'Predicted label \n\n Precision: {params["precision"]:.2f} \n Recall: {params["recall"]:.2f} \n F1_score: {params["F1_score"]:.2f}')
    plt.show()
    return params, metric_dict