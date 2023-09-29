import numpy as np
import pandas as pd
import time

FILE_PATH = "../result_5_tags.csv"
data = pd.read_csv(FILE_PATH)

data.dropna(subset=['Released'], inplace=True)

print(data.isnull().sum())
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
def count_days_since_release(release_date):
    print(release_date)
    formats = ["%d %b, %Y", "%Y %m %d", "%d %b %Y", "%b %d, %Y"]
    release_date = release_date.replace("févr.", "Feb,")
    release_date = release_date.replace("déc.", "Dec,")
    release_date = release_date.replace("oct.", "Oct,")
    release_date = release_date.replace("janv.", "Jan,")
    release_date = release_date.replace("avr.", "Apr,")
    release_date = release_date.replace("juil.", "Jul,")
    release_date = release_date.replace("juin", "Jun,")
    release_date = release_date.replace("sept.", "Sep,")
    release_date = release_date.replace("mars", "Mar,")
    release_date = release_date.replace("aout", "Aug,")
    release_date = release_date.replace("mai", "May,")
    release_date = release_date.replace("March", "Mar")
    release_date = release_date.replace("Coming soon", "15 May, 2024")
    try_date = release_date
    for f in formats:
        try:
            release_time = time.mktime(time.strptime(try_date, f))
            break
        except ValueError:
           elements = release_date.split(' ')
           if len(elements) == 2:
               try_date = "15 " + release_date
           elif len(elements) == 6:
                try_date = f"{elements[0]} {elements[2]} {elements[4]}"

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
data.to_csv("result_6.csv")




