from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_db = FAISS.load_local(
    "supremecampus_faiss_index",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
) 

retriever = vector_db.as_retriever(search_kwargs={"k": 3})


from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyA6UpweMaEIRpnY7uLUZ4rOKWQsR6AchZU"

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    
)

from langchain.chains import RetrievalQA

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

query = "What is the Supreme Business Model?"
result = rag_chain.invoke({"query": query})

print(" Answer:", result["result"])

