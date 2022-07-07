# Reči sa hovoria, chleba sa je. Ale za peniaze nakúpiš. Slobodna Europa

import requests
import time
import math

from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def wrong_code(url:str, headers:dict, error_name = '', error_message = '') -> None:

	if error_name != '':
		error_line = f'{url}, {headers}\n{error_name}: {error_message}\n'
	else:
		error_line = f'{url}, {headers}\n'

	with open('errors_log.txt', 'a', encoding='utf-8') as f:
		f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
		f.write(error_line)

	time.sleep(600)

def get_new_header():
	ua = UserAgent()
	header = ua.random

	return {'User-Agent': '{header}'}

def extractor(groceries: list) -> None:
	"""
	Funkcia extractor prijma ako parameter blok html kodu z bs4 
	a z neho vybera jednotlive udaje
	"""
	for t in groceries:

		# meno je vzdy prve a na svojom mieste
		name = t.find_all('a')[1].text

		# cena
		# ak sa jedna o polozku ako jablka, banany, oriesky, paprika a ine volne tovary,
		# nema zmysel si evidovat cenu 1 bananu - 1 standardizovaneho bananu
		# niektore veci vnimame automaticky na kila, metre, litre
		#
		# POZOR od 02/02/2022 zmena span 3 nie 4

		# POZOR 18/05/2022 zmena sablony

		# if t.find_all('span')[3].text == 'Množstvo':
		try:
			if t.find_all('span', {'class': 'styled__StyledLabel-sc-1ttuvhr-0 hPDfsf beans-radio-button-with-label__label beans-label'})[0].text == 'Množstvo':
				price_per_unit = price_per_si = t.find_all('p', {'class': 'styled__StyledFootnote-sc-119w3hf-7 icrlVF styled__Subtext-sc-8qlq5b-2 bNJmdc beans-price__subtext'})[0].text
		except IndexError:
			try:
				price_per_unit = t.find_all('p', {'class': 'styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text'})[0].text
				price_per_si = t.find_all('p', {'class': 'styled__StyledFootnote-sc-119w3hf-7 icrlVF styled__Subtext-sc-8qlq5b-2 bNJmdc beans-price__subtext'})[0].text

			except IndexError:
				print(name)
				continue

		# MJ
		try:
			unit_of_quantity = price_per_si.split(' €/')[-1]
		except:
			unit_of_quantity = 'NaN'

		# Cena za balenie
		try:	
			price_per_unit = price_per_unit.split(' ')[0].replace(' ', '')
		except:
			price_per_unit = 'NaN'

		# cena za MJ
		try:
			price_per_si = price_per_si.split(' €/')[0].replace(' ', '')
		except:
			price_per_si = 'NaN'


		if t.find('span', {'class': 'offer-text'}) != None:
			discount = t.find('span', {'class': 'offer-text'}).text
			discount_splitted = discount.split(', ')

			discount_percentage = discount_splitted[0]
			old_price = discount_splitted[1].replace('predtým ','').replace(' €','')
		else:
			discount = ''
			old_price = ''
			discount_splitted = ''
			discount_percentage = ''

		# PLU resp. ich kod tovaru
		plu = t.find('input', {'name': 'id'})['value']

		# EAN
		# polozky ktore nemaju balenie / obal, nemaju ean, tak im nejaky vymysleli
		# ale olej, muka, vino, ... to ma realny unikatny ean
		# link na img nepotrebujem evidovat, ten si vyskladam z cat a ean
		link_to_image = t.find('img', {'class': 'product-image'})['src']

		#						cat	ean
		#						|	 |
		#						V	 V
		# "https://secure.ce-tescoassets.com/assets/SK/030/0000031429030/ShotType1_225x225.jpg"

		sub_folder = link_to_image.split('/')[5]
		ean = link_to_image.split('/')[6]

		#print('{:<100}{:<10}{:<10}{:<5}{:<5}{:<10}{:<15}{:<5}{:<15}'.format(name, price_per_unit, price_per_si, unit_of_quantity, discount_percentage, old_price, plu, sub_folder, ean))

		row = '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";\n'.format(name, price_per_unit, price_per_si, unit_of_quantity, discount_percentage, old_price, category, plu, sub_folder, ean)

		file1.write(row)
		file1.flush()	

categories = ['ovocie-a-zelenina', 'mliecne-vyrobky-a-vajcia', 'pecivo', 'maso-ryby-a-lahodky',
		'trvanlive-potraviny', 'specialna-a-zdrava-vyziva','mrazene-potraviny',
		'napoje', 'alkohol', 'starostlivost-o-domacnost', 'zdravie-a-krasa',
		'starostlivost-o-dieta', 'chovateske-potreby','domov-a-zabava']

for category in categories:

	headers = get_new_header()

	url = 'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/' + category + '/all?page=' + '1' + '&count=48'

	try:
		r = requests.get(url, headers=headers)
		print(r.status_code, category)
		if str(r.status_code) != '200':
			wrong_code(url, headers)

	except Exception as E:
		print(str(E))
		wrong_code(E.__class__.__name__, str(E))

	soup = BeautifulSoup(r.content, 'html.parser')

	# na zaciatku sa nachadza informacia, kolko produktov sa v danej sekcii nachadza
	# podla tejto info vieme vypocitat, kolko stran ma dana sekcia

	items_count = soup.find('span', {'class', 'items-count'}).text
	items_count_int = int(items_count.replace(' ','').replace('(','').replace(')',''))

	number_of_pages = math.ceil(items_count_int / 48)

	date_for_file_name = time.strftime('%Y-%m-%d', time.localtime())

	file_name = date_for_file_name + '_tesco_ceny.csv'
	file1 = open(file_name, 'a', encoding='utf-8')

	for page in range(1, number_of_pages + 1):
		# parsuj parsuj vykrucaj

		time.sleep(5)

		headers = get_new_header()
		url = 'https://potravinydomov.itesco.sk/groceries/sk-SK/shop/' + category + '/all?page=' + str(page) +'&count=48'

		try:
			r = requests.get(url, headers=headers)
			print(r.status_code, category, page)
			if str(r.status_code) != '200':
				wrong_code(url, headers)

		except Exception as E:
			print(str(E))
			wrong_code(E.__class__.__name__, str(E))
			page -= 1

		soup = BeautifulSoup(r.content, 'html.parser')

		## li cely 1 produkt, na stranke je ich niekolko
		tag = 'li'
		identificator_name = 'class'
		identificator_value = 'product-list--list-item'

		groceries = soup.find_all(tag, {identificator_name: identificator_value})

		extractor(groceries)


	file1.close()
