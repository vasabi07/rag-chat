from langchain.prompts import ChatPromptTemplate;
from langchain_openai import ChatOpenAI;
import requests
from bs4 import BeautifulSoup
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify the origin you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QuestionRequest(BaseModel):
    question: str


template = """
you are a peerTopeer application assistant. answer questions only related to money,transactions,savings.
reply that you dont know about it.if the question is some other topic. 
answer the following question :
Question : {question}
"""
prompt = ChatPromptTemplate.from_template(template)
@app.post("/ask-me")
async def ask_me(question: QuestionRequest):
    try:
        print(f"Received question: {question.question}")
        chain = prompt | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser()
        answer = chain.invoke({"question": question.question})
        print(f"Generated answer: {answer}")
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ddg = DuckDuckGoSearchAPIWrapper()
# def web_search(query:str,num_results:int = 3):
#     results = ddg.results(query,num_results)
#     return [r["link"] for r in results]

# def scrape_doc(url: str): 
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text,"html.parser")
#             page_text = soup.get_text(separator = " ",strip=True)
#             return page_text
#         else :
#             return f"failed to retrieve he webpage: Status_code {response.status_code}"
#     except Exception as e:
#         print(e)
#         return f"failed to retrieve webpage {e}"
    

# url = "https://www.turito.com/learn/physics/gravitation-grade-10"
# SEARCH_PROMPT = ChatPromptTemplate.from_messages(
#     [
#         (
#             "user",
#             "Write 3 google search queries to search online that form an "
#             "objective opinion from the following: {question}\n"
#             "You must respond with a list of strings in the following format: "
#             '["query 1", "query 2", "query 3"].',
#         ),
#     ]
# )



# summarize_chain  = RunnablePassthrough.assign(context = lambda x:scrape_doc(x["url"])[:10000] ) | prompt | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser()
# web_search_chain =RunnablePassthrough.assign(urls = lambda x:  web_search(x["question"])) | (lambda x: [{"question": x["question"],"url" : u} for u in x["urls"]]) | summarize_chain.map()
# sub_question_chain = SEARCH_PROMPT | ChatOpenAI() | StrOutputParser() | json.loads
# chain = sub_question_chain | (lambda x: [{"question": q} for q in x]) | web_search_chain.map()
# answer = chain.invoke({
#     "question": "which is better macos or windows?",
    
# })

# print("Page Context Length:", len(page_context))  # Check the length of the context
# print("Page Context:", page_context[:500])  # Print the first 500 characters of the context
#   # Print the answer from the chain
