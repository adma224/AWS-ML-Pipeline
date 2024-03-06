# data_utils.py
import requests
import pandas as pd
import json

def fetch_random_users(sample_size):
    response = requests.get(f'https://randomuser.me/api/?results={sample_size}')
    if response.status_code == 200:
        users_json = response.json()['results']
        users_df = pd.json_normalize(users_json)  # Convert JSON to DataFrame
        return users_df
    else:
        return None

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def save_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)