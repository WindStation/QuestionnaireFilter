import pandas as pd
from pandas import DataFrame

if __name__ == '__main__':
    content = [['a1', 'a2'],
               ['b1', 'b2'],
               ['c1', 'c2', 'c3']]
    df = DataFrame(content)
    print(df)

    for index, row in df.iterrows():
        print(f'index:{index}, \nrow:{row}\n\n')

    for index, row in df.iterrows():
        if index == 1:
            df = df.drop(index)

    print(df)
