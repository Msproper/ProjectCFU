import requests
from bs4 import BeautifulSoup
import pandas as pd

recipe_data = []
# Скачиваем страницу с рецептами
for i in range(1,30):
    url = f"https://eda.ru/recepty?page={i}"
    response = requests.get(url)

    # Парсим HTML-код страницы
    soup = BeautifulSoup(response.content, "html.parser")

    # Находим все блоки с рецептами
    recipes = soup.find_all("div", class_="emotion-m0u77r")

    # Создаем пустой список для хранения данных о рецептах


    # Проходим по каждому блоку с рецептом
    for recipe in recipes:
        a=recipe.find("a")['href']
        new = requests.get(url[:22] + a[8:])
        soupinfor=BeautifulSoup(new.content, 'html.parser')
        info=soupinfor.find("div", {'class':"emotion-2k9cfu"})
        di={}
        di["name"]=info.find("meta",{"itemprop":"keywords"}).get("content")
        di["category"]=info.find("meta",{"itemprop":"recipeCategory"}).get("content")
        di["coisine"]=info.find("meta",{"itemprop":"recipeCuisine"}).get("content")
        di["photo"]=info.find("div", {"class": "emotion-1voj7e4"}).find("picture").find("source").get("srcset")
        di["time"]=info.find("div", {"class": "emotion-my9yfq"}).text
        di['ingredients']=[i.text for i in info.find("div", {'class': "emotion-1509vkh"}).find("div", {"class": "emotion-yj4j4j"}).find_all("span", {"itemprop":"recipeIngredient"})]
        di["arr"]=[i.find("span", {"itemprop":"text"}).text.replace('\xa0', ' ') for i in info.find_all("div", {"itemprop": "recipeInstructions"})]
        recipe_data.append(di)
        print(di)
print(recipe_data)
print(len(recipe_data))
df=pd.DataFrame(recipe_data)
df.to_excel('recipe.xlsx', index=False)