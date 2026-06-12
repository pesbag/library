from database.db_connection import get_connection
class MemberDB:
    def __init__(self,host,port,user,password,database):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database

    def create_member(self,data:dict):
        conn=get_connection()
        cursor=conn.cursor()
        sql="INSERT INTO members (name,email,is_active,total_borrows) VALUES (%s,%s,%s,%s)"
        values=(data["name"],data["email"],data["is_active"],data["total_borrows"])
        cursor.execute(sql,values)
        conn.commit()
        new_id=cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id

    def get_all_members(self):
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT name FROM members")
        names=cursor.fetchall()
        if not names:
            return names
        cursor.close()
        conn.close()
        return [name[0] for name in names]

    def get_member_by_id(self,id:int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members WHERE id=%s",(id,))
        member=cursor.fetchone()
        cursor.close()
        conn.close()
        return member

    def update_member(self,id:int,data:dict):
        conn = get_connection()
        cursor = conn.cursor()
        set_part = [f"{key}=%s" for key in data.keys()]
        set_clause = ",".join(set_part)
        sql = f"UPDATE members SET {set_clause} WHERE id=%s"
        values = list(data.values()) + [id]
        cursor.execute(sql, values)
        conn.commit()
        changed = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return changed

    def deactivate_member(self,id:int):
        pass

    def activate_member(self,id):
        pass
    def increment_borrows(self,id):
        pass
    def count_active_members(self):
        pass
    def get_top_count(self):
        pass