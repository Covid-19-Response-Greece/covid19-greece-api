<p align="center">
    <img src="https://cdn2.iconfinder.com/data/icons/covid-19-2/64/29-Doctor-256.png">
</p>

# Coronavirus Tracker API for Greece

This repository provides an API with up-to-date data about the Coronavirus (COVID-19) outbreak in Greece.

This project is performed by volunteers of [COVID-19 Response Greece](https://www.covid19response.gr).

## Data sources
This API combines data from multiple sources. All data are fetched from [here](https://github.com/Covid-19-Response-Greece/covid19-data-greece) and updated 3 times a day using Github Actions.

* Johns Hopkins CSSE: https://systems.jhu.edu/research/public-health/ncov

* National Public Health Organization (NPHO) of Greece: https://eody.gov.gr

* Wikipedia: https://el.wikipedia.org/wiki/Πανδημία_του_κορονοϊού_στην_Ελλάδα_το_2020

* World Health Organization: https://www.who.int

  ( [+ suggest a data source!](mailto:alex.delitzas@gmail.com) )
  
## Requirements

Run the following command to install depedencies:

    pip install -r requirements.txt 

## How to run

    python app.py
    
## How to test

*Example*: Get the number of confirmed cases

Request:

    curl -v localhost:5000/confirmed
    
Response:
    
```
{
  "cases": [
    {
      "date": "2020-01-22",
      "confirmed": 0
    },
    {
      "date": "2020-01-23",
      "confirmed": 0
    },
    ...
  ]
}   
```


    
