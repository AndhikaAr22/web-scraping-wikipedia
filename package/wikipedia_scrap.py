import requests
import pandas as pd
from bs4 import BeautifulSoup
import json


class Wikipedia:
    def __init__(self, url):
        self.url = url 

    def get_html_page(self):
        res = requests.get(self.url)
        if res.status_code != 200:
            print(f"Failed to retrieve data: {res.status_code}")
            return None
        # Extract data html dari Wikipedia
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.select_one("table.wikitable.sortable.sticky-header")
        if table is None:
            print("Failed to find the table in the HTML")
            return None
        rows = table.find_all('tr')
        print(rows)
        return rows

    def get_data(self):
        rows = self.get_html_page()
        if rows is None:
            return

        data = []
        for i in range(1, len(rows)):
            cols = rows[i].find_all('td')

            values = {
                'rank': i,
                'stadion': cols[0].get_text(strip=True),
                'capacity': cols[1].get_text(strip=True).split('[')[0].strip(),
                'region': cols[3].get_text(strip=True),
                'city': cols[4].get_text(strip=True),
                'image': 'https://' + cols[5].find('img').get('src').split("//")[1] if cols[5].find('img') else None,
                'home_team': cols[6].get_text(strip=True)
            }
            data.append(values)
        json_rows = json.dumps(data, indent=4)
        print(json_rows)
        return data