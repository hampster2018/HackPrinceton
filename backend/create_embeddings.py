import os
from langchain.vectorstores import FAISS
from langchain.document_loaders import PDFMinerLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import json
from get_graph import get_graph_with_summaries
from get_topics import get_topics_textbook
import re

# load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def process_textbook(
    textbook_name: str,
    embeddings: OpenAIEmbeddings,
    extractor: any,
):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    if not os.path.exists("./textbooktxts/" + textbook_name + ".txt"):
        print("beginning pdf mining")
        pdf_doc = PDFMinerLoader("./textbooks/" + textbook_name + ".pdf").load()
        # save the single large document to a txt file
        with open(
            "./textbooktxts/" + textbook_name + ".txt", "w", encoding="utf-8"
        ) as f:
            # output = "".join(
            #     c
            #     for c in pdf_doc[0].page_content
            #     if (c.isalnum() or c in [" ", "\n", "\t", ".", ",", "?", "!", ":", ";"])
            # )
            output = re.sub(r"[^a-zA-Z0-9 \n\t.,?!:;]+", " ", pdf_doc[0].page_content)
            # output = pdf_doc[0].page_content
            pdf_text = output
            f.write(pdf_text)
        print("finished pdf mining")
        if os.path.exists("./textbookdbs/" + textbook_name + ".faiss"):
            return 1
        chunks = splitter.split_text(pdf_doc[0].page_content)
        list_of_documents: list[Document] = []

        for chunk in chunks:
            list_of_documents.append(Document(page_content=chunk))

        print("creating FAISS database")
        if embeddings is None:
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vector_store = FAISS.from_documents(list_of_documents, embedding=embeddings)
        vector_store.save_local("./textbookdbs/" + textbook_name + ".faiss")
        print("finished embedding creation")
    if not os.path.exists("./textbooktopics/" + textbook_name + ".json"):
        print("beginning topic extraction")
        topics = get_topics_textbook(
            "./textbooktxts/" + textbook_name + ".txt", extractor=extractor
        )
        with open("./textbooktopics/" + textbook_name + ".json", "w") as f:
            f.write(json.dumps(topics))
        print("finished topic extraction")

    # if we have all the files, we can go ahead and make the graph
    if not os.path.exists("./textbookgraphs/" + textbook_name + ".json"):
        print("beginning graph creation")
        graph = get_graph_with_summaries("./textbooktopics/" + textbook_name + ".json")
        with open("./textbookgraphs/" + textbook_name + ".json", "w") as f:
            f.write(json.dumps(graph))
        print("finished graph creation")
    return 1
