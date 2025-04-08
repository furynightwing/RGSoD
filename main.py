from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from middleware.asset_middleware import AssetMiddleware
from middleware.logging_middleware import LoggingMiddleware
import json
import uvicorn




# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

app = FastAPI()

# Add logging middleware first to capture everything
app.add_middleware(LoggingMiddleware)
# Include AssetMiddleware for on-the-fly encryption
app.add_middleware(AssetMiddleware, config=config)

# Optionally add CORS or other middlewares here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for security if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example endpoint to test server is working
@app.get("/")
def read_root():
    return {"status": "Python server running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
