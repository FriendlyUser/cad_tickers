import requests
import re
import os


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall("filename=(.+)", cd)
    if len(fname) == 0:
        return None
    return fname[0]


list_of_stocks_files = [101, 102, 106, 110, 114, 118, 122, 129, 570, 713]


def downloads_tsx_files():
    for x in list_of_stocks_files:
        url = f"http://www.tsx.com/resource/en/{x}"
        r = requests.get(url, allow_redirects=True)
        filename = getFilename_fromCd(r.headers.get("content-disposition"))

        if filename != None:
            kill_range = 0
            new_filename = filename.replace('"', "")
            tsx_filename, file_extension = os.path.splitext(new_filename)
            remove_list = [
                "policy",
                "Policy",
                "policies",
                "pdd-template",
                "paid-distribution",
                "notice",
                "2007" "2008",
                "2009",
                "2010",
                "2011",
                "2012",
                "2013",
                "2014",
                "accept",
                "rules-amendments",
            ]
            if any(substring in tsx_filename for substring in remove_list):
                continue
            if file_extension in [".xls", ".xlsx", ".pdf"]:
                # cad_tickers data_files
                new_path = os.path.join("cad_tickers", "data_files", new_filename)
                open(new_path, "wb").write(r.content)


if __name__ == "__main__":
    downloads_tsx_files()