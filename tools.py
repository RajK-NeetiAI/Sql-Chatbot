from datetime import datetime


def get_sql_tool(database_schema_string: str, database_definitions: str) -> list[dict]:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_sql_query_response",
                "description": "Use this function to answer user questions about Production data. Input should be a fully formed MySQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""MySQL query extracting info to answer the user's question. \
MySQL should be written using this database schema: \
{database_schema_string} \
The query should be returned in plain text, not in JSON. \
Use today's date {datetime.now()}. \
Don't assume any column names that are not in the database schema, use the \
following data definitions instead: \
{database_definitions}"""
                        }
                    },
                    "required": ["query"],
                },
            }
        }
    ]

    return tools
