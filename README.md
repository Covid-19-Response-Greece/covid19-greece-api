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


## Projects & Organizations utilizing Coronavirus Greece API ([+ add yours!](#user-content-adding-your-project-to-the-list))

 * [Data & Web Science Laboratory](https://datalab.csd.auth.gr/), Aristotle University of Thessaloniki
 
 * [Data Science Lab](http://www.datastories.org/), University of Piraeus
 
 * [Postgraduate program “International Medicine / Health-Crisis Management”](http://crisis.med.uoa.gr/?lang=en), School of  Medicine, National & Kapodistrian University of Athens

 * [CovidDEXP-COVID-19 Data Exploration](https://covid19.csd.auth.gr) ([repo](https://github.com/Datalab-AUTH/covid19_dashboard)): An exploratory data analysis tool to worldwide monitor and detail the COVID-19 pandemic outbreak with visually rich presentation. A special segment about Greece can be found [here](https://covid19.csd.auth.gr/?tab=greece)
 
 * [Region of Western Macedonia](https://www.pdm.gov.gr/): Enrich daily region reports with explanatory visualizations
 
 * [COVID-19 Greece Tracker](https://covid-greece.github.io): Visualization of total and daily data with respect to severity and age,gender & region distribution.
 
## Adding your project to the list

If your project/organization utilizes the Coronavirus Greece API, you are kindly asked to place it here, under the following rules: 
- Add only open source projects.
- Make sure to cite this repo under your project as a source (together with a link). 
- Follow the same order as in the rest of the list `* [project_or_organization-name](project_or_organizatio-url) ([repo](repo-url)): description`
- Be careful to conform with the existing text formatting.

👉 [Add a new project to the list](https://github.com/Covid-19-Response-Greece/covid19-greece-api/edit/master/README.md)
