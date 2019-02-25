import func.all_func as func
import datetime

logger = func.logger_init('SNEMOVNA')

def get_value():
    logger.info("START")
    url = "https://www.snemovnavjakubsky.cz/cz/poledni-menu"
    html = func.get_html_obj(url)
    """
    pasre html objektu a vrácení potřebných hodnot
    :param html: ovstupní objekt html class html
    :return: vrací pole
    """
    meal_tags = html.xpath("//tbody")
    day_offer_all = []
    week_offer_all = []
    day_of_week = datetime.datetime.today().weekday()  # zjistíme dnešní den

    for meal in meal_tags:
        #vyberem hodnoty pro denní nabídku
        day_offer_name = meal.xpath("tr[@class='menu-card-dish']/td[@class='menu-card-dishname']/text()")
        day_offer_price = meal.xpath("tr[@class='menu-card-dish']/td[@class='menu-card-dishprice']/text()")
        #vybereme hodnoty týdenní nabídku
        week_offer_name = meal.xpath("tr[@class='menu-card-dish menu-card-highlight']/td[@class='menu-card-dishname']/text()")
        week_offer_price = meal.xpath("tr[@class='menu-card-dish menu-card-highlight']/td[@class='menu-card-dishprice']/text()")

        day_offer_all.append([day_offer_name, day_offer_price])
        week_offer_all.append([week_offer_name[2:4], week_offer_price[2:4]])

    #vybereme jídla daného dne
    day_offer_today = day_offer_all[day_of_week]
    week_offer = week_offer_all[day_of_week]

    #spojíme denní nabídku s týdení
    day_final_food = day_offer_today[0] + week_offer[0]
    day_final_price = day_offer_today[1] + week_offer[1]

    #spojíme jídla a ceny
    final = func.assigne_price(day_final_food, day_final_price)
    logger.info("END")
    return final