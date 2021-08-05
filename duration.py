"""
created on Wed Aug 4

@author: Sayeh Bayat
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from distance import monthly_dist, lowess_plot


def tot_daily_trip_dur(df):
    df = df[['id', 'Trip_Start_Date', 'Trip_Time']].groupby(['id', 'Trip_Start_Date']).sum()
    df['id'] = df.index.get_level_values(0)
    df['day'] = df.index.get_level_values(1)
    df["Trip_Time"] /= 60

    df2 = df[['id', 'day', 'Trip_Time']].groupby(['day']).mean()
    A = df[['id', 'day', 'Trip_Time']].groupby(['day']).sem()
    df2['day'] = df2.index.get_level_values(0)
    df2['SE'] = A.Trip_Time
    return df2.reset_index(drop=True)


if __name__ == '__main__':
    df = pd.read_pickle("D:/COVID_data/covid_data.pkl")

    pwd = df[df["ab42_stat30"] == 1]
    pwd_dist_daily = tot_daily_trip_dur(pwd)
    pwd_dist_daily = pwd_dist_daily.iloc[1:, :]

    ctl = df[df["ab42_stat30"] == 0]
    ctl_dist_daily = tot_daily_trip_dur(ctl)
    ctl_dist_daily = ctl_dist_daily.iloc[1:, :]
    plt = lowess_plot(ctl_dist_daily, pwd_dist_daily, "Trip_Time")
    plt.show()

    monthly_pwd = monthly_dist(pwd_dist_daily)
    monthly_ctl = monthly_dist(ctl_dist_daily)

    plt = lowess_plot(monthly_ctl, monthly_pwd, "Trip_Time")
    plt.show()


