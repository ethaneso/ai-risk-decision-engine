from fastapi import FastAPI

app = FastAPI(
    title="AI Risk Decision Engine",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "AI Risk Decision Engine",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }