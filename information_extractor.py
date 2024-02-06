from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from tools import get_id, get_cast_details, get_rating, get_awards, get_plot
from tools import GetAwardsInput, GetCastDetailsInput, GetRatingInput, GetPlotInput
from langchain.tools.render import format_tool_to_openai_function
from schema import UserIntent
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.agent import AgentFinish
class Information_Extractor:
    
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful ai designed to extract information about movies and TV shows.
                    """,
                ),
                ("user", "{input}"),
            ]
        )
        self.functions =  [format_tool_to_openai_function(f) for f in [get_cast_details, get_rating, get_awards, get_plot]]
        self.model = ChatOpenAI(
            api_key=self.api_key, temperature=0.0, model="gpt-3.5-turbo-1106"
        ).bind(
            functions=self.functions
        )  
        # self.output_parser = PydanticOutputFunctionsParser()
        self.chain = self.prompt | self.model | OpenAIFunctionsAgentOutputParser() | self.route
    
    def route(self, result):
        if isinstance(result, AgentFinish):
            return result.return_values['output']
        else:
            tools = {
                "get_plot": get_plot, 
                "get_cast_details": get_cast_details,
                "get_rating": get_rating,
                "get_awards": get_awards
            }
            return tools[result.tool].run(result.tool_input)
    
    def get_information(self, user_intent : UserIntent) -> str:
        movie_id : str = get_id(user_intent.name)
        input_query = f"I want to know about the movie with id {movie_id} and want to talk about the {user_intent.intent}."
        information : str = self.chain.invoke({"input" : input_query})
        return information
