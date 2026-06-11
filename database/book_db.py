cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
cursor.execute("USE library_db")