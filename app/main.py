from fastapi import FastAPI

app = FastAPI(
    title="E-commerce Product API",
    version="1.0.0",
    description="REST API for managing products, categories, and sellers"
)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}