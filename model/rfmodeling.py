import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score 
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
def model_wrangling(conditions_aqi_df, df):
  conditions_aqi_df = conditions_aqi_df
  df_alias = df.copy()
  print(df_alias.shape)
  sql_query = 'SELECT b.*, a.pvPower, a.Second, a.Minute FROM df_alias a LEFT JOIN conditions_aqi_df b ON a.Day = b.Day AND a.Year = b.Year AND a.Month = b.Month AND a.Hour = b.Hour'
  queried = sqldf(sql_query, locals())
  print('shape wrangled ' + str(queried.shape))
  return queried
#one-hot encode and return concatenated df
def build_cats(df):
  df=df.copy()
  catv = 'Weather Condition Code' #variable col name
  # one dummy variable should be dropped to avoid multicollinearity
  if catv not in df.columns: return df
  codes=pd.get_dummies(df[catv],drop_first=True)
  df = df.drop(catv,axis=1)
  df=pd.concat([df,codes],axis=1)
  df.columns=df.columns.astype(str) #catv dummies are floats
  return df

def build_time_features(df):
  x = df.copy()
  print('orig' + ' ' + str(len(x.columns)) + ' ' + 'features')
  # Extract time features for 'Month'
  x['month_sin'] = np.sin(2 * np.pi * x['Month'] / 12)  # Encode month as a cyclical feature using sine transformation
  x['month_cos'] = np.cos(2 * np.pi * x['Month'] / 12)  # Encode month as a cyclical feature using cosine transformation

  # Extract time features for 'Hour'
  x['hour_sin'] = np.sin(2 * np.pi * x['Hour'] / 24)  # Encode hour as a cyclical feature using sine transformation
  x['hour_cos'] = np.cos(2 * np.pi * x['Hour'] / 24)  # Encode hour as a cyclical feature using cosine transformation

  # Extract time features for 'Minute'
  x['minute_sin'] = np.sin(2 * np.pi * x['Minute'] / 60)  # Encode minute as a cyclical feature using sine transformation
  x['minute_cos'] = np.cos(2 * np.pi * x['Minute'] / 60)  # Encode minute as a cyclical feature using cosine transformation

  # Extract time features for 'Second'
  x['second_sin'] = np.sin(2 * np.pi * x['Second'] / 60)  # Encode second as a cyclical feature using sine transformation
  x['second_cos'] = np.cos(2 * np.pi * x['Second'] / 60)  # Encode second as a cyclical feature using cosine transformation

  # Create interaction features
  x['hour_month_interaction'] = x['Hour'] * x['Month']  # Interaction between hour and month
  x['hour_minute_interaction'] = x['Hour'] * x['Minute']  # Interaction between hour and minute
  x['hour_second_interaction'] = x['Hour'] * x['Second']  # Interaction between hour and second
  x=x.drop(columns=['Hour','Minute','Second']) #not dropping month
  print('final' + ' ' + str(len(x.columns)) + ' ' + 'features')
  return x

def model_df(conditions_aqi_df, df):
  df=df.copy()
  df = model_wrangling(conditions_aqi_df, df)
  df=df.copy()
  df=df[df.pvPower>0]
  df = build_cats(df)
  df = df.dropna()
  df = build_time_features(df)
  print('running rf')
  reg, y_pred = plot_rf(df)
  # df['pvPower_pred'] = y_pred
  return (df,reg,y_pred)

# def model_x_y_builds(df):
#   x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)
#   return {'x_train':x_train, 'x_test':x_test,'y_train':y_train, 'y_test':y_test}

def rf(x,y):
  print('creating rf')
  params = {
    "n_estimators": 500,
    "max_depth": 20,
    "min_samples_split": 5,
    "warm_start":True,
    "oob_score":True,
    "random_state": 42
    }
  reg =RandomForestRegressor(**params)
  print('train_test_split')
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)
  print('x_train shape: ' + str(x_train.shape) + ' ' + 'x_test shape: ' + str(x_test.shape) + ' ')
  print('y_train shape: ' + str(x_train.shape) + ' ' + 'y_test shape: ' + str(x_test.shape) + ' ')
  reg.fit(x_train, y_train)
  y_pred = reg.predict(x_test)
  mse=mean_squared_error(y_test, y_pred)
  rmse = np.sqrt(mse)
  print("Root Mean Squared Error:", rmse)
  r2 = r2_score(y_test, y_pred)
  print("R-squared Score:", r2)
  return (reg,y_pred)

def plot_rf(df):
  print('building x,y')
  y = df.pvPower
  x = df.drop(columns=['pvPower'])
  print('x shape: ' + str(x.shape))
  print('y shape: ' + str(y.shape))
  reg, y_pred = rf(x,y)
  # Get feature importances
  feature_importance = reg.feature_importances_

  # Get feature names
  feature_names = x.columns  # Assuming X is feature matrix
  print('num feature names: ' + str(len(x.columns)))

  # Sort feature importances in descending order
  sorted_idx = np.argsort(feature_importance)[::-1]

  # Plot feature importances
  plt.figure(figsize=(10, 6))
  plt.bar(range(len(feature_importance)), feature_importance[sorted_idx], align='center')
  plt.xticks(range(len(feature_importance)), feature_names[sorted_idx], rotation='vertical')
  plt.xlabel('Features')
  plt.ylabel('Importance')
  plt.title('Feature Importance')
  plt.tight_layout()
  plt.show()
  return (reg, y_pred)
