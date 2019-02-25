import pycurl
from lxml import html
import io
import logging
import datetime
import csv

def get_curl(url_in: str):
    """
    Funkce vrací Curl connector nastavený pro použití v KB
    :argument url: URL stahovaného souboru
    :return: Curl objekt
    """
    c = pycurl.Curl()
    # c.setopt(pycurl.VERBOSE, True)
    c.setopt(pycurl.PROXY, "vsproxy.kb.cz")
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.PROXYPORT, 8080)
    c.setopt(pycurl.FOLLOWLOCATION, 1)  # Povolit přesměrování URL
    c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)
    c.setopt(pycurl.PROXYAUTH, pycurl.HTTPAUTH_NTLM)
    c.setopt(pycurl.PROXYUSERNAME, '')
    c.setopt(pycurl.PROXYPASSWORD, '')
    c.setopt(pycurl.URL, url_in)
    c.setopt(pycurl.COOKIEFILE, 'C:\Python\Daily_Menu\logs\cookie.txt')
    c.setopt(pycurl.COOKIEJAR, 'C:\Python\Daily_Menu\logs\cookie.txt')
    return c

def get_html_obj(url_in: str):
    """
    :param url_in: url adresa stránky
    :return: html objekt připravený pro  scrapping
    """
    buffer = io.BytesIO()
    c = get_curl(url_in)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()
    c.close()
    page = buffer.getvalue().decode("UTF-8")
    html_str = html.fromstring(page)
    return html_str

def merge_values (array1_in: list, array2_in: list):
    """
    :param meal_in: pole
    :param price_in: pole
    :return: jedno pole
    """
    final = []
    for i, val in enumerate(array1_in):
        final.append(val.replace('\xa0', ' ') + array2_in[i].replace('\xa0', ' '))
    return final

def assigne_price (food_in: list, price_in: list):
    """
    :param meal_in: meal pole
    :param price_in: price pole
    :return: pole polí, v rámci jedno prvku je název i cena
    """
    final = []
    for i, val in enumerate(food_in):
        final.append([val.replace('\xa0', ' '), price_in[i]])
    return final


def logger_init(name):
    '''
    initial looger setup
    :param name: app field
    :return: logger object
    '''
    LogFileName='LUNCHAPP_run_'+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.log')
    LogPath='C:/Python/Daily_Menu/logs/'
    #FileLocation = './log'
    # Setup logging
    rootlg = logging.getLogger(name)
    rootlg.setLevel(logging.DEBUG)
    # Log on screen
    sthl = logging.StreamHandler()
    sthl.setLevel(logging.INFO)
    sthl.setFormatter(logging.Formatter('%(asctime)s %(name)-6s:%(levelname)-8s %(message)s'))
    rootlg.addHandler(sthl)
    # Log into file
    fihl = logging.FileHandler(filename=LogPath+LogFileName)
    fihl.setLevel(logging.INFO)
    fihl.setFormatter(logging.Formatter('%(asctime)s %(name)-6s:%(levelname)-8s %(message)s'))
    rootlg.addHandler(fihl)
    return rootlg

def file_export(dic_in: dict):
    """
    export staženýh dat do souboru
    :param dic_in: dictionary k exportu
    :return: nic nevrací, vytvoří soubor v adresáři
    """
    file = 'Today.txt'
    path = 'C:/Python/Daily_Menu/'
    line_break = "\r"
    with open(path+file, 'w') as file:
        csv.register_dialect('escaped',
                             delimiter=' ',
                             escapechar=' ',
                             doublequote=True,
                             quoting=csv.QUOTE_NONE,
                             lineterminator='\r')
        w = csv.writer(file, dialect='escaped')
        for key, val in dic_in.items():
            w.writerow(key)
            w.writerows(val)
            w.writerow(line_break)
    return None