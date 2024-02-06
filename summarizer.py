from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
class Summarizer:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful ai that can answer user's question based on the context provided. 
                    """,
                ),
                ("user", "{input}"),
            ]
        )
        self.model = ChatOpenAI(
            api_key=self.api_key, temperature=0.0, model="gpt-3.5-turbo-1106"
        ) 
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.model | self.output_parser
    
    def summarize(self, context: str, question : str) -> str:
        response : str = self.chain.invoke(
            {"input": f""" Context : {context} Question : {question}"""}
        )
        return response