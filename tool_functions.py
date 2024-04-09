from database_functions import *


def get_sql_query_response(function_args: dict) -> str:
    query = function_args['query']
    print(f'Generated SQL Query -> {query}')
    rows = execute_function_call(query)
    if rows == '':
        return "Politely reply that you don't have the answer for the question."
    else:
        return rows

available_functions = {
    "get_sql_query_response": get_sql_query_response
}
