import numpy as np
import pandas as pd
import time

FILE_PATH = "../result_3_tags.csv"
data = pd.read_csv(FILE_PATH)

# print(data.isnull().sum())
#
# print(data['Discount'].unique())
#
# print(data.dtypes)
#
# print(type(data['Platforms']))
#
# print(data['Platforms'].unique())


# create a new feature `Multiplatform` (1 = multi platform, 0 = single platform)
def is_multi_platform(value):
    if value == 'Music' or value == 'Win':
        return 0
    else:
        return 1

for value in data['Platforms']:
    print(value, is_multi_platform(value))

is_multi_platform_column = [is_multi_platform(v) for v in data['Platforms']]
data.insert(2, "Multiplatform", is_multi_platform_column, True)


# for p, d, dp in zip(data['Price'], data['Discount'], data['Discounted price']):
#     if not pd.isna(d) and d != 0:
#         print(p, d, dp)


# replace None with 100 % discount
data['Discount'].fillna(100, inplace=True)



# create new feature `Day_since_release` extracted from `Release`
def count_days_since_release(release_data):
    print(release_data)
    release_time = time.mktime(time.strptime(release_data, "%d %b, %Y"))
    return int((time.time() - release_time) / (24 * 60 * 60))


days_since_release = [count_days_since_release(v) for v in data['Released']]
data.insert(8, "Day_since_release", days_since_release, True)



# create new feature `On_sale` (1 = on sale, 0 = 0 discount)
def is_on_sale(value):
    if value == 0:
        return 0
    else:
        return 1

for value in data['Discount']:
    print(value, is_on_sale(value))


on_sale = [is_on_sale(v) for v in data['Discount']]
data.insert(11, "On_sale", on_sale, True)


# export to csv file
data.to_csv("result_4.csv")




