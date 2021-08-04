"""
created on Wed Aug 4

@author: Sayeh Bayat
"""
import numpy as np
import pandas as pd
from biomarker import format_lumi_df, csf_date_filter
from pandas import Timestamp



def merge_csf_trip(lumi, tdf):
    tdf = pd.merge(tdf, lumi, left_on=["id"], right_on=["Subject ID"], how='left')
    tdf['TStime'] = pd.to_datetime(tdf['Trip_Start_Date'])
    tdf.dropna(subset=["csf_date"], inplace=True)
    tdf.reset_index(drop=True, inplace=True)
    return tdf


def merge_trip_activity(demo, trip):
    df = pd.merge(trip, demo, on="id", how="left")
    return df[df['id'].isin(demo.id.unique())][:]


def merge_all(lumi, trip, demo):
    df = pd.merge(trip, demo, on="id", how="left")

    lumi = format_lumi_df(lumi)

    a = Timestamp('1905-01-01 00:00:00')
    b = Timestamp('1910-01-01 00:00:00')
    lumi = csf_date_filter(lumi, a, b)

    df2 = merge_csf_trip(lumi, df)
    return df2


if __name__ == '__main__':
    demo = pd.read_sas("C:/Users/Sayeh/OneDrive - University of Toronto/Documents/Git/Drives/data/"
                       "repeated3_landmarks_021421.sas7bdat")

    trip = pd.read_sas("C:/Users/Sayeh/OneDrive - University of Toronto/Documents/Git/Drives/data/"
                     "sayeh_landmarks_021521.sas7bdat")

    lumi = pd.read_csv("C:/Users/Sayeh/OneDrive - University of Toronto/Documents/Git/Drives/"
                       "data/UP0320_LUMIPULSE_012821_forCollab.csv")

    df = merge_all(lumi, trip, demo)
    df.to_pickle("D:/COVID_data/covid_data.pkl")
    print(df)