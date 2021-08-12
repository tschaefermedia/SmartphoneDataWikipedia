import pandas as pd
import requests
import datetime


# base data
now = datetime.datetime.now()

base_url = "https://en.wikipedia.org/wiki/Comparison_of_smartphones"

data = pd.DataFrame(columns=["Model", "Brand", "SoC/Processor", "CPU Spec", "GPU", "Storage", "Removable storage", "RAM", "OS", "Custom Launcher", "Dimensions", "Weight", "Battery",
                    "Charging", "Display", "Rear Camera", "Front Camera", "Video", "Fingerprint Sensor", "Facial recognition", "Networks", "Type", "Form Factor", "Data Inputs", "Connectivity", "Release Date"])

response = requests.get(base_url)

content = response.text

content = content.replace("“", "\"")
content = content.replace("”", "\"")
content = content.replace("</li><li>", "</li>,<>")
content = content.replace("<p>", ",<p>")
content = content.replace("<br />", "<br />,")
content = content.replace("\xa0", " ")

# Extract all tables from the wikipage
dfs = pd.read_html(content)

for i in range(len(dfs)):
    year = now.year - (i - 1)
    if year > now.year:
        continue

    if year >= 2017:
        current_year_of_phones = dfs[i]
        current_year_of_phones.replace(u'\xa0', u' ', regex=True, inplace=True)
        for index, row in current_year_of_phones.iterrows():
            phone = dict()
            name = row["Model"]
            brand, model = name.split(" ", 1)
            phone["Model"] = model
            phone["Brand"] = brand
            try:
                phone["SoC/Processor"] = [c.strip()
                                          for c in row["SoC"].split(",")]
            except:
                phone["SoC/Processor"] = [c.strip()
                                          for c in row["CPU"].split(",")]
            print(phone)
        # The last row is just the date of the last update
        # df = df.iloc[:-1]

        # print(df)
