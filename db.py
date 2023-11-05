# import MySQLdb
import os
import mysql.connector

# db_config = {
#     'host': 'viaduct.proxy.rlwy.net',
#     'user': 'root',
#     'password': 'D2dh23-662B1GFFBfCCcA2HBGB1aG4-d',
#     'database': 'railway',
# }

# database di railway
# conn = MySQLdb.connect(
#     host='viaduct.proxy.rlwy.net',
#     port=15076,
#     user='root',
#     password='D2dh23-662B1GFFBfCCcA2HBGB1aG4-d',
#     database='railway'
# )

## mySQL local
db_host = os.getenv('MYSQL_HOST')
db_port = os.getenv('MYSQL_PORT')
db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')


conn = mysql.connector.connect(
    host=db_host,
    port=int(db_port),
    user=db_user,
    password=db_password,
    database='bakerytst'
)