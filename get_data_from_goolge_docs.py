# script to download data from google doc to csv file
# secrets.py contains data about the key on a google spreadsheet
# example url https://docs.google.com/spreadsheets/d/1-GZ36cIpx1oIjiZ4hCZ1L6JieierCfJA4rsK36Lbe0E
# where "1-GZ36cIpx1oIjiZ4hCZ1L6JieierCfJA4rsK36Lbe0E" is the key

# importing public libraries
import pandas as pd
from io import BytesIO
import requests

# importing internal modules
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
    google_authorization_data_key = secrets.google_authorization_data_key
    authorization_data_link = secrets.authorization_data_link
    authorization_data_name = secrets.authorization_data_name

    df_authorization_data = down_load_google_doc(google_authorization_data_key)
    save_df_to_csv(df_authorization_data,
                   authorization_data_link,
                   authorization_data_name)

    google_chat_id_data_key = secrets.google_chat_id_data_key
    chat_id_data_link = secrets.chat_id_data_link
    chat_id_data_name = secrets.chat_id_data_name

    df_chat_id_data = down_load_google_doc(google_chat_id_data_key)
    save_df_to_csv(df_chat_id_data,
                   chat_id_data_link,
                   chat_id_data_name)