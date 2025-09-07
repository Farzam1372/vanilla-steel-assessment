import pandas as pd
import numpy as np

#clean supplier 1 dataset
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

    df[["weight_kg", "thickness_mm", "width_mm"]] = df[["weight_kg", "thickness_mm", "width_mm"]].apply(
    lambda col: col.astype(str).str.replace(",", ".").astype(float)
    )


    df["material"] = None
    df["source"] = "supplier1"

    return df

#clean supplier 2 dataset
def clean_supplier2(df):
    df = df.copy()
    df.rename(columns={
        'Material': 'material',
        'Description': 'description',
        'Weight (kg)': 'weight_kg',
        'Quantity': 'quantity'
    }, inplace=True)

    df['weight_kg'] = df['weight_kg'].astype(str).str.replace(",", ".").astype(float)

    df[["grade", "finish", "thickness_mm", "width_mm"]] = None
    df["source"] = "supplier2"

    return df


def merge_suppliers(df1, df2):
    return pd.concat([df1, df2], ignore_index=True)