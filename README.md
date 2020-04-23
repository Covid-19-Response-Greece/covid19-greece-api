<p align="center">
    <img src="https://cdn2.iconfinder.com/data/icons/covid-19-2/64/29-Doctor-256.png">
</p>

# Coronavirus Tracker API for Greece

This repository provides an API with real-time data about the Coronavirus (COVID-19) outbreak in Greece.

API page: [https://covid-19-greece.herokuapp.com](https://covid-19-greece.herokuapp.com)

This project is performed by volunteers of [COVID-19 Response Greece](https://www.covid19response.gr).

## Documentation

API documentation can be found [here](https://covid-19-greece.herokuapp.com/docs).

## Example

All the endpoints are located at [https://covid-19-greece.herokuapp.com/](https://covid-19-greece.herokuapp.com/) and are accessible via https. 

*Example*: Get the number of confirmed cases as timeseries

<ins>Request</ins>:

You can visit https://covid-19-greece.herokuapp.com/confirmed via a browser or run the following command:

    curl https://covid-19-greece.herokuapp.com/confirmed | json_pp
    
<ins>Response</ins>:
    
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

## How to run locally

    python app.py
    
## How to test locally

*Example*: Get the number of confirmed cases

Request:

    curl -v localhost:5000/confirmed


    
