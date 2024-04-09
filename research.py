import anthropic

import config

client = anthropic.Anthropic(
    api_key=config.CLOUDE_API_KEY
)

response = client.beta.tools.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    ],
    messages=[
        {"role": "user", "content": "What's the weather like in San Francisco?"}],
)
print(response)
