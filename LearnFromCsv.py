import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
from datetime import datetime

# Function to train a machine learning model
def train_model(csv_file):
    # Read CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file)

    # Separate features and target variable
    X = data.iloc[:, :-1]  # Assuming the target variable is the last column
    y = data.iloc[:, -1]   # Assuming the target variable is the last column

    # Handle categorical data with one-hot encoding
    X = pd.get_dummies(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Drop rows with missing values in the features
    X_train_clean = X_train.dropna()
    y_train_clean = y_train[X_train.index.isin(X_train_clean.index)]

    X_test_clean = X_test.dropna()
    y_test_clean = y_test[X_test.index.isin(X_test_clean.index)]

    # Combine the training and testing sets for target variable encoding
    y_combined = pd.concat([y_train_clean, y_test_clean], axis=0)

    # Encode the target variable using a common LabelEncoder
    le = LabelEncoder()
    y_combined_encoded = le.fit_transform(y_combined)

    # Split the encoded target variable back to training and testing sets
    y_train_encoded = y_combined_encoded[:len(y_train_clean)]
    y_test_encoded = y_combined_encoded[len(y_train_clean):]

    # Initialize a Random Forest classifier
    model = RandomForestClassifier()

    # Train the model
    model.fit(X_train_clean, y_train_encoded)

    # Make predictions on the test set
    y_pred = model.predict(X_test_clean)

    # Decode the predictions (if needed)
    y_pred_decoded = le.inverse_transform(y_pred)

    # Evaluate the accuracy of the model
    accuracy = accuracy_score(y_test_encoded, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")

    # Save the trained model with a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    model_filename = f"./trained_models/trained_model_{timestamp}.joblib"
    joblib.dump(model, model_filename)
    print(f"Trained model saved to {model_filename}")

if __name__ == "__main__":
    # Replace 'your_dataset.csv' with the path to your CSV file
    csv_file_path = './csv_files/vgsales.csv'
    train_model(csv_file_path)
