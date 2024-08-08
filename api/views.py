# import os
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import google.generativeai as genai
# import json

# # Configure the API key
# genai.configure(api_key="AIzaSyDROuVe8O5uxXpWe-n7BySIw9qt-3MZGpM")

# @csrf_exempt
# def chatbot(request):
#     if request.method == 'POST':
#         try:
#             # Parse the request body to get the message
#             body = json.loads(request.body.decode('utf-8'))
#             message = body.get('message', '')

#             if not message:
#                 return JsonResponse({'error': 'Message is required'}, status=400)

#             # Initialize the model
#             model = genai.GenerativeModel('gemini-1.5-flash')
#             chat = model.start_chat(history=[])

#             # Send the message to the model
#             response = chat.send_message(message)

#             # Extract the response content
#             answer = response._result.candidates[0].content.parts[0].text

#             # Return the response as JSON
#             return JsonResponse({'answer': answer}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# import google.generativeai as genai

# genai.configure(api_key="AIzaSyDROuVe8O5uxXpWe-n7BySIw9qt-3MZGpM")


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Accept the connection
#         await self.accept()

#         # Initialize the chat history
#         self.history = []

#     async def receive(self, text_data):
#         # Receive a message from the WebSocket
#         text_data_json = json.loads(text_data)
#         message = text_data_json.get('message', '')

#         # Initialize the model with the current history
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         chat = model.start_chat(history=self.history)

#         # Send the message to the model
#         response = chat.send_message(message)
#         answer = response._result.candidates[0].content.parts[0].text

#         # Update the history with the new message and response
#         self.history.append({'user': message, 'bot': answer})

#         # Send the explanation back to the WebSocket client
#         await self.send(text_data=json.dumps({
#             'answer': answer
#         }))
