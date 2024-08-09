from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import PIL.Image
import google.generativeai as genai
import io
import re
import base64
import json
from decouple import config


GEMINI_API_KEY = config('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


@csrf_exempt
def get_artists_name_with_similar_work(request):
    """
    Handles POST requests to generate artist names with similar artworks based on the provided image.

    This view function expects a POST request with a JSON payload containing a base64 encoded image URL. 
    It decodes the image, uses a generative model to get artist names with similar artworks, and returns 
    these names as a JSON response.

    The JSON payload should have the following format:
    {
        "image_base64_url": "<base64_encoded_image>"
    }

    Example Request:
    POST /get-artists/
    Content-Type: application/json

    {
        "image_base64_url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
    }

    Example Success Response:
    {
        "artists": [
            "Antonio Canova - Known for his neoclassical style and sculptures of angels.",
            "Bertel Thorvaldsen - Known for his neoclassical style and sculptures of mythological figures."
        ]
    }

    HTTP Status Codes:
        - 200 OK: Successfully processed the image and returned artist names.
        - 400 Bad Request: No image_base64_url provided or other client-side errors.
        - 405 Method Not Allowed: Invalid request method (only POST is allowed).
        - 500 Internal Server Error: If an exception occurs during processing.
    """
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            base64_url = data.get('image_base64_url')
            prompt = data.get('prompt')
            
            if not base64_url:
                return JsonResponse({'error': 'No image_base64_url provided'}, status=400)

            # Extract the base64 string from the URL
            base64_string = base64_url.split(',')[1]

            # Decode the base64 string to binary data
            image_data = base64.b64decode(base64_string)

            # Create a BytesIO object from the binary data
            image_io = io.BytesIO(image_data)

            # Open the image with PIL from the BytesIO object
            img = PIL.Image.open(image_io)

            # Generate content using the image
            response = model.generate_content([prompt, img])
            response_text = response._result.candidates[0].content.parts[0].text

            # Extract artist names and descriptions
            artists = response_text.replace("*","").split("\n")
            # Return extracted artist names as JSON
            return JsonResponse({'artists': artists})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)