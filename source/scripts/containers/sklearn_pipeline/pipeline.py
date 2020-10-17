import os
import datetime
import pandas as pd
import numpy as np
import pandas_gbq as gbq
from google.oauth2 import service_account
from sklearn.linear_model import LogisticRegression


# fetch the data set and add IDs 
games_df = pd.read_csv("https://github.com/bgweber/Twitch/raw/master/Recommendations/games-expand.csv")
games_df['user_id'] = games_df.index 
games_df['new_user'] = np.random.choice([0, 1], size=len(games_df), p=[0.9, 0.1])

# train and test groups 
train = games_df.query("new_user == 0")
x_train = train.drop(columns=['label', 'user_id', 'new_user'])
y_train = train['label']
test = games_df.query("new_user == 1")
x_test = test.drop(columns=['label', 'user_id', 'new_user'])

# build a model
model = LogisticRegression()
model.fit(x_train, y_train)
y_pred = model.predict_proba(x_test)[:, 1]

# build a predictions data frame
result_df = pd.DataFrame({'user_id': test['user_id'], 
                          'pred': y_pred,
                          'time': str(datetime.datetime.now())})

# save predictions to BigQuery 
table_id = "dsp_demo.user_scores"
project_id = os.environ['GOOGLE_PROJECT_ID']
credentials = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']
)
gbq.to_gbq(dataframe=result_df, 
           destination_table=table_id, 
           project_id=project_id, 
           if_exists='replace',
           credentials=credentials)
