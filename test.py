from player.Character import Character
from model.game_functions import get_location, get_map
from ollama import chat
from ollama import ChatResponse

c = Character("Skye", 100, 25, 20, 20, 15, 10, 10, 100, 20, [], {})

def call_game_function(function_name: str, *args, **kwargs):
    game_functions = {
        'get_location': get_location,
        'get_map': get_map,
        'get_stat': c.get_stat, 
        'set_stat': c.set_stat,
    }
    if function := game_functions.get(function_name):
        return function(*args, **kwargs)
    else:
        raise ValueError(f"Function {function_name} not found in game functions.")

messages = [{'role': 'user', 'content': 'What is my current gold?'}]

response: ChatResponse = chat(
    'llama3.2',
    messages=messages
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if tool.function.name in ['get_location', 'get_map']:
            try:
                output = call_game_function(tool.function.name, **tool.function.arguments)
                print('Function output:', output)
            except Exception as e:
                print('Error calling game function:', e)
else:
    print('No tool calls returned from model')

if response.message.tool_calls:
    messages.append(response.message)
    messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})
    final_response = chat('llama3.2', messages=messages)
    print('Final response:', final_response.message.content)
else:
    print('No tool calls returned from model')