import func.all_func as func

logger = func.logger_init('HUSA')

def get_value():
    logger.info("START")
    url = "http://www.potrefena-husa.eu/"
    html = func.get_html_obj(url)
    """
    pasre html objektu a vrácení potřebných hodnot
    :param html: ovstupní objekt html class html
    :return: vrací pole
    """
    food = html.xpath("//div[@class='foodbox denninabidka']/h4/text()")
    desc = html.xpath("//div[@class='foodbox denninabidka']/p/text()")
    price = html.xpath("//div[@class='foodbox denninabidka']/span[@class='price']/text()")

    #spijíme jídlo s popisem
    food_final = func.merge_values(food, desc)
    #spojíme jídla s cenou
    final = func.assigne_price(food_final, price)
    logger.info("END")
    return final