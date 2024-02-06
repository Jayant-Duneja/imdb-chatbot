import requests
import json

# url = "https://imdb146.p.rapidapi.com/v1/find/"
# querystring = {"query": "game of thrones"}
# headers = {
#     "X-RapidAPI-Key": "9bf945d759mshde4fe1a4916fc96p176ed9jsnd4cd2f06b55e",
#     "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
# }

# def get_all_results():
#     next_cursor = None
#     all_results = []
    
#     while True:
#         params = querystring.copy()
#         if next_cursor:
#             params['next'] = next_cursor
        
#         response = requests.get(url, headers=headers, params=params)
#         data = response.json()
#         try:
#             all_results.extend(data['titleResults']['results'])
#             next_cursor = data.get('titleResults', {}).get('nextCursor')
#             if not next_cursor:
#                 break
#         except KeyError:
#             break
    
#     return all_results

# # Get all results and pretty-print them
# all_results = get_all_results()
# print(json.dumps(all_results, indent=4))

# url = "https://imdb8.p.rapidapi.com/title/v2/find"

# querystring = {"title":"game of","limit":"20","sortArg":"moviemeter,asc"}

# headers = {
# 	"X-RapidAPI-Key": "9bf945d759mshde4fe1a4916fc96p176ed9jsnd4cd2f06b55e",
# 	"X-RapidAPI-Host": "imdb8.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)
# data = response.json()
# print(json.dumps(data, indent=4))

import requests

url = "https://imdb8.p.rapidapi.com/title/v2/find"

querystring = {"title":"Pathaan","limit":1,"sortArg":"moviemeter,asc"}

headers = {
	"X-RapidAPI-Key": "9bf945d759mshde4fe1a4916fc96p176ed9jsnd4cd2f06b55e",
	"X-RapidAPI-Host": "imdb8.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
try:
	movie_id = response.json()['results'][0]['id'].split('/')[2]
except IndexError:
	print("Could not find the movie. Could you please try again?")
print(movie_id)


url = "https://imdb8.p.rapidapi.com/title/get-top-cast"

querystring = {"tconst":movie_id}
response = requests.get(url, headers=headers, params=querystring)
cast = response.json()[:5]
ret = ""
print(cast)
# for actor_code in cast:
# 	url = "https://imdb8.p.rapidapi.com/actors/get-bio"

# 	querystring = {"nconst":actor_code.split('/')[2]}
# 	response = requests.get(url, headers=headers, params=querystring)
# 	actor_bio = response.json()
# 	ret+=f"""Actor Name: {actor_bio['name']}\n"""
# 	first_mini_bio = actor_bio['miniBios'][0]['text'] if actor_bio['miniBios'] else None
# 	if first_mini_bio:
# 		ret+=f"""Actor Mini-Bio: {first_mini_bio}\n"""
# 		ret+="------------------------------------------------------\n"
# 	else:
# 		pass
# print(ret)