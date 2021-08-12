import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from distance import monthly_dist, lowess_plot


def speed_buckets(v):
    frequency, bins = np.histogram(v, bins=[0, 0.001, 5, 20, 50, 80, 130])
    return frequency/len(v)


def df_speed_bucket(df):
    df['v1'], df['v2'], df['v3'], df['v4'], df['v5'], df['v6'] = \
        zip(*df['Vehicle_Speed'].map(speed_buckets))
    return df


def speed_timeseries(df, var="v1"):
    df = df[['uid', 'Trip_Start_Date', var]].groupby(['uid', 'Trip_Start_Date']).mean()
    df['id'] = df.index.get_level_values(0)
    df['day'] = df.index.get_level_values(1)

    df2 = df[['id', 'day', var]].groupby(['day']).mean()
    A = df[['id', 'day', var]].groupby(['day']).sem()
    df2['day'] = df2.index.get_level_values(0)
    df2['SE'] = A[var]
    return df2.reset_index(drop=True)


if __name__ == '__main__':
    df = pd.read_pickle("D:/COVID_data/covid_data2.pkl")
    df = df_speed_bucket(df)
    print(df.columns)
    print(df.v2)

    pwd = df[df["ab42_stat30"] == 2]
    pwd_v2_daily = df_speed_bucket(pwd)
    pwd_v2_daily = speed_timeseries(pwd_v2_daily, var="v2")

    ctl = df[df["ab42_stat30"] == 0]
    ctl_v2_daily = df_speed_bucket(ctl)
    ctl_v2_daily = speed_timeseries(ctl_v2_daily, var="v2")

    print(ctl_v2_daily.columns)
    plt.plot(np.arange(1, len(ctl_v2_daily) + 1), ctl_v2_daily.v2, 'b.')
    plt.plot(np.arange(1, len(pwd_v2_daily) + 1), pwd_v2_daily.v2, 'k.')
    plt.show()

    plt = lowess_plot(ctl_v2_daily, pwd_v2_daily, "v2")
    plt.show()