import pandas as pd
import data as cache_data


data = cache_data.data_2019plus_socials


df = pd.DataFrame(data)

print(df.columns)
print(df)
