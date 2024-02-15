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

    url = 'https://imdb146.p.rapidapi.com/v1/find/'
    headers = get_headers()
    querystring = {"query":name}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        # Find the first item with an 'id' key and break the loop
        for item in data['titleResults']['results']:
            if 'id' in item:
                movie_id = item['id']
                break
        logger.debug(f"Movie ID was succesfully retrieved. Movie ID: {movie_id}")
        return movie_id
    except Exception as e:
        logger.debug(f"Not able to find the movie ID for the movie: {name}")
        logger.debug(f"Error: {e}")
        return f"Movie ID not found for the movie: {name}"

@tool(args_schema=GetCastDetailsInput)
def get_cast_details(id: str) -> str:
    """Get the cast details of the movie or the TV show from the ID"""
    url = "https://imdb146.p.rapidapi.com/v1/title/"

    querystring = {"id": id}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    print(response.json()['cast'])
    logger.debug(f"Inside the get_cast_details function")
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the cast for the movie with ID: {id}. Response text: {response.text}"
    else:
        logger.debug(f"Cast retrieved successfully")
    cast = response.json()['cast']
    ret = ""
    for edge in cast['edges']:
        ret += f"""Actor Name: {edge['node']['name']['nameText']['text']}\n"""
        ret += "------------------------------------------------------\n"
    logger.debug(f"Returning the cast details succesfully")
    return ret


# @tool(args_schema=GetRatingInput)
# def get_rating(id: str) -> str:
#     """Get the rating of the movie or the TV show from the ID"""

#     url = "https://imdb-com.p.rapidapi.com/title/ratings"

#     querystring = {"tconst": id}
#     headers = get_headers()
#     response = requests.get(url, headers=headers, params=querystring)
#     if response.status_code != 200:
#         logger.debug(f"Response status code: {response.status_code}")
#         logger.debug(f"Response headers: {response.headers}")
#         logger.debug(f"Response body: {response.text}")
#         return f"Not able to retrieve the rating for the movie with ID: {id}. Response text: {response.text}"
#     else:
#         logger.debug(f"Rating retrieved successfully")
#     data = response.json()
#     aggregate_rating = data['data']['entityMetadata']['ratingsSummary']['aggregateRating']
    
#     # Initialize the summary string
#     summary = f"Aggregate Rating: {aggregate_rating}\n\n"
    
#     # Check if histogramData exists
#     if 'histogramData' in data['data']['entityMetadata']:
#         # Extract the histogram data
#         histogram_data = data['data']['entityMetadata']['histogramData']
        
#         # Extract the country-specific ratings
#         country_ratings = histogram_data['countryData']
        
#         # Add country-specific ratings to the summary
#         summary += "Country-specific Ratings:\n"
#         for country_rating in country_ratings:
#             summary += f"{country_rating['displayText']}: {country_rating['aggregateRating']} (Votes: {country_rating['totalVoteCount']})\n"
        
#         # Extract the histogram values
#         histogram_values = histogram_data['histogramValues']
        
#         # Add histogram values to the summary
#         summary += "\nHistogram Values:\n"
#         for histogram_value in histogram_values:
#             summary += f"Rating: {histogram_value['rating']} (Votes: {histogram_value['formattedVoteCount']})\n"
#     # Print the entire output string
#     logger.debug(f"Returning the rating details succesfully")
#     return summary


@tool(args_schema=GetAwardsInput)
def get_awards(id: str) -> str:
    """Get the awards of the movie or the TV show from the ID"""

    url = "https://imdb146.p.rapidapi.com/v1/title/"

    querystring = {"id": id}
    headers = get_headers()
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the awards for the movie with ID: {id}. Response text: {response.text}"
    data = response.json()
    print(data['wins'])
    print(data['nominations'])
    print(data['prestigiousAwardSummary'])
    # Create a summary string
    summary = f"Total Nominations: {data['wins']['total']}\n" \
          f"Total Awards: {data['wins']['total']}\n" \
          f"Number of Wins: {data['prestigiousAwardSummary']['wins']}\n" \
          f"Last Prestigious Award: {data['prestigiousAwardSummary']['award']['text']} (ID: {data['prestigiousAwardSummary']['award']['id']})"
    logger.debug(f"Returning the awards details succesfully")
    return summary
    # # Extract the title, year, and highlighted award information
    # title = data["title"]
    # year = data["year"]
    # highlighted_award = data["awardsSummary"]["highlighted"]["awardName"]
    # highlighted_award_count = data["awardsSummary"]["highlighted"]["count"]
    # highlighted_award_is_winner = (
    #     "Winner" if data["awardsSummary"]["highlighted"]["isWinner"] else "Nominated"
    # )

    # # Append the title, year, and highlighted award information to the summary string
    # summary += f"Title: {title}\n"
    # summary += f"Year: {year}\n"
    # summary += (
    #     f"Highlighted Award: {highlighted_award} ({highlighted_award_count} times)\n"
    # )
    # summary += f"Status: {highlighted_award_is_winner}\n"

    # # Append the other nominations and wins count to the summary string
    # summary += (
    #     f"Other Nominations Count: {data['awardsSummary']['otherNominationsCount']}\n"
    # )
    # summary += f"Other Wins Count: {data['awardsSummary']['otherWinsCount']}\n"

    # # Append the highlighted ranking information to the summary string
    # summary += f"Highlighted Ranking: {data['highlightedRanking']['label']} (Rank: {data['highlightedRanking']['rank']})\n"
    


@tool(args_schema=GetPlotInput)
def get_plot(id: str) -> str:
    """Get the plot of the movie or the TV show from the ID"""

    url = "https://imdb146.p.rapidapi.com/v1/title/"
    headers = get_headers()
    querystring = {"id": id}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response body: {response.text}")
        return f"Not able to retrieve the plot for the movie with ID: {id}. Response text: {response.text}"
    data = response.json()['plot']
    # Initialize an empty string to hold the formatted output
    plots_summary = response.json()['plot']['plotText']['plainText']

    # # Iterate over the plots and append each plot's text to the summary string
    # for plot in data["plots"][:5]:
    #     plots_summary += plot["text"] + "\n\n"
    logger.debug(f"Returning the plot details succesfully")
    return plots_summary  # Return the formatted output
