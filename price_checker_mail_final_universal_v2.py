import re
import time
import os

# os.system("sudo apt-get install -qq python3-pip < /dev/null > /dev/null")
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3\nRun using python3 instead of python")

try:
    import requests
except ImportError:
    os.system("pip3 install requests")
    print("Installing Dependencies...\n")
    time.sleep(3)
    import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    os.system("sudo apt-get install python3-bs4")
    time.sleep(3)
    from bs4 import BeautifulSoup
try:
    from mailjet_rest import Client
except ImportError:
    os.system("pip3 install mailjet_rest")
    time.sleep(3)
    from mailjet_rest import Client

timer = 60 * 60


def smtp_send_email(email, nameam, priceam, namefl, pricefl, URL, j):
    api_key = '9c357ca9d2e695d571117648c47680c8'
    api_secret = '3b51faf454e90309d8b9ec695b25a8c1'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    expectedprice = expected_prompt()
    URL2 = "https://www.amazon.in/s?k=" + nameam.replace(' ', '+').replace('(', '%28').replace(')', '%29').replace(',',
                                                                                                                   '%2C')

    if j == 1:
        URL2 = "https://www.amazon.in/s?k=" + nameam.replace(' ', '+').replace('(', '%28').replace(')', '%29').replace(
            ',', '%2C')
        data = {
            'Messages': [
                {
                    'From': {
                        'Email': 'dr_pricetracker@mailinator.com',
                        'Name': 'Price Tracker'
                    },

                    'To': [
                        {
                            'Email': email
                        }
                    ],

                    'Subject': 'Price Drop Alert for ' + nameam + ' on Amazon',
                    'TextPart': 'Dear User, the price of ' + nameam + ' has dropped below Rs.' + str(
                        expectedprice) + '.\nCheck it out: ' + URL2
                }
            ]
        }

    if j == 2:
        data = {
            'Messages': [
                {
                    'From': {
                        'Email': 'dr_pricetracker@mailinator.com',
                        'Name': 'Price Tracker'
                    },

                    'To': [
                        {
                            'Email': email
                        }
                    ],

                    'Subject': 'Price Drop Alert for ' + namefl + ' on Flipkart',
                    'TextPart': 'Dear User, the price of ' + namefl + ' has dropped below Rs.' + str(
                        expectedprice) + '.\nCheck it out: ' + URL
                }
            ]
        }

    while True:
        if j == 1:
            if priceam < expectedprice:
                result = mailjet.send.create(data=data)
                print("Email sent successfully!\nExitting!\n")
                exit(0)
            else:
                print(
                    "\nThe price right now is above your target price\nThis program will check every hour for price drop\nKeep this program running to get notified!")
                time.sleep(timer)
                (priceam, namefl) = price_amazon_search(URL2, headers)
                continue

        if j == 2:
            if pricefl < expectedprice:
                result = mailjet.send.create(data=data)
                print("Email sent successfully!\nExitting!\n")
                exit(0)
            else:
                print(
                    "\nThe price right now is above your target price\nThis program will check every hour for price drop\nKeep this program running to get notified!")
                time.sleep(timer)
                (pricefl, namefl) = price_flipkart_search(namefl, headers)
                continue

        if j == 3:
            # if pricefl<expectedprice:
            if priceam < expectedprice:
                URL2 = "https://www.amazon.in/s?k=" + nameam.replace(' ', '+').replace('(', '%28').replace(')',
                                                                                                           '%29').replace(
                    ',', '%2C')
                data = {
                    'Messages': [
                        {
                            'From': {
                                'Email': 'dr_pricetracker@mailinator.com',
                                'Name': 'Price Tracker'
                            },

                            'To': [
                                {
                                    'Email': email
                                }
                            ],

                            'Subject': 'Price Drop Alert for ' + namefl + ' on Amazon',
                            'TextPart': 'Dear User, the price of ' + namefl + ' has dropped below Rs.' + str(
                                expectedprice) + '.\nCheck it out: ' + URL2
                        }
                    ]
                }
            if pricefl < expectedprice:
                data = {
                    'Messages': [
                        {
                            'From': {
                                'Email': 'dr_pricetracker@mailinator.com',
                                'Name': 'Price Tracker'
                            },

                            'To': [
                                {
                                    'Email': email
                                }
                            ],

                            'Subject': 'Price Drop Alert for ' + namefl + ' on Flipkart',
                            'TextPart': 'Dear User, the price of ' + namefl + ' has dropped below Rs.' + str(
                                expectedprice) + '.\nCheck it out: ' + URL
                        }
                    ]
                }

            if priceam < expectedprice and pricefl < expectedprice:
                URL2 = "https://www.amazon.in/s?k=" + nameam.replace(' ', '+').replace('(', '%28').replace(')',
                                                                                                           '%29').replace(
                    ',', '%2C')
                data = {
                    'Messages': [
                        {
                            'From': {
                                'Email': 'dr_pricetracker@mailinator.com',
                                'Name': 'Price Tracker'
                            },

                            'To': [
                                {
                                    'Email': email
                                }
                            ],

                            'Subject': 'Price Drop Alert for ' + nameam + ' on Amazon and Flipkart',
                            'TextPart': 'Dear User, the price of ' + nameam + ' has dropped below Rs.' + str(
                                expectedprice) + '.\nCheck it out on\nAmazon: ' + URL2 + '\nFlipkart: ' + URL
                        }
                    ]
                }

            if (j == 1 and priceam > expectedprice) or (j == 2 and pricefl > expectedprice) or (
                    j == 3 and pricefl > expectedprice and priceam > expectedprice):
                print(
                    "\nThe price right now is above your target price\nThis program will check every hour for price drop\nKeep this program running to get notified!")
                time.sleep(timer)
                (priceam, nameam) = price_amazon_search(URL2, headers)
                (pricefl, namefl) = price_flipkart_search(URL, headers)
                continue

            result = str(mailjet.send.create(data=data))
            if result == '<Response [200]>':
                print("Email sent successfully!\nExitting!\n")
                exit(0)
            else:
                print("There was some trouble sending the email\n")
                print("Error Code: " + str(result) + '\n')


