
# import streamlit as st
# from utils import load_api_key, create_qa_prompt_template, instantiate_openai_model, initialize_qa_chain, create_embeddings, ask_question, load_config
# import warnings
# warnings.filterwarnings("ignore")

# # Load configuration and initialize components
# config = load_config("config.yaml")
# instruction_text = config['instruction_text']
# db = create_embeddings()
# api_key = load_api_key()
# qa_prompt_template = create_qa_prompt_template(instruction_text)
# llm = instantiate_openai_model(api_key)
# chain = initialize_qa_chain(llm, qa_prompt_template)

# # Set up Streamlit app with custom title and header
# st.set_page_config(page_title="Claim Verification - Ask a Question")
# # Dark Blush Color
# st.markdown("<h1 style='border-bottom: 2px solid #9b1b30; padding-bottom: 10px; color: #9b1b30;'>Claim Verification - Ask a Question</h1>", unsafe_allow_html=True)

# # Sidebar with instruction box
# st.sidebar.markdown(
#     """
#     **Instructions:**

#     Please enter your question in the following format:
#     *Patient's disease/symptoms, doctor's prescription, test, medicine.*

#     Example: 
#     "Patient has a fever, doctor prescribed Paracetamol, test: Blood test, medicine: 500mg Paracetamol"
#     """
# )

# # Stretchable text area for user question
# user_question = st.text_area("Enter your question:", height=150)

# # Add submit button
# if st.button("Ask"):
#     if user_question.strip():  # Check if the input is not empty
#         response = ask_question(db, chain, user_question, num_references=1)
#         st.markdown("### Answer:")
#         st.markdown(f"<div style='padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>{response}</div>", unsafe_allow_html=True)
#     else:
#         st.warning("Please enter a question before submitting.")





# import streamlit as st
# from utils import load_api_key, create_qa_prompt_template, instantiate_openai_model, initialize_qa_chain, create_embeddings, ask_question, load_config
# import warnings
# warnings.filterwarnings("ignore")

# # Load configuration and initialize components
# config = load_config("config.yaml")
# instruction_text = config['instruction_text']
# doctor_instruction_text = config['doctor_instruction_text']
# db = create_embeddings()
# api_key = load_api_key()
# qa_prompt_template = create_qa_prompt_template(instruction_text)
# llm = instantiate_openai_model(api_key)
# chain = initialize_qa_chain(llm, qa_prompt_template)

# # Set up Streamlit app with custom title and header
# st.set_page_config(page_title="Claim Verification - Ask a Question")

# # Sidebar for navigation between pages
# page = st.sidebar.radio("Select a Page", ["Claim Verification", "Virtual Doctor"])

# # Claim Verification page
# if page == "Claim Verification":
#     st.markdown("<h1 style='border-bottom: 2px solid #9b1b30; padding-bottom: 10px; color: #9b1b30;'>Claim Verification - Ask a Question</h1>", unsafe_allow_html=True)

#     # Stretchable text area for user question
#     user_question = st.text_area("Enter your question:", height=150)

#     # Add submit button
#     if st.button("Ask"):
#         if user_question.strip():  # Check if the input is not empty
#             response = ask_question(db, chain, user_question, num_references=1)
#             st.markdown("### Answer:")
#             st.markdown(f"<div style='padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>{response}</div>", unsafe_allow_html=True)
#         else:
#             st.warning("Please enter a question before submitting.")

# # Virtual Doctor page
# elif page == "Virtual Doctor":
#     # Use doctor instruction text for the virtual doctor page
#     doctor_qa_prompt_template = create_qa_prompt_template(doctor_instruction_text)
#     doctor_chain = initialize_qa_chain(llm, doctor_qa_prompt_template)

#     st.markdown("<h1 style='border-bottom: 2px solid #9b1b30; padding-bottom: 10px; color: #9b1b30;'>Virtual Doctor - Ask a Question</h1>", unsafe_allow_html=True)

