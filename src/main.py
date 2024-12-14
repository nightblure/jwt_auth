import uvicorn  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
