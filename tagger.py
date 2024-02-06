from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from schema import UserIntent

class Tagger:
    
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful ai that can tag and extract important information from the user's input. 
                    """,
                ),
                ("user", "{input}"),
            ]
        )

        self.functions = [
            convert_pydantic_to_openai_function(UserIntent)
        ]

        self.model = ChatOpenAI(
            api_key=self.api_key, temperature=0.0, model="gpt-3.5-turbo-1106"
        ).bind(
            functions=self.functions
        )  
        #gpt-3.5-turbo-1106 context window: 16,385t / output: 4,096t

        self.parser = PydanticOutputFunctionsParser(
            pydantic_schema={"UserIntent": UserIntent}
        )

        self.chain = self.prompt | self.model | self.parser
    
    def extract_information(self, input: str) -> UserIntent:
        intent : UserIntent = self.chain.invoke(
            {"input": f"Exract the name of the movie and the intent from the user's input.  {input}"}
        )
        return intent