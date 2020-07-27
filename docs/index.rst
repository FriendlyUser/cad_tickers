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
   :maxdepth: 4
   :caption: Contents:

.. automodule:: cad_tickers.exchanges.cse
   :members:
   :undoc-members:

.. automodule:: cad_tickers.exchanges.tsx
   :members:
   :undoc-members:


Examples
---------------

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
