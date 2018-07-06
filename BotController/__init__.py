#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from time import sleep as snooze
from Debug import Log as log
from os import path, makedirs
from os.path import join
import pickle

#Declaring and assigning globals
global uname, pword, sex, bdaymonth, bdayday, bdayyear, amountOfTries, waitTime, successUrl, proxyURL, proxyEnabled, outputFolder;
uname="";pword="";sex="";bdaymonth="";successUrl="";proxyURL="";bdayday="";bdayyear="";amountOfTries=0;waitTime=0;outputFolder="";
proxyEnabled = False;

#Info
def setupUser(username, password=None, gender="Male", bdayMonth="Aug", bdayDay="7", bdayYear="2002"):
    global uname, pword, sex, bdaymonth, bdayday, bdayyear;
    uname = username
    if(password == None):
        pword = username[::-1]
    else:
        pword = password
    sex = gender #Female
    bdaymonth = bdayMonth
    bdayday = bdayDay
    bdayyear = bdayYear

def configIni(**kwargs):
    global amountOfTries, waitTime, successUrl, proxyURL, proxyEnabled, outputFolder;
    amountOfTries = 18  #5The amount of attempts to look for a successful account creation.
    waitTime = 10  #2The amount of time in seconds till it checks again for successful account creation.
    successUrl = "roblox.com/games"  #The url that is redirected to after a successful account creation. #https://www.roblox.com/games?SortFilter=default&TimeFilter=0
    proxyURL = "140.227.81.53:3128"
    proxyEnabled = False
    outputFolder = "accounts"

def createUser():
    global uname, pword, sex, bdaymonth, bdayday, bdayyear, amountOfTries, waitTime, successUrl, proxyURL, proxyEnabled;
    executeableDriver = 'chromedriver.exe'
    #executeableDriver = 'phantomjs.exe'

    chromeOptions = Options()
    #chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--proxy-server="+proxyURL)

    '''
    if(proxyEnabled):
        service_args = [
        '--proxy={}'.format(proxyURL),
        '--proxy-type=socks5',
        ]
    else:
        service_args = []
        '''

    browser = webdriver.Chrome(executeableDriver, chrome_options=chromeOptions)
    #browser = webdriver.PhantomJS(executeableDriver)#,service_args=service_args
    browser.get('https://www.roblox.com')

    print("{0}:{1}:{2}:{3}/{4}-{5}".format(uname,pword,sex,bdaymonth,bdayday,bdayyear),end="", flush=True)

    #Assigns different ids from the homepage variable names.
    usernameId = browser.find_element_by_id("signup-username")
    passwordId = browser.find_element_by_id("signup-password")
    password2Id = browser.find_element_by_id("signup-password-confirm")
    gender = browser.find_element_by_id(sex+"Button")
    month = browser.find_element_by_id("MonthDropdown")
    day = browser.find_element_by_id("DayDropdown")
    year = browser.find_element_by_id("YearDropdown")

    #BDAY: Sets the birthdate.
    select = Select(month)
    select.select_by_value(bdaymonth)
    select = Select(day)
    select.select_by_value(bdayday)
    select = Select(year)
    select.select_by_value(bdayyear)

    #Uses the ids assigned before, clicks and types in boxes.
    usernameId.send_keys(uname);
    passwordId.send_keys(pword);
    password2Id.send_keys(pword);
    gender.click()
    browser.find_element_by_xpath('//*[@id="agreeTermsPrivacyLabel"]').click()
    browser.find_element_by_xpath('//*[@id="signup-button"]').click()

    #Checks weather the registration was successful.
    CurrURL = browser.current_url
    log(CurrURL)
    tries = 0
    while not successUrl in CurrURL:
        if(tries < amountOfTries):
            CurrURL = browser.current_url
            log("Trying again, Tries: {0}/{1}; URL: {2}".format(tries, amountOfTries, CurrURL))
            snooze(waitTime)
            tries += 1
        else: break;
    #browser.save_screenshot('screen.png')
    if(successUrl in CurrURL):
        #Created account successfully.
        print("...Account was created.")
        try:
            makedirs(join(outputFolder,"cookies"))
        except: pass
        if not(proxyEnabled):
            open(join(outputFolder,uname),'w').write("{0}:{1}".format(uname,pword))
        else:
            open(join(outputFolder,uname),'w').write("{0}:{1}.{2}".format(uname,pword,proxyURL))
        pickle.dump(browser.get_cookies(), open(join(outputFolder,"cookies",uname+".pkl"), "wb"))
    else:
        #Failed creating account.
        print("...Account could not be created. Landing page: {}".format(CurrURL))
    browser.save_screenshot('screenshot {}.png'.format(uname))
    browser.quit()

#setupUser("JorgeCrawford39")
configIni()
#createUser()


'''
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
    '''