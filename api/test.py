# import os
import google.generativeai as genai 
import os
import PIL.Image
import re
import PIL 
import io
import base64
import requests

genai.configure(api_key="AIzaSyCaSmIPJ5GabW5hwsDDBmPyUFFiz6hmSnE")
model = genai.GenerativeModel('gemini-1.5-flash')



def test_chatbot():
    chat = model.start_chat(history=[])

    response = chat.send_message(
        'In one sentence, explain how a computer works to a young child.')

    print(response._result.candidates[0].content.parts[0].text)



# Open the image file
organ = PIL.Image.open("./test.jpg")

def generate_text_from_image(image):
    response = model.generate_content(["Give me artist names with similar artworks for this image", organ])
    response = response._result.candidates[0].content.parts[0].text


    pattern = re.compile(r'\*\*([^\*]+?)\:\*\*')
    artists = pattern.findall(response)

    # Print extracted artist names
    for artist in artists:
        print(artist)

# generate_text_from_image(organ)



# Open the image file and convert to base64
image_path = "./test.jpg"

with open(image_path, "rb") as image_file:
    # Read and encode the image to base64
    image_data = image_file.read()
    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    base64_url = f"data:image/jpeg;base64,{base64_encoded}"


def generate_text_from_image(base64_url):
    # Extract the base64 string from the URL
    base64_string = base64_url.split(',')[1]

    # Decode the base64 string to binary data
    image_data = base64.b64decode(base64_string)

    # Save the binary data to a file
    with open("imageToSave.png", "wb") as fh:
        fh.write(image_data)


    organ = PIL.Image.open("./imageToSave.png")

    # Generate content using the image base64 URL
    response = model.generate_content(["Give me artist names with similar artworks for this image", organ])
    response_text = response._result.candidates[0].content.parts[0].text

    # Print response text
    print("Response Text:", response_text)

    # Extract artist names from the response
    pattern = re.compile(r'\*\*([^\*]+?)\:\*\*')
    artists = pattern.findall(response_text)

    # Print extracted artist names
    for artist in artists:
        print(artist)


# generate_text_from_image(base64_url)

def request_api():
    # Define the URL of the Django endpoint
    url = "http://localhost:8000/get-artists/"

    # Load an image and encode it to base64
    image_path = "test.jpg"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
        base64_url = f"data:image/jpeg;base64,{base64_encoded}"

    # Create the JSON payload with the base64 URL
    payload = {
        "image_base64_url": base64_url,
        "prompt":"Give me artist names with similar artworks for this image"
    }

    # Make the POST request to the Django endpoint
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response JSON (artist names)
        print("Artists:", response.json())
    else:
        # Print the error message
        print("Error:", response.json().get('error'))


request_api()