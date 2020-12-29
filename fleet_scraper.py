import requests
import time
from bs4 import BeautifulSoup
from csv import writer
from geopy.geocoders import Nominatim
from tqdm import tqdm


agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
geolocator = Nominatim(user_agent="jwh")
timestamp = time.strftime('%Y%m%d-%I_%M_%p')
filename = timestamp + '-Fleet Location.csv'

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

start = time.time()

with open(filename, 'w', newline='') as file:
    csv_writer = writer(file)
    
    # Add Headers
    csv_writer.writerow(['Vessel', 'Lat-Long','Last Update','Address'])
    
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
        # Reverse lat-lon lookup, giving address
        physical = geolocator.reverse(position)
        location = physical.address
        
        # Isolate and clean last position update
        time_since_last_position = table[11].get_text() # coordinate row
        cleaned_time = time_since_last_position[:-3]
        
        
        # Write results to spreadsheet row
        csv_writer.writerow([boat, position, cleaned_time, location])
        
        # Wait n seconds in between requests
        time.sleep(1)
        
end = time.time()
duration = end - start

print(f'Finished. This script took {duration} seconds to run')