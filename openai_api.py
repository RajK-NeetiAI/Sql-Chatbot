import json

from openai import OpenAI

import config
from tools import *
from tool_functions import *
from database_functions import *

client = OpenAI(api_key=config.OPENAI_API_KEY)

tools = get_sql_tool(
    get_database_schema_string(),
    get_database_definitions()
)


def chat_completion(query: str, messages: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model=config.GPT_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(function_args)
            insert_new_row(
                query, function_args['query'], function_response['response'], function_response['status'])
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response['response'],
                }
            )
        second_response = client.chat.completions.create(
            model=config.GPT_MODEL,
            messages=messages,
        )
        return second_response.choices[0].message.content
    else:
        return response_message.content
