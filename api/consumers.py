import json
from channels.generic.websocket import AsyncWebsocketConsumer
import google.generativeai as genai 
from decouple import config

GEMINI_API_KEY = config('GEMINI_API_KEY')


genai.configure(api_key=GEMINI_API_KEY)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling chat interactions using the Generative AI model.

    This WebSocket consumer manages chat sessions by receiving user messages, generating responses
    using a generative AI model, and sending responses back to the client. It maintains a chat history
    for context in the conversation.

    Methods:
        connect: Handles the WebSocket connection and initializes chat history.
        receive: Receives messages from the WebSocket, processes them using the generative AI model,
                updates chat history, and sends responses back to the client.
    """
    async def connect(self):
        """
        Handles the WebSocket connection event.

        This method accepts the WebSocket connection and initializes the chat history.

        WebSocket events:
            - Accepts the connection.
            - Initializes the chat history list.
        """
        # Accept the connection
        await self.accept()

        # Initialize the chat history
        self.history = []

    async def receive(self, text_data):
        """
        Handles incoming WebSocket messages.

        This method receives a message from the WebSocket, processes it using the generative AI model,
        updates the chat history, and sends the response back to the client.

        Args:
            text_data (str): The message received from the WebSocket as a JSON string.

        WebSocket events:
            - Receives and parses the message from the WebSocket.
            - Generates a response using the Generative AI model.
            - Updates the chat history with the user message and the generated response.
            - Sends the response back to the WebSocket client.

        Responses:
            - On success: Sends back the generated response and the user message.
            - On error: Sends back an error message if an exception occurs during processing.
        """
        try:
            # Receive a message from the WebSocket
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')

            # Initialize the model with the current history
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=self.history)


            # Set up generation configurations
            generation_config = genai.types.GenerationConfig(
                candidate_count=1,  # Only one response candidate
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