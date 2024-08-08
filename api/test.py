# import os
# import google.generativeai as genai

# # Access your API key as an environment variable.
# genai.configure(api_key="AIzaSyDROuVe8O5uxXpWe-n7BySIw9qt-3MZGpM")
# # Choose a model that's appropriate for your use case.
# model = genai.GenerativeModel('gemini-1.5-flash')

# prompt = "Write a story about a magic backpack."

# response = model.generate_content(prompt)

# print( response._result.candidates[0].content.parts[0].text)


import os
import google.generativeai as genai 

genai.configure(api_key="AIzaSyAcB5yKvXm68cPzCCpLqJyGYcvX5XLLNVg")


model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

response = chat.send_message(
    'In one sentence, explain how a computer works to a young child.')


print(response._result.candidates[0].content.parts[0].text)

# response = chat.send_message(
#     'Okay, how about a more detailed explanation to a high schooler?')




# response = chat.send_message(
#     'Okay, how about a more detailed explanation to a high schooler?')

# print(response.text)