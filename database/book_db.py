# import db_connection
# from encodings.punycode import insertion_sort
import logging
from database.db_connection import DbConnection
connection=DbConnection()
logger=logging.getLogger(__name__)

class BookDb:
    logger.info("Enter to class BookDb")
    def __init__(self,host,port,user,password,database):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database

    def create_book(self,data:dict):
        logger.info("Enter to create_book function in class BookDb")
        conn=connection.get_connection()
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
        logger.info("Enter to get_all_books function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT title FROM books")
        names=cursor.fetchall()
        cursor.close()
        conn.close()
        return [name[0] for name in names] if names else None

    def get_book_by_id(self,id):
        logger.info("Enter to get_book_by_id function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id=%s",(id,))
        book=cursor.fetchone()
        cursor.close()
        conn.close()
        return book

    def count_total_books(self):
        logger.info("Enter to count_total_books function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total_books FROM books")
        total=cursor.fetchone()["total_books"]
        cursor.close()
        conn.close()
        return total

    def count_available_books(self):
        logger.info("Enter to count_available_books function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total FROM books WHERE is_available=%s",(True,))
        total=cursor.fetchone()["total"]
        cursor.close()
        conn.close()
        return total

    def update_book(self,id:int,data:dict):
        logger.info("Enter to update_book function in class BookDb")
        conn=connection.get_connection()
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

    def set_available(self,id:int,val:str,member_id:int):
        logger.info("Enter to set_available function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        if val=="return":
            cursor.execute("UPDATE books SET is_available=True, borrowed_by_member_id=NULL WHERE id=%s",(id,))
        elif val=="borrow":
            cursor.execute("UPDATE books SET is_available=False, borrowed_by_member_id=%s WHERE id=%s",(member_id,id))
        conn.commit()
        changed=cursor.rowcount>0
        cursor.close()
        conn.close()
        return changed

    def count_borrowed_books(self):
        logger.info("Enter to count_borrowed_books function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM books WHERE is_available=%s",(False,))
        total=cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

    def count_by_genre(self):
        logger.info("Enter to count_by_genre function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT genre,COUNT(*) AS books_at_genre FROM books GROUP BY genre")
        total=cursor.fetchall()
        cursor.close()
        conn.close()
        return total

    def count_active_borrows_by_member(self,member_id):
        logger.info("Enter to count_active_borrows_by_member function in class BookDb")
        conn=connection.get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books WHERE borrowed_by_member_id=%s",(member_id,))
        total_books=cursor.fetchone()
        cursor.close()
        conn.close()
        return total_books[0] if total_books else None