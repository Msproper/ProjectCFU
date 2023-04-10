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
        di["photo"]=info.find("div", {"class": "emotion-1voj7e4"}).find("picture").find("source").get("srcset")
        recipe_data.append(di)
        print(di)
print(recipe_data)
print(len(recipe_data))
df=pd.DataFrame(recipe_data)
df.to_excel('recipe1.xlsx', index=False)