def expected_prompt():
    while (1):
        expectedpricein = input("\nEnter the price below which you want to get notified:\nRs.")

        try:
            expectedprice = int(expectedpricein)
            return expectedprice
        except ValueError:
            print("Please enter a valid number!")


def track_prompt(email, nameam, priceam, namefl, pricefl, URL):
    j = 9
    while True:
        j = int(input(
            "\nChoose an option:\n1. Track on Amazon\n2. Track on Flipkart\n3. Track on both\n0. Go back to previous menu\n9. Exit\n"))
        if j == 0:
            return j, email
        if j == 9:
            exit(0)
        if j == 1 or j == 2 or j == 3:
            if email == '':
                email = str(input("Enter your Email ID: "))
            smtp_send_email(email, nameam, priceam, namefl, pricefl, URL, j)
        else:
            print("Invalid option!\nTry Again\n")


def price_amazon(URL, headers):
    try:
        page = requests.get(URL.strip(), headers=headers)
    except:
        print("Error Reaching Amazon\nIf your internet is working fine, try changing User Agent by entering 404 in the main menu\n")
        exit(0)

    soup2 = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(soup2.prettify(), 'html.parser')

    try:
        title = soup.find(id='productTitle').get_text()
        price = soup.find(id='priceblock_ourprice').get_text()
    except:
        print("There was an error fetching from the URL\nPlease check the URL and your Internet Connection")
        exit(404)
    #converted_price = float(price.replace(',', '').replace('Rs.', '').strip())

    dashind = price.find('-')
    if dashind == -1:
        converted_price = float(''.join(re.findall('\d+', price)))
    else:
        converted_price = float(''.join(re.findall('\d+', price[0:dashind])))

    if price.find('.') != -1:
        converted_price = converted_price/100

    return converted_price, title.strip()


