import requests
import re
import os
import pandas as pd

# initialize list of lists
data = []


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


kill_range = 0
for x in range(1, 5000):
    url = f"http://www.tsx.com/resource/en/{x}"
    r = requests.get(url, allow_redirects=True)
    filename = getFilename_fromCd(r.headers.get("content-disposition"))
    if kill_range > 30:
        print(kill_range, x)
        print("probably no more files")
        exit(1)
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
        print(x, tsx_filename, file_extension)
        data.append([x, tsx_filename, file_extension, url])
        if any(substring in tsx_filename for substring in remove_list):
            continue
        if file_extension in [".xls", ".xlsx", ".pdf"]:
            new_path = os.path.join("tsx_files", new_filename)
            open(new_path, "wb").write(r.content)
    else:
        kill_range = kill_range + 1

# Create the pandas DataFrame
# path is ttp://www.tsx.com/resource/en/{x}
df = pd.DataFrame(data, columns=["FileId", "filename", "extension", "url"])
df.to_csv("updated_tsx.csv")
