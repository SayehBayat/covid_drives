"""
created on Wed Aug 4

@author: Sayeh Bayat
"""
import numpy as np
import pandas as pd
from biomarker import format_lumi_df, csf_date_filter
from pandas import Timestamp
from geopy.distance import great_circle


def trip_dist(str_coord, end_coord):
    return [great_circle(a, b).km for a, b in zip(str_coord, end_coord)]


def trip_date(TStime):
    return [ts.date() for ts in TStime]


def merge_csf_trip(lumi, tdf, le_o="id", ri_o="Subject ID"):
    tdf = pd.merge(tdf, lumi, left_on=[le_o], right_on=[ri_o], how='left')
    #tdf['TStime'] = pd.to_datetime(tdf['Trip_Start_Date'])
    tdf.dropna(subset=["csf_date"], inplace=True)
    tdf.reset_index(drop=True, inplace=True)
    return tdf


def merge_trip_activity(demo, trip, le_o="id", ri_o="id"):
    df = pd.merge(trip, demo, left_on=le_o, right_on=ri_o, how="left")
    return df[df[ri_o].isin(demo[ri_o].unique())][:]


def merge_all(lumi, trip, demo, le_o="id", ri_o="id"):
    df = pd.merge(trip, demo, left_on=le_o, right_on=ri_o, how="left")

    lumi = format_lumi_df(lumi)

    a = Timestamp('1905-01-01 00:00:00')
    b = Timestamp('1910-01-01 00:00:00')
    lumi = csf_date_filter(lumi, a, b)

    df2 = merge_csf_trip(lumi, df, le_o="uid")
    return df2


def time_periods(df):
    df['covid_time'] = [0] * len(df)
    t1 = Timestamp('2019-01-01 00:00:00')
    t2 = Timestamp('2019-03-15 00:00:00')
    mask = (df['TStime'] > t1) & (df['TStime'] < t2)
    df.loc[mask, 'covid_time'] = 'Early1'

    t1 = Timestamp('2019-03-15 00:00:00')
    t2 = Timestamp('2019-06-15 00:00:00')
    mask = (df['TStime'] >= t1) & (df['TStime'] < t2)
    df.loc[mask, 'covid_time']  = 'Mid1'

    t1 = Timestamp('2020-06-15 00:00:00')
    t2 = Timestamp('2021-01-01 00:00:00')
    mask = (df['TStime'] >= t1) & (df['TStime'] < t2)
    df.loc[mask, 'covid_time']  = 'Late1'

    t1 = Timestamp('2020-01-01 00:00:00')
    t2 = Timestamp('2020-03-15 00:00:00')
    mask = (df['TStime'] > t1) & (df['TStime'] < t2)
    df.loc[mask, 'covid_time']  = 'Early2'

    t1 = Timestamp('2020-03-15 00:00:00')
    t2 = Timestamp('2020-06-15 00:00:00')
    mask = (df['TStime'] >= t1) & (df['TStime'] < t2)
    df.loc[mask, 'covid_time']  = 'Mid2'

    t1 = Timestamp('2020-06-15 00:00:00')
    t2 = Timestamp('2021-01-01 00:00:00')
    mask = (df['TStime'] >= t1) & (df['TStime'] < t2)
    df.loc[mask, 'covid_time']  = 'Late2'
    return df



if __name__ == '__main__':
    demo = pd.read_sas("C:/Users/Sayeh/OneDrive - University of Toronto/Documents/Git/Drives/data/"
                       "repeated3_landmarks_021421.sas7bdat")

    trip = pd.read_pickle("C:/Users/Sayeh/OneDrive - University of Toronto/Documents/Git/Drives/data/trip_v2.pkl")

    lumi = pd.read_csv("C:/Users/Sayeh/OneDrive - University of Toronto/Documents/Git/Drives/"
                       "data/UP0320_LUMIPULSE_012821_forCollab.csv")

    print(trip.TStime)

    df = merge_all(lumi, trip, demo, le_o="uid")
    str_coord = zip(df.TSLat, df.TSLong)
    end_coord = zip(df.TELat, df.TELong)
    df['Trip_Dist'] = trip_dist(str_coord, end_coord)
    df['Trip_Start_Date'] = trip_date(df.TStime)
    df = df[df['Trip_Dist'] < 200]
    df = df[df['Trip_Dist'] > 0.05]

    df = df[df['Duration'] < 500]
    df = df[df['Duration'] > 2]

    t1 = Timestamp('2019-01-01 00:00:00')
    t2 = Timestamp('2021-01-01 00:00:00')
    mask = (df['TStime'] > t1) & (df['TStime'] <= t2)
    df = df.loc[mask][:]
    df = time_periods(df)
    df.to_pickle("D:/COVID_data/covid_data2.pkl")
    print(df)