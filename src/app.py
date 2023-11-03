import pandas as pd
from bs4 import BeautifulSoup as bs

url_ = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

import requests
import time

html_data = requests.get(url_, time.sleep(10)).text


if "403 Forbidden" in html_data:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    request = requests.get(url_, headers = headers)
    time.sleep(10)
    html_data = request.text

soap = bs(html_data, "html.parser")

soap.find_all("table")

tables = soap.find_all("table")

for index, table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
        break
table_tesla_quarterly = tables[1]

tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({
            "Date": Date,
            "Revenue": Revenue
        }, index = [0])], ignore_index = True)

tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]

import sqlite3 as sq

con = sq.connect("tabla_tesla")

con.execute("""CREATE TABLE TESLA_REVENUE_SQ (Date, Revenue)""")

tesla_tuples = list(tesla_revenue.to_records(index = False))

con.executemany("INSERT INTO TESLA_REVENUE_SQ VALUES (?,?)", tesla_tuples)
con.commit()

import matplotlib.pyplot as plt
import seaborn as sns

fig, axis = plt.subplots(figsize = (10, 5))

tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].astype('int')
sns.lineplot(data = tesla_revenue, x = "Date", y = "Revenue")

plt.tight_layout()
plt.show()

fig, axis = plt.subplots(figsize = (10, 5))

tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
tesla_revenue_yearly = tesla_revenue.groupby(tesla_revenue["Date"].dt.year).sum().reset_index()

sns.barplot(data = tesla_revenue_yearly[tesla_revenue_yearly["Date"] < 2023], x = "Date", y = "Revenue")

plt.tight_layout()

plt.show()

fig, axis = plt.subplots(figsize = (10, 5))

tesla_revenue_monthly = tesla_revenue.groupby(tesla_revenue["Date"].dt.month).sum().reset_index()

sns.barplot(data = tesla_revenue_monthly, x = "Date", y = "Revenue")

plt.tight_layout()

plt.show()
