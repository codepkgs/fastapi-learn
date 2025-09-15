from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Learn",
    description="FastAPI Learn Demo",
    version="0.1.0",
    debug=True,
)


@app.get("/", tags=["入口"], summary="入口", description="网站主页")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
