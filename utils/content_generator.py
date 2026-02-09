import google.generativeai as genai
import os

class ContentGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_caption(self, image_analysis, platform, tone):
        """Generate social media caption based on image analysis"""
        platform_guidelines = {
            "Instagram": "engaging, hashtag-friendly, 150-200 characters, visually focused",
            "Twitter": "concise, witty, under 280 characters, punchy",
            "LinkedIn": "professional, informative, 100-150 words, value-driven",
            "Facebook": "conversational, story-driven, 100-200 words, relatable"
        }
        
        prompt = f"""Based on this image analysis:
        
        {image_analysis}
        
        Create a {tone.lower()} social media caption for {platform}.
        
        Guidelines for {platform}: {platform_guidelines[platform]}
        
        The caption should include:
        - An attention-grabbing opening
        - The key message about the image
        - A clear call-to-action
        - 3-5 relevant hashtags
        
        Make it {tone.lower()} in tone and optimized for {platform}.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_image_prompt(self, description, style="vibrant social media"):
        """Generate an image generation prompt based on description"""
        prompt = f"""Based on this description:
        {description}
        
        Create a detailed image generation prompt for AI image generators (like DALL-E, Midjourney, Stable Diffusion).
        
        The prompt should:
        - Be specific and descriptive
        - Include art style: {style}
        - Specify mood and lighting
        - Be optimized for social media (1:1 or 16:9 ratio)
        - Be professional and visually appealing
        
        Provide only the image prompt, nothing else."""
        
        response = self.model.generate_content(prompt)
        return response.text