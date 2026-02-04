import ollama 
import streamlit as st
import io 
from PIL import Image


st.set_page_config(page_title="Ollama OCR", layout="wide")

_, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear"):
        if 'ocr_results' in st.session_state:
            del st.session_state['ocr_results']
        st.rerun()
st.title("Ollama OCR")
st.markdown("---")


        

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
_,center,_ = st.columns(3)
with center:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image')
    else:
        # Display default image
        try:
            default_image = Image.open("demo.jpg")
            st.image(default_image, caption='Default Image (Upload an image to extract Content)', width  = 400 )
        except FileNotFoundError:
            st.info("Upload an image to get started.")

if st.button("Extract Content"):
    with st.spinner('Extracting Content...'):
        try:
            # Use uploaded file if available, otherwise use default image
            if uploaded_file is not None:
                image_data = uploaded_file.getvalue()
            else:
                try:
                    with open("demo.jpg", "rb") as f:
                        image_data = f.read()
                except FileNotFoundError:
                    st.error("Default image not found. Please upload an image.")
                    image_data = None
            
            if image_data is not None:
                response = ollama.chat(
                    model='qwen3-vl:2b',
                    messages=[{
                        'role': 'user',
                        'content': """Analyze the text in the provided image. Extract all readable content
                                        and present it in a structured Markdown format that is clear, concise, 
                                        and well-organized. Ensure proper formatting (e.g., headings, lists, or
                                        code blocks) as necessary to represent the content effectively.""",
                        'images': [image_data]
                    }]
                )
                st.session_state['ocr_results'] = response.message.content
        except Exception as e:
            st.error(f"An error occurred: {e}")
                    
if 'ocr_results' in st.session_state:
    st.subheader("Extracted Content")
    st.code(st.session_state['ocr_results'], wrap_lines =True)
    st.markdown("---")
