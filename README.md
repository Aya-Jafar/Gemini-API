# 🌟 Gemini API 🌟

This project is a Django-based chatbot and rest-api application that uses Django Channels for real-time WebSocket communication and Google Generative AI for generating chat responses in addition to an endpoint for generating text based on image input using Gemini API.

## Setup Instructions

Follow these steps to set up the project environment and run the server:

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/Aya-Jafar/Gemini-API.git
cd your-repository
```

### 2. Create a virtual environment

Creating a virtual environment isolates your project dependencies. Use the following commands based on your operating system:

```bash
python3 -m venv env
```

### 3. Activate the Virtual Environment

Activate the virtual environment with the following commands:

##### On macOS/Linux:

```bash
source env/bin/activate
```

##### On Windows:

```bash
source env\Scripts\activate
```

### 4. Install the Required Packages

With the virtual environment activated, install the necessary Python packages from requirements.txt:

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

With the virtual environment activated, install the necessary Python packages from requirements.txt:

```bash
DJANGO_SECRET_KEY=your_project_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

### 6. Run the Daphne Server

In a new terminal window, start the Daphne server for WebSocket support:

```bash
daphne Gemini_API.asgi:application
```

### Happy coding! 🚀
