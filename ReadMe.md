[![PyPI version](https://badge.fury.io/py/cad-tickers.svg)](https://badge.fury.io/py/cad-tickers) [![Downloads](https://pepy.tech/badge/cad-tickers)](https://pepy.tech/project/cad-tickers) [![Documentation Status](https://readthedocs.org/projects/cad-tickers/badge/?version=latest)](https://cad-tickers.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/FriendlyUser/cad_tickers/branch/master/graph/badge.svg)](https://codecov.io/gh/FriendlyUser/cad_tickers)
 
## Cad Tickers
Function to extract exchange data from the cse and tsx websites and various other data sources. This package is primarily focussed on scrapping data for the canadian stock market.


The entire 0.2.x version of tsx functions are now depricated.


### How to run tests

```
pytest
```

```
# Needed for readthedocs documentation
poetry export -f requirements.txt > requirements.txt.
```

#### Todo

Add parameters and returns, double sync with readthe docs and github pages.

Add include/exclude functionality https://python-poetry.org/docs/pyproject/#include-and-exclude
- [x] update documentation to use graphql constants
- [x] Get tsx tickers with new approach, downloading
all the xlsx files and merging them and/or the json api - https://www.tsx.com/json/company-directory/search/tsx/.*

- [x] make another function that uses the new graphql api instead of the standard api for tsx (have to know).
- [ ] Go through list in https://thecse.com/en/listings and make pandas dataframe?
Iterate until last css is no longer present
- [x] Convert all the Input to Parameters and output to Return
- [x] add just read the docs
- [x] add code coverage uploading 
- [x] news and iiroc fetching
