import requests
from bs4 import BeautifulSoup
from lxml import etree
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

URL = 'https://www.x-rates.com/calculator/?from=HUF&to=GBP&amount=1'

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', \
            'Accept-Language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7'})

webpage = requests.get(URL, headers=HEADERS)

soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup))

GBP = (dom.xpath('//*[@id="content"]/div[1]/div/div[1]/div/div/span[2]/text()'))
for i in GBP:
    GBP_currency = float(i)
    HUF_GBP = round(1 / GBP_currency, 2)


MY_EMAIL = os.getenv("MY_SECRET_EMAIL")
MY_PASSWORD = os.getenv("MY_SECRET_EMAIL_PASSWORD")

def GBP_send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="norbert.nagy.1994@gmail.com",
                msg=f"Subject:GBP central rate alert!\n\nGBP's central rate just droped below 435HUF, as it is {HUF_GBP}HUF now.\nLet's buy some!")

if HUF_GBP <= 435:
    GBP_send_email()
else:
    print(f"The value of GBP is: {HUF_GBP} HUF.")