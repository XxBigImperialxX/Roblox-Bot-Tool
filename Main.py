#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from time import sleep as snooze

#Info
uname = "JorgeCrawford38"
pword = uname[::-1]
sex = "Male" #Female
bdaymonth = "Aug"
bdayday = "7"
bdayyear = "2002"

#Config
amountOfTries = 5  #The amount of attempts to look for a successful account creation.
waitTime = 2  #The amount of time in seconds till it checks again for successful account creation.
successUrl = "roblox.com/games"  #The url that is redirected to after a successful account creation.

print('''
Username: {0}
Password: {1}
Gender: {2}
Birthdate: {3}/{4}/{5}'''.format(uname,pword,sex,bdaymonth,bdayday,bdayyear))

#executeableDriver = 'chromedriver.exe'
executeableDriver = r'phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe'

#chromeOptions = Options()
#chromeOptions.add_argument("--headless")

#browser = webdriver.Chrome(executeableDriver)
browser = webdriver.PhantomJS(executeableDriver)
browser.get('https://www.roblox.com')


#Ids and classes
username = browser.find_element_by_id("signup-username")
password = browser.find_element_by_id("signup-password")
password2 = browser.find_element_by_id("signup-password-confirm")
#termsofService = browser.find_element_by_xpath("//*[@id="agreeTermsPrivacyLabel"]").click() #//*[@id="agreeTermsPrivacyLabel"]
gender = browser.find_element_by_id(sex+"Button")
month = browser.find_element_by_id("MonthDropdown")
day = browser.find_element_by_id("DayDropdown")
year = browser.find_element_by_id("YearDropdown")

#BDAY:
select = Select(month)
select.select_by_value(bdaymonth)
select = Select(day)
select.select_by_value(bdayday)
select = Select(year)
select.select_by_value(bdayyear)

username.send_keys(uname);
password.send_keys(pword);
password2.send_keys(pword);
gender.click()
browser.find_element_by_xpath('//*[@id="agreeTermsPrivacyLabel"]').click() #//*[@id="agreeTermsPrivacyLabel"]
browser.find_element_by_xpath('//*[@id="signup-button"]').click()

CurrURL = browser.current_url
print(CurrURL)
tries = 0
while not successUrl in CurrURL:
    if(tries < amountOfTries):
        CurrURL = browser.current_url
        print("Trying again, Tries: {0}/{1}; URL: {2}".format(tries, amountOfTries, CurrURL))
        snooze(waitTime)
        tries += 1
    else: break;
browser.save_screenshot('screen.png')
if(successUrl in CurrURL):
    #Created account successfully.
    print("Account was created.")
else:
    #Failed in creating account.
    print("Account could not be created. Landing page: {}".format(CurrURL))
browser.save_screenshot('screenEnd.png')

#browser.quit()