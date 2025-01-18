from player.Character import Character
from model.game_functions import get_location, get_map
from ollama import chat

c = Character("Skye", 100, 25, 20, 20, 15, 10, 10, 100, 20, [], {})

game_functions = {
    'get_location': get_location,
    'get_map': get_map,
    'get_stat': c.get_stat,
    'set_stat': c.set_stat,
}

def call_game_function(function_name: str, *args, **kwargs):
    if function := game_functions.get(function_name):
        return function(*args, **kwargs)
    raise ValueError(f"Function {function_name} not found in game functions.")

messages = [{'role': 'user', 'content': 'What is my current gold?'}]
response = chat('llama3.2', messages=messages)

if tool_calls := response.message.tool_calls:
    for tool in tool_calls:
        try:
            output = call_game_function(tool.function.name, **tool.function.arguments)
            messages.extend([
                response.message,
                {'role': 'tool', 'content': str(output), 'name': tool.function.name}
            ])
            final_response = chat('llama3.2', messages=messages)
            print('Final response:', final_response.message.content)
        except Exception as e:
            print('Error calling game function:', e)
else:
    print('No tool calls returned from model')