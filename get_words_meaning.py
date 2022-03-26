import re
from xml.dom.minidom import Element
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from typing import Final

baseUrl: Final = r"https://gufo.me/dict/efremova"
chromeDriverPath: Final = r"C:/Users/User/Documents/chromedriver.exe"
wordsFileName: Final = "word"
failsFileName: Final = "meaning_fails"
meaningFileName: Final = "meaning"
programFileFormat: Final = "txt"

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--ignore-certificate-errors-spki-list")
driver = webdriver.Chrome(options=options, executable_path=chromeDriverPath)

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    run_on_insecure_origins=False,
)


def getMeaningBloc(driver):
    block = driver.find_element(By.TAG_NAME, "article")
    return block.find_elements(By.TAG_NAME, "p")


def convertToText(elem):
    return elem.text


def getOneDescriptonFromList(rawList):
    del rawList[0]
    listWithDescriptions = list(map(convertToText, rawList))
    romanNumeral = False
    arabicNumeral = False
    for item in listWithDescriptions:
        if romanNumeral:
            if "1." in item:
                return item[3:]
            else:
                return item
        if "I " in item:
            romanNumeral = True
        if not romanNumeral and "1." in item:
            arabicNumeral = True
            return item[3:]
        if not romanNumeral and not arabicNumeral:
            return item


fileWithFails = open(f"{failsFileName}.{programFileFormat}", "w")
fileWithMeaningWords = open(f"{meaningFileName}.{programFileFormat}", "w")
counter = 0
with open(f"{wordsFileName}.{programFileFormat}", "r") as fileWithWords:
    for word in fileWithWords:
        counter += 1
        url = f"{baseUrl}/{word.lower()}"
        driver.get(url)
        try:
            blockDescription = getMeaningBloc(driver)
            fixedMeaning = getOneDescriptonFromList(blockDescription)
            # capitalize only first letter
            fixedMeaning = fixedMeaning[0].upper() + fixedMeaning[1:]
            # replace " to \" for code files
            fixedMeaning = fixedMeaning.replace('"', '\\"')
            fileWithMeaningWords.write(f'"{word[:-1].lower()}": "{fixedMeaning}",\n')
        except:
            # meaning of the word is not on the page
            fileWithFails.write(url)

fileWithWords.close()
fileWithFails.close()
fileWithMeaningWords.close()
driver.quit()
