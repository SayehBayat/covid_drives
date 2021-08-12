"""
created on Wed Aug 4

@author: Sayeh Bayat
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from distance import monthly_dist, lowess_plot


def tot_daily_trip_dur(df, var="Duration"):
    df = df[['uid', 'Trip_Start_Date', var]].groupby(['uid', 'Trip_Start_Date']).sum()
    df['id'] = df.index.get_level_values(0)
    df['day'] = df.index.get_level_values(1)
    #df[var] /= 60

    df2 = df[['id', 'day', var]].groupby(['day']).mean()
    A = df[['id', 'day', var]].groupby(['day']).sem()
    df2['day'] = df2.index.get_level_values(0)
    df2['SE'] = A[var]
    return df2.reset_index(drop=True)


def dur_buckets(df):
    criteria = [df["Duration"].between(1, 10), df["Duration"].between(10, 30), df["Duration"].between(30, 60),
                df["Duration"].between(60, 120)]
    values = [1, 2, 3, 4]
    df['dur_grp'] = np.select(criteria, values, 0)
    return df


if __name__ == '__main__':
    df = pd.read_pickle("D:/COVID_data/covid_data2.pkl")
    print(df.Duration.min())
    print(df.Duration.max())
    print(df.Duration.mean())
    df = dur_buckets(df)
    print(df.head())

    df = df[df["dur_grp"] != 0]

    pwd = df[df["ab42_stat30"] == 2]
    pwd_dist_daily = tot_daily_trip_dur(pwd)
    #pwd_dist_daily = pwd_dist_daily.iloc[1:, :]

    ctl = df[df["ab42_stat30"] == 0]
    ctl_dist_daily = tot_daily_trip_dur(ctl)
    #ctl_dist_daily = ctl_dist_daily.iloc[1:, :]
    plt = lowess_plot(ctl_dist_daily, pwd_dist_daily, "Duration")
    plt.show()



