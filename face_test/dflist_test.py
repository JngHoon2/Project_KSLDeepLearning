import pandas as pd

col_list = []

for i in range(10):
    suffix = ['_x', '_y']
    for j in suffix:
        col_list.append("head_" + str(i) + j)

print(col_list)


posedf = pd.DataFrame(columns='as', 'ab', 'ac')


print(posedf)
