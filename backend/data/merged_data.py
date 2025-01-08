import pandas as pd

files = ["data/mostar_weather.csv", "data/fojnica_weather.csv", "data/jablanica_weather.csv"]

columns_to_keep = ['datetime', 'temp', 'humidity', 'precip', 'precipprob', 'windspeed']


dfs = []
for file in files:
    df = pd.read_csv(file)
    df = df[columns_to_keep]
    df['city'] = file.split("/")[-1].replace("_weather.csv", "").capitalize()
    dfs.append(df)


combined_df = pd.concat(dfs, ignore_index=True)


combined_df.to_csv('data/merged_flood_data.csv', index=False)
print("Podaci su uspješno spojeni u data/merged_flood_data.csv")
