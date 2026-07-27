# be server start cheyyali

# python -
# uvicorn -- python third party lib which is used to create
# be server
# fastapi---to build apis in be


# pip install fastapi uvicorn
# pip install uvicorn


# pip install langchain
# pip install langchain-Core
# pip install pypdf
# pip install python-multipart
# pip install sentence-transformers
# pip install langchain-community
# pip install langchain-chroma
# pip install langchain_text_splitters
# pip install langchain-huggingface
# pip install langchain-groq


from fastapi import FastAPI, File, UploadFile  # import FastAPI

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma

from langchain_groq import ChatGroq


# creating FastAPI object
fast_api_obj = FastAPI()


# creating ChatGroq LLM object
llm = ChatGroq(

    # paste your Groq API key here
    api_key="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",

    # selecting the Groq model
    model="llama-3.3-70b-versatile"
)


# creating POST API endpoint
@fast_api_obj.post("/anylyse_resume")
async def resume_taker(resume: UploadFile = File(...)):

    # getting uploaded resume file name
    file_name = resume.filename  # ashrith.pdf


    # saving uploaded resume into local system
    with open(file_name, "wb") as f:

        f.write(await resume.read())


    # checking file content type
    # print(resume.content_type)


    # loading PDF file using PyPDFLoader
    loader = PyPDFLoader(file_name)


    # loading PDF documents
    # one PDF can contain multiple pages
    docs = loader.load()


    # creating text splitter
    splitter = RecursiveCharacterTextSplitter(

        # each chunk contains maximum 700 characters
        chunk_size=700,

        # overlapping 150 characters between chunks
        chunk_overlap=150
    )


    # splitting PDF documents into small chunks
    chunks = splitter.split_documents(docs)


    # creating embedding model
    e_model = HuggingFaceEmbeddings(

        # converting text into numerical vectors
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    # storing document chunks as vectors in ChromaDB
    vector_db = Chroma.from_documents(

        # PDF chunks
        documents=chunks,

        # embedding model
        embedding=e_model,

        # ChromaDB folder
        persist_directory="./chroma_folder"
    )


    # retrieving similar documents from ChromaDB
    # similarity_search is used for retrieving relevant information

    r_docs = vector_db.similarity_search(

        # query for searching relevant resume content
        query="analyze resume and give pros and cons",

        # retrieving top 5 similar documents
        k=5
    )


    # creating context from retrieved documents
    context = "\n\n".join(

        # getting page content from every document
        [d.page_content for d in r_docs]
    )


    # creating prompt with context
    prompt = f"""

    You are an expert HR recruiter.

    Analyze the following resume and provide:

    1. Candidate Summary
    2. Technical Skills
    3. Projects
    4. Strengths
    5. Weaknesses
    6. Suggested Job Roles
    7. Resume Score out of 10

    Resume:
    --------

    {context}

    """


    # calling ChatGroq LLM
    # sending prompt to LLM for response generation

    response = llm.invoke(prompt)


    # returning AI generated response to frontend
    return {

        # response.content contains actual AI answer
        "msg": response.content
    }


# @fast_api_obj.post("/get_students_data")


# Run backend server:

# python -m uvicorn be:fast_api_obj --reload