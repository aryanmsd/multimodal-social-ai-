import streamlit as st
from utils.image_analyzer import ImageAnalyzer
from utils.content_generator import ContentGenerator
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="AI Social Media Generator", layout="wide")

st.title("🎨 AI-Powered Social Media Content Generator")
st.markdown(
    "Upload an image and generate **platform-specific captions** and "
    "**AI image prompts** using Google Gemini."
)

# -----------------------------
# Session State Initialization
# -----------------------------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "caption" not in st.session_state:
    st.session_state.caption = None

if "image_prompt" not in st.session_state:
    st.session_state.image_prompt = None

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
st.sidebar.info("🤖 Powered by Google Gemini")

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
        st.image(image, caption="Uploaded Image", use_container_width=True)

# -----------------------------
# Column 2: Generated content
# -----------------------------
with col2:
    st.subheader("✨ Generated Content")

    # -------- Generate analysis + caption --------
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

        # Reset old prompt when regenerating
        st.session_state.image_prompt = None

    # -------- Display analysis --------
    if st.session_state.analysis:
        with st.expander("📊 Image Analysis", expanded=True):
            st.markdown(st.session_state.analysis)

    # -------- Display caption --------
    if st.session_state.caption:
        st.markdown("### 📝 Generated Caption")
        st.success(st.session_state.caption)
        st.code(st.session_state.caption)

    # ===============================
    # Image Prompt Generation (Option 1)
    # ===============================
    if st.session_state.analysis:
        st.markdown("---")
        generate_prompt = st.checkbox("🎨 Generate AI Image Prompt for this post")

        if generate_prompt:
            with st.spinner("🧠 Generating AI image prompt..."):
                try:
                    st.session_state.image_prompt = generator.generate_image_prompt(
                        description=st.session_state.analysis,
                        style="high-quality social media image, professional, vibrant, detailed"
                    )
                except Exception as e:
                    st.error(f"Error generating image prompt: {e}")

    # -------- Display image prompt --------
    if st.session_state.image_prompt:
        st.markdown("### 🖼️ AI Image Prompt")
        st.info(st.session_state.image_prompt)
        st.code(st.session_state.image_prompt)
        st.caption(
            "💡 Use this prompt in DALL·E, Midjourney, Stable Diffusion, Leonardo AI, etc."
        )

# -----------------------------
# Footer / Help
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Features")
st.sidebar.markdown("✅ Image understanding (Gemini Vision)")
st.sidebar.markdown("✅ Platform-specific captions")
st.sidebar.markdown("✅ AI image prompt generation")
st.sidebar.markdown("✅ Stable multimodal pipeline")

with st.expander("📖 How to Use"):
    st.markdown("""
    1. Upload an image (under 5MB)
    2. Select platform and tone
    3. Click **Generate Content**
    4. Optionally generate an AI image prompt

    This app demonstrates **image → text → image-prompt** multimodal AI.
    """)
