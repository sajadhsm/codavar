import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

test_name = __loader__.name

def selenium_test(sub_dir_path):
    print('--- Start "{}" TEST ---'.format(test_name))
    
    score = 0

    index_url = "file://{}/index.html".format(sub_dir_path)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(index_url)
    title = driver.title

    driver.close()

    if title == 'First Test': score = 20
    
    print('--- End "{}" TEST [Score: {}] ---'.format(test_name, score))
  
    return score