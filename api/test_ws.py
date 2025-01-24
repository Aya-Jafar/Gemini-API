import websocket
import json

def on_message(ws, message):
    print(f"Message received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket connection established")
    ws.send(json.dumps({"message": "Hello from client!"}))

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://127.0.0.1:8001/ws/chatbot/",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
