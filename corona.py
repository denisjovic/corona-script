from bs4 import BeautifulSoup
import requests
from datetime import datetime
import smtplib
import sqlite3

url = 'https://epidemic-stats.com/coronavirus/serbia'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# getting data from the website
infected_live = soup.find('h5', class_='card-title')
today = datetime.today().strftime('%Y-%m-%d')

message = f'{today} - {infected_live.text} infected in Serbia \nLink to source: {url}'

EMAIL = 'youremail@mail.com'
PASS = 'your_password_here'
TARGET = 'target_email'

# email sending
conn = smtplib.SMTP('smtp.gmail.com', 587) 
conn.ehlo() 
conn.starttls()
print(conn.login(EMAIL, PASS))
conn.sendmail(EMAIL, TARGET, f'Subject: Corona stats for {today} \n\n{message}')
print('Success')
conn.quit()

# sqlite database creation
def create_table():
    con = sqlite3.connect('table.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS results (date TEXT, numbre INT)")
    con.commit()
    con.commit()

# inserting data into database
def insert(date, number):
    con = sqlite3.connect('table.db')
    cur = con.cursor()
    cur.execute("INSERT INTO results VALUES(?,?)", (date, number))
    con.commit()
    con.commit()

def view():
    con = sqlite3.connect('table.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM results")
    rows = cur.fetchall()
    con.close()
    return rows

def delete(item):
    con = sqlite3.connect('table.db')
    cur = con.cursor()
    cur.execute("DELETE FROM results WHERE date=?", (item,))
    con.commit()
    con.close()


create_table()
insert(today, infected_live.text)











