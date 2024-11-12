
import streamlit as st
from utils import load_api_key, create_qa_prompt_template, instantiate_openai_model, initialize_qa_chain, create_embeddings, ask_question, load_config
import warnings
warnings.filterwarnings("ignore")

# Load configuration and initialize components
config = load_config("config.yaml")
instruction_text = config['instruction_text']
db = create_embeddings()
api_key = load_api_key()
qa_prompt_template = create_qa_prompt_template(instruction_text)
llm = instantiate_openai_model(api_key)
chain = initialize_qa_chain(llm, qa_prompt_template)

# Set up Streamlit app with custom title and header
st.set_page_config(page_title="Claim Verification - Ask a Question")
# Dark Blush Color
st.markdown("<h1 style='border-bottom: 2px solid #9b1b30; padding-bottom: 10px; color: #9b1b30;'>Claim Verification - Ask a Question</h1>", unsafe_allow_html=True)


# Black Color
# st.markdown("<h1 style='border-bottom: 2px solid #000000; padding-bottom: 10px; color: #000000;'>Claim Verification - Ask a Question</h1>", unsafe_allow_html=True)

# Stretchable text area for user question
user_question = st.text_area("Enter your question:", height=150)

# Add submit button
if st.button("Ask"):
    if user_question.strip():  # Check if the input is not empty
        response = ask_question(db, chain, user_question, num_references=1)
        st.markdown("### Answer:")
        st.markdown(f"<div style='padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>{response}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a question before submitting.")