def price_flipkart(URL, headers):
    try:
        page = requests.get(URL.strip(), headers=headers)
    except:
        print("Error Reaching Flipkart\nIf your internet is working fine, try changing User Agent by entering 404 in the main menu\n")
        exit(1)

    soup2 = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(soup2.prettify(), 'html.parser')
    try:
        mydivs2 = soup.find("div", {"class": "_1vC4OE" and "_3qQ9m1"}).encode('utf-8')
    except:
        print("There was an error fetching from the URL\nPlease check the URL and your Internet Connection\nExitting...")
        exit(1)

    if mydivs2 == 'None':
        mydivs = soup.find("div", {"class": "_1vC4OE"}).get_text().encode('utf-8')
    else:
        mydivs = soup.find("div", {"class": "_1vC4OE" and "_3qQ9m1"}).get_text().encode('utf-8')

    price = mydivs[3:]
    converted_price = float(price.replace(',', '').replace('Rs.', '').strip())
    title2 = str(soup.find("span", {'class': '_35KyD6'}))

    if title2 == 'None':
        title = str(soup.find("a", {'class': '_2cLu-l'})['title'])
    else:
        title = str(soup.find("span", {'class': '_35KyD6'}).get_text())

    return converted_price, title.strip()


# Search by product:
def price_flipkart_search(URL, headers):
    try:
        page = requests.get(URL.strip(), headers=headers)
    except:
        print("Error reaching FLipkart\nIf your internet is working fine, try changing User Agent by entering 404 in the main menu\n")
        exit(0)

    soup2 = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(soup2.prettify(), 'html.parser')

    try:
        mydivs2 = soup.find("div", {"class": "_1vC4OE"}).encode('utf-8')
        if mydivs2 == 'None':
            mydivs = soup.find("div", {"class": "_1vC4OE" and "_2rQ-NK"}).get_text().strip().encode('utf-8')
        else:
            mydivs = str(soup.find("div", {"class": "_1vC4OE"}).get_text().strip())
    except:
        print("Invalid Query")
        exit(0)
    #print(mydivs)
    price = mydivs[1:]
    converted_price = float(price.replace(',', '').strip())
    __title2 = soup.find('div', {"class": "_3wU53n"})
    if str(__title2) != 'None':
        __title = str(__title2.get_text().strip())
    else:
        __title2 = soup.find('a', {"class": "_2cLu-l"})
        if str(__title2) != 'None':
            __title = str(__title2['title'].strip())
        else:
            __title2 = soup.find('div', {"class": "_2B_pmu"})
            __title3 = soup.find('a', {"class": "_2mylT6"})
            if str(__title2) != 'None' and str(__title3)!='None':
                __title = str(__title2.get_text().strip()) +" "+ str(__title3['title'].strip())
            else:
                print("There was an error fetching the name on Flipkart")
                __title = "Error!!!"
    return converted_price, __title


def price_amazon_search(URL, headers):
    try:
        page = requests.get(URL.strip(), headers=headers)
    except:
        print("Error Reaching Amazon\nIf your internet is working fine, try changing User Agent by entering 404 in the main menu\n")
        exit(0)

    soup2 = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(soup2.prettify(), 'html.parser')

    allprice = soup.select("a.a-size-base.a-link-normal.s-no-hover.a-text-normal")
    allprice2 = soup.find_all("span", {"class": "a-price-whole"})
    alltitle = soup.find_all("a", {"class": "a-link-normal" and "a-text-normal"})
    price = str('')
    __title = str('')

    try:
        i = 0
        for element in allprice:
            ind = str(element).find('href')
            if str(element)[ind+6:ind+17] == '/gp/slredir':
                i=i+1
                continue
            else:
                price = element.select_one('span.a-price-whole').get_text()
                break
        titleelement = None
        for element in alltitle:
            if element['href'][0:11] == '/gp/slredir':
                continue
            else:
                titleelement = element
                break
    except:
        print("Invalid Query")
        exit(0)

    __title = str(titleelement.find("span", {"class": "a-size-base-plus" and "a-color-base" and "a-text-normal"}).get_text().strip())
    converted_price = float(''.join(re.findall('\d+', price)))
    return converted_price, __title


