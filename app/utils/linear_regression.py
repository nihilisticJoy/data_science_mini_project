from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from math import sqrt


def evaluate_linear_regression(df, features, target):
    dff = df[features + [target]].dropna()
    X = dff[features]
    y = dff[target]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict using the test set
    y_pred = model.predict(X_test)

    # Calculate metrics
    coefficients = model.coef_
    training_score = model.score(X_train, y_train)  # R^2 on training data
    r2 = r2_score(y_test, y_pred)  # R^2 on test data
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = sqrt(mse)

    return {
        "coefficients": coefficients,
        "training_score": training_score,
        "r2": r2,
        "mse": mse,
        "mae": mae,
        "rmse": rmse,
        "predictions": model.predict(X),
        "cleaned_df": dff,
    }
