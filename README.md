# IMDb Chatbot

## Overview

This project is an IMDb chatbot that interacts with the IMDb (Internet Movie Database) API to provide information about movies and TV shows. Users can ask questions about movies or TV shows, and the chatbot will retrieve and present relevant information from the IMDb database.

## Features

- **Information Extraction**: Uses the IMDb API to fetch detailed information about movies and TV shows.
- **Natural Language Processing**: Understands user queries and extracts relevant information.
- **Text Summarization**: Provides concise summaries of movie or TV show information.
- **Tagging**: Categorizes movies or TV shows based on user queries.
- **Interactive Interface**: Offers a conversational interface through Streamlit.

## Getting Started

### Prerequisites

- Python  3.x
- IMDb API access
- Streamlit for the web application interface

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/imdb-chatbot.git
   ```
2. Navigate to the project directory:
   ```
   cd imdb-chatbot
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   X-RapidAPI-Key=your_rapid_api_key
   X-RapidAPI-Host=rapid-api-host
   ```

### Running the Application

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Access the chatbot in your web browser at `http://localhost:8501`.

## Usage

Once the application is running, you can interact with the IMDb chatbot by typing queries related to movies or TV shows. The chatbot will respond with information retrieved from the IMDb database.
To extract Imdb data, I am using this rapidapi : https://rapidapi.com/apidojo/api/imdb8/

## Contact

Your Name - jayant.duneja@colorado.edu
