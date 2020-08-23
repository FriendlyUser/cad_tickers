.. cad_tickers documentation master file, created by
   sphinx-quickstart on Sun Jul 26 08:33:39 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cad_tickers's documentation!
=======================================

.. image:: https://badge.fury.io/py/cad-tickers.svg
   :target: https://badge.fury.io/py/cad-tickers

.. image:: https://codecov.io/gh/FriendlyUser/cad_tickers/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/FriendlyUser/cad_tickers


.. toctree::
    :maxdepth: 2

.. autosummary::
     :toctree:

      cad_tickers
      cad_tickers.exchanges
      cad_tickers.util
      cad_tickers.news

Canadian Securities Exchange
=============================

Functions to download tickers from the cse

.. automodule:: cad_tickers.exchanges.cse
   :members:
   :undoc-members:



Toronto Stock Exchange
========================

Set of functions to scrap ticker data from the toronto stock exchange.

Will definitely split into smaller files once the graphql api becomes the main api.

.. automodule:: cad_tickers.exchanges.tsx
   :members:
   :undoc-members:


Stock News
=======================

Extract news from stocks on yahoo

.. automodule:: cad_tickers.news.stock_news
   :members:
   :undoc-members:

IIROC Halts
=========================

Find out what latest stocks have been halted from iiroc (only canada)

.. automodule:: cad_tickers.news.iiroc_halts
   :members:
   :undoc-members:

Stock Utilities
===============

Contains various utility classes

.. automodule:: cad_tickers.util.utils
   :members:
   :undoc-members:

Examples
=================

*Grab Descriptions for all tsx tickers*

.. code-block:: python

   from cad_tickers.exchanges.tsx import dl_tsx_xlsx, add_descriptions_to_df_pp
   from datetime import datetime
   start_time = datetime.now()
   df = dl_tsx_xlsx()
   # df = add_descriptions_to_df(df)
   df = add_descriptions_to_df_pp(df)
   end_time = datetime.now()
   df.to_csv('tsx_all_descriptions.csv')
   print(end_time - start_time)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
