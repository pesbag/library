from database.db_connection import DbConnection
connection=DbConnection()
import logging
logger=logging.getLogger(__name__)
class MemberDB:
    def __init__(self,host,port,user,password,database):
        logger.info("Enter to class MemberDB")
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database

    def create_member(self,data:dict):
        logger.info("Enter to create_member function in class MemberDB")
        conn=connection.get_connection()
        cursor=conn.cursor()
        logger.debug("check if the current email is already exists in the table")
        cursor.execute("SELECT id FROM members WHERE email=%s",(data["email"],))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return None
        logger.info("insert the values the table")
        sql="INSERT INTO members (name,email,is_active) VALUES (%s,%s,%s)"
        values=(data["name"],data["email"],data["is_active"])
        cursor.execute(sql,values)
        conn.commit()
        logger.debug("find the new id of the row that added")
        new_id=cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id

    def get_all_members(self):
        logger.info("Enter to get_all_members function in class MemberDB")
        conn=connection.get_connection()
        cursor=conn.cursor()
        logger.info("get the names of all the members in the table")
        cursor.execute("SELECT name FROM members")
        names=cursor.fetchall()
        logger.debug("check the the names list is not empty")
        if not names:
            return names
        cursor.close()
        conn.close()
        return [name[0] for name in names]

    def get_member_by_id(self,id:int):
        logger.info("Enter to get_member_by_id function in class MemberDB")
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        logger.info("find a specific member by his id")
        cursor.execute("SELECT * FROM members WHERE id=%s",(id,))
        member=cursor.fetchone()
        cursor.close()
        conn.close()
        return member

    def update_member(self,id:int,data:dict):
        logger.info("Enter to update_member function in class MemberDB")
        conn = connection.get_connection()
        cursor = conn.cursor()
        set_part = [f"{key}=%s" for key in data.keys()]
        set_clause = ",".join(set_part)
        if "email" in data.keys():
            logger.debug("check if the current email is already exists in the table")
            cursor.execute("SELECT id FROM members WHERE email=%s",(data["email"],))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return None
            logger.info("update data of a specific member")
        sql = f"UPDATE members SET {set_clause} WHERE id=%s"
        values = list(data.values()) + [id]
        cursor.execute(sql, values)
        conn.commit()
        logger.debug("check if any row affected from the update")
        changed = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return changed

    def deactivate_member(self,id:int):
        logger.info("Enter to deactivate_member function in class MemberDB")
        conn = connection.get_connection()
        cursor = conn.cursor()
        logger.info("update member to be a unactive member")
        cursor.execute("UPDATE members SET is_active=False WHERE id=%s",(id,))
        conn.commit()
        logger.debug("check if any row affected from the update")
        changed=cursor.rowcount >0
        cursor.close()
        conn.close()
        return changed

    def activate_member(self,id:int):
        logger.info("Enter to activate_member function in class MemberDB")
        conn = connection.get_connection()
        cursor = conn.cursor()
        logger.info("update member to be an active member")
        cursor.execute("UPDATE members SET is_active=True WHERE id=%s", (id,))
        conn.commit()
        logger.debug("check if any row affected from the update")
        changed = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return changed

    def increment_borrows(self,id:int,member_id:int):
        logger.info("Enter to increment_borrows function in class MemberDB")
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        logger.info("get total borrows of specific member")
        cursor.execute("SELECT total_borrows FROM members WHERE id=%s",(member_id,))
        row=cursor.fetchone()
        logger.debug("check if the specific member is exists before we try to get him")
        if not row:
            cursor.close()
            conn.close()
            return None
        total=row["total_borrows"]
        cursor.execute("UPDATE members SET total_borrows=%s WHERE id=%s",(total+1,member_id))
        cursor.execute("UPDATE books SET borrowed_by_member_id=%s WHERE id=%s",(member_id,id))
        conn.commit()
        cursor.close()
        conn.close()
        return total

    def count_active_members(self):
        logger.info("Enter to count_active_members function in class MemberDB")
        conn = connection.get_connection()
        cursor = conn.cursor()
        logger.info("get the numbers of all the active members")
        cursor.execute("SELECT COUNT(*) FROM members WHERE is_active IS TRUE")
        total_active=cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total_active

    def get_top_member(self):
        logger.info("Enter to get_top_member function in class MemberDB")
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        logger.info("get the members who borrow the most")
        cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1 ")
        max_b=cursor.fetchone()
        cursor.close()
        conn.close()
        return {"member_id":max_b["id"],"borrowed":max_b["total_borrows"]}