import func.all_func as func

logger = func.logger_init('HYBERNIA')

def get_value():
    logger.info("START")
    url = "https://www.hybernia.cz/"
    html = func.get_html_obj(url)
    """
    parse html objektu a vrácení potřebných hodnot
    :param html: ovstupní objekt html class html
    :return: vrací pole
    """
    meal_tags = html.xpath("//div[@class='dailyMenu__meal']")
    final = []
    for meal in meal_tags:
        name = meal.xpath("span[@class='dailyMenu__meal-name']/text()")
        price = meal.xpath("span[@class='dailyMenu__meal-price']/text()")
        desc = meal.xpath("p[@class='dailyMenu__meal-description']/text()")

        try:
            final.append([name[0] +' '+ desc[0], price[0]])
        except:
            final.append([name[0], price[0]])
    logger.info("END")
    return final