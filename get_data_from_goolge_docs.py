#script to download data from google doc to csv file
#secrets.py contains data about the key on a google spreadsheet
#example url https://docs.google.com/spreadsheets/d/1-GZ36cIpx1oIjiZ4hCZ1L6JieierCfJA4rsK36Lbe0E 
#where "1-GZ36cIpx1oIjiZ4hCZ1L6JieierCfJA4rsK36Lbe0E" is the key

#importing public libraries
import pandas as pd
from io import BytesIO
import requests

#importing internal modules
import secrets

def down_load_google_doc(doc_key):
    google_doc_url = 'https://docs.google.com/spreadsheets/d/'
    output_param = '/export?gid=0&format=csv'
    r = requests.get(google_doc_url + doc_key + output_param)
    data = r.content
    df = pd.read_csv(BytesIO(data), index_col=0)
    return(df)

def save_df_to_csv(df, link, file_name):
    df.to_csv(link + f'{file_name}.csv')

if __name__ == '__main__':
    doc_key = secrets.google_doc_key
    link = secrets.authorization_data_link
    file_name = secrets.authorization_data_name

    df = down_load_google_doc(doc_key)
    save_df_to_csv(df, link, file_name)