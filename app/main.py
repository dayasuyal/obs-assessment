from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello Observability World! as We are planing to grouth of OB Domain with SRE and DevOps!"}
