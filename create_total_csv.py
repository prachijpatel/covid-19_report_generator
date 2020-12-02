import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta
from create_csv import get_data


get_data()


def get_total(df, s):
    df_t = df.T
    df_t = df_t.rename(columns=df["states"])
    df_t = df_t.drop(["states", "id", "total"], axis=0)
    df_t = df_t.reset_index()
    df_t = df_t.rename(columns={"index": "dates"})
    df_t = df_t.set_index(["dates"], drop=True)
    df_t.index = pd.to_datetime(df_t.index)
    df_t = df_t.groupby([(df_t.index.year), (df_t.index.month)]).sum()
    df_t["total"] = df_t.iloc[:, 0:].mean(axis=1)
    month = {1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "june", 7: "july",
             8: "aug", 9: "sept", 10: "oct", 11: "nov", 12: "dec"}

    df_t["months"] = df_t.index.map(lambda x: month[x[1]])
    df_t.to_csv("./total_csv/{}_total.csv".format(s))
    return df_t


def graph(df, label, color):
    plt.figure(figsize=(9, 6))
    plt.style.use("seaborn")
    plt.plot(df["months"], df["total"], label=label, color=color)
    plt.ylabel('Total cases per month')
    plt.xlabel('Month')
    plt.legend()
    plt.title("{} COVID-19 Cases in India till {}".format(
        label, (date.today()-timedelta(days=1)).strftime("%B %d,%Y")))
    plt.savefig("./images/{}_graph.png".format(label))


def grab_total(df):
    df_t = df.T
    df_t = df_t.rename(columns=df["states"])
    df_t = df_t.drop(["states", "id", "total"], axis=0)
    df_t = df_t.reset_index()
    df_t = df_t.rename(columns={"index": "dates"})
    df_t = df_t.set_index(["dates"], drop=True)
    df_t.index = pd.to_datetime(df_t.index)
    #
    df_t = df_t.groupby([(df_t.index.year), (df_t.index.month)]).sum()
    df_t["sum"] = df_t.iloc[:, 0:].sum(axis=1)
    df_t["total"] = df_t.iloc[:, 0:].mean(axis=1)
    month = {1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "june", 7: "july",
             8: "aug", 9: "sept", 10: "oct", 11: "nov", 12: "dec"}
    df_t["months"] = df_t.index.map(lambda x: month[x[1]])
    Total = df_t["sum"].sum()
    return Total


def get_diff(df):
    df_t = df.iloc[:, :-3]
    df_t = df_t.T
    df_t = df_t.rename(columns=df["states"])
    df_t = df_t.drop(["states"], axis=0)
    df_t = df_t.reset_index()
    df_t = df_t.rename(columns={"index": "dates"})
    df_t = df_t.set_index(["dates"], drop=True)
    df_t.index = pd.to_datetime(df_t.index)
    df_t = df_t.groupby([(df_t.index.year), (df_t.index.month)]).sum()
    df_t["sum"] = df_t.iloc[:, 0:].sum(axis=1)
    df_t["total"] = df_t.iloc[:, 0:].mean(axis=1)
    month = {1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "june", 7: "july",
             8: "aug", 9: "sept", 10: "oct", 11: "nov", 12: "dec"}
    df_t["months"] = df_t.index.map(lambda x: month[x[1]])
    Total1 = df_t["sum"].sum()
    diff = grab_total(df)-Total1
    return diff
# confirmed = pd.read_csv("./data/confirmed_t.csv")
# confirmed = get_total(confirmed, "confirmed")
# # confirmed.to_csv("./data/confirmed_total.csv")
# deceased = pd.read_csv("./data/deceased_t.csv")
# deceased = get_total(deceased, "deceased")

# recovered = pd.read_csv("./data/recovered_t.csv")
# recovered = get_total(recovered, "recovered")

# graph(pd.read_csv("./total_csv/confirmed_total.csv"), "Confirmed", "b")
# graph(pd.read_csv("./total_csv/deceased_total.csv"), "Deceased", "r")

# graph(pd.read_csv("./total_csv/recovered_total.csv"), "Recovered", "g")
