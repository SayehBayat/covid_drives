"""
created on Wed Aug 4

@author: Sayeh Bayat
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from distance import monthly_dist, lowess_plot


def daily_trip_count(df):
    df = df[['id', 'Trip_Start_Date', 'Duration']].groupby(['id', 'Trip_Start_Date']).size().reset_index(name='counts')

    print(df)
    df2 = df[['id', 'Trip_Start_Date', 'counts']].groupby(['Trip_Start_Date']).mean()
    A = df[['id', 'Trip_Start_Date', 'counts']].groupby(['Trip_Start_Date']).sem()
    df2['day'] = df2.index.get_level_values(0)
    df2['SE'] = A.counts
    return df2.reset_index(drop=True)


if __name__ == '__main__':
    df = pd.read_pickle("D:/COVID_data/covid_data2.pkl")

    pwd = df[df["ab42_stat30"] == 2]
    print(len(pwd['id'].unique()))
    pwd_dist_daily = daily_trip_count(pwd)
    #pwd_dist_daily = pwd_dist_daily.iloc[1:, :]

    ctl = df[df["ab42_stat30"] == 0]
    print(len(ctl['id'].unique()))
    ctl_dist_daily = daily_trip_count(ctl)
    #ctl_dist_daily = ctl_dist_daily.iloc[1:, :]
    plt = lowess_plot(ctl_dist_daily, pwd_dist_daily, "counts")
    plt.show()

    #monthly_pwd = monthly_dist(pwd_dist_daily)
    #monthly_ctl = monthly_dist(ctl_dist_daily)

    #plt = lowess_plot(monthly_ctl, monthly_pwd, "counts")
    #plt.show()


