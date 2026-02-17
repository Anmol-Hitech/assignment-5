from routes import router
from fastapi import FastAPI
app=FastAPI()
app.include_router(router)
@app.get("/")
def root():
    return {"message":"This is the root api"}
