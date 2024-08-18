import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from pandas.plotting import table

# Initialization of known entities
url = "https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films"
db_name = "Movies.db"
table_name = "Top_50"
csv_path = 'C:/Users/Lenovo/PycharmProjects/Python/WebScraping_Project/top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank", "Film", "Year", "Rotten Tomatoes Top 100", "IMDb Top 100"])
count = 0

# Loading the webpage for Webscraping
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

# extract the appropriate information from the web page
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

# Iterate over the rows to find meaningful data
for row in rows:
    if count<50:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Average Rank": col[0].contents[0],
                         "Film": col[1].contents[0],
                         "Year": col[2].contents[0],
                         "Rotten Tomatoes Top 100": col[3].contents[0],
                         "IMDb Top 100": col[4].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            count+=1
    else:
        break

# Show data frame
print(df)

df.to_csv(csv_path)

# store data in a database
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()