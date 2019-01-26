import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_manual(food_name):
    def search_food(food_name):
        try:
            search_url = 'https://www.xiachufang.com/'

            driver = webdriver.Chrome() #setup driver
            #optional headless
            option_ = Options()
            option_.add_argument('headless')

            driver.get(search_url)

            #search for food
            search_input = driver.find_element_by_xpath("//input[@name='keyword']")
            search_input.clear()
            search_input.send_keys(food_name)  #input food name
            driver.find_element_by_xpath("//input[@value='搜菜谱']").click()  #点击 搜索

            #return searched page/link
#             food_searched_page = driver.find_element_by_xpath("//link[@rel='canonical']").get_attribute('href')


            food_manual_div_tag = driver.find_element_by_xpath("//div[@class='info pure-u']")
            food_manual_name = driver.find_element_by_xpath(".//img").get_attribute('alt')
            food_manual_page = driver.find_element_by_xpath(".//p[@class='name']//a").get_attribute('href')
            # food_manual_page = base_url + food_manual_page
            print(food_manual_name, food_manual_page, sep='\n')

            driver.quit()
        except:
            base_url = 'https://www.xiachufang.com'
            search__url = 'https://www.xiachufang.com/search/?keyword='
            response = requests.get(search_url + food_name)
            soup = bs4.BeautifulSoup(response.content, 'lxml')
            print(soup)
            div_tag = soup.find('div', {'class':'info pure-u'})
            # print(div_tag)
            p_tag = div_tag.find('p', {'class':'name'})
            food_page  = p_tag.find('a').get('href')
            food_manual_page = base_url + food_page
        return food_manual_page

    
    food_url = search_food(food_name)
    response = requests.get(food_url)
    soup = bs4.BeautifulSoup(response.content, 'lxml')
    # print(soup)
    body_tag = soup.find('div', {'class':'block recipe-show'})
    ings_tag = body_tag.find('div', {'class':'ings'})
    steps_tag = body_tag.find('div', {'class':'steps'})
    ings_a_tags_list = ings_tag.find_all('a')
    steps_p_tags_list = steps_tag.find_all('p')

    ingredient = ','.join([a_tag.get_text() for a_tag in ings_a_tags_list])
    recipe = '\n'.join([p_tag.get_text() for p_tag in steps_p_tags_list])
    print(ingredient, recipe, sep='\n\n\n')
    return [ingredient, recipe]
