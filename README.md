# Winter 2021 SI507 Final Project: Wildland Fire in U.S. National Parks

This program is a SI 507 final project designed to facilitate management of safety in national sites. After implementing the interactive command line tool, the users can enter a state to obtain useful information about the national sites in that state, including site name, site category (national site, national historical site etc.), phone. Users can also obtain some charts showing the fire information of that national park. 
Several basic programming techniques are adopted in the project, which includes accessing data efficiently with caching via scraping and web API, using SQLite for data manipulating and using Plotly for data visualization, etc.

## Data sources

The program relied on:

* [National Park Service Data API](https://www.nps.gov/subjects/digital/nps-data-api.htm)
* [National Park Service Website](https://www.nps.gov/index.htm)
* [Wildland Fire In National Parks CSV File](https://public-nps.opendata.arcgis.com/datasets/wildland-fire-locations/data?geometry=62.234%2C-13.945%2C130.437%2C73.016)
* [NationalPark CSV File](https://github.com/xinyuma0214/final-proj-datasource.git)

## Run the project


### Step 1: apply for API key

a. Go to data source 1 to apply an API key.

b. Create a new python file "secrets.py" in the same folder as "final_proj.py". And add the code:
```
API_KEY = '<your key>'
```

### Step 2: install related package
You may need to install Plotly, numpy, BeautifulSoup, sqlite3, requests, etc. The command is below:
```
$ python3 -m pip install {new_module}
```

### Step 3: run!

The "final_proj.py" file will initiate the program.
```
$ python3 final_proj.py
```
:angel: __Note: before running, please change the directory to the final project directory before you run the program__

## Data presentation

* The first interactive command is to enter a state name, users can get that state’s all national parks’ info (e.g. name, phone, address, zipcode).
* Secondly, users can choose which park’s detailed to look at (to enter a number), then they can get (1) the topics in the park to see which topic is prone to cause the human cause fire so that they can change that to a safe one (2) email-contact and website of that park, which can provide manager the contact info of that park. (3) total acres of that park. (4) total number of fires happened in that park during 1800 to 2021. Users are free to enter “back” to research another state and “exit” to end the program.
* Thirdly, if they want to see the visualization of the result, they can enter A/B/C/D to see:
    * A __bar chart__ showing the Number of fires happened with the interval of 20 years and the comparison to the average of the fires in all parks.
    * Fire cause in that park in a __pie chart__.
    * A __bar chart__ showing the count of each size class during past 120 years (size class: A to G represents fire level from low to high).
    * A __bar chart__ showing the park fire acres compared to all parks fire acres with the interval of every 20 years.

## Authors

* **Xinyu Ma** - [xinyuma](https://github.com/xinyuma0214)

## Acknowledgments

* Professor Bobby Madamanchi and all GSI of SI 507 in winter 2021.



