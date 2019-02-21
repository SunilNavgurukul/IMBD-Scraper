import requests
import os
import json
import pprint
import random
import time
from bs4 import BeautifulSoup
# That is IMBD tops movies URL
IMDB_url="https://www.imdb.com/india/top-rated-indian-movies/"

#This function i make for to get the data from IMBD's top indian movies link also it program convert
#it into json formate it basically it program gives us position, movies url, movies name, movie year and rating
#Task 1
def scrape_top_list(url):
	if os.path.exists('page.json'):
		pass
	else:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		tbody_div = soup.find('tbody', class_="lister-list")
		trs = tbody_div.find_all('tr')
		IMDB_top_movie=[]
		for tr in trs:
			name_title = tr.find('td',class_="titleColumn")
			half_url = name_title.find("a")
			url = "https://www.imdb.com"+half_url["href"]
			rating_class = tr.find('td', class_="ratingColumn imdbRating")
			rating = float(rating_class.find('strong').get_text())
			dict = {'position':'','name':'','year':'','rating':'','IMDB_url':''}
			a = name_title.get_text().strip().split('\n')
			dict['position'] = int(a[0].strip('.'))		
			dict['year']=int(a[2][1:5])
			dict['name'] = a[1].strip()
			dict['rating'] = rating
			dict['IMDB_url'] = url
			IMDB_top_movie.append(dict)
		with open ('page.json',"w") as data:
			json.dump(IMDB_top_movie,data)
	with open ('page.json',"r") as data:
		read = data.read()
		IMDB_top_movie = json.loads(read)
	return IMDB_top_movie
scraped_movie=scrape_top_list(IMDB_url)
# pprint.pprint(scraped_movie)


#here i use scrape_top_list(IMDB_url) funtion for arrenge movies by year
#Task 2
def group_by_year(Top_movies_list):
	key_year=[]
	movie_group=[]
	for i in Top_movies_list:
		if i['year'] not in key_year:
			key_year.append(i['year'])
		key_year.sort()
	for x in key_year:
		dic={x:[]}
		for z in Top_movies_list:
			if x == z['year']:
				dic[x].append(z)
		movie_group.append(dic)
	return(movie_group)
	# return(key_year)
year_by=group_by_year(scraped_movie)
# pprint.pprint(year_by)


#here i group_by_year(scraped_movie){year_by} function for arrenge as a decade by year
#Task 3
def group_by_decade(movie):
	decate_year_key=[]
	for i in range(1950,2020,10):
		decate_year_dic={i:[]}
		decate_year_key.append(decate_year_dic)
	for x in movie:
		for y in x:
			for z in decate_year_key:
				for b in z:
					c=b+10
					if b<=y and y<=c:	
						z[b].append(x)
	return decate_year_key
decaded_group=group_by_decade(year_by)
# pprint.pprint(decaded_group)

#Task 13
#this the task 13 this task will give us cast for one movie
def scrape_movie_cast(movie_caste_url):
	movie_cast=movie_caste_url['IMDB_url']
	half_cast_url=movie_cast[:37]
	cast_url=half_cast_url+"fullcredits?ref_=tt_cl_sm#cast"
	cast = requests.get(cast_url)
	soup = BeautifulSoup(cast.text,"html.parser")
	a_name=soup.find("table",class_="cast_list")
	tds=a_name.find_all("td",class_='')
	cast_dic={}
	cast_list=[]
	for x in range(len(tds)):
		actors=tds[x].find('a').get('href')[6:15]
		cast_dic["imbd_actor_id"]=actors
		actor_name=tds[x].get_text().strip()
		cast_dic["name"]=actor_name
		cast_list.append(cast_dic.copy())
	return cast_list
# cast_data=scrape_movie_cast(scraped_movie)
# print(cast_data)

# a=scraped_movie[0]

