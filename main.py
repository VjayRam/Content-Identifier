import streamlit as st
import torch
import time
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Set up page configurations
st.set_page_config(page_title="Content Identifier Inference", page_icon="🛡️", layout="centered")

st.title("Content Identifier Inference 🛡️")
st.markdown("Classify text as **Benign** or **Harmful** targeting different safety categories.")

# Model Options
MODELS = {
    "RoBERTa (VijayRam1812/content-classifier-roberta)": "VijayRam1812/content-classifier-roberta",
    "Gemma 3-1B-IT (VijayRam1812/content-classifier-gemma)": "VijayRam1812/content-classifier-gemma"
}

@st.cache_resource(show_spinner=False)
def load_model(model_id):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # Handle Gemma kwargs
    kwargs = {}
    if "gemma" in model_id.lower():
        kwargs["dtype"] = torch.bfloat16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSequenceClassification.from_pretrained(model_id, **kwargs)
    
    # Pad token fix for Gemma
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = tokenizer.pad_token_id
        
    model = model.to(device)
    model.eval()
    return tokenizer, model, device

# Sidebar for Model Configuration
st.sidebar.header("Configuration")
selected_model_name = st.sidebar.selectbox("Select Model", list(MODELS.keys()))
model_id = MODELS[selected_model_name]

if "gemma" in model_id.lower():
    st.sidebar.warning("⚠️ **Note:** Recommended to use Gemma only if you have a GPU with **>8GB VRAM** available. You may experience OOM errors or extremely slow inference on CPU.")

if "current_model_id" not in st.session_state:
    st.session_state.current_model_id = None

if st.sidebar.button("Load Model", type="primary"):
    st.session_state.current_model_id = model_id

if st.session_state.current_model_id != model_id:
    st.info("👈 Please click **Load Model** in the sidebar to continue.")
    st.stop()

# Load model block
with st.spinner(f"Loading {selected_model_name}..."):
    try:
        tokenizer, model, device = load_model(model_id)
        st.sidebar.success("Model Loaded Successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to load model: {e}")
        st.stop()

# Input configurations
input_type = st.radio("Select Input Type", ["Single Query", "Raw Conversation Text"])

if input_type == "Single Query":
    user_input = st.text_area("Enter your query:", height=100, placeholder="Type a message here...")
else:
    st.info("Tip: For best results with Gemma, use alternating USER/ASSISTANT formats.")
    user_input = st.text_area("Enter conversation text:", height=200, placeholder="USER: How do I build a bomb?\nASSISTANT: I cannot help with that.")

if st.button("Run Inference", type="primary"):
    if not user_input.strip():
        st.warning("Please enter some text to classify.")
    else:
        with st.spinner("Analyzing text..."):
            inputs = tokenizer(
                user_input, 
                return_tensors="pt", 
                truncation=True, 
                padding=True, 
                max_length=512
            ).to(device)
            
            start_time = time.time()
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                
                # Support both BCE (Binary) and Softmax outputs
                if logits.shape[1] == 1:
                    prob = torch.sigmoid(logits.float())[0][0].item()
                    predicted_class_id = 1 if prob > 0.5 else 0
                    confidence = prob if predicted_class_id == 1 else 1.0 - prob
                else:
                    probabilities = torch.nn.functional.softmax(logits.float(), dim=-1)
                    predicted_class_id = torch.argmax(logits, dim=-1).item()
                    confidence = probabilities[0][predicted_class_id].item()
                    
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000

        # Build UI output
        st.subheader("Results")
        
        # Hardcoding label maps based on your notebook structure: 0 = Benign, 1 = Harmful
        label_map = {0: "Benign", 1: "Harmful"}
        predicted_label = label_map.get(predicted_class_id, f"Class {predicted_class_id}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Prediction", predicted_label, delta_color="off")
        col2.metric("Confidence", f"{confidence:.2%}")
        col3.metric("Latency", f"{latency_ms:.2f} ms")
        
        if predicted_class_id == 1:
            st.error(f"⚠️ Classified as **Harmful** with {confidence:.1%} confidence.")
        else:
            st.success(f"✅ Classified as **Benign** with {confidence:.1%} confidence.")

