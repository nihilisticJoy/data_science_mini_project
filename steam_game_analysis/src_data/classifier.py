import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


FILE_PATH = "./clean_data.csv"
original_data = pd.read_csv(FILE_PATH)

print(original_data['On_sale'].value_counts())
# value 0 = 21350 (68.17%)
# value 1 = 9966 (31.82%)

data = original_data.copy()

data.drop(['Unnamed: 0', 'Title', 'Platforms', 'Reviews', 'Review_summary', 'Released', 'Discount', 'Final_price', 'Main_tag', 'Url', 'All_tags'], axis=1, inplace=True)
#print(data.isnull().sum())

print(data)

x, y = data.drop('On_sale', axis=1), data['On_sale']

x = x.to_numpy()
y = y.to_numpy()

# Shuffle data
random_sequence = np.random.permutation(len(x))
x = x[random_sequence]
y = y[random_sequence]


train_size = int(len(x) * 0.8)

train_data = x[:train_size]
test_data = x[train_size:]
train_labels = y[:train_size]
test_labels = y[train_size:]


classifier = LogisticRegression(max_iter=100000)
classifier.fit(train_data, train_labels)
score = classifier.score(test_data, test_labels)
print("Score:", score)
