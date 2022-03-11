from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from flask import Flask, request
import time

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

url = "https://www.cars.com/shopping/results/"

#fonksiyona filtreleme için istenen değerler girilebilir
def get_car_list(brand=None, year=None, transmission=None, exteriorcolor=None):
    driver.get(url)

    carlist = []
    exceptionlist = [] #seçimi başarısız olan filtreler listelenir

    if brand is not None:
        brandbtn = Select(driver.find_element(By.ID, "make_select"))
        brandbtn.select_by_visible_text(brand.lower().capitalize())

    if year is not None:
        minyearbtn = Select(driver.find_element(By.ID, "year_year_min_select"))
        minyearbtn.select_by_visible_text(year)
        maxyearbtn = Select(driver.find_element(By.ID, "year_year_max_select"))
        maxyearbtn.select_by_visible_text(year)

    if transmission is not None:
        time.sleep(2)
        try:
            transtoggle = driver.find_element(By.ID, "trigger_transmissions")
            transtoggle.click()
        except:  # nosuchelementexception fırlatabilir
            exceptionlist.append("Vites seçilemedi.")
            pass
        try:
            time.sleep(2)
            transstring = "//label[@for='transmissions_" + transmission.lower() + "']"
            transbtn = driver.find_element(By.XPATH, transstring)
            transbtn.click()
        except:  # nosuchelementexception fırlatabilir
            exceptionlist.append("Vites bulunamadı.")
            pass

    if exteriorcolor is not None:
        time.sleep(2)
        try:
            extcolortoggle = driver.find_element(By.ID, "trigger_exterior_colors")
            extcolortoggle.click()
        except:  # nosuchelementexception fırlatabilir
            exceptionlist.append("Renk seçilemedi.")
            pass
        try:
            time.sleep(2)
            extcolorstring = "//label[@for='exterior_colors_" + exteriorcolor.lower() + "']"
            extcolorbtn = driver.find_element(By.XPATH, extcolorstring)
            extcolorbtn.click()
        except:  # nosuchelementexception fırlatabilir
            exceptionlist.append("Renk bulunamadı.")
            pass
    #50 araç seçince 48 adet araç listeleniyor bu nedenle 100 araç seçildi
    pagebtn = Select(driver.find_element(By.ID, "pagination-dropdown"))
    pagebtn.select_by_visible_text("100 results per page")
    time.sleep(2)
    #filtreleme exceptionları yazdırılıyor
    for x in exceptionlist:
        print(x)
    #50 araç seçiliyor
    carlisttemp = driver.find_elements(By.CLASS_NAME, 'vehicle-card   ')
    carlisttemp = carlisttemp[:50]

    for car in carlisttemp:
        cartitle = car.find_element(By.XPATH, './/*[@class="title"]').text
        carbrand = cartitle.split(' ')[1]
        caryear = cartitle.split(' ')[0]
        price = car.find_element(By.XPATH, './/*[@class="primary-price"]').text
        try:
            photoUrl = car.find_element(By.XPATH, './/*[@class="vehicle-image"]').get_attribute(
                "src")
        except:
            photoUrl = " "
    #burada mevcut araç bulunup tıklanılmaya çalışıldı...
        # temp = driver.find_element(By.ID, car.id)
        # temp.find_element(By.CLASS_NAME, 'title').click()
        # time.sleep(4)
        # driver.execute_script("window.history.go(-1)")
        # time.sleep(4)

        carlist.append({
            'title': cartitle,
            'brand': carbrand,
            'year': caryear,
            'price': price,
            'photoUrl': photoUrl
        })
    #test amaçlı json liste yazdırıldı
    for car in carlist:
        print(car)
    #json dönüş
    return {'car': carlist}

#fonksiyon uygulamaları

get_car_list(brand="Ford", year="2018")
#get_car_list(brand="audi", year="2018", transmission="automatic", exteriorcolor="black")
# get_car_list(brand="ford", year="2010", transmission="Manual", exteriorcolor="black")
