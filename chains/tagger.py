from operator import itemgetter
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from schema.schema import UserIntent
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain_core.messages import BaseMessage, AIMessage


class Tagger:
    """
    A class responsible for tagging and extracting important information from user input.

    Attributes:
        api_key (str): The API key used for authentication with the OpenAI API.
        prompt (ChatPromptTemplate): An instance of ChatPromptTemplate that defines the conversation prompt.
        functions (list): A list of functions converted to OpenAI format for use in the GPT-3 model.
        model (ChatOpenAI): An instance of ChatOpenAI that handles the interaction with the GPT-3 model.
        conversation_buffer (ConversationBufferMemory): A buffer for storing conversation history.
        parser (PydanticOutputFunctionsParser): A parser for parsing the output from the GPT-3 model.
        chain (Chain): A chain of operations to perform on the user input.
    """

    def __init__(self, api_key) -> None:
        """
        Initializes the Tagger with the given API key and sets up the necessary components for tagging and information extraction.

        Args:
            api_key (str): The API key used for authentication with the OpenAI API.
        """
        self.api_key = api_key
        self.session_id = "tagger"
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful ai that can tag and extract important information from the user's input. 
                    In case the user has not clearly mentioned about a movie, use the previous messages saved in the memory for context.
                    """,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("user", "{input}"),
            ]
        )
        self.store = {}
        self.functions = [convert_pydantic_to_openai_function(UserIntent)]

        self.model = ChatOpenAI(
            api_key=self.api_key, temperature=0.0, model="gpt-3.5-turbo-1106"
        ).bind(functions=self.functions)
        # gpt-3.5-turbo-1106 context window: 16,385t / output: 4,096t

        self.parser = PydanticOutputFunctionsParser(
            pydantic_schema={"UserIntent": UserIntent}
        )

        self.runnable = (
            self.prompt
            | self.model
            | self.parser
        )

    def extract_information(self, input: str) -> UserIntent:
        """
        Extracts the name of the movie and the intent from the user's input using the GPT-3 model.

        Args:
            input (str): The user's input string.

        Returns:
            UserIntent: An object containing the extracted name and intent from the user's input.
        """
        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in self.store:
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]

        self.chain = RunnableWithMessageHistory(
            self.runnable,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        intent: UserIntent = self.chain.invoke(
            {
                "input": f"Exract the name of the movie and the intent from the user's input.  {input}",},
                # config={"configurable": {"session_id": self.session_id}, 'callbacks': [ConsoleCallbackHandler()]}
                config={"configurable": {"session_id": self.session_id}}
        )
        self.store[self.session_id].add_message(AIMessage(content=f"User wants to know about the movie {intent.name} and wants to talk about the {intent.intent}."))
        return intent
