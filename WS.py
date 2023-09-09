#!/usr/bin/python3.7
from bs4 import BeautifulSoup
from urllib.request import urlopen
import subprocess
import requests
import csv

url_list = ['https://chico.craigslist.org/search/sga?lang=ja', 'https://chico.craigslist.org/search/sga?s=120&lang=ja','https://chico.craigslist.org/search/sga?s=240&lang=ja']
query = input('Enter query parameter: ')
max_price = float(input('Enter max price: '))
total_products = 0

for url in url_list:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='sortable-results')

    product_elems = results.find_all('li', class_='result-row')

    with open('listings.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for product_elem in product_elems:
            title_elem = product_elem.find('a', class_='result-title hdrlnk')
            price_elem = product_elem.find('span', class_='result-price')
            location_elem = product_elem.find('span', class_='result-hood')

            if None in (title_elem, price_elem) or price_elem.text.strip() == '$0':
                continue

            title = title_elem.text.strip()
            price = float(price_elem.text.strip().replace('$', '').replace(',', ''))

            if location_elem is not None:
                location = location_elem.text.strip().replace('(', '').replace(')', '')
            else:
                location = ''

            if query.lower() in title.lower() and price <= max_price and location != '':
                writer.writerow([title, price, location])
                total_products += 1
                print(f'Title: {title}')
                print(f'Price: ${price:.2f}')
                print(f'Location: {location}\n')

print(f'Total products: {total_products}')

spath= "/home/lahazelton/sort.sh"

subprocess.call(['bash', spath])


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl


# Email details
sender_email = "*********"
receiver_email = "********"
password = "*******" 
subject = "Shell Lab"
body = "Email sent using Python."

# Create a message object
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Add body to the message
message.attach(MIMEText(body, "plain"))

# Attach file to the message
filename = "top5.csv"
attachment = open(filename, "rb")
part = MIMEBase("application", "octet-stream")
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", "attachment; filename= %s" % filename)
message.attach(part)

# Create a secure SSL context
context = ssl.create_default_context()

# Send the message
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent!")



