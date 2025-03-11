import datetime
import os
import json
import time

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
You are an AI that interprets a natural-language timeframe in any language.
Output a JSON object with the following format:
{{"before": <offset_in_seconds>, "after": <offset_in_seconds>}}
- The offsets are relative to the current time (in seconds).
- If the timeframe corresponds to a single moment, set both "before" and "after" to 0.
- If the timeframe represents a range, set "before" to the offset for the more recent time and "after" to the offset for the older time.
Only output the JSON object without any additional text.
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
def interpret_timeframe_tool(raw_timeframe: str) -> str:
    """
    Use the LLM chain to parse a natural-language timeframe into a JSON object with relative offsets (in seconds).
    The offsets indicate the relative shift from the current time:
      - For a past timeframe (e.g. "last minute", "yesterday"), both offsets should be negative.
      - For a future timeframe (e.g. "next minute", "tomorrow"), both offsets should be positive.
    The code then adds these offsets to the current Unix timestamp to compute absolute timestamps.
    If parsing fails, it defaults to a range of 7 days:
      - For past queries: now and now - 7 days.
      - For future queries: now and now + 7 days.

    Args:
        raw_timeframe (str): A natural-language timeframe string to interpret.

    Returns:
        str: A JSON string in the format {"before": <unixtimestamp>, "after": <unixtimestamp>}.
    """
    current_time_iso = datetime.datetime.utcnow().isoformat()
    response = multi_lang_time_parser_chain.run(
        {"raw_timeframe": raw_timeframe, "current_time": current_time_iso}
    )
    # Define simple heuristics for past and future
    raw_lower = raw_timeframe.lower()
    past_keywords = ["ago", "last", "past", "previous", "yesterday"]
    future_keywords = ["next", "coming", "tomorrow", "later", "in "]
    is_past = any(kw in raw_lower for kw in past_keywords)
    is_future = any(kw in raw_lower for kw in future_keywords)

    try:
        result = json.loads(response)
        # Extract relative offsets in seconds
        before_offset = int(float(result.get("before", 0)))
        after_offset = int(float(result.get("after", 0)))

        # Enforce sign based on detected timeframe
        if is_past:
            if before_offset > 0:
                before_offset = -abs(before_offset)
            if after_offset > 0:
                after_offset = -abs(after_offset)
        elif is_future:
            if before_offset < 0:
                before_offset = abs(before_offset)
            if after_offset < 0:
                after_offset = abs(after_offset)

        now = time.time()
        absolute_before = int(now + before_offset)
        absolute_after = int(now + after_offset)
        absolute_result = {"before": absolute_after, "after": absolute_before}
        return json.dumps(absolute_result)
    except (ValueError, KeyError, json.JSONDecodeError):
        now = time.time()
        if is_past:
            fallback = {"before": int(now), "after": int(now - 7 * 24 * 3600)}
        elif is_future:
            fallback = {"before": int(now), "after": int(now + 7 * 24 * 3600)}
        else:
            # Default to past if uncertain
            fallback = {"before": int(now), "after": int(now - 7 * 24 * 3600)}
        return json.dumps(fallback)


@tool(parse_docstring=True)
def current_timestamp_tool() -> str:
    """
    Get the current timestamp as a string.

    Returns:
        str: The current timestamp.
    """
    return str(datetime.datetime.utcnow().timestamp())
