import requests
from bs4 import BeautifulSoup
import discord

BASE_URL = "https://dining.umich.edu/menus-locations/dining-halls/"
MOSHER = BASE_URL + "mosher-jordan/"
MARKLEY = BASE_URL + "markley/"


def get_meals(selections):
    foodItems = []
    selections = selections.find("ul", class_="courses_wrapper").find_all(
        "li", recursive=False
    )
    for selection in selections:
        tempMeals = []
        tempItems = []
        tempMeals.append(selection.find("h4").text)
        items = selection.find_all(class_="item-name")
        for item in items:
            tempItems.append(item.text.strip())

        tempMeals.append(tempItems)
        foodItems.append(tempMeals)

    return foodItems


def get_menu(location):
    response = requests.get(location)

    soup = BeautifulSoup(response.content, "html.parser")
    soup.prettify()

    menu = soup.find(id="mdining-items")

    mealNames = menu.find_all("h3")

    all_courses = menu.find_all(class_="courses")

    meals = []

    for index, course in enumerate(all_courses):
        tempArray = []
        tempArray.append(mealNames[index].text.strip())
        tempArray.append(get_meals(course))
        meals.append(tempArray)

    return meals


print(get_menu(MARKLEY))
