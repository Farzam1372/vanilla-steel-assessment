import pandas as pd
import numpy as np

def clean_supplier1(df):
    df = df.copy()
    df.rename(columns={
        'Quality/Choice': 'quality',
        'Grade': 'grade',
        'Finish': 'finish',
        'Thickness (mm)': 'thickness_mm',
        'Width (mm)': 'width_mm',
        'Description': 'description',
        'Gross weight (kg)': 'weight_kg',
        'Quantity': 'quantity'
    }, inplace=True)

    df['weight_kg'] = df['weight_kg'].astype(str).str.replace(",", ".").astype(float)
    df['thickness_mm'] = df['thickness_mm'].astype(str).str.replace(",", ".").astype(float)
    df['width_mm'] = df['width_mm'].astype(str).str.replace(",", ".").astype(float)

    df["material"] = None
    df["source"] = "supplier1"

    return df


def clean_supplier2(df):
    df = df.copy()
    df.rename(columns={
        'Material': 'material',
        'Description': 'description',
        'Weight (kg)': 'weight_kg',
        'Quantity': 'quantity'
    }, inplace=True)

    df['weight_kg'] = df['weight_kg'].astype(str).str.replace(",", ".").astype(float)

    df["grade"] = None
    df["finish"] = None
    df["thickness_mm"] = None
    df["width_mm"] = None
    df["source"] = "supplier2"

    return df


def merge_suppliers(df1, df2):
    return pd.concat([df1, df2], ignore_index=True)