# Ethiopia Regions Population Dashboard - Version 1

The purpose of this dashboard is to visualize livestock population data from: 
* ETH CSA Livestock Reports
    * Population data for 
        * Cattle
        * Sheep
        * Goats
        * Camels
        * Poultry
        * Dairy Cows
        * Milking Cows
        * Mules
        * Donkeys
        * Horses

## Running the app

* Ensure you have requirements.txt installed 
* Run python index.py 

## Files and editting

### File structure 

```
├─requirements.txt
├─index.py
├─utils/
│ ├─get_data.py
│ └─api_helpers.py
├─assets/
│ ├─GBADs-LOGO-Black-sm.png
│ └─eth_admbnda_adm1_csa_bofedb_2021.geojson
├─README.md
├─layouts/
│ ├─metadata_tab.py
│ ├─map_tab.py
│ ├─layout.py
│ ├─styling.py
│ ├─data_tab.py
│ ├─graph_helpers.py
│ └─graph_tab.py
├─app.py
└─data/
  └─csa.csv
```

### Tabs 

The contents of each tab is in the layouts/ dir. 
