from cad_tickers.exchanges.cse import (
    get_cse_files,
    get_cse_tickers_df,
    get_description_for_url,
)
from cad_tickers.util import make_cse_path
import os


def test_dl_cse():
    path = get_cse_files("cse.xlsx")
    assert path == "cse.xlsx"
    assert os.path.exists(path)


def test_dl_all():
    path = get_cse_files("cse.pdf", "pdf")
    assert path == "cse.pdf"
    assert os.path.exists(path)


def test_cse_listing_url():
    cse_path = make_cse_path("1933 Industries Inc.", "Diversified Industries")
    assert (
        cse_path
        == "https://thecse.com/en/listings/diversified-industries/1933-industries-inc"
    )


def test_clean_cse_csv():
    df = get_cse_tickers_df()
    num_rows = df.isnull().T.any().T.sum()
    assert num_rows > 2


def test_dl_cse_none():
    path = get_cse_files("cse.pdf", "html")
    assert path == None


def test_get_description_for_ip():
    description = get_description_for_url(
        "https://thecse.com/en/listings/diversified-industries/imaginear-inc"
    )
    ref_description_2020 = "<strong>ImagineAR Inc.</strong>"
    assert description == ref_description_2020
