[![PyPI version](https://badge.fury.io/py/cad-tickers.svg)](https://badge.fury.io/py/cad-tickers) [![Downloads](https://pepy.tech/badge/cad-tickers)](https://pepy.tech/project/cad-tickers) [![Documentation Status](https://readthedocs.org/projects/cad-tickers/badge/?version=latest)](https://cad-tickers.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/FriendlyUser/cad_tickers/branch/master/graph/badge.svg)](https://codecov.io/gh/FriendlyUser/cad_tickers)
 
## Cad Tickers


*Note* Anything below `0.2.0` should be considered testing, code, the apis are subject to change until `0.2.0`.

Set of utilities modules designed to scrap data from the web.

Will write more documentation later, for now refer to test cases.


For the tsx searching, it was kinda tedious to test each of the possible values, as a result, only `exchanges` and `marketcap` values are validated.

Given the new redesign of the web.tmxmoney site, don't expect the existing api to work
for a super long period of time.

Support will be provided to the best of my ability.

### How to run tests

```
pytest
```

### How to deploy


```
# Needed for readthedocs documentation
poetry export -f requirements.txt > requirements.txt.
```

#### Todo

Add parameters and returns, double sync with readthe docs and github pages.

- [ ] Go through list in https://thecse.com/en/listings and make pandas dataframe?
Iterate until last css is no longer present

- [ ] make another function that uses the new graphql api instead of the standard api.
- [x] Convert all the Input to Parameters and output to Return
- [x] add just read the docs
- [x] add code coverage uploading 
