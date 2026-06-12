from fastapi import FastAPI

app = FastAPI(title="FastAPI", version="1.0.0", root_path="/backend")


@app.get("/")
async def root():
    return {"message": "Hello World"}
