from getpass import getpass

import pymysql

con = pymysql.connect(host="localhost", user="root", password=getpass("MySQL password: "), database="shopnest")
cur = con.cursor()

cur.execute("SELECT * FROM demo_product")
rows = cur.fetchall()

name = "X' OR '1'='1"
cur.execute(f"SELECT * FROM demo_product WHERE name = '{name}'")
print(cur.fetchall())
# SELECT * FROM demo_product WHERE name = 'X' OR '1'='1'

cur.execute("SELECT * FROM demo_product WHERE name = %s", (name,))
print(cur.fetchall())