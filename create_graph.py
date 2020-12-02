import matplotlib.pyplot as plt
import pandas as pd


def graph(df, label, color):
    plt.figure()
    plt.style.use("seaborn")
    plt.plot(df["months"], df["total"], label=label, color=color)
    plt.ylabel('Total cases per month')
    plt.xlabel('Month')
    plt.legend()
    plt.savefig("./images/{}_graph.png".format(label))
    # plt.show()


#graph(pd.read_csv("./total_csv/confirmed_total.csv"), "confirmed", "b")
#graph(pd.read_csv("./total_csv/deceased_total.csv"), "deceased", "r")

#graph(pd.read_csv("./total_csv/recovered_total.csv"), "recovered", "g")
