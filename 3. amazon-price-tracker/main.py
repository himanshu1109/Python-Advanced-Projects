import requests
import smtplib
from bs4 import BeautifulSoup

EMAIL = "MAIL"
PASSWORD = "PWD"
SMTP_ADDRESS = "smtp.gmail.com"
BUY_PRICE = 900

url = "https://www.amazon.com/R5-3550H-Processor-Graphics-FX505DT-AH51-Keyboard/dp/B07VBK4SYS/ref=sr_1_1?qid=1627482143"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.114 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")

title = soup.find(id="productTitle").get_text().strip()

price = soup.find(id="priceblock_ourprice").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs="RECEIVER_MAIL",
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
        )
