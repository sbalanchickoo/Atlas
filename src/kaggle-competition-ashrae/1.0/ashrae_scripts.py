import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import gc

def fill_by_neighbor(col: str,df: pd.DataFrame) -> pd.DataFrame:
    rename1 = {col+'_x': col}
    rename2 = {col+'_y': col+'1'}
    rename3 = {col+'_y': col+'2'}
    col1 = col+'1'
    col2 = col+'2'

    df = df.merge(df[col].fillna(method='ffill'),left_index=True,right_index=True)
    df = df.rename(columns=rename1)
    df = df.rename(columns=rename2)

    df = df.merge(df[col].fillna(method='bfill'),left_index=True,right_index=True)
    df = df.rename(columns=rename1)
    df = df.rename(columns=rename3)
    
    df[col] = (df[col1].fillna(df[col2]) + df[col2].fillna(df[col1]))/2
    df.drop([col1, col2], 1, inplace=True)
        
    return df

def fill_by_group(col: str, grouper: str, df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.groupby(grouper)[col].mean().round(0)
    df1 = df1[df1.notnull()]
    df1 = df1.reset_index()
    df = df.merge(df1, left_on=grouper, right_on=grouper, how='left')
    col_x = col + '_x'
    col_y = col + '_y'
    df[col_x].fillna(df[col_y])
    df = df.rename(columns={col_x: col})
    df.drop([col_y], 1, inplace=True)
    del df1
    gc.collect()
    return df

def process_df(df, df_bldg_meta, df_weather):
    df = df.merge(df_bldg_meta, left_on='building_id', right_on='building_id', how='left')
    df = df.merge(df_weather, on=['site_id', 'timestamp'], how='left')
    df = df.astype({'timestamp': 'datetime64'}) 
    
    # Add time columns
    df['month'] = pd.Series(df['timestamp'].dt.month, dtype='int8')
    df['day'] = pd.Series(df['timestamp'].dt.dayofyear, dtype='int8')
    df['hour'] = pd.Series(df['timestamp'].dt.hour, dtype='int8')
    df['day_of_week'] = pd.Series(df['timestamp'].dt.dayofweek, dtype='int8')
    df['weekend'] = (df['day_of_week'] == 5) | (df['day_of_week'] == 6)
    df['night'] = (df['hour'] >= 19) | (df['day_of_week'] < 7)
    
    # Fill in weather gaps
    cols = ['sea_level_pressure', 'dew_temperature', 'air_temperature', 'cloud_coverage'
            , 'precip_depth_1_hr', 'wind_direction', 'wind_speed']
    dtype1 = {col: 'float32' for col in cols}
    df = df.astype(dtype1)
    for col in cols:
        df = fill_by_neighbor(col, df)
    dtype1 = {col: 'float16' for col in cols}
    dtype1.update({'site_id': 'int8', 'square_feet': 'float64'})
    if 'meter_reading' in df.columns:
        dtype1.update({'meter_reading': 'float64'})
    df = df.astype(dtype1)  
    
    return df

def get_bldg_meta(df_bldg_meta):
    df = fill_by_group('floor_count', 'primary_use', df_bldg_meta)
    df = fill_by_group('floor_count', 'site_id', df)
    df = fill_by_group('year_built', 'site_id', df)
    df['floor_count'].fillna(-1, inplace=True)
    df['year_built'].fillna(-1, inplace=True)
    df = df.astype({'floor_count': 'int8', 'year_built': 'int16'})
    df.reset_index(drop=True)
    return df

def get_weather(df_weather):
    cols = ['air_temperature', 'cloud_coverage', 'dew_temperature', 'sea_level_pressure']
    for col in cols:
        df_weather = fill_by_neighbor(col, df_weather)
    
    cols = ['cloud_coverage', 'precip_depth_1_hr', 'wind_direction', 'wind_speed']
    for col in cols:
        df_weather[col].fillna(0, inplace=True)
    
    dtype = {'air_temperature': 'float16'
                , 'cloud_coverage': 'float16'
                , 'dew_temperature': 'float16'
                , 'sea_level_pressure': 'float16'}
    df_weather = df_weather.astype(dtype)
    return df_weather

    