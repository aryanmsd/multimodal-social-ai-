import google.generativeai as genai
import os
from PIL import Image

class ImageAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_image(self, image_path):
        """Analyze image and extract key details using Gemini Vision"""
        # Load image
        img = Image.open(image_path)
        
        prompt = """Analyze this image in detail and provide:
        1. Main subject/product - what is the primary focus?
        2. Colors and mood - describe the color palette and emotional tone
        3. Setting/background - describe the environment
        4. Key visual elements - list important objects, people, or features
        5. Suggested tone for social media post - what tone would work best?
        
        Provide the analysis in a clear, structured format."""
        
        # Generate response
        response = self.model.generate_content([prompt, img])
        
        return response.text