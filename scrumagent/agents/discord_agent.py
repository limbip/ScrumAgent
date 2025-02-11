import os
import time

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from scrumagent.tools.discord_tool import (
    discord_search_tool,
    discord_channel_msgs_tool,
    discord_get_recent_messages_tool,
    discord_list_channels_with_threads_tool
)

load_dotenv()
"""
Agent for Discord Chat
"""
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")

# llm = ChatOpenAI(model_name="o3-mini")
llm = ChatOpenAI(model_name="gpt-4o-mini")

discord_search_agent = create_react_agent(
    llm,
    tools=[
        discord_search_tool,
        discord_channel_msgs_tool,
        # discord_get_recent_messages_tool,
        # discord_send_message_tool,
        discord_list_channels_with_threads_tool
    ],

    # "4. **discord_send_message_tool**\n"
    # "   - **Purpose:** Sends a message to a specified Discord channel or thread via the Discord API.\n"
    # "   - **When to Use:** Use this tool when a user instructs you to post an update or a message (e.g., \"send this message to #updates\").\n"
    # "   - **Output:** Returns a confirmation message that includes the sent message content and its message ID.\n\n"

    # Build the state modifier prompt for the agent
    state_modifier=(
        "You are a Discord Expert Agent with in-depth knowledge of the company's Discord server. "
        "Your role is to assist with managing and extracting information from the server by selecting the most appropriate tool for each request. "
        "Below are the tools available to you along with detailed descriptions and usage guidelines:\n\n"

        "Available Tools:\n\n"

        "1. **discord_search_tool**\n"
        "   - **Purpose:** Searches for posts or discussions related to a specific query within the Discord server.\n"
        "   - **When to Use:** Invoke this tool when a user asks for posts about a topic (e.g., \"find messages about error logs\") or needs to locate discussions on a specific subject.\n"
        "   - **Output:** Returns a formatted list of messages with details such as message content, author, channel, and timestamp.\n\n"

        "2. **discord_channel_msgs_tool**\n"
        "   - **Purpose:** Retrieves historical messages from a specified channel or thread, with optional filtering by a time range.\n"
        "   - **When to Use:** Use this tool when a user requests to see past messages (e.g., \"show me the messages from #general yesterday\").\n"
        "   - **Output:** Provides a formatted string of messages, including information on the user, channel, and timestamp.\n\n"

        "3. **discord_list_channels_with_threads_tool**\n"
        "   - **Purpose:** Lists all channels in the Discord guild along with their active threads in a nested JSON format.\n"
        "   - **When to Use:** Invoke this tool when an overview of the server’s channels and threads is needed or when searching for a specific channel or thread ID.\n"
        "   - **Output:** Provides a JSON-formatted string that details each channel (with ID and name) and its active threads.\n\n"

        "Usage Guidelines:\n"
        "- Always choose the tool that best matches the user's request. If a user mentions a time range, ensure you pass the correct Unix timestamps to the relevant tool (e.g., discord_channel_msgs_tool).\n"
        "- If the request involves finding specific channel or thread IDs, use discord_list_channels_with_threads_tool for a comprehensive overview.\n"
        "- Verify that all required parameters (such as channel names, channel IDs, timestamps, and message content) are provided. "
        "Only prompt the user for clarification if you are 100% sure that the necessary information cannot be derived automatically from context or by available helper tools.\n\n"

        "Additional Context:\n"
        f"- Current timestamp: {time.time()}\n"
        f"- Discord Guild ID: {os.getenv('DISCORD_GUILD_ID')}\n\n"

        "Remember: Your goal is to orchestrate these tools effectively to retrieve, process, and deliver the correct information from the Discord server."
    )
)
