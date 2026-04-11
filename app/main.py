from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    import uvicorn

    try:
        uvicorn.run("main:app", reload=True)
    except KeyboardInterrupt:
        print("Server Stopped Correctly")
