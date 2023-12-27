# necessary libraries imports
import os
from langchain.llms import GooglePalm
from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# import the key_caller function from the key caller file
from key_caller import call_key



load_dotenv()

# api key calling
api_key = call_key('C:\\Users\\BAB AL SAFA\\Desktop\\MINE\\Automated-Responder\\key.txt')

model = GooglePalm(google_api_key=api_key, temperature=0.5)


embeddings = HuggingFaceInstructEmbeddings(query_instruction='Represent the query for retrieval: ')
vectordb_path = 'faiss_index'

def vector_database():
    loader = CSVLoader(file_path='codebasics_faqs.csv', source_column='prompt', encoding='latin-1')
    data = loader.load()
    vectordb = FAISS.from_documents(documents=data, embedding=embeddings)
    vectordb.save_local(vectordb_path)

def getQAchain():
    vectordb = FAISS.load_local(vectordb_path, embeddings)

    #creating retriever to query the database
    retriever = vectordb.as_retriever(score_threshold=0.75)

    prompt_template = """
    Given the following context and a question, generate an answer based on this context only. 
    In the answer try to provide as much text as possible from 'response' section in the source document context without making any 
    assumptions. If the context is not found in the content, kindly state 'I don't know.'

    CONTEXT: {context}

    QUESTION: {question}
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=['context', 'question']
    )

    chain = RetrievalQA.from_chain_type(llm=model,
            chain_type="stuff",
            retriever=retriever,
            input_key="query",
            return_source_documents=True,
                                    chain_type_kwargs={"prompt": PROMPT})

    return chain



chain = getQAchain()
    