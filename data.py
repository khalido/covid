"""
Loads data from interwebs"""

import numpy as np
import pandas as pd
import streamlit as st


def get_total_cases(start_date: str = "27 June 2021"):
    """gets total local cases"""
    start_date = pd.to_datetime(start_date, dayfirst=True)

    df = pd.read_html("https://covidlive.com.au/report/daily-source-overseas/nsw")[1]

    df.columns = df.columns.str.title()  # hate caps
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)  # need dates
    df = df.query("Date >= @start_date")  # only want dates for current spread

    df = df.sort_values(by="Date", ignore_index=True)  # sorted properly

    df = df[["Date", "Net", "Net2"]]
    df = df.rename(columns={"Net": "Local_cases", "Net2": "Overseas_cases"})

    # drop lines with "-", gotta be a better way of doing this
    row = df.iloc[-1]
    if any(row[["Local_cases", "Overseas_cases"]] == "-"):
        print(f"{row.Date:%d %b} is being updated")
        df = df.iloc[:-1]

    return df


def get_wild_cases():
    """returns df of infectious cases in the community"""
    try:
        df = pd.read_html("https://covidlive.com.au/report/daily-wild-cases/nsw")[1]
    except:
        print(f"something went wrong trying to access the data")
        return False

    df.columns = df.columns.str.title()  # hate caps
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)  # need dates
    df = df.sort_values(by="Date", ignore_index=True)  # sorted properly

    # drop lines with "-", gotta be a better way of doing this
    row = df.iloc[-1]
    if any(row[["Full", "Part", "Unkn"]] == "-"):
        print(f"{row.Date:%d %b} is being updated")
        df = df.iloc[:-1]

    return df


def get_data():
    """returns cleaned and joined data"""
    df_wild = get_wild_cases()
    df_total = get_total_cases()

    assert df_wild.shape[0] == df_total.shape[0]

    df = pd.merge(df_wild, df_total, on=["Date"])
    df["Isolating"] = df.Local_cases - df.Total

    # splitting unknown cases by ratio
    ratio = np.mean((df.Full + df.Part) / (df.Local_cases - df.Unkn))
    df["Unkn_inf"] = np.ceil(ratio * df.Unkn)
    df["Unkn_iso"] = df.Unkn - df.Unkn_inf

    df["Total_infectious"] = df.Full + df.Part + df.Unkn_inf

    # some stats
    for col in [
        "Full",
        "Part",
        "Unkn",
        "Unkn_inf",
        "Total_infectious",
        "Total",
        "Isolating",
        "Local_cases",
    ]:
        # exponential weighted avg
        df[f"{col}_ewa"] = df[col].ewm(span=7, adjust=False).mean()

        # rolling mean, though ideally add some forward prediction
        df[f"{col}_roll"] = df[col].rolling(7, center=True, min_periods=4).mean()

    return df
