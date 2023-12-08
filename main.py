from fastapi import FastAPI
import uvicorn
import mysql.connector
from routes.Bakery.CakeController import cakeRouter
from routes.Bakery.CustomerController import customerRouter
from routes.Bakery.OrderController import orderRouter
from routes.auth.auth import authRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRouter)
app.include_router(cakeRouter)
app.include_router(customerRouter)
app.include_router(orderRouter)

@app.get("/")
async def home():
    print("Server is running")

if __name__ == "__main__" :
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)