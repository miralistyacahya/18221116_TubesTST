from fastapi import FastAPI
import uvicorn

from routes.Bakery.CakeController import cakeRouter

app = FastAPI()

app.include_router(cakeRouter)

if __name__ == "__main__" :
    uvicorn.run("main:app", host="0.0.0.0", port=8500, reload=True)