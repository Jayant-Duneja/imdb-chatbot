import requests
import json
from pydantic.v1 import BaseModel, Field
from langchain.agents import tool
from dotenv import load_dotenv, find_dotenv
import os


class GetCastDetailsInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")


class GetRatingInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")


class GetAwardsInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")


class GetPlotInput(BaseModel):
    id: str = Field(..., title="ID", description="ID of the movie or the TV show")


def get_headers():
    _ = load_dotenv(find_dotenv())  # read local .env file
    return {
        "X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
        "X-RapidAPI-Host": os.getenv("X-RapidAPI-Host"),
    }

from utils.logger import logger

def get_id(name: str) -> str:
    """Get the ID of the movie or the TV show from the name"""

    url = "https://imdb8.p.rapidapi.com/title/v2/find"
    headers = get_headers()
    querystring = {"title": name, "limit": 1, "sortArg": "moviemeter,asc"}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        movie_id = response.json()["results"][0]["id"].split("/")[2]
        logger.debug(f"Movie ID was succesfully retrieved. Movie ID: {movie_id}")
        return movie_id
    except Exception as e:
        logger.debug(f"Not able to find the movie ID for the movie: {name}")
        logger.debug(f"Error: {e}")
        return f"Movie ID not found for the movie: {name}"
   


@tool(args_schema=GetCastDetailsInput)
def get_cast_details(id: str) -> str:
    """Get the cast details of the movie or the TV show from the ID"""
    url = "https://imdb8.p.rapidapi.com/title/get-top-cast"

    querystring = {"tconst": id}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    logger.debug(f"Inside the get_cast_details function")
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the cast for the movie with ID: {id}. Response text: {response.text}"
    else:
        logger.debug(f"Cast retrieved successfully")
    cast = response.json()
    ret = ""
    for actor_code in cast[:5]:
        url = "https://imdb8.p.rapidapi.com/actors/get-bio"
        logger.debug(f"Calling the get-bio endpoint for actor: {actor_code}")
        if response.status_code != 200:
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            logger.debug(f"Response body: {response.text}")
            return f"Not able to retrieve the bio for the actor with code: {actor_code}. Response text: {response.text}"
        querystring = {"nconst": actor_code.split("/")[2]}
        response = requests.get(url, headers=headers, params=querystring)
        actor_bio = response.json()
        ret += f"""Actor Name: {actor_bio['name']}\n"""
        first_mini_bio = (
            actor_bio["miniBios"][0]["text"] if actor_bio["miniBios"] else None
        )
        if first_mini_bio:
            ret += f"""Actor Mini-Bio: {first_mini_bio}\n"""
            ret += "------------------------------------------------------\n"
        else:
            pass
    logger.debug(f"Returning the cast details succesfully")
    return ret


@tool(args_schema=GetRatingInput)
def get_rating(id: str) -> str:
    """Get the rating of the movie or the TV show from the ID"""

    url = "https://imdb8.p.rapidapi.com/title/get-ratings"

    querystring = {"tconst": id}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the rating for the movie with ID: {id}. Response text: {response.text}"
    else:
        logger.debug(f"Rating retrieved successfully")
    data = response.json()
    output = ""

    # Extract the title, rating, and ratingCount
    title = data["title"]
    rating = data["rating"]
    rating_count = data["ratingCount"]

    # Append the title, rating, and ratingCount to the output string
    output += f"Title: {title}\n"
    output += f"Rating: {rating}\n"
    output += f"Rating Count: {rating_count}\n"

    # Append each demographic and their ratings to the output string
    for demographic, details in data["ratingsHistograms"].items():
        output += f"\n{demographic}:\n"
        output += f"  Aggregate Rating: {details['aggregateRating']}\n"
        # output += f"  Histogram:\n"
        # for rating_value, count in details['histogram'].items():
        #     output += f"    {rating_value}: {count}\n"

    # Print the entire output string
    logger.debug(f"Returning the rating details succesfully")
    return output


@tool(args_schema=GetAwardsInput)
def get_awards(id: str) -> str:
    """Get the awards of the movie or the TV show from the ID"""

    url = "https://imdb8.p.rapidapi.com/title/get-awards-summary"
    headers = get_headers()
    querystring = {"tconst": id}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the awards for the movie with ID: {id}. Response text: {response.text}"
    data = response.json()
    summary = ""

    # Extract the title, year, and highlighted award information
    title = data["title"]
    year = data["year"]
    highlighted_award = data["awardsSummary"]["highlighted"]["awardName"]
    highlighted_award_count = data["awardsSummary"]["highlighted"]["count"]
    highlighted_award_is_winner = (
        "Winner" if data["awardsSummary"]["highlighted"]["isWinner"] else "Nominated"
    )

    # Append the title, year, and highlighted award information to the summary string
    summary += f"Title: {title}\n"
    summary += f"Year: {year}\n"
    summary += (
        f"Highlighted Award: {highlighted_award} ({highlighted_award_count} times)\n"
    )
    summary += f"Status: {highlighted_award_is_winner}\n"

    # Append the other nominations and wins count to the summary string
    summary += (
        f"Other Nominations Count: {data['awardsSummary']['otherNominationsCount']}\n"
    )
    summary += f"Other Wins Count: {data['awardsSummary']['otherWinsCount']}\n"

    # Append the highlighted ranking information to the summary string
    summary += f"Highlighted Ranking: {data['highlightedRanking']['label']} (Rank: {data['highlightedRanking']['rank']})\n"
    logger.debug(f"Returning the awards details succesfully")
    return summary


@tool(args_schema=GetPlotInput)
def get_plot(id: str) -> str:
    """Get the plot of the movie or the TV show from the ID"""

    url = "https://imdb8.p.rapidapi.com/title/get-plots"
    headers = get_headers()
    querystring = {"tconst": id}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the plot for the movie with ID: {id}. Response text: {response.text}"
    data = response.json()
    # Initialize an empty string to hold the formatted output
    plots_summary = ""

    # Iterate over the plots and append each plot's text to the summary string
    for plot in data["plots"][:5]:
        plots_summary += plot["text"] + "\n\n"
    logger.debug(f"Returning the plot details succesfully")
    return plots_summary  # Return the formatted output
