# jk-fuzzy-heroku
This is used to perform the fuzzy name match between two inputted text'  

---
**NOTE**

The code is tested on Window 11, but should not be a problem running it in Ubuntu >= 18.04

---

## A typical top-level directory layout
***
    .
    ├── csv_files                   # Updated test files 
    ├── preprocess                  # tools and utilities files
    ├── utility                     # main functional module to process the name text according to the requirements 
    ├── fuzzy_matcher               # calling python file (generate .csv/ one2one matching accordingly)
    ├── requirements.txt
    └── README.md

## Getting Started
***
The following packages mentioned are must:

* Python Levenshtein 0.12.2
* Fuzzywuzzy  0.18.0
* Pandas 1.4.2
* Python 3.9.12
* pip3 21.2.4

## Create your virtual environment
***
* Conda is used create a virtual environment using anaconda prompt
  * #### Create
    * `conda create --name <environment-name>`
  * ####  Activate
    * `conda activate <environment-name>`

## Install the other requirement as follows:
***
* #### Installation
  * Requirements
    * `pip install -r requirements.txt` 


## From your favorite development directory:
***
* #### Cloning
  * `git clone  https://github.com/jai-kisan/jk-fuzzy-heroku.git`
* #### Branching
  * `git checkout divyanshu`

## Check versioning
***
* #### Python
  * `python --version`
* #### Pip
  * `pip --version`

## Running the code
***
***Here we have used conda to create a virtual environment using anaconda prompt***
* `python fuzzy_matcher.py`