#     # Stretchable text area for user question
#     user_question = st.text_area("Enter your health-related question:", height=150)

#     # Add submit button
#     if st.button("Ask"):
#         if user_question.strip():  # Check if the input is not empty
#             response = ask_question(db, doctor_chain, user_question, num_references=1)
#             st.markdown("### Answer:")
#             st.markdown(f"<div style='padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>{response}</div>", unsafe_allow_html=True)
#         else:
#             st.warning("Please enter a question before submitting.")




    
import streamlit as st
from streamlit_option_menu import option_menu
from utils import load_api_key, create_qa_prompt_template, instantiate_openai_model, initialize_qa_chain, create_embeddings, ask_question, load_config
import warnings
warnings.filterwarnings("ignore")

# Load configuration and initialize components
config = load_config("config.yaml")
instruction_text = config['instruction_text']
doctor_instruction_text = config['doctor_instruction_text']
db = create_embeddings()
api_key = load_api_key()
qa_prompt_template = create_qa_prompt_template(instruction_text)
llm = instantiate_openai_model(api_key)
chain = initialize_qa_chain(llm, qa_prompt_template)

# Set up Streamlit app with custom title and header
st.set_page_config(page_title="Claim Verification - Ask a Question")

# Sidebar with navigation buttons
with st.sidebar:
    selected_page = option_menu(
        "Explore",
        ["Virtual Doctor", "Claim Verification"],
        icons=["check2-circle", "stethoscope"],  # Add appropriate icons
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )

    # Instructions for the selected page
    if selected_page == "Virtual Doctor":
        st.markdown(
            """
            **Instructions:**
            Please describe the patient's disease, symptoms, and how long they have been experiencing these symptoms. 
            For example:
            - "The patient has been experiencing a headache for the past 3 days."
            - "Patient has a fever and cough for 2 days."
            """
        )
    elif selected_page == "Claim Verification":
        st.markdown(
            """
            **Instructions:**
            Please enter your question in the following format:
            *Patient's disease/symptoms, doctor's prescription, test, medicine.* 
            
            Example:
            - "Patient has a fever, doctor prescribed Paracetamol, test: Blood test, medicine: 500mg Paracetamol"
            """
        )

# Claim Verification page
if selected_page == "Virtual Doctor":
    # Use doctor instruction text for the virtual doctor page
    doctor_qa_prompt_template = create_qa_prompt_template(doctor_instruction_text)
    doctor_chain = initialize_qa_chain(llm, doctor_qa_prompt_template)

    st.markdown("<h1 style='border-bottom: 2px solid #9b1b30; padding-bottom: 10px; color: #9b1b30;'>Virtual Doctor - Ask a Question</h1>", unsafe_allow_html=True)

    # Stretchable text area for user question
    user_question = st.text_area("Enter your health-related question:", height=150)

    # Add submit button
    if st.button("Ask", key="virtual_doctor"):
        if user_question.strip():  # Check if the input is not empty
            response = ask_question(db, doctor_chain, user_question, num_references=1)
            st.markdown("### Answer:")
            st.markdown(f"<div style='padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a question before submitting.")
            
# Virtual Doctor page
elif selected_page == "Claim Verification":
    st.markdown("<h1 style='border-bottom: 2px solid #9b1b30; padding-bottom: 10px; color: #9b1b30;'>Claim Verification - Ask a Question</h1>", unsafe_allow_html=True)

    # Stretchable text area for user question
    user_question = st.text_area("Enter your question:", height=150)

    # Add submit button
    if st.button("Ask", key="claim_verification"):
        if user_question.strip():  # Check if the input is not empty
            response = ask_question(db, chain, user_question, num_references=1)
            st.markdown("### Answer:")
            st.markdown(f"<div style='padding: 10px; background-color: #f0f2f6; border-radius: 5px;'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a question before submitting.")



