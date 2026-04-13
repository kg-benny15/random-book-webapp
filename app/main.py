from fastapi import FastAPI
from core.extensions import static
from web.routes import home

app = FastAPI()

# Mounting static files
app.mount("/static", static, name="static")

# Including the routers
app.include_router(home.router)

if __name__ == "__main__":
    import uvicorn

    try:
        uvicorn.run("main:app", reload=True)
    except KeyboardInterrupt:
        print("Server Stopped Correctly")
