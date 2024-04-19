from database_functions import *
import config


def get_sql_query_response(function_args: dict) -> str:
    try:
        query = function_args['query']
        print(f'Generated SQL Query -> {query}')
        rows = execute_function_call(query)
        if rows == '' or len(rows) == 0:
            return "Politely reply that you don't have the answer for the question."
        else:
            return rows
    except Exception as e:
        print(f'Error at get_sql_query_response -> {e}.')
        return config.ERROR_MESSAGE


available_functions = {
    "get_sql_query_response": get_sql_query_response
}
