import requests
import pandas as pd
from datetime import datetime


def get_halts_resumption() -> pd.DataFrame:
    """Gets the latest 25 halts from the iiroc

    Returns:
      halt_df
        Dataframe with bad data removed

        ==========  ====================================================================
        Halts       Details of halts
        Listing     Extracted ticker from halt
        ==========  ====================================================================
    """
    now = datetime.now()
    year = now.year
    # get year
    iiroc_url = f"https://iiroc.mediaroom.com/index.php?year={year}"
    r = requests.get(iiroc_url)
    html_data = r.text
    halts_df = pd.read_html(html_data, attrs={"class": "spintable"})
    halt_df = halts_df[0]
    halt_df.columns = ["Halts"]
    halt_df["Listing"] = halt_df["Halts"].str.split().str[-1]
    halt_df = halt_df.drop(halt_df.tail(1).index)
    return halt_df
    # extract last word as
    # #wd_printable_content > div.wd_newsfeed_releases > div > table


if __name__ == "__main__":
    get_halts_resumption()
