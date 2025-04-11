
# CRAWLER
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def extract(url):
    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(
            only_text=True,
            excluded_tags=['script', 'style', 'video', 'iframe', 'embed', 'object', 'footer', 'nav']
        )
        result = await crawler.arun(url=url, config=config)
        return result.markdown


# REST API functionality
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import uvicorn

# Define the request model
class ExtractionRequest(BaseModel):
    url: HttpUrl

# Create the FastAPI app
app = FastAPI(title="Web Crawler API")

@app.post("/extract", response_model=dict)
async def extract_endpoint(request: ExtractionRequest):
    try:
        content = await extract(str(request.url))
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_api(host="0.0.0.0", port=5000):
    """Run the FastAPI application with uvicorn server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_api()
