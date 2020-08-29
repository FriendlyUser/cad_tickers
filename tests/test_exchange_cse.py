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


def get_description_for_ip():
    description = get_description_for_url(
        "https://thecse.com/en/listings/diversified-industries/imaginear-inc"
    )
    description_2020 = "ImagineAR Inc.  is an augmented reality (AR) platform that enables businesses of any size to create and implement their own AR campaigns with no programming or technology experience. Every organization, from professional sports franchises to small retailers, can develop interactive AR campaigns that blend the real and digital worlds using ImagineARTM. Customers simply point their mobile device at logos, signs, buildings, products, landmarks and more to instantly engage videos, information, advertisements, coupons, 3D holograms and any interactive content all hosted in the cloud and managed using a menu-driven portal. Integrated real-time analytics means that all customer interaction is tracked and measured in real-time. The ImagineARTM Enterprise platform supports both IOS and Android mobile devices and upcoming wearable technologies."
