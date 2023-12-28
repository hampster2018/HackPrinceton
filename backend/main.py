# run this file with 'uvicorn main:app --reload'
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from pydantic import BaseModel
from typing import Dict
import os
import json

# load_dotenv()


class Message(BaseModel):
    question: str
    answer: str


embeddings = None
openai_model = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
extractor = None


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield
#     print("Exiting lifespan...")


app = FastAPI()
# app = FastAPI(lifespan=lifespan)
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello_world():
    return {"Hello": "World"}


@app.get("/get_textbooks")
async def get_textbooks():
    textbooks_held = os.listdir("./textbooks")
    textbooks = []
    for textbook in textbooks_held:
        if textbook != ".gitignore":
            textbooks.append(textbook[:-4])
    return {"textbooks": textbooks}


# make a chat_textbook route that takes in a textbook name, topic, and Messages object and returns a chatbot response
@app.post("/chat_textbook")
async def chat_textbook(textbook_name: str, messages: list[Message]):
    global embeddings
    if embeddings is None:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    textbook_path = "./textbookdbs/" + textbook_name + ".faiss"

    db = FAISS.load_local(textbook_path, embeddings=embeddings)

    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    qa_llm = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
    )

    prompt = messages[-1].question

    output = qa_llm({"query": prompt})

    return {"answer": output["result"]}


# make route to upload textbook and create embeddings (in background)
@app.post("/upload_textbook")
async def upload_textbook(file: UploadFile, background_tasks: BackgroundTasks):
    from create_embeddings import process_textbook

    global embeddings
    if not os.path.exists("./textbooks/" + file.filename):
        print("Textbook already exists!")
        with open("./textbooks/" + file.filename, "wb") as buffer:
            buffer.write(file.file.read())
    if (
        not os.path.exists("./textbookdbs/" + file.filename[:-4] + ".faiss")
        or not os.path.exists("./textbooktxts/" + file.filename[:-4] + ".txt")
        or not os.path.exists("./textbooktopics/" + file.filename[:-4] + ".json")
        or not os.path.exists("./textbookgraphs/" + file.filename[:-4] + ".json")
    ):
        background_tasks.add_task(
            process_textbook,
            file.filename[:-4],
            embeddings=embeddings,
            extractor=extractor,
        )
    return {"filename": file.filename}


@app.get("/get_topic_nodes")
async def get_topic_nodes(textbook_name: str):
    """
    THIS IS FUNCTIONALLY DEPRECATED!
    """
    with open("./textbooktopics/" + textbook_name + ".json", "r") as f:
        topics = json.load(f)
    return {"topics": topics}


@app.get("/get_textbook_graph")
async def get_textbook_graph(textbook_name: str):
    """
    This function returns the textbook graph for the given textbook name.
    The graph is in the form: {"nodes": [], "edges": []} where each node is of the form
    {"id": int, "label": str, "group": int, "completed": bool} and each edge is of the form
    """
    with open("./textbookgraphs/" + textbook_name + ".json", "r") as f:
        graph: dict = json.load(f)
    return graph


@app.post("/update_completion")
async def update_completion(textbook_name: str, node_id: int):
    with open("./textbookgraphs/" + textbook_name + ".json", "r") as f:
        graph: dict = json.load(f)
    for node in graph["nodes"]:
        if node["id"] == node_id:
            node["completed"] = True
    with open("./textbookgraphs/" + textbook_name + ".json", "w") as f:
        f.write(json.dumps(graph))
    return {"success": True}


@app.post("/update_completion_all")
async def update_completion_all(textbook_name: str):
    with open("./textbookgraphs/" + textbook_name + ".json", "r") as f:
        graph: dict = json.load(f)
    for node in graph["nodes"]:
        node["completed"] = True
    with open("./textbookgraphs/" + textbook_name + ".json", "w") as f:
        f.write(json.dumps(graph))
    return {"success": True}


@app.get("/topic_summary")
async def topic_summary(textbook_name: str, topic: str):
    global embeddings
    if embeddings is None:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    textbook_path = "./textbookdbs/" + textbook_name + ".faiss"

    db = FAISS.load_local(textbook_path, embeddings=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    PROMPT = PromptTemplate(
        template="""Use the following pieces of context to summarize the topic the user will give. You will not respond to the user or speak as if you are a chatbot. You are only to send the summary.

{context}

Topic to summarize: {question}
Answer as if you are a STEM textbook:""",
        input_variables=["context", "question"],
    )
    chain_type_kwargs = {"prompt": PROMPT}
    qa_llm = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, chain_type_kwargs=chain_type_kwargs
    )

    output = qa_llm({"query": topic})

    return {"answer": output["result"]}


# make an api route to send the textbook files to the frontend
@app.get("/get_textbook_files")
async def get_textbook_files(textbook_name: str):
    with open("./textbooks/" + textbook_name + ".pdf", "rb") as f:
        pdf = f.read()
    return {"pdf": pdf}
