import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import time

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

if "vector" not in st.session_state:
    st.session_state.embeddings = OpenAIEmbeddings()
    st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs = st.session_state.loader.load()

    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])

    st.session_state.vectordb = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("ChatGroq Demo")
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="Gemma-7b-It",
    temperature=0)

prompt = ChatPromptTemplate.from_template(
"""
Answer the following questions based on the provided context only.
Please provide the answer based on the question
<conetnt>
{context}
<context>

Question: {input}
"""
)

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = st.session_state.vectordb.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

prompt = st.text_input("Input your prompt here")

if prompt:
    start_time = time.process_time()
    response = retrieval_chain.invoke({"input": prompt})
    end_time = time.process_time()
    st.write(f"Time taken: {end_time - start_time} seconds")
    st.write(response["answer"])

    # Withe streamlit expander

    with st.expander("Document Similarity Search"):
        # Find relevant document chuncks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-" * 100)


