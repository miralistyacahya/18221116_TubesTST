# import MySQLdb
# import os
import mysql.connector

# database di railway

railway_db_config = {
    "host": "viaduct.proxy.rlwy.net",
    "port": 35170,
    "user": "root",
    "password": "632BfeAd5EGD3dF5bBhbbh6CB62bCeb6",
    "database": "railway"
}

conn = mysql.connector.connect(**railway_db_config)


## mySQL local
# db_host = os.getenv('MYSQL_HOST')
# db_port = os.getenv('MYSQL_PORT')
# db_user = os.getenv('MYSQL_USER')
# db_password = os.getenv('MYSQL_PASSWORD')


# conn = mysql.connector.connect(
#     host=db_host,
#     port=int(db_port),
#     user=db_user,
#     password=db_password,
#     database='bakerytst'
# )