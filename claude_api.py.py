from datetime import datetime
from database_functions import *
from tool_functions import *
from tools import *
import anthropic

import config

client = anthropic.Anthropic(
    api_key=config.CLOUDE_API_KEY
)


tools = [
    {

        "name": "get_sql_query_response",
        "description": "Use this function to answer user questions about Production data. Input should be a fully formed MySQL query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""MySQL query extracting info to answer the user's question. \
MySQL should be written using this database schema: \
{get_database_schema_string()} \
The query should be returned in plain text, not in JSON. \
Use today's date {datetime.now()}. \
Don't assume any column names that are not in the database schema, use the \
following data definitions instead: \
{get_database_definitions()}"""
                }
            },
            "required": ["query"],
        },

    }
]


def chat_completion(messages: list[dict[str, str]]) -> str:
    response = client.beta.tools.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=messages,
        tools=tools
    )
    if len(response.content) > 1:
        tool_call = response.content[1]
        function_name = tool_call.name
        function_id = tool_call.id
        function_to_call = available_functions[function_name]
        function_args = tool_call.input
        function_response = function_to_call(function_args)
        messages.append(
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": response.content[0].text
                    },
                    {
                        "type": "tool_use",
                        "id": function_id,
                        "name": function_name,
                        "input": function_args
                    }
                ]
            }
        )
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": function_id,
                        "content": f'Here is the response {function_response}, please format this in natural language.'
                    }
                ]
            }
        )
        print(messages)
        second_response = client.beta.tools.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=messages,
            tools=tools
        )
        return second_response.content[0].text
    else:
        return response.content[0].text