#this program getting url from task 1
#also this program write all basic detail with the help of url and  add all detail into dictonary
#Task 4
def scrape_movie_details(movie_url):
	#Task 9
	#random function i use for to get rendomlly number between 1 to 3
	time_sleep=random.randint(1,3)
	#Task 8
	file_url=movie_url['IMDB_url'][27:36]+'.json'
	if os.path.exists('/home/sunil/Documents/sunil codes/Web Scraping/Moies_data/'+file_url):
		pass
	else:
		movie_detail_dic={'name':'','director':'','country':'','language':[],'poster_image_url':'','bio':'','runtime':'','genre':''}
		# seleted_movies_url=movie_url[movie_url]['IMDB_url']
		movie_name=movie_url['name']
		seleted_movies_url=movie_url['IMDB_url']

		#Task 9
		#time.sleep is an time module(sleep is an method) I use it to set a time period because i want to set
		#the it in request
		time.sleep(time_sleep)
		detail=requests.get(seleted_movies_url)
		soup=BeautifulSoup(detail.text, 'html.parser')
		director_shell=soup.find('div', class_='credit_summary_item')
		director_list= director_shell.find_all('a')
		director_name_final=[]
		genre=[]
		for i in director_list:
			director_name_final.append(i.get_text())
		bio_class=soup.find(class_='summary_text').get_text().strip()
		poster_image_url=soup.find(class_='poster').find('a').find('img')['src']
		subtext_class=soup.find(class_='subtext')
		time_run=subtext_class.find('time').get_text().strip()
		run_time= int(time_run[0])*60
		if 'min' in time_run:
			time_min=time_run[3:].split('min')[0]
			run_time+=int(time_min)
		genre_all=subtext_class.find_all('a')
		for i in genre_all:
			genre.append(i.get_text())
		extra_details = soup.find('div', attrs={"class":"article","id":"titleDetails"})
		list_of_divs = extra_details.find_all('div')
		for div in list_of_divs:
			tag_h4 =  div.find_all('h4')
			for text in tag_h4:
				if 'Language:' in text:
					tag_anchor = div.find_all('a')
					movie_language = [language.get_text() for language in tag_anchor]
				elif 'Country:' in text:
					tag_anchor = div.find_all('a')
					movie_country = ''.join([country.get_text() for country in tag_anchor])
		movie_detail_dic['country']=movie_country
		movie_detail_dic['language']=movie_language
		movie_detail_dic['name']=movie_name
		movie_detail_dic['director']=director_name_final
		movie_detail_dic['bio']=bio_class
		movie_detail_dic['poster_image_url']=poster_image_url
		movie_detail_dic['genre']=genre[-1::-1][1:]
		movie_detail_dic['runtime']=run_time,'mins'
		movie_detail_dic['cast']=scrape_movie_cast(movie_url)
		with open ('/home/sunil/Documents/sunil codes/Web Scraping/Moies_data/'+file_url,"w") as data:
			json.dump(movie_detail_dic.copy(),data)
	with open ('/home/sunil/Documents/sunil codes/Web Scraping/Moies_data/'+file_url,"r") as data:
			read = data.read()
			movie_detail_dic= json.loads(read)
	return(movie_detail_dic)
# j=scrape_movie_details(a)
# print(j)

#this program append all movies detais in movies's name list to call scraped_movie name funtion(Task 1)
#task 5
def get_movie_list_details(movies_list):
	movies=[]
	for x in range(len(movies_list)):
		index=movies_list[x]
		a=scrape_movie_details(index)
		movies.append(a)
	return movies
all_det=get_movie_list_details(scraped_movie)
# pprint.pprint(all_det)

#this program analyse the movies language
#Task 6
def Analyse_movie_language(movie_list):
	dic_lang={}
	for movie in movie_list:
		for lang in movie['language']:
			dic_lang[lang]= 0
	return dic_lang
	for movie in movie_list:
		for lang in movie['language']:
			dic_lang[lang]+= 1
	# return dic_lang
# analysis_language=Analyse_movie_language(all_det)
# print(analysis_language)

# this program analyse the movies director
#Task 7
def Analyse_movie_director(movie_list):
	director_dic={}
	for dictr in movie_list:
		for direct in dictr['director']:
			director_dic[direct]= 0
			# print (direct)
	for dictr in movie_list:
		for direct in dictr['director']:
			director_dic[direct]+= 1
	return director_dic
# analysis_director=Analyse_movie_director(all_det)
# print(analysis_director)

#Task 10
def analyse_language_and_directors(movie_list):
	#directors_dict={i:{} for i in analysis_director}
	directors_dict = Analyse_movie_director(movie_list)
	directors_lang = {director:{} for director in directors_dict}
	for i in range(len(movie_list)):
		for director in directors_lang:
			if director in movie_list[i]['director']:
				for language in movie_list[i]['language']:
					directors_lang[director][language] = 0
	for i in range(len(movie_list)):
		for director in directors_lang:
			if director in movie_list[i]['director']:
				for language in movie_list[i]['language']:
					directors_lang[director][language] += 1
	return directors_lang	
# analyse_ld=analyse_language_and_directors(all_det)
# pprint.pprint(analyse_ld)
#Task 11
def analyse_movies_genre(movies_list):		
	dic_genra={}
	for movie in movies_list:
		for genre in movie['genre']:
			dic_genra[genre]= 0
	for movie in movies_list:
		for genre in movie['genre']:
			dic_genra[genre]+=1
	return dic_genra
# by_genra=(analyse_movies_genre(all_det))
# print(by_genra)

#Task 15

def analyse_actors(movie_list):
	dict={}
	all_actor=[]
	id_list=[]
	for movie in movie_list:
		for i in movie['cast']:
			dict[i['imbd_actor_id']]={'name':movie['name'],'num_movie':0}
			id_list.append(i["imbd_actor_id"])
			set_list=list(set(id_list))
	for movie in movies_list:
		for actor in movie["cast"]:
			actors_dic[actor['imbd_actor_id']]['num_movie'] += 1	
	pprint.pprint(actors_dic)
analyse_actors(all_det)


