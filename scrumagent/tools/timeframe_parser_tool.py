import datetime
import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ---------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the OpenAI API key is available for the used libraries
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

multi_lang_time_parser_prompt = PromptTemplate(
    input_variables=["raw_timeframe", "current_time"],
    template="""
You are an AI that interprets a natural-language timeframe in any language...
(Output an ISO-8601 date with no extra text)
User timeframe: {raw_timeframe}
Current time: {current_time}
Answer:
"""
)

multi_lang_time_parser_chain = LLMChain(
    llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0),
    prompt=multi_lang_time_parser_prompt
)


@tool(parse_docstring=True)
def interpret_timeframe_tool(raw_timeframe: str, return_as_human_readable_string: bool = False) -> str:
    """
    Use the LLM chain to parse a timeframe and time strings into a timestamp.
    For example, "2 weeks ago", "last Monday" or "today" will be converted to a timestamp.
    If parsing fails, defaults to 7 days ago.
    Can also return the timestamp as a string.

    Args:
        raw_timeframe (str): A natural-language timeframe string to interpret.
        return_as_human_readable_string (bool, optional): Whether to return the timestamp as a human-readable string. Defaults to False.

    Returns:
        str: The timestamp of the interpreted timeframe.
    """
    iso_response = multi_lang_time_parser_chain.run(
        {"raw_timeframe": raw_timeframe, "current_time": datetime.datetime.utcnow().isoformat()})
    try:
        if return_as_human_readable_string:
            return iso_response
        return str(datetime.datetime.fromisoformat(iso_response).timestamp())
    except ValueError:
        if return_as_human_readable_string:
            return "7 days ago"
        return str((datetime.datetime.utcnow() - datetime.timedelta(days=7)).timestamp())


@tool(parse_docstring=True)
def current_timestamp_tool() -> str:
    """
    Get the current timestamp as a string.

    Returns:
        str: The current timestamp.
    """
    return str(datetime.datetime.utcnow().timestamp())
