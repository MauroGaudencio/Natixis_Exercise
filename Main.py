import sys
import logging
import xml.etree.ElementTree as ET
from lackey import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains

#redirect console output into logfile
sys.stdout = open('logfile.txt', 'w')

#redirect logging messages to logfile
logging.basicConfig(
    filename='logfile.txt',
    format="%(asctime)s - %(levelname)s - %(message)s",
     style="%",
     datefmt="%Y-%m-%d %H:%M",
     level=logging.DEBUG,
)

def read_params():
    # Load and parse the XML file
    tree = ET.parse('param.xml')
    root = tree.getroot()

    browser = "None"

    #get browser value
    for child in root:
        if child.tag == "browser":
            browser = child.attrib['value']

    logging.debug("Browser value loaded from param.xml=%s", browser)
    return browser

def webdriver_startup(browser):
    #Options detach -> Maximizes the browser window
    options = Options()
    options.add_experimental_option("detach", True)

    #open the browser according to which one was specified
    if browser == "Edge":
        driver = webdriver.Edge()
        logging.debug("Webdriver value=Edge")
    elif browser == "Chrome":
        driver = webdriver.Chrome()
        logging.debug("Webdriver value=Chrome")
    else:
        logging.critical("No browser was recognized, browser value=%s", str(browser))
        sys.exit() #interrupt the script if browser is not recognized

    return driver

#This function scrolls the page until the specific screenshot is found within the page
#Useful for Step 3 since immediately scrolling all the way down means the "Find agency" button section
#will be skipped(atleast in my screen with resolution 1366x768, might not happen on bigger resolutions)
#so its best to scroll one page down at the time, since it will 100% cover the entire page until the element is found
def Scroll_to_webelement(driver, sshot_element):
    #get page Height
    pageHeight = driver.execute_script("return document.body.scrollHeight")

    Scr = Screen(0)
    while True:
        #if screenshot element was found then return True
        if Scr.exists(sshot_element):
            logging.debug("Screenshot element found for screenshot=%s", sshot_element)
            return True

        #check if end of page was reached
        new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
        if new_height >= pageHeight:
            logging.debug("End of page reached without element being found for screenshot=%s", sshot_element)
            break

        #scroll the page by doing a PageDown
        html = driver.find_element(By.XPATH,'//body')
        html.send_keys(Keys.PAGE_DOWN)

    #Page was fully scanned and element was never found
    return False

#function searches for a screenshot of a button in the current screen and presses it if it exists
def Press_Button(sshot_button, buttontoclick):
    Scr = Screen(0)
    if Scr.exists(sshot_button):
        Scr.click(buttontoclick)
    else:
        logging.debug("Button not found for button=%s", buttontoclick)

#open browser on specified url
def Step1_Access_URL(webdriver, url):
    webdriver.get(url)
    webdriver.maximize_window()

#scroll to find agency and presses it
def Step3_FindAgency(driver, sshot_element):
    if Scroll_to_webelement(driver, sshot_element):
        Scr = Screen(0)
        Scr.click(sshot_element)
    else:
        logging.debug("Button not found for button=%s", sshot_element)

#searches for the agency by checking all the fields and inserting correct values
def Step4_SearchAgency(driver):
    #insert Rue value
    Press_Button(sshot_folder + "Search_Agency.bmp", sshot_folder + "Rue_Button.bmp")
    ActionChains(driver) \
        .send_keys("Lyon") \
        .perform()

    #insert Code_Postal value
    Press_Button(sshot_folder + "Search_Agency.bmp", sshot_folder + "Code_postal_Button.bmp")
    ActionChains(driver) \
        .send_keys("69000") \
        .perform()

    #Press Rechercher
    Press_Button(sshot_folder + "Rechercher_Button.bmp", sshot_folder + "Rechercher_Button.bmp")

    #Choose LyonPerrache
    Press_Button(sshot_folder + "LyonPerrache.bmp", sshot_folder + "LyonPerrache.bmp")

def Step5_Press_4(driver):
    Scr = Screen(0)
    if Scr.exists(sshot_folder + "Lyon_2eme_Page.bmp"):
        Press_Button(sshot_folder + "Icon_4.bmp", sshot_folder + "Icon_4.bmp")
    else:
        logging.debug("Button not found for button=Icon_4.bmp")

sshot_folder = "Screenshots/"

#get browser to use from param.xml file
browser = read_params()
if(browser != "Edge" and browser != "Chrome"):
    logging.critical("Browser is not defined as 'Edge' or 'Chrome'. Browser value=%s, please check param.xml file.", str(browser))
    sys.exit()  # interrupt the script if browser is not recognized

#Start the browser
logging.debug("Opening browser")
driver = webdriver_startup(browser)

#Step 1
logging.debug("Starting Step1")
Step1_Access_URL(driver, "https://www.banquepopulaire.fr/")

#Step 2
logging.debug("Starting Step2")
Press_Button(sshot_folder + "Cookies_fr.bmp", sshot_folder + "AcceptAllButton_fr.bmp")

#Step 3
logging.debug("Starting Step3")
Step3_FindAgency(driver, sshot_folder + "Find_Agency.bmp")

#Step 4
logging.debug("Starting Step4")
Step4_SearchAgency(driver)

#Step 5
logging.debug("Starting Step5")
Step5_Press_4(driver)

time.sleep(2)

#close browser
logging.debug("Closing browser")
driver.quit()

sys.stdout.close()