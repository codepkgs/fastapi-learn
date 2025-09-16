from fastapi import FastAPI

from app.config import get_settings

settings = get_settings()
print(settings)
print(settings.app.name)
print(settings.app.description)
print(settings.app.version)
print(settings.app.debug)

app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    version=settings.app.version,
    debug=settings.app.debug,
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
