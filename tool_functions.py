from datetime import datetime

from database_functions import *
import config


def get_sql_query_response(function_args: dict) -> str:
    try:
        query = function_args['query']
        print(f'Generated SQL Query -> {query}')
        rows = run_execute_database_query(query)
        if rows == '':
            failed_sql_query_response = """Politely reply that you don't have the answer for the question. \
# Instructions: \
# 1. Do not mention any other courses details."""
            return {
                'status': True,
                'response': failed_sql_query_response
            }
        else:
            sql_query_response = f"""Explain PostgreSQL data in natural language, \
            
# Parameters: \
# - SQL data: {rows}

# Instructions: \
# 1. Keep the response short and concise and never mention id of the PostgreSQL database. \
# 2. If needed consider today's date as {datetime.datetime.now().strftime("%b %d, %Y")}. \
# 3. If there is a course URL in the SQL data then use "https://www.netcomlearning.com/" to provide it in the answer otherwise don't mention the URL in the awnser. \
# 4. Never mention that you are reading information from a SQL Database."""
            return {
                'status': True,
                'response': sql_query_response
            }
    except Exception as e:
        print(f'Error at get_sql_query_response -> {e}.')
        return {
            'status': False,
            'response': config.ERROR_MESSAGE
        }


available_functions = {
    "get_sql_query_response": get_sql_query_response
}
