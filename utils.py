from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import streamlit as st
from langchain_pinecone import PineconeVectorStore
from langchain.vectorstores import Pinecone as pic
from langchain.embeddings import OpenAIEmbeddings
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os

load_dotenv()
api_key = os.getenv("openai_api_key")
pinecone_key = os.getenv("PINECONE_API_KEY")

client = OpenAI(api_key=api_key)

def speech_to_text(audio_data):
    try:
        with open(audio_data, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                response_format="text",
                file=audio_file
            )
        return transcript, None        
    except Exception as e:
        return None, str(e)
    
def query_to_id(query, content_type):

    if content_type == "tv_show":
        namespace = "tv shows"
    else:
        namespace = "movies"

    embeddings = OpenAIEmbeddings()
    vector_store = PineconeVectorStore(
        pic.get_pinecone_index("bot"),
        embedding=embeddings,
        namespace=namespace
    )

    results = vector_store.similarity_search(query, k=16)
    ids = ','.join(result.metadata['unique_id'] for result in results)

    # ids = ''
    # for result in results:
    #     ids += result.metadata['unique_id']
    #     if result != results[-1]:
    #         ids += ','
    return ids    

def rag_bot(query):
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    
    
    
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    rag_chain.invoke(query)
    
def rag_chain():

    llm = ChatOpenAI(
        openai_api_key='',
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    qa.run(query)

    
