import warnings
from utils import load_api_key, create_qa_prompt_template, instantiate_openai_model, initialize_qa_chain, create_embeddings, ask_question, load_config

warnings.filterwarnings("ignore")

config = load_config("config.yaml")
instruction_text = config['instruction_text']
db = create_embeddings()
api_key = load_api_key()
qa_prompt_template = create_qa_prompt_template(instruction_text)
llm = instantiate_openai_model(api_key)
chain = initialize_qa_chain(llm, qa_prompt_template)
user_question = input("Please enter your question: ")
response = ask_question(db, chain, user_question, num_references=1)
print(response)