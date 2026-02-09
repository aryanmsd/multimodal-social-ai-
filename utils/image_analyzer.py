import google.generativeai as genai
import os
from PIL import Image
import io

def resize_image(image, max_size=(512, 512)):
    image = image.convert("RGB")
    image.thumbnail(max_size)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=70)
    buffer.seek(0)
    return Image.open(buffer)

class ImageAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

    def analyze_image(self, image_file):
        """
        image_file = uploaded file from Streamlit (not path)
        """

        # Resize BEFORE sending to Gemini
        img = Image.open(image_file)
        img = resize_image(img)

        prompt = """
Analyze this image and return:
1. Main subject
2. Colors and mood
3. Background/setting
4. Key visual elements
5. Best social media tone

Keep the response concise and structured.
"""

        response = self.model.generate_content([prompt, img])
        return response.text
