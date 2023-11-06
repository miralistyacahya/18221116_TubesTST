from fastapi import FastAPI
import uvicorn
import mysql.connector
from routes.Bakery.CakeController import cakeRouter
from routes.Bakery.CustomerController import customerRouter
from routes.Bakery.OrderController import orderRouter

app = FastAPI()

app.include_router(cakeRouter)
app.include_router(customerRouter)
app.include_router(orderRouter)

@app.get("/")
async def home():
    print("Server is running")

railway_db_config = {
    "host": "viaduct.proxy.rlwy.net",
    "port": 35170,
    "user": "root",
    "password": "632BfeAd5EGD3dF5bBhbbh6CB62bCeb6",
    "database": "railway"
}

try:
    conn = mysql.connector.connect(**railway_db_config)
    print("Success connect to db")
except mysql.connector.Error as e:
    print(e)
else:
    cursor = conn.cursor()

if __name__ == "__main__" :
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)