import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="secret",
        database="library_db"
    )
def create_tables():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    cursor.execute("USE library_db")
    sql="""CREATE TABLE IF NOT EXISTS books(
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(50) NOT NULL,
        genre ENUM('Non-Fiction','Fiction','Science','History','Other'),
        is_available BOOLEAN NOT NULL DEFAULT FALSE,
        borrowed_by_member_id INT 
    )"""
    cursor.execute(sql)
    conn.commit()
    sql="""
        CREATE TABLE IF NOT EXISTS members(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email  VARCHAR(50) NOT NULL UNIQUE,
        is_active BOOLEAN NOT NULL DEFAULT FALSE,
        total_borrows INT NOT NULL AUTO_INCREMENT
        )
        """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def show():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DESCRIBE TABLES members")
    s=cursor.fetchall()
    cursor.close()
    conn.close()
    return s

if __name__=="__main__":
    create_tables()
    print(show())

