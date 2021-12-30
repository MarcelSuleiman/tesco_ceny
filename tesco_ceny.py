
from selenium import webdriver
# #from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

from time import sleep
import time

start = time.time()


def zapis_chybu(nazov, popis, meno = '', odkaz = ''):

    path = '.\\logy\\'

    suborLog = path + datum + '_logChyby.txt'

    print('...........................idem zapisat chybu')
    print(f'{meno} {odkaz}')

    with open(suborLog, 'a', encoding="utf-8") as chyba:
        if meno == '':
            text = f'{nazov}: {popis}\n'
        elif meno != '':
            text = f'{nazov}: {popis} ...\n{odkaz} {meno}\n'

        chyba.write(text)


def nacitaj_nanovo_a_over(url, cisloScreenu):
    try:
        menoProduktu = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[2]/' \
                       'div/div/div/ul/li[1]/div/div/div/div/div[1]/div[1]/h3/a'
        meno = ff.find_element_by_xpath(menoProduktu)
    except:

        pp = ff.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[5]/div/div[1]/strong[2]').text

        # zakomentovane lebo nechcem screenshoty momentalne
        # ff.get_screenshot_as_file('C:\\Users\\Marcel\\Desktop\\tesco_screeny\\chyby\\Tesco_{0}_chyba_{0}.png'.format(cisloScreenu))
        ff.delete_all_cookies()
        sleep(2)
        print('nacitam nanovo:', ff.current_url, 'lebo nenaslo ani len prvy produkt')
        ff.get(ff.current_url)

        nacitaj_nanovo_a_over(ff.current_url, cisloScreenu)

nextPage = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[5]/nav/ul/li[7]/a/span'

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument("--start-maximized")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

'''
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
'''

'''
image_preferences = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", image_preferences)
'''

# Uz len kvoli PIVU si to rozdel na podkategorie - dakujem. M

# kategorie = ['https://potravinydomov.itesco.sk/groceries/sk-SK/shop/oblecenie-a-moda/all?page=',
kategorie = ['https://potravinydomov.itesco.sk/groceries/sk-SK/shop/ovocie-a-zelenina/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/mliecne-vyrobky-a-vajcia/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/pecivo/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/maso-ryby-a-lahodky/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/trvanlive-potraviny/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/specialna-a-zdrava-vyziva/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/mrazene-potraviny/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/napoje/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/alkohol/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/starostlivost-o-domacnost/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/zdravie-a-krasa/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/starostlivost-o-dieta/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/chovateske-potreby/all?page=',
             'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/domov-a-zabava/all?page=']

datum = time.strftime('%Y-%m-%d', time.localtime())
subor = 'tesco_ceny_' + datum + '.csv'

# #ff = webdriver.Firefox(firefox_profile=profile, options=options) # spustanie bez obrazkov a celkovo nech FF nie je vidno

cisloScreenu = 0
cisloScreenu2 = 0

