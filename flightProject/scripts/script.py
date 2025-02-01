import json
import pandas as pd
import cloudscraper
from sqlalchemy import create_engine
import pymysql


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



def fetch_flight_data(url):
    response = cloudscraper.create_scraper().post(url, json=payload)
    response.raise_for_status()
    return response


def parse_json_content(response_content):
    """
    Parse JSON content from the response content.

    Args:
    response_content (bytes): The response content in bytes.

    Returns:
    dict: The parsed JSON content as a dictionary.
    """
    return json.loads(response_content)


def format_json_data(json_data):
    """
    Format JSON data with indentation for better readability.

    Args:
    json_data (dict): The JSON data to format.

    Returns:
    str: The formatted JSON data as a string.
    """
    return json.dumps(json_data, indent=4)


def convert_to_dataframe(json_data, key='returnValue', section='flightsForToday'):
    """
    Convert JSON data to a pandas DataFrame.

    Args:
    json_data (dict): The JSON data to convert.
    key (str): The key in the JSON data that contains the list of records.

    Returns:
    pandas.DataFrame: The resulting DataFrame.
    """
    return pd.json_normalize(json_data[key][section])



def process_flights_to_df(url):
    # Fetch the flight data
    response = fetch_flight_data(url)
    print(f"HTTP Status Code: {response.status_code}")

    # Step 1: Raw Data
    raw_data = response.content

    # Step 2: Structured Data
    structured_data = parse_json_content(raw_data)

    formatted_data = format_json_data(structured_data)

    # Step 3: JSON Format Data
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

    filtered_df = new_df[(new_df['gate'] >= 62) & (new_df['gate'] <= 68)]

    return filtered_df

def df_to_html(df):
    return df.to_html("flights.html")

def save_to_sql(df, table_name="todays_flights", connection_string='mysql+pymysql://root:VavaChab!2!6@localhost:3306/flights_data'):
    engine = create_engine(connection_string)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Data stored in table '{table_name}' successfully.")
    
def main():
    flights_df = process_flights_to_df(url)
    df_to_html(flights_df)
    
main()