import json
import pandas as pd
import cloudscraper
import sqlite3

# Define the URL and payload for fetching flight data
url = "https://www.admtl.com/en-CA/webruntime/api/apex/execute?language=en-CA&asGuest=true&htmlEncode=false"

payload = {
    "namespace": "",
    "classname": "@udd/01pMm00000AWKuH",
    "method": "getFlights",
    "isContinuation": False,
    "params": {
        "language": "en-CA",
        "page": "departures"
    },
    "cacheable": False
}

# SQL Query to create the flights_today table
create_table_q = """
CREATE TABLE IF NOT EXISTS flights_today (
    AirlineName TEXT,
    gate INTEGER,
    time DATETIME,
    updatedTime DATETIME,
    AirportName TEXT,
    status TEXT,
    UniqueDisplayNo TEXT PRIMARY KEY
);
"""

def fetch_flight_data(url):
    response = cloudscraper.create_scraper().post(url, json=payload)
    response.raise_for_status()
    return response

def parse_json_content(response_content):
    return json.loads(response_content)

def format_json_data(json_data):
    return json.dumps(json_data, indent=4)

def convert_to_dataframe(json_data, key='returnValue', section='flightsForToday'):
    return pd.json_normalize(json_data[key][section])

def process_flights_to_df(url):
    response = fetch_flight_data(url)
    print(f"HTTP Status Code: {response.status_code}")

    raw_data = response.content
    structured_data = parse_json_content(raw_data)
    formatted_data = format_json_data(structured_data)

    flights_df = convert_to_dataframe(structured_data)

    flights_df.rename(columns={
        'TerminalGate': 'gate',
        'FormattedScheduledTime': 'time',
        'FormattedUpdatedTime': 'updatedTime',
        'OperationalStatusDescription': 'status'
    }, inplace=True)

    new_columns_of_interest = ['AirlineName', 'gate', 'time', 'updatedTime', 'AirportName', 'status', 'UniqueDisplayNo']
    new_df = flights_df[new_columns_of_interest]

    new_df = new_df.copy()
    new_df['gate'] = new_df['gate'].str.extract('(\d+)')  # Extract digits
    new_df = new_df.dropna()
    new_df['gate'] = new_df['gate'].astype(int)

    return new_df



def save_to_sql(df):
    connection = sqlite3.connect('flights_today.db')
    df.to_sql('flights_today', con=connection, if_exists='replace', index=False)
    connection.close()
    print("Data stored in SQLite database successfully.")

def main():

    # Process flights and store them
    flights_df = process_flights_to_df(url)
    save_to_sql(flights_df)

main()