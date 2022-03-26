import re
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from typing import Final

baseUrl: Final = r"https://gufo.me/dict/efremova"
chromeDriverPath: Final = r"C:/Users/User/Documents/chromedriver.exe"
lettersNumber: Final = 5
failsFileName: Final = "word_fails"
wordsFileName: Final = "word"
programFileFormat: Final = "txt"
letters: Final = [
    "а",
    "б",
    "в",
    "г",
    "д",
    "е",
    "ё",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "о",
    "п",
    "р",
    "с",
    "т",
    "у",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "э",
    "ю",
    "я",
]


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


def findWords(block):
    wordBlocks = block.find_elements(By.TAG_NAME, "li")
    data = []
    for element in wordBlocks:
        if len(element.text) == lettersNumber:
            data.append(element.text)
    return data


fileWithFails = open(f"{failsFileName}.{programFileFormat}", "w")
fileWithWords = open(f"{wordsFileName}.{programFileFormat}", "w")
for letter in letters:
    nextPageExist = True
    pageNumber = 0
    while nextPageExist:
        pageNumber += 1
        url = f"{baseUrl}?page={pageNumber}&letter={letter}"
        driver.get(url)
        try:
            block1 = driver.find_element(
                By.CSS_SELECTOR,
                "#all_words > div > div:nth-child(1) > ul",
            )
            data1 = findWords(block1)
            try:
                # if there is no second column
                block2 = driver.find_element(
                    By.CSS_SELECTOR,
                    "#all_words > div > div:nth-child(2) > ul",
                )
                data2 = findWords(block2)
            except:
                nextPageExist = False
                data2 = []
            data1 += data2
        except:
            fileWithFails.write(url + "\n")
        for wordBegin in data1:
            # filtering words with only english letters
            if re.fullmatch(r"[а-яёА-ЯЁ]+", wordBegin):
                correctWord = wordBegin.lower().replace("ё", "е")
                fileWithWords.write(correctWord + "\n")
    print(f"Complete for letter {letter}")

fileWithWords.close()
fileWithFails.close()
driver.quit()
