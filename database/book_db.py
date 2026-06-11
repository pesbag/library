# import db_connection
from database.db_connection import get_connection

class BookDb:
    def __init__(self,host,port,user,password,database):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database

    def create_book(self,data:dict):
        conn=get_connection()
        cursor=conn.cursor()
        sql="INSERT INTO books (title,author,genre) VALUES (%s,%s,%s)"
        values=(data["title"],data["author"],data["genre"])
        cursor.execute(sql,values)
        conn.commit()
        new_id=cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id

    def get_all_books(self):
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT title FROM books")
        names=cursor.fetchall()
        cursor.close()
        conn.close()
        return [name[0] for name in names] if names else None

    def get_book_by_id(self,id):
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id=%s",(id,))
        book=cursor.fetchone()
        cursor.close()
        conn.close()
        return book

    def count_total_books(self):
        conn=get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total_books FROM books")
        total=cursor.fetchone()["total_books"]
        cursor.close()
        conn.close()
        return total

    def count_available_books(self):
        conn=get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total FROM books WHERE is_available=%s",(True,))
        total=cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total

    def update_book(self,id:int,data:dict):
        conn=get_connection()
        cursor=conn.cursor()
        set_part=[f"{key}=%s" for key in data.keys()]
        set_clause=",".join(set_part)
        sql=f"UPDATE books SET {set_clause} WHERE id=%s"
        values=list(data.values())+[id]
        cursor.execute(sql,values)
        conn.commit()
        changed=cursor.rowcount>0
        cursor.close()
        conn.close()
        return changed

    def set_available(self,id,val,member_id):
        pass
    def count_borrowed_books(self):
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM books WHERE is_available=%s",(False,))
        total=cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

