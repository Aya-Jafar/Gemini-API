import json
from channels.generic.websocket import AsyncWebsocketConsumer
import google.generativeai as genai 
from decouple import config

GEMINI_API_KEY = config('GEMINI_API_KEY')


genai.configure(api_key=GEMINI_API_KEY)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Initialize the chat history
        self.history = []

    async def receive(self, text_data):
        try:
            # Receive a message from the WebSocket
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')

            # Initialize the model with the current history
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=self.history)

            # TODO: Add check for the "SAFETY" response 

            # Set up generation configurations
            generation_config = genai.types.GenerationConfig(
                candidate_count=1,  # Only one response candidate
                max_output_tokens=40,  # Limit the response length
                temperature=2.0,  # Control creativity (lower is less creative)
            )

            # Send the message to the model
            response = chat.send_message(message, generation_config=generation_config)
            answer = response._result.candidates[0].content.parts[0].text

            # Update the history with the new message and response
            self.history.append({'user': message, 'bot': answer})

            # Send the explanation back to the WebSocket client
            await self.send(text_data=json.dumps({
                'answer': answer,
                'message': message
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': 'An error occurred while processing your request.'
            }))