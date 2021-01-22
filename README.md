# Fleet Position Scraper
This is a script I developed for work to help me keep track of different vessels in our fleet.

## How it Works
1. The script scrapes updated LAT/LON data string from an AIS source for each defined vessel.
2. The string is converted into a format that gets fed into a reverse geographic lookup, resulting in a physical location.
3. Desired attributes are written to a .CSV file. The file name is formatted to start with the current DATETIME for historical purposes.
