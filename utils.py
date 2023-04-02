from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import bs4
import requests
import concurrent
from deep_translator import GoogleTranslator


def clonarPaginaWeb(URL):
    # create a new Chrome browser instance
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    # navigate to the website
    driver.get(URL)
    driver.implicitly_wait(5)
    
    #dropdowns = driver.find_elements(By.XPATH, f'//button[contains(@class, "main-nav-dropdown")]')
    #dropdowns = driver.find_elements(By.CSS_SELECTOR, "button.dropdown-toggle")
   # dropdowns = driver.find_elements(By.XPATH, f'//button[contains(@class, "main-nav-dropdown js-main-nav-dropdown")]')
    dropdowns1 = driver.find_elements(By.XPATH, '//nav[contains(@class, "main-nav-dropdown js-main-nav-dropdown")]')
    dropdowns2 = driver.find_element(By.XPATH, '//button[@data-name = "MAIN_NAV_TRIGGER"]')

    dropdowns = driver.find_elements(By.XPATH, '//button[contains(@data-name, "LARGE_UP_MAIN_NAV_TRIGGER")]')
    print(dropdowns)
    #actions = ActionChains(driver)
    for dropdown in dropdowns:
        driver.implicitly_wait(5)
        #ActionChains(driver).move_to_element(dropdown).click(dropdown).perform()
        dropdown.click()
        time.sleep(0.5)

    scroll_pos_init = driver.execute_script("return window.pageYOffset;")
    stepScroll = 300

    while True:
        driver.execute_script(f"window.scrollBy(0, {stepScroll});")
        scroll_pos_end = driver.execute_script("return window.pageYOffset;")
        time.sleep(0.75)
        if scroll_pos_init >= scroll_pos_end:
            break
        scroll_pos_init = scroll_pos_end

    # get the raw HTML content
    html = driver.page_source

    # close the browser
    driver.quit()

    with open('website_original.html', 'w', encoding='utf-8') as htmlFile:
        htmlFile.write(html)


def translate_subarray(subarray):
    translator = GoogleTranslator('auto', 'hi')
    translated = translator.translate_batch(subarray)
    return ['-' if p == None else p for p in translated]


def traducirTags():
    # Scrape the file HTML
    with open('website_original.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # obtener tags
    all_tags = [tag.name for tag in soup.find_all()]
    tags = list(set(all_tags))
    # print(f'All tags: {tags}')

    # obtener tags con texto
    exclude = [bs4.element.Script, bs4.element.Stylesheet, None, "Class Central"]
    text_tags = [tag for tag in soup.find_all(tags) if tag.string not in exclude and type(tag.string) not in exclude]

    # procesar tags con texto
    phrases_pre = [txt.text.replace('\n', '') for txt in text_tags]
    phrases = [p.strip() for p in phrases_pre]
    
    # Dividimos la lista de frases en sub-listas más pequeñas
    subarray_size = 50
    subarray = [phrases[i:i+subarray_size] for i in range(0, len(phrases), subarray_size)]

    # Ejecutar la función para cada subarray en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(translate_subarray, subarray))

    # Juntar los resultados de cada subarray en un solo array
    translated = [phrase for sublist in results for phrase in sublist]

    # reemplazar texto de tags
    for i, tag in enumerate(text_tags):
        tag.string = translated[i]

    with open(f'website_translated.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))
