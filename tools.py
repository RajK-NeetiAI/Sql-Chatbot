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
                            "description": f'''Generate a PostgreSQL query to extract information based on a user's question. \
                        
# Parameters: \
- Database Schema: {database_schema_string} \
- Current Date: Use today's date as {datetime.now()} where needed in the query. \

# Instructions: \
- Construct an SQL query using only the tables and columns listed in the provided schema. \
- Ensure the query avoids assumptions about non-existent columns. \
- Consider performance and security best practices, such as avoiding SQL injection risks. \
- Format the query in plain text for direct execution in a PostgreSQL database. \
- When you select fields, make sure to reference the table to avoid ambiguity. \

# Example Query: \
# If the user asks for the number of employees in each department, the query should look like this: \
# "SELECT department_id, COUNT(*) FROM employees GROUP BY department_id;"'''
                        }
                    },
                    "required": ["query"],
                },
            }
        }
    ]

    return tools
