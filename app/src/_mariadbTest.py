import mysql.connector

# コネクションの作成
conn = mysql.connector.connect(
	host='db',
	port='3306',
	user='root',
	password='myrtpassword',
	database='marialsl'
)


# コネクションが切れた時に再接続してくれるよう設定
conn.ping(reconnect=True)

# 接続できているかどうか確認
print(conn.is_connected())

cr = conn.cursor()

cr.execute("SELECT * FROM sticker_list")
rows = cr.fetchall()
for row in rows :
	print (row)

conn.close()




