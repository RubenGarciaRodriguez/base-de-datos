from fastapi import FastAPI

app = FastAPI(
    title="Movie API",
    description="API REST para gestionar películas y géneros",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {
        "message": "Movie API funcionando"
    }