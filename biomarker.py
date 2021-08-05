"""
created on Wed Aug 4

@author: Sayeh Bayat
"""

import numpy as np
import pandas as pd
from pandas import Timestamp
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt


def find_ab42_ratio(ab42, ab40):
    """
    Compute ab42/ab40 biomarker
    """
    ab42_ratio = ab42 / ab40
    ab42_stat = ab42_ratio < 0.0673
    ab42_stat = ab42_stat.astype(int)
    return ab42_ratio, ab42_stat


def find_ab42_ratio_30(ab42, ab40):
    """
    Compute ab42/ab40 biomarker
    """
    ab42_ratio = ab42 / ab40
    ab42_stat = ab42_ratio <= 0.04147
    ab42_stat = ab42_stat.astype(int)
    return ab42_stat


def find_ptau_ratio(ptau, ab42):
    """
    Compute pTau/ab42 biomarker
    """
    ptau_ratio = ptau / ab42
    ptau_stat = ptau_ratio > 0.0649
    ptau_stat = ptau_stat.astype(int)
    return ptau_ratio, ptau_stat


def format_lumi_df(df):
    """
    format lumi dataframe
    """
    df["csf_date"] = [datetime.strptime(t, '%m/%d/%Y') for t in df["CSF_LP_DATE"]]
    df["Subject ID"] = df["Subject ID"].astype(int)

    ab42_ratio, ab42_stat = find_ab42_ratio(df.LUMIPULSE_CSF_AB42, df.LUMIPULSE_CSF_AB40)
    ab42_stat30 = find_ab42_ratio_30(df.LUMIPULSE_CSF_AB42, df.LUMIPULSE_CSF_AB40)
    ptau_ratio, ptau_stat = find_ab42_ratio(df.LUMIPULSE_CSF_pTau, df.LUMIPULSE_CSF_AB42)

    df["ab42_ratio"] = ab42_ratio
    df["ab42_stat"] = ab42_stat
    df["ab42_stat30"] = ab42_stat30
    df["ptau_ratio"] = ptau_ratio
    df["ptau_stat"] = ptau_stat
    return df


def csf_date_filter(lumi, t1, t2):
    """
    Only keep CSF data between dates t1 and t2
    """
    mask = (lumi['csf_date'] > t1) & (lumi['csf_date'] <= t2)
    lumi2 = lumi.loc[mask][:]
    return lumi2.sort_values(by='csf_date').drop_duplicates(subset=["Subject ID"], keep="last")


if __name__ == '__main__':
    lumi = pd.read_csv("C:/Users/Sayeh/OneDrive - University of Toronto/Documents/Git/Drives/"
                       "data/UP0320_LUMIPULSE_012821_forCollab.csv")
    df = format_lumi_df(lumi)

    a = Timestamp('1905-01-01 00:00:00')
    b = Timestamp('1910-01-01 00:00:00')
    df = csf_date_filter(df, a, b)
    plt.hist(df.ab42_ratio)
    plt.show()
    print(df.ab42_ratio.min(), df.ab42_ratio.max())
    print(df)