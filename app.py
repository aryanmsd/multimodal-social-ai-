import streamlit as st
from utils.image_analyzer import ImageAnalyzer
from utils.content_generator import ContentGenerator
from utils.image_generator import generate_image
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="AI Social Media Generator", layout="wide")

st.title("🎨 AI-Powered Social Media Content Generator")
st.markdown(
    "Upload an image and generate **captions + AI-generated images** using Google Gemini and Stable Diffusion."
)

# -----------------------------
# Session State Initialization
# -----------------------------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "caption" not in st.session_state:
    st.session_state.caption = None

# -----------------------------
# Initialize components
# -----------------------------
@st.cache_resource
def init_components():
    analyzer = ImageAnalyzer()
    generator = ContentGenerator()
    return analyzer, generator

analyzer, generator = init_components()

# -----------------------------
# Sidebar configuration
# -----------------------------
st.sidebar.header("⚙️ Configuration")

platform = st.sidebar.selectbox(
    "Select Platform",
    ["Instagram", "Twitter", "LinkedIn", "Facebook"]
)

tone = st.sidebar.selectbox(
    "Select Tone",
    ["Professional", "Casual", "Humorous", "Inspirational", "Promotional"]
)

st.sidebar.markdown("---")
st.sidebar.info("🤖 Powered by Google Gemini + Stable Diffusion")

# -----------------------------
# Main layout
# -----------------------------
col1, col2 = st.columns(2)

# -----------------------------
# Column 1: Image upload
# -----------------------------
with col1:
    st.subheader("📤 Upload Image")

    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("🚫 Image too large. Please upload an image under 5MB.")
            st.stop()

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

# -----------------------------
# Column 2: Generated content
# -----------------------------
with col2:
    st.subheader("✨ Generated Content")

    # -------- Button: Generate text content --------
    if uploaded_file and st.button("🚀 Generate Content", type="primary"):

        # Step 1: Analyze image
        with st.spinner("🔍 Analyzing image with Gemini Vision..."):
            try:
                st.session_state.analysis = analyzer.analyze_image(uploaded_file)
            except Exception as e:
                st.error(f"Error analyzing image: {e}")
                st.stop()

        # Step 2: Generate caption
        with st.spinner(f"✍️ Generating {platform} caption..."):
            try:
                st.session_state.caption = generator.generate_caption(
                    st.session_state.analysis,
                    platform,
                    tone
                )
            except Exception as e:
                st.error(f"Error generating caption: {e}")
                st.stop()

    # -------- Display stored analysis --------
    if st.session_state.analysis:
        with st.expander("📊 Image Analysis", expanded=True):
            st.markdown(st.session_state.analysis)

    # -------- Display stored caption --------
    if st.session_state.caption:
        st.markdown("### 📝 Generated Caption")
        st.success(st.session_state.caption)
        st.code(st.session_state.caption)

    # ===============================
    # STEP 4: Checkbox (outside button)
    # ===============================
    if st.session_state.analysis:
        st.markdown("---")
        generate_ai_image = st.checkbox("🎨 Generate AI Image for this post")

        # ===============================
        # STEP 5: Generate AI Image
        # ===============================
        if generate_ai_image:
            with st.spinner("🎨 Generating AI image for social media..."):
                try:
                    image_prompt = generator.generate_image_prompt(
                        description=st.session_state.analysis,
                        style="high-quality social media post, vibrant, professional"
                    )

                    ai_image = generate_image(image_prompt)

                    st.markdown("### 🖼️ AI Generated Image")
                    st.image(ai_image, width=True)

                except Exception as e:
                    st.error(f"Image generation failed: {e}")

# -----------------------------
# Footer / Help
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Features")
st.sidebar.markdown("✅ Image understanding (Gemini Vision)")
st.sidebar.markdown("✅ Platform-specific captions")
st.sidebar.markdown("✅ AI image generation (Stable Diffusion)")
st.sidebar.markdown("✅ True multimodal AI pipeline")

with st.expander("📖 How to Use"):
    st.markdown("""
    1. Upload an image (under 5MB)
    2. Select platform and tone
    3. Click **Generate Content**
    4. Optionally generate an AI image for the post

    This app demonstrates **image → text → image** multimodal AI.
    """)
