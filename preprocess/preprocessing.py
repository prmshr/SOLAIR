import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def row_selection_device_id(df):
  df_new = df
  columns_verification_list = ['tripCode','mainsOKFlag','lowBatteryFlag',\
  'overloadFlag','fuseBlownFlag','systemState','uvFlag','ovFlag','solarFlag',\
  'solarOverloadFlag','lineCurrentOverLoadFlag']
  value_for_correct_row = 'nan'
  for column in columns_verification_list:
    df_new = df_new[df_new[column].astype(str) == value_for_correct_row]
  return df_new
def feature_selection_device_id(df):
  return df[['DeviceId', 'SendDate', 'pvCurrent', 'pvPower', 'pvVoltage', 'solarKWHDaily']]
def read_solar_data(filepath):
  df = pd.DataFrame()
  if filepath[-3:] == 'csv':
    df = pd.read_csv(filepath)
  elif filepath[-4:] == 'xlsx' or filepath[-3:] == 'xls':
    df = pd.read_excel(filepath)
  else:
    raise Exception('Incorrect filetype: use .xls, .xlsx or .csv only.')
  return df

def send_date_checker(df):
    #select valid rows by SendDate
  df=df.copy()
  if (list(df.SendDate[df.SendDate.astype(str).str.contains('-') == False]))==[]:
    print('SendDates valid')
  else:
    print('removing invalid SendDates')
    df = df[df.SendDate.astype(str).str.contains('-') == False]
  return df

def generate_time_cols(df):
  df = df.copy()
  df['Hour'] = pd.to_datetime(df['SendDate']).dt.hour
  df['Time'] = pd.to_datetime(df['SendDate']).dt.time
  df['Year'] = pd.to_datetime(df['SendDate']).dt.year
  df['Day'] = pd.to_datetime(df['SendDate']).dt.day
  df['Minute'] = pd.to_datetime(df['SendDate']).dt.minute
  df['Month'] = pd.to_datetime(df['SendDate']).dt.month
  df['Second'] = pd.to_datetime(df['SendDate']).dt.second
  return df

def solar_data(filepath):
  df = read_solar_data(filepath)
  print('raw n_rows, n_cols:' + str(df.shape))
  df = row_selection_device_id(df)
  df = feature_selection_device_id(df)
  df = send_date_checker(df)
  print('cooking time features using SendDate...')
  df = generate_time_cols(df)
  print('selecting relevant features...')
  df = df[['Hour','Minute','Second','Day','Month','Year','pvPower']].reset_index(drop=True)
  print('final n_rows, n_cols:' + str(df.shape))
  print('success')
  print(df.head())
  return df