for kategoria in kategorie:
    try:
        # ff = webdriver.Firefox(firefox_profile=profile)# , options=options)
        ff = webdriver.Chrome(executable_path=r"C:\\DEV\\chromedriver\\chromedriver96.exe", options=chrome_options)
        # ff = webdriver.Chrome(options=chrome_options)

        kategoria_list = kategoria.split('/')
        popis_kategoria = kategoria_list[-2:-1][0]
        print(popis_kategoria)

        url = kategoria + '1'

        try:
            ff.delete_all_cookies()
        except:
            print('Zlyhalo ff.delete_all_cookies()')

        try:
            ff.get(url)
        except:
            print('Zlyhalo ff.get')

        try:
            page_source = ff.page_source
        except:
            print('zlyhalo: page_source = ff.page_source')

        nacitaj_nanovo_a_over(ff.current_url, cisloScreenu)

        #ff.get_screenshot_as_file('C:\\Users\\Marcel\\Desktop\\tesco_screeny\\Tesco_{}.png'.format(start))

        try:
            pp = ff.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]'
                                          '/div[5]/div/div[1]/strong[2]').text

        except:
            print('Zlyhalo nacitanie poctu poloziek pre vypocet poctu stran produktov v kategorii')
            nacitaj_nanovo_a_over(ff.current_url, cisloScreenu)

        print(pp)
        pocetPoloziek = pp.replace(' položiek', '')
        pocetPoloziek = int(pocetPoloziek)

        import math

        pocetStran = math.ceil(pocetPoloziek / 48)

        ff.delete_all_cookies()

        file1 = open(subor, "a", encoding="utf-8")
        file2 = open('tesco_ceny_all.csv', 'a', encoding="utf-8")

        for j in range(1, pocetStran + 1):

            link = kategoria + str(j) + '&count=48'
            ff.get(link)

            cisloScreenu += 1
            # ff.get_screenshot_as_file('C:\\Users\\Marcel\\Desktop\\tesco_screeny\\Tesco_{}.png'.format(cisloScreenu))

            nacitaj_nanovo_a_over(ff.current_url, cisloScreenu)

            baseScroll = 480
            toPoint = 0

            for i in range(1, 49):

                ff.delete_all_cookies()

                toPoint += baseScroll
                ff.execute_script(f"window.scrollTo(0, {toPoint});")

                nacitaj_nanovo_a_over(ff.current_url, cisloScreenu)

                menoProduktu = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[2]/' \
                               'div/div/div/ul/li[' + str(i) + ']/div/div/div/div/div[1]/div[1]/h3/a'
                menoProduktuAkcia = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[2]' \
                                    '/div/div/div/ul/li[' + str(i) + ']/div/div/div/div[1]/div[1]/div[1]/h3/a'

                # cena sa deli podla toho ci je to na vahu alebo striktne ks/bal a pod.
                cenaZaMnJednotku001 = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]' \
                                      '/div[2]/div/div/div/ul/li[' + str(i) + ']/div/div/div/div/div[2]/form/div' \
                                                                              '/div[1]/div[2]/span[1]/span[1]'
                cenaZaMnJednotku002 = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]' \
                                      '/div[2]/div/div/div/ul/li[' + str(i) + ']/div/div/div/div/div[2]/form/div' \
                                                                              '/div[2]/div[2]/span[1]/span[1]'

                mernaJednotka001 = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[2]' \
                                   '/div/div/div/ul/li[' + str(i) + ']/div/div/div/div[1]/div[2]/form/div/div[2]' \
                                                                    '/div[2]/span[2]'
                mernaJednotka002 = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[2]/' \
                                   'div/div/div/ul/li[' + str(i) + ']/div/div/div/div/div[2]/form/div/div[1]/div[2]' \
                                                                   '/span[2]'

                povodnaCenaZaMnJednotku = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]' \
                                          '/div[2]/div/div/div/ul/li[' + str(i) + ']/div/div/div/div[1]/div[1]' \
                                                                                  '/div[2]/div/ul/li/a/div/span[1]'

                try:
                    meno = ff.find_element_by_xpath(menoProduktu).text
                    produktLink = ff.find_element_by_xpath(menoProduktuAkcia).get_attribute('href')
                    produktID = produktLink.split('/')[-1:]

                    linkNaObrazok = '/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[4]/' \
                                    'div[2]/div/div[2]/div/ul/li[' + str(i) + ']/div/div/div/div/a/div/img'
                    produktImg = str(ff.find_element_by_xpath(linkNaObrazok).get_attribute('src'))
                    ean = str(produktImg.split('/')[6])
                    categoryInImageLink = str(produktImg.split('/')[5])

                    try:
                        povodnaCenaText = ff.find_element_by_xpath(povodnaCenaZaMnJednotku).text
                        # -43%, predtým 1,39 €, teraz 0,79 €;

                        vyskaZlavy = povodnaCenaText.split(',')[0].replace('-',
                                                                           '')  # chcem to mat zapisane aj s percentami

                        uvedenaPovodnaCena = povodnaCenaText.split(',')
                        uvedenaPovodnaCena = uvedenaPovodnaCena[1] + ',' + uvedenaPovodnaCena[2]
                        uvedenaPovodnaCena = uvedenaPovodnaCena.replace(' predtým ', '').replace(' €', '')

                        novaCena = povodnaCenaText.split(',')
                        novaCena = novaCena[3] + ',' + novaCena[4]
                        novaCena = novaCena.replace(' teraz ', '').replace(' €', '')

                        povodnaCena = '{};{};{};{}'.format(povodnaCenaText, vyskaZlavy, uvedenaPovodnaCena, novaCena)

                        # print(povodnaCena)
                    except Exception as E:
                        povodnaCena = ';;;'

                    try:
                        cena = ff.find_element_by_xpath(cenaZaMnJednotku001).text
                    except:
                        cena = ff.find_element_by_xpath(cenaZaMnJednotku002).text

                    try:
                        mj = ff.find_element_by_xpath(mernaJednotka001).text
                    except:
                        mj = ff.find_element_by_xpath(mernaJednotka002).text



                    '''
                    try:
                        special_chars = 'ÀàÉéÈèÊêÎîÏïÙùÛûÜüŸÿ'

                        neziaduci_znak = ['À', 'à', 'â', 'È', 'è', 'Ê', 'ê', 'Î', 'î', 'Ï', 'ï',
                                          'Ù', 'ù', 'Û', 'û', 'Ü', 'ü', 'Ÿ', 'ÿ', 'ñ', 'х', '¹', '⁰', '³', 'Ø', 'β']

                        ziaduci_znak = ['A', 'a', 'a', 'E', 'e', 'E', 'e', 'I', 'i', 'I', 'i',
                                        'U', 'u', 'U', 'U', 'U', 'u', 'Y', 'y', 'n', 'x' '1', '0', '3', 'priem.', 'beta']

                        # print(torrent_name.replace('ľščťžýáíéúäňô','lsctzyaieuano'))

                        for i in range(len(neziaduci_znak)):
                            if neziaduci_znak[i] in meno:
                                meno = meno.replace(neziaduci_znak[i], ziaduci_znak[i])
                    except:
                        print('pruser pri zamienani pismen')
                        
                    '''




                    text = f'{meno};{cena};{mj.replace("/", "")};{povodnaCena};{popis_kategoria};{produktID[0]};{ean};{categoryInImageLink};'
                    text2 = f'{datum};{meno};{cena};{mj.replace("/", "")};{povodnaCena};{popis_kategoria};{produktID[0]};{ean};{categoryInImageLink};'

                    try:
                        file1.write(text + '\n')
                        file2.write(text2 + '\n')

                    except Exception as E:


                        # zvlastny produkt lebo obsahuje specialne (francuzske znaky) --- Opravene otvor subor ako utf-8
                        odkaz = '________________________________Divny produkt, zvlastne znaky v nom:'
                        print(E.__class__.__name__, str(E), meno, odkaz)
                        print(f'{odkaz} {meno}')
                        zapis_chybu(E.__class__.__name__, str(E), meno, odkaz)
                        continue

                except Exception as E:

                    if i > 1:
                        pass
                    else:

                        # toto by bolo treba riesit inak, napr pred kazdym skenovanim produktov vyratat,
                        # kolko ich na stranke ma byt a nie ist naslepo do konca

                        print('riadok 298: ', E.__class__.__name__ + str(E))
                        zapis_chybu(E.__class__.__name__, str(E), meno)

                        # tu je break lebo ak nenacita polozku napr 26, je to preto ze sme na konci kategorie,
                        # na poslednej strane je uz len zvysnach 25 poloziek, 26, 27,28, ... tam uz nie su
                        break


                # ff.delete_all_cookies()

            ff.delete_all_cookies()
            # print('Strana {} zapisana'.format(j))
            # sleep(1)
            # ff.delete_all_cookies()
    except Exception as A:
        print('chyba riadok 313: ', A.__class__.__name__ + str(A))
        zapis_chybu(A.__class__.__name__, str(A))
        # ff.quit()

    file1.close()
    file2.close()
    ff.quit()

    sleep(10)

end = time.time()
print(end - start)

print('\n\n\nFin!')
ff.quit()
