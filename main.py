from fastapi import FastAPI
import uvicorn

from routes.Bakery.CakeController import cakeRouter
from routes.Bakery.CustomerController import customerRouter
from routes.Bakery.OrderController import orderRouter

app = FastAPI()

app.include_router(cakeRouter)
app.include_router(customerRouter)
app.include_router(orderRouter)

if __name__ == "__main__" :
    uvicorn.run("main:app", host="0.0.0.0", port=8600, reload=True)