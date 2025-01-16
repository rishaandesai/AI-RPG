from ollama import chat


'''
Example of streaming:
from ollama import generate


for part in generate('llama3.2', 'Why is the sky blue?', stream=True):
  print(part['response'], end='', flush=True)
'''

messages = []

while True:
  user_input = input('Chat with history: ')
  response = chat(
    'llama3.2',
    messages=messages
    + [
      {'role': 'user', 'content': user_input},
    ],
    stream=True
  )
  s = ''
  for part in chat('llama3.2', messages=messages, stream=True):
    print(part['message']['content'], end='', flush=True)
    s += part['message']['content']

  messages += [
    {'role': 'user', 'content': user_input},
    {'role': 'assistant', 'content': s},
  ]



