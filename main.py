from fastapi import FastAPI, Request
import uvicorn
from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms import HuggingFaceHub
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'  # set hf token to access llm

app = FastAPI()


def create_summarizer():
    """Creates summarization model"""

    # Define the Hugging Face Hub model
    llm = HuggingFaceHub(repo_id="facebook/bart-large-cnn", model_kwargs={"temperature": 0.7})

    # Create the simplest summarization chain using defined llm
    summarize_chain = load_summarize_chain(llm, chain_type="stuff")

    return summarize_chain


def transform_text(text):
    """Create list of Documents"""

    # Transform text into Documents
    splitter = RecursiveCharacterTextSplitter()
    docs = splitter.create_documents([text])

    return docs


@app.post("/summarize")
async def summarize(request: Request):
    """Endpoint to summarize the text"""

    data = await request.json()
    text = data.get("text", "")

    docs = transform_text(text)
    summarize_chain = create_summarizer()

    # Use the summarization chain to summarize the text
    result = summarize_chain.invoke(docs)
    summary = result['output_text']

    return {"summary": summary}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
