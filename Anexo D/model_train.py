import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import joblib

file_path = 'C:/Users/ruipsilv/OneDrive - Capgemini/Desktop/Dataset Docs/dataset_model.xlsx'
df = pd.read_excel(file_path)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

joblib.dump(clf, 'C:/Users/ruipsilv/OneDrive - Capgemini/Desktop/Dataset Docs/Model.joblib')

clf = joblib.load('C:/Users/ruipsilv/OneDrive - Capgemini/Desktop/Dataset Docs/Model.joblib')

# Step 5: Make predictions on the test set
y_pred = clf.predict(X_test)

# Step 6: Evaluate the model
# Calculate the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)

# Print the results
print("Confusion Matrix:")
print(conf_matrix)
print("\nAccuracy:", accuracy)