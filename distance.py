"""
created on Wed Aug 4

@author: Sayeh Bayat
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import itertools
import operator
from pandas import Timestamp
from datetime import datetime, timedelta, date
from statsmodels.nonparametric.smoothers_lowess import lowess as sm_lowess
from geopy.distance import great_circle
from scipy.stats import sem


def trip_dist(str_coord, end_coord):
    return [great_circle(a, b).km for a, b in zip(str_coord, end_coord)]


def tot_daily_dist(df):
    df = df[['id', 'Trip_Start_Date', 'Trip_Dist']].groupby(['id', 'Trip_Start_Date']).sum()
    df['id'] = df.index.get_level_values(0)
    df['day'] = df.index.get_level_values(1)

    df2 = df[['id', 'day', 'Trip_Dist']].groupby(['day']).mean()
    A = df[['id', 'day', 'Trip_Dist']].groupby(['day']).sem()
    df2['day'] = df2.index.get_level_values(0)
    df2['SE'] = A.Trip_Dist
    return df2.reset_index(drop=True)

def biomarker_id_map(uid, bmrk, df):
    atn_id = dict(zip(uid, bmrk))
    df['biomarker'] = df['id'].map(atn_id)
    return df


def group_data(df, grp):
    df2 = df[df['biomarker'] == grp].groupby(["day"]).mean()
    df2.columns = df2.columns.get_level_values(0)
    return df2


def monthly_dist(df):
    df["month"] = [t.month if t.year < 2020 else t.month + 12 for t in df.day]
    df_distM = df.groupby(['month']).mean()
    #df_distM['id'] = df_distM.index.get_level_values(0)
    df_distM['month'] = df_distM.index.get_level_values(0)
    return df_distM.reset_index(drop=True)


def lowess_plot(ctl, pwd, var, f=1. / 5.):
    sm_x, sm_y = sm_lowess(ctl[var], np.arange(1, len(ctl)+1), frac=f,
                           it=5, return_sorted=True).T
    plt.plot(sm_x, sm_y, color='tomato')
    #plt.plot(np.arange(1, len(ctl)+1), ctl.Trip_Dist, 'r.')

    sm_x, sm_y = sm_lowess(pwd[var], np.arange(1, len(pwd)+1), frac=f,
                           it=5, return_sorted=True).T
    plt.plot(sm_x, sm_y, color='blue')
    plt.legend(["CTL", "PWD"])
    plt.ylabel(var)
    plt.xlabel("day")
    #plt.plot(np.arange(1, len(pwd) + 1), pwd.Trip_Dist, 'b.')
    return plt

if __name__ == '__main__':
    df = pd.read_pickle("D:/COVID_data/covid_data.pkl")
    str_coord = zip(df.Trip_Start_Latitude, df.Trip_Start_Longitude)
    end_coord = zip(df.TELat, df.TELong)
    df['Trip_Dist'] = trip_dist(str_coord, end_coord)
    print(df.Trip_Dist)

    pwd = df[df["ab42_stat30"] == 1]
    pwd_dist_daily = tot_daily_dist(pwd)
    pwd_dist_daily = pwd_dist_daily.iloc[1:, :]

    ctl = df[df["ab42_stat30"] == 0]
    ctl_dist_daily = tot_daily_dist(ctl)
    ctl_dist_daily = ctl_dist_daily.iloc[1:, :]
    plt = lowess_plot(ctl_dist_daily, pwd_dist_daily, var="Trip_Dist")
    plt.show()

    monthly_pwd = monthly_dist(pwd_dist_daily)
    monthly_ctl = monthly_dist(ctl_dist_daily)

    plt = lowess_plot(monthly_ctl, monthly_pwd, var="Trip_Dist", f=1. / 4.)
    plt.show()

