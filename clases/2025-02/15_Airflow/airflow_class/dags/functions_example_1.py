from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

import pandas as pd


def clean_data():
    df = pd.read_csv("employee_attrition.csv", on_bad_lines='skip')
    df = df.drop(columns=['Employee ID'])
    X = df.drop(columns=['Attrition'])
    y = df['Attrition']
    categorical_columns = X.select_dtypes(include=['object']).columns
    df_transformed = pd.get_dummies(X, columns=categorical_columns, drop_first=True)
    df_transformed = pd.concat([df_transformed, y], axis=1)
    df_transformed.to_csv("clean_employee_attrition.csv")


def ml_train_LGBM():
    df = pd.read_csv("clean_employee_attrition.csv",index_col=0, on_bad_lines='skip')
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('Attrition', axis=1), df['Attrition'], test_size=0.2, random_state=42
    )
    model = LGBMClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
