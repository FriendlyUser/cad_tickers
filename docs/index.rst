.. cad_tickers documentation master file, created by
   sphinx-quickstart on Sun Jul 26 08:33:39 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cad_tickers's documentation!
=======================================

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

.. code:: python
   from cad_tickers.exchanges.tsx import dl_tsx_xlsx, add_descriptions_to_df_pp
   from datetime import datetime
   start_time = datetime.now()
   df = dl_tsx_xlsx()
   # df = add_descriptions_to_df(df)
   df = add_descriptions_to_df_pp(df)
   # print(df)
   len(df)
   end_time = datetime.now()
   print(end_time - start_time)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
