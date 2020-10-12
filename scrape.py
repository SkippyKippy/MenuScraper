import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import asyncio

BASE_URL = "https://dining.umich.edu/menus-locations/dining-halls/"
MOSHER = BASE_URL + "mosher-jordan/"
MARKLEY = BASE_URL + "markley/"

token = "NzY1MDk2MTM5OTc1NTU3MTQw.X4P1Tg.oVQBO8nZ5wVHRG2mq9fuQHMgofQ"
client = commands.Bot(command_prefix="?")


async def get_meals(selections):
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


async def get_menu(location):
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
        tempArray.append(await get_meals(course))
        meals.append(tempArray)

    return meals


@client.command(pass_context=True)
async def m(ctx, *args):
    food = []
    # if args == "mojo":
    #     food = await get_menu(MOSHER)
    # elif args == "markley":
    #     food = await get_menu(MARKLEY)
    food = await get_menu(MOSHER)
    embed = discord.Embed(
        title="menu",
        color=0x099F5F,
    )
    for courses in food:
        embed.add_field(name=f"__{courses[0]}__", value="‎⠀", inline=False)
        for course in courses[1]:
            food_items = ""
            for food_item in course[1]:
                food_items += food_item + "\n"
            embed.add_field(name=course[0], value=food_items, inline=False)
    await ctx.send(embed=embed)


client.run(token)
