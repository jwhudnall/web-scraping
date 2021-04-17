# Web Scraping
This repo is a collection of scripts created while self-learning web scraping. The original intent of the data collection was to update boat positions (Lat/Lon) to assist with fleet tracking for my primary job. This later evolved into hunting for one of the elusive RTX 3000 series GPUs.

## 1. fleet-positions (Not Working as of 2021-04)
<b>2021-04 Update</b> The website from which this script collects data was modified. The script needs to be updated.
This is a script I developed to assist in tracking the positioning of our fleet, both at runtime and over time.

### How it Works
1. The script scrapes updated LAT/LON data string from an AIS source for each defined vessel.
2. The string is converted into a format that gets fed into a reverse geographic lookup, resulting in a physical location.
3. Desired attributes are written to a .CSV file. The file name is formatted to start with the current DATETIME for historical purposes.

tqdm is used to show progress as the script enumerates the fleet:
![Boat Scraper Progress](/web-scraper-progress.png)

## 2. gpu-search
I take the skills I've learned so far and apply it to searching Best Buy's website for one of the new RTX 3000 series cards.

### Strategy
The script uses <a href="https://chromedriver.chromium.org/downloads">chromedriver</a> to:
1. Load the specified GPU's landing page.
2. Retrieve the text value for the purchase button (usually "Add to Cart").
3. If the text is <i>not</i> "Add to Cart", the window closes. The script restarts shortly thereafter. 
4. If the text <i>is</i> "Add to Cart", an audible alarm sounds, indicating the card is available for purchase.
