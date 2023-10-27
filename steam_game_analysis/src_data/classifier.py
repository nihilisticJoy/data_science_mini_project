import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
import scikitplot as skplt
from sklearn.ensemble import GradientBoostingClassifier


np.random.seed(350)

FILE_PATH = "./clean_data.csv"
original_data = pd.read_csv(FILE_PATH)

print(original_data['On_sale'].value_counts())
# value 0 = 21350 (68.17%)
# value 1 = 9966 (31.82%)

data = original_data.copy()

data.drop(['Unnamed: 0', 'Title', 'Platforms', 'Reviews', 'Players', 'Review_summary', 'Released', 'Discount', 'Final_price', 'Main_tag', 'Url', 'All_tags'], axis=1, inplace=True)
#print(data.isnull().sum())

print(data)

x, y = data.drop('On_sale', axis=1), data['On_sale']

x = x.to_numpy()
y = y.to_numpy()

# Shuffle data
random_sequence = np.random.permutation(len(x))
x = x[random_sequence]
y = y[random_sequence]


# keep 30% of data for testing
# Order of the output variables is important
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3)


# model = LogisticRegression(max_iter=100000, class_weight='balanced')
# fit the model on the training data
# model.fit(x_train, y_train)

# predict y for the test inputs
# y_test_predictions = model.predict(x_test)

# Generate confusion matrix for the predictions
# conf_matrix = confusion_matrix(y_test, y_test_predictions)


# evaluation scores
# accuracy = accuracy_score(y_test, y_test_predictions)
# precision = precision_score(y_test, y_test_predictions)
# recall = recall_score(y_test, y_test_predictions)
# f1 = f1_score(y_test, y_test_predictions)
# roc_auc = roc_auc_score(y_test, y_test_predictions)

# display evaluation scores
# print(f"Accuracy = {accuracy.round(4)}")       # Accuracy = 0.7969
# print(f"Precision = {precision.round(4)}")     # Precision = 0.9964
# print(f"Recall = {recall.round(4)}")           # Recall = 0.3668
# print(f"F1 Score = {f1.round(4)}")             # F1 Score = 0.5362
# print(f"Roc_auc Score = {roc_auc.round(4)}")   # Roc_auc Score = 0.6831


# skplt.metrics.plot_confusion_matrix(y_test, y_test_predictions, normalize=False)
# plt.show()

gbc = GradientBoostingClassifier()
gbc_model = gbc.fit(x_train, y_train)
y_gbc_proba = gbc_model.predict_proba(x_test)
y_gbc_pred = np.where(y_gbc_proba[:,1] > 0.5, 1, 0)


skplt.metrics.plot_confusion_matrix(y_test, y_gbc_pred, normalize=False, title= "")
plt.show()

accuracy = accuracy_score(y_test, y_gbc_pred)
precision = precision_score(y_test, y_gbc_pred)
recall = recall_score(y_test, y_gbc_pred)
f1 = f1_score(y_test, y_gbc_pred)
roc_auc = roc_auc_score(y_test, y_gbc_pred)

print(f"Accuracy = {accuracy.round(4)}")
print(f"Precision = {precision.round(4)}")
print(f"Recall = {recall.round(4)}")
print(f"F1 Score = {f1.round(4)}")
print(f"Roc_auc Score = {roc_auc.round(4)}")
