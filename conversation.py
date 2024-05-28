from openai_api import chat_completion
import config


def format_chat_history(chat_history: list[list]) -> list[list]:
    formated_chat_history = [
        {"role": "system", "content": "Consider yourself as a helpful data analyst Netcome Learning. \
You help user get information about the data and answer their questions."}
    ]
    for ch in chat_history:
        formated_chat_history.append({
            'role': 'user',
            'content': ch[0]
        })
        if ch[1] == None:
            pass
        else:
            formated_chat_history.append({
                'role': 'assistant',
                'content': ch[1]
            })
    return formated_chat_history


def handle_chat_completion(chat_history: list[list]) -> list[list]:
    try:
        query = chat_history[-1][0]
        print(f'User query -> {query}')
        formated_chat_history = format_chat_history(chat_history)
        response = chat_completion(query, formated_chat_history)
        print(f'Chatbot respons -> {response}')
        chat_history[-1][1] = response
        return chat_history
    except:
        chat_history[-1][1] = config.ERROR_MESSAGE
        return chat_history


def handle_user_query(message: str, chat_history: list[tuple]) -> tuple:
    chat_history += [[message, None]]
    return '', chat_history
