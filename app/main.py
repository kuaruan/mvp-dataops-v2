from fastapi import FastAPI

app = FastAPI(title="MVP Dataops v2")


@app.get("/")
def root():
    return{"message": "API de MVP Dataops v2 Funcionando!"}

@app.get("/health")
def health():
    return {"status": "Todo Okay!"}

