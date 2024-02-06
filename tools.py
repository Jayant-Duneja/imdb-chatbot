import requests
import json
from pydantic.v1 import BaseModel, Field
from langchain.agents import tool

class GetCastDetailsInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")

class GetRatingInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")

class GetAwardsInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")

class GetPlotInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")

headers = {
        "X-RapidAPI-Key": "9bf945d759mshde4fe1a4916fc96p176ed9jsnd4cd2f06b55e",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
def get_id(name : str) -> str:
    """ Get the ID of the movie or the TV show from the name"""
    
    url = "https://imdb8.p.rapidapi.com/title/v2/find"
    querystring = {"title":name,"limit":1,"sortArg":"moviemeter,asc"}
    response = requests.get(url, headers=headers, params=querystring)
    movie_id = None
    try:
        movie_id = response.json()['results'][0]['id'].split('/')[2]
    except IndexError:
        print("Could not find the movie. Could you please try again?")
    return movie_id

@tool(args_schema=GetCastDetailsInput)
def get_cast_details(id : str) -> str:
    """ Get the cast details of the movie or the TV show from the ID""" 
    url = "https://imdb8.p.rapidapi.com/title/get-top-cast"

    querystring = {"tconst":id}
    response = requests.get(url, headers=headers, params=querystring)
    print(id)
    print(response)
    cast = response.json()
    ret = ""
    for actor_code in cast[:5]:
        url = "https://imdb8.p.rapidapi.com/actors/get-bio"

        querystring = {"nconst":actor_code.split('/')[2]}
        response = requests.get(url, headers=headers, params=querystring)
        actor_bio = response.json()
        ret+=f"""Actor Name: {actor_bio['name']}\n"""
        first_mini_bio = actor_bio['miniBios'][0]['text'] if actor_bio['miniBios'] else None
        if first_mini_bio:
            ret+=f"""Actor Mini-Bio: {first_mini_bio}\n"""
            ret+="------------------------------------------------------\n"
        else:
            pass
    return ret

@tool(args_schema=GetRatingInput)
def get_rating(id : str) -> str:
    """ Get the rating of the movie or the TV show from the ID"""
    
    url = "https://imdb8.p.rapidapi.com/title/get-ratings"

    querystring = {"tconst":id}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    # Extract the rating
    data = response.json()
    output = ""

    # Extract the title, rating, and ratingCount
    title = data['title']
    rating = data['rating']
    rating_count = data['ratingCount']

    # Append the title, rating, and ratingCount to the output string
    output += f"Title: {title}\n"
    output += f"Rating: {rating}\n"
    output += f"Rating Count: {rating_count}\n"

    # Append each demographic and their ratings to the output string
    for demographic, details in data['ratingsHistograms'].items():
        output += f"\n{demographic}:\n"
        output += f"  Aggregate Rating: {details['aggregateRating']}\n"
        # output += f"  Histogram:\n"
        # for rating_value, count in details['histogram'].items():
        #     output += f"    {rating_value}: {count}\n"

    # Print the entire output string
    return output

@tool(args_schema=GetAwardsInput)
def get_awards(id : str) -> str:
    """ Get the awards of the movie or the TV show from the ID"""
    
    url = "https://imdb8.p.rapidapi.com/title/get-awards-summary"

    querystring = {"tconst":id}

    headers = {
        "X-RapidAPI-Key": "9bf945d759mshde4fe1a4916fc96p176ed9jsnd4cd2f06b55e",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    summary = ""

    # Extract the title, year, and highlighted award information
    title = data['title']
    year = data['year']
    highlighted_award = data['awardsSummary']['highlighted']['awardName']
    highlighted_award_count = data['awardsSummary']['highlighted']['count']
    highlighted_award_is_winner = "Winner" if data['awardsSummary']['highlighted']['isWinner'] else "Nominated"


    # Append the title, year, and highlighted award information to the summary string
    summary += f"Title: {title}\n"
    summary += f"Year: {year}\n"
    summary += f"Highlighted Award: {highlighted_award} ({highlighted_award_count} times)\n"
    summary += f"Status: {highlighted_award_is_winner}\n"

    # Append the other nominations and wins count to the summary string
    summary += f"Other Nominations Count: {data['awardsSummary']['otherNominationsCount']}\n"
    summary += f"Other Wins Count: {data['awardsSummary']['otherWinsCount']}\n"

    # Append the highlighted ranking information to the summary string
    summary += f"Highlighted Ranking: {data['highlightedRanking']['label']} (Rank: {data['highlightedRanking']['rank']})\n"
    return summary

@tool(args_schema=GetPlotInput)
def get_plot(id : str) -> str:
    """ Get the plot of the movie or the TV show from the ID"""
    
    url = "https://imdb8.p.rapidapi.com/title/get-plots"

    querystring = {"tconst":id}

    headers = {
        "X-RapidAPI-Key": "9bf945d759mshde4fe1a4916fc96p176ed9jsnd4cd2f06b55e",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    # Initialize an empty string to hold the formatted output
    plots_summary = ""

    # Iterate over the plots and append each plot's text to the summary string
    for plot in data['plots'][:5]:
        plots_summary += plot['text'] + "\n\n"
    return plots_summary  # Return the formatted output
