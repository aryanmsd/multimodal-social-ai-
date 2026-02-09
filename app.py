import streamlit as st
from utils.image_analyzer import ImageAnalyzer
from utils.content_generator import ContentGenerator
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Social Media Generator", layout="wide")

st.title("🎨 AI-Powered Social Media Content Generator")
st.markdown("Upload an image and generate platform-specific captions with **Google Gemini AI**!")

# Initialize components
@st.cache_resource
def init_components():
    analyzer = ImageAnalyzer()
    generator = ContentGenerator()
    return analyzer, generator

analyzer, generator = init_components()

# Sidebar for options
st.sidebar.header("⚙️ Configuration")
platform = st.sidebar.selectbox(
    "Select Platform",
    ["Instagram", "Twitter", "LinkedIn", "Facebook"]
)
tone = st.sidebar.selectbox(
    "Select Tone",
    ["Professional", "Casual", "Humorous", "Inspirational", "Promotional"]
)

# Add info about Gemini
st.sidebar.markdown("---")
st.sidebar.info("🤖 Powered by Google Gemini 1.5 Flash")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("🚫 Image too large. Please upload under 5MB.")
        st.stop()

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=None)

with col2:
    st.subheader("✨ Generated Content")
    
    if uploaded_file and st.button("🚀 Generate Content", type="primary"):
        
        # Step 1: Analyze image
        with st.spinner("🔍 Analyzing image with Gemini AI..."):
            try:
                analysis = analyzer.analyze_image(uploaded_file)
                with st.expander("📊 Image Analysis", expanded=True):
                    st.markdown(analysis)
            except Exception as e:
                st.error(f"Error analyzing image: {str(e)}")
                st.stop()
        
        # Step 2: Generate caption
        with st.spinner(f"✍️ Generating {platform} caption..."):
            try:
                caption = generator.generate_caption(analysis, platform, tone)
                
                st.markdown("### 📝 Generated Caption")
                st.success(caption)
                
                # Copy button functionality
                st.code(caption, language=None)
                
            except Exception as e:
                st.error(f"Error generating caption: {str(e)}")
                st.stop()
        
        # Step 3: Generate AI image prompt (optional)
        if st.checkbox("🎨 Generate AI Image Prompt"):
            with st.spinner("Creating image generation prompt..."):
                try:
                    image_prompt = generator.generate_image_prompt(
                        analysis, 
                        style="vibrant, social media ready, high quality"
                    )
                    
                    st.markdown("### 🖼️ AI Image Generation Prompt")
                    st.info(image_prompt)
                    st.caption("Use this prompt in DALL-E, Midjourney, or Stable Diffusion")
                    
                    st.code(image_prompt, language=None)
                    
                except Exception as e:
                    st.error(f"Error generating image prompt: {str(e)}")

# Footer with features
st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Features")
st.sidebar.markdown("✅ Multi-platform support")
st.sidebar.markdown("✅ AI image analysis (Gemini Vision)")
st.sidebar.markdown("✅ Smart caption generation")
st.sidebar.markdown("✅ Multiple tone options")
st.sidebar.markdown("✅ AI image prompt creator")

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Get Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. **Upload Image**: Choose any product, scene, or photo
    3. **Select Platform**: Choose your target social media platform
    4. **Choose Tone**: Pick the mood for your post
    5. **Generate**: Click the button and get your content!
    
    **Tip**: You can generate multiple captions by changing platform/tone and clicking generate again!
    """)

# Sample images section
st.markdown("---")
st.markdown("### 💡 Try These Sample Use Cases")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**Product Launch**")
    st.caption("Upload product images for launch announcements")

with col_b:
    st.markdown("**Travel Content**")
    st.caption("Create engaging posts from travel photos")

with col_c:
    st.markdown("**Food & Lifestyle**")
    st.caption("Generate appetizing food descriptions")