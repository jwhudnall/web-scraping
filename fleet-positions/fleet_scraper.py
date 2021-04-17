import requests
import time
import os
from bs4 import BeautifulSoup
from csv import writer
from geopy.geocoders import Nominatim
from tqdm import tqdm


agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
geolocator = Nominatim(user_agent="jwh")

timestamp = time.strftime('%Y%m%d-%I_%M_%p')
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)
timestamp = time.strftime('%Y%m%d-%I_%M_%p')
filename = timestamp + '-Fleet Location.csv'
scrape_file = os.path.join(DATA_DIR, filename)

boats = {
    "Brangus": "https://www.vesselfinder.com/vessels/BRANGUS-IMO-0-MMSI-366899270",
    "Calcasieu River": "https://www.vesselfinder.com/vessels/CALCASIEU-RIVER-IMO-0-MMSI-367313850",
    "Cavalier State": "https://www.vesselfinder.com/vessels/CAVALIER-STATE-IMO-0-MMSI-367340130",
    "Columbia River": "https://www.vesselfinder.com/vessels/COLUMBIA-RIVER-IMO-0-MMSI-367187130",
    "Cooper River": "https://www.vesselfinder.com/vessels/COOPER-RIVER-IMO-0-MMSI-366867370",
    "East River": "https://www.vesselfinder.com/vessels/EAST-RIVER-IMO-0-MMSI-366898790",
    "Evergreen State": "https://www.vesselfinder.com/vessels/EVERGREEN-STATE-IMO-0-MMSI-367156370",
    "Lone Star State": "https://www.vesselfinder.com/vessels/LONESTAR-STATE-IMO-0-MMSI-367183730",
    "McCormack Boys": "https://www.vesselfinder.com/vessels/MCCORMACK-BOYS-IMO-0-MMSI-366872170",
    "Miami River": "https://www.vesselfinder.com/vessels/MIAMI-RIVER-IMO-0-MMSI-366898810",
    "Muskegon River": "https://www.vesselfinder.com/vessels/MUSKEGON-RIVER-IMO-0-MMSI-367509760",
    "Ohio River": "https://www.vesselfinder.com/vessels/OHIO-RIVER-IMO-0-MMSI-366899290",
    "Pearl River": "https://www.vesselfinder.com/vessels/PEARL-RIVER-IMO-0-MMSI-367187120",
    "Saginaw River": "https://www.vesselfinder.com/vessels/SAGINAW-RIVER-IMO-0-MMSI-367511230",
    "St Johns River": "https://www.vesselfinder.com/vessels/SAINT-JOHNS-RIVER-IMO-0-MMSI-367313760",
    "St Louis River": "https://www.vesselfinder.com/vessels/ST-LOUIS-RIVER-IMO-0-MMSI-367609770",
    "Volunteer State": "https://www.vesselfinder.com/vessels/VOLUNTEER-STATE-IMO-0-MMSI-367314110",
    "Wolf River": "https://www.vesselfinder.com/vessels/WOLF-RIVER-IMO-0-MMSI-367060910"
    }

def abbreviate_state(state):
    state_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
    }
    if state in state_dict:
        state = state_dict[state]
    return state


def get_city(raw):
    if 'city' in raw['address']:
        town = raw['address']['city']
        
    elif 'town' in raw['address']:
        town = raw['address']['town']
        
    elif 'village' in raw['address']:
        town = raw['address']['village']
        
    elif 'county' in raw['address']:
        town = raw['address']['county']
        
    else:
        town = 'Error'
        
    return town


def convert_time(last_update):
    unit_to_minutes = {'day':24*60, 'hour': 60, 'min': 1}
    # Extract leading integer unit measurement
    number = ''.join(x for x in last_update if x.isdigit())
    number = int(float(number))
    for unit in unit_to_minutes:
        if unit in last_update:
            conversion = number * unit_to_minutes[unit]
            return conversion
    return last_update

start = time.time()

with open(scrape_file, 'w', newline='') as file:
    csv_writer = writer(file)
    
    # Add Headers
    csv_writer.writerow(['Vessel', 'Lat-Long','Last Update', 'Last Update (minutes)','City', 'State'])
    
    for boat, url in tqdm(boats.items()):
        response = requests.get(url, headers=agent)
        soup = BeautifulSoup(response.text,"html.parser")
        
        # Isolate table of interest
        table = soup.find_all(class_='v3')
        
        # Isolate and clean lat, long coordinates
        coords = table[9] # coordinate row
        text = coords.get_text() # Text from coordinate row
        latlon = text.split('/')
        latlon_clean = [val[:-2] for val in latlon]
        latlon_clean[1] = '-'+latlon_clean[1]  
        position = ', '.join(latlon_clean)

        # Obtain raw physical data
        physical = geolocator.reverse(position)
        # location = physical.address # Gives full address. Too much for our needs.
        vessel_raw = physical.raw 
        
        # Isolate town, state data values
        town = get_city(vessel_raw)

        state = vessel_raw['address']['state']
        state = abbreviate_state(state) # Abbreviate state from full name to a 2-letter code

        # Isolate and clean last position update
        time_since_last_position = table[11].get_text() # coordinate row
        cleaned_time = time_since_last_position[:-3]
        converted_time = convert_time(cleaned_time)
        
        # Write results to spreadsheet row
        csv_writer.writerow([boat, position, cleaned_time, converted_time, town, state])
        
        # Wait n seconds in between requests
        time.sleep(1)
        
end = time.time()
duration = end - start

print(f'Finished. This script took {duration} seconds to run')