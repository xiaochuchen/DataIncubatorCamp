import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


matplotlib.style.use('ggplot')

df = pd.read_csv("/Users/xc/Downloads/SCN_DS_30102016210739282.csv", header=0, sep=',', quotechar='"')

countries = ["CAN", "ISR", "CHN", "KOR", "DEU", "GBR"]

def convert_to_number(x):
    if ("enterprise" in x):
        return 1
    if ("government" in x):
        return 2
    if ("education" in x):
        return 3
    if ("non-profit" in x):
        return 4
    return 5

df2014 = df[(df["Indicator"].str.contains("%")) & (df["LOCATION"].isin(countries)) & (df["Time"] == 2014)].copy()
df2014["Indicator"] = df2014["Indicator"].apply(convert_to_number)

df2000 = df[(df["Indicator"].str.contains("%")) & (df["LOCATION"].isin(countries)) & (df["Time"] == 2000)].copy()
df2000["Indicator"] = df2000["Indicator"].apply(convert_to_number)

df_diff = df2014.merge(df2000, on=["Indicator", "LOCATION"], how='inner')
df_diff["diff"] = df_diff["Value_x"] - df_diff["Value_y"]

plt.figure(figsize=(20,10))
for key, grp in df2014.groupby("LOCATION"):
    plt.plot(grp["Indicator"], grp["Value"], label=key, linewidth=4)

plt.legend(loc='best')
plt.xticks([1,2,3,4],["enterprise","government","education","non-profit"])
plt.savefig('graph_2014.png')

plt.figure(figsize=(20,10))
for key, grp in df_diff.groupby("LOCATION"):
    plt.plot(grp["Indicator"], grp["diff"], label=key, linewidth=4)

plt.legend(loc='best')
plt.xticks([1,2,3,4],["enterprise","government","education","non-profit"])
plt.savefig('graph_diff.png')
