# Import the Dependencies required for code to work
# pip3 install bs4 requests pywhatkit pynput
from bs4 import BeautifulSoup as bs
import requests
import time
import pywhatkit
from pynput.keyboard import Key, Controller
from datetime import datetime

"""
Enter the Web scraping URL here. This will be used to go to the site where the web scraping will take place.

1. 3080: https://rptechindia.in/nvidia-geforce-rtx-3080.html
2. 3070: https://rptechindia.in/nvidia-geforce-rtx-3070.html
3. 3060TI: https://rptechindia.in/nvidia-geforce-rtx-3060-ti.html
"""
URList = ["https://rptechindia.in/nvidia-geforce-rtx-3070.html", "https://rptechindia.in/nvidia-geforce-rtx-3080.html",
"https://rptechindia.in/nvidia-geforce-rtx-3060-ti.html", "https://rptechindia.in/nvidia-geforce-rtx-3090.html"]

NumberList = []

# Set your User Agent (Google My User Agent to find out what your user agent is)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}

keyboard = Controller()

def check_price(URL):
    # Scrape the web page
    # Call the page at the URL using the Headers declared above.
    page = requests.get(URL, headers=headers)
    # print(page)

    # Get the page contents inside the soup
    # Parse the fetched page using BeautifulSoup and display the contents using prettify. It should display the entire HTML code of the webpage.
    soup = bs(page.content,'html.parser')
    # print(soup.prettify())

    # Find in Soup to get relevant fields
    # Out of the output HTML, we need to find for out items. We will be finding the title, price and whether the description says "Out of stock" or not.
    title = soup.find_all("h1" , {"class" : "product-title"})[0].text.strip()
    # print(title)

    span_text = soup.find_all("span", {"class" : "rs2"})[0].text
    # print(span_text)

    price = soup.find_all("span", {"class" : "price"})[0].text
    converted_price = price.replace(',','')[1:6]
    sell_price = int(converted_price)
    # print(price + " > " + converted_price + " > " + str(sell_price))

    # Actual Logic for Code
    """
    Now we need to check if the span_text no longer says "Out of stock" and if the prices are below the correct threshold depending on the GPU.
    Threshholds:
    NVIDIA GEFORCE RTX 3080 : 65,000
    NVIDIA GEFORCE RTX 3070 : 45,000
    NVIDIA GEFORCE RTX 3060TI : 38,000
    NVIDIA GEFORCE RTX 3090: 1,40,000
    """
    if len(span_text) != 0 and sell_price != 0:
        if 'Out of stock' not in span_text:
            if title == 'NVIDIA GEFORCE RTX 3080' and sell_price < 65000:
                print("Buy")
                send_whatsapp(URL, NumberList[0])
                send_whatsapp(URL, NumberList[2])
                send_group_message(URL)
            elif title == 'NVIDIA GEFORCE RTX 3070' and sell_price < 45000:
                print("Buy")
                send_whatsapp(URL, NumberList[0])
                send_whatsapp(URL, NumberList[1])
                send_group_message(URL)
            elif title == "NVIDIA GEFORCE RTX 3060 Ti" and sell_price < 38000:
                print("Buy")
                send_whatsapp(URL, NumberList[0])
                send_whatsapp(URL, NumberList[1])
                send_group_message(URL)
            elif title == "NVIDIA GEFORCE RTX 3090" and sell_price < 140000:
                print("Buy")
                send_whatsapp(URL, NumberList[2])
                send_whatsapp(URL, NumberList[0])
                send_group_message(URL)
            else:
                print('Scalpers alert')
        else:
            if title == "NVIDIA GEFORCE RTX 3060 Ti":
                print('3060Ti is out of stock')
            elif title == 'NVIDIA GEFORCE RTX 3090':
                print('3090 is out of stock')
            elif title == 'NVIDIA GEFORCE RTX 3080':
                print('3080 is out of stock')
            elif title == 'NVIDIA GEFORCE RTX 3070':
                print('3070 is out of stock')
            else:
                patience()
    soup.decompose()

def send_whatsapp(link, number):
    msg = "GPU is available for purchase at: " + str(link)
    now = datetime.now()
    current_hour = int(now.strftime("%H"))
    current_min = now.strftime("%M")
    send_min = int(current_min) + 1
    pywhatkit.sendwhatmsg(number, msg, current_hour, send_min, 10)
    time.sleep(7)
    keyboard.press(Key.ctrl_l)
    keyboard.tap('w')
    keyboard.release(Key.ctrl_l)
    keyboard.tap(Key.enter)

def send_group_message(link):
    msg = "GPU is available for purchase at: " + str(link)
    now = datetime.now()
    current_hour = int(now.strftime("%H"))
    current_min = int(now.strftime("%M")) + 1
    pw.sendwhatmsg_to_group(NumberList[3], msg, current_hour, current_min, 10)
    time.sleep(7)
    keyboard.press(Key.ctrl_l)
    keyboard.tap('w')
    keyboard.release(Key.ctrl_l)
    keyboard.tap(Key.enter)

def patience():
    print('Patience my young padawan')

if __name__ == '__main__':
    for line in open('numbers.txt', 'r').readlines(  ):
        NumberList.append(line[:14])
    print(NumberList)
    try:
        while(True):
            now = datetime.now()
            curhour = int(now.strftime("%H"))
            curmin = int(now.strftime("%M"))
            if(curhour < 22 and curhour > 7):
                print(f"Execution Time: {curhour}:{curmin}")
                for URL in URList:
                    check_price(URL)
                #check again in 60 mins
                time.sleep((60*60)-5)
    except Exception as err:
        print(f"Thanks for using app./n Exit Code: {err}")