email = ''
expectedprice = int(0)
headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

while True:
    i2 = input("Choose an option:\n1. Search by URL\n2. Search by product name\n9. Exit\n")
    try:
        i = int(i2)
    except ValueError:
        print("Please enter a valid number\n")
        continue
    if i == 1:
        URL = str(input("Enter URL of product:"))

        # headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

        if URL.find("amazon.in") < len(URL) and URL.find("amazon.in") > 0:
            (priceam, nameam) = price_amazon(URL, headers)
            print('\n')
            print("Amazon:\n" + nameam + ': Rs.' + str(int(priceam)))

            flipurl = "https://www.flipkart.com/search?q=" + nameam.replace(' ', '%20').replace('(', '%20').replace(')',
                                                                                                                    '%20')
            (pricefl, namefl) = price_flipkart_search(flipurl, headers)

            print("Flipkart:\n" + namefl + ': Rs.' + str(int(pricefl)) + '\n')

            if pricefl < priceam:
                print("Cheaper on Flipkart by Rs." + str(priceam - pricefl) + '\n')
            if priceam < pricefl:
                print("Cheaper on Amazon by Rs." + str(pricefl - priceam) + '\n')
            if priceam == pricefl:
                print("Same price on Amazon and Flipkart.\n")

            track_prompt(email, nameam, priceam, namefl, pricefl, URL)

        else:
            if URL.find("flipkart.com") < len(URL) and URL.find("flipkart.com") > 0:
                (pricefl, namefl) = price_flipkart(URL, headers)
                print("\nFlipkart:\n" + namefl + ': Rs.' + str(int(pricefl)) + '\n')

                amazurl = "https://www.amazon.in/s?k=" + namefl.replace(' ', '+').replace('(', '%28').replace(')',
                                                                                                              '%29').replace(
                    ',', '%2C')
                (priceam, nameam) = price_amazon_search(amazurl, headers)
                print("Amazon:\n" + nameam + ': Rs.' + str(int(priceam)) + '\n')

                if pricefl < priceam:
                    print("Cheaper on Flipkart by Rs." + str(priceam - pricefl) + '\n')
                if priceam < pricefl:
                    print("Cheaper on Amazon by Rs." + str(pricefl - priceam) + '\n')
                if priceam == pricefl:
                    print("Same price on Amazon and Flipkart.\n")

                track_prompt(email, nameam, priceam, namefl, pricefl, URL)

            else:
                print("Invalid URL")
                continue

    if i == 2:
        title = str(input("Enter name of product: "))
        title2 = title
        URL = "https://www.flipkart.com/search?q=" + title.replace(' ', '%20')
        # headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

        (price, namefl) = price_flipkart_search(URL, headers)

        URL2 = "https://www.amazon.in/s?k=" + title2.replace(' ', '+')
        # print(URL2)
        (price2, nameam) = price_amazon_search(URL2, headers)

        print('\n')
        print("Flipkart:")
        print(namefl + ': Rs.' + str(int(price)))
        print("Amazon:")
        print(nameam + ': Rs.' + str(int(price2)) + '\n')

        if price < price2:
            print("Cheaper on Flipkart by Rs." + str(price2 - price) + '\n')
        if price2 < price:
            print("Cheaper on Amazon by Rs." + str(price - price2) + '\n')
        if price == price2:
            print("Same price on Amazon and Flipkart.\n")

        track_prompt(email, nameam, price2, namefl, price, URL)

    if i == 4:
        # test
        print("Sending Email")
        smtp_send_email()

    if i == 9:
        print("\nThank You for using this tool\nHave a nice day\n")
        exit(0)

    if i == 404:
        print(
            "\nYou've chosen the option to change your user agent (beta)\nTo change your user agent, simply Google 'What's my user agent' and paste the result here: ")
        agentcustom = str(input())
        headers = {"User-Agent": agentcustom}
        print("User Agent Changed!")

    if i != 1 and i != 2 and i != 404 and i != 9:
        print("Please Choose a valid option")
