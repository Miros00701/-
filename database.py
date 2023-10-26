import sqlite3 as sql

class Database:
    def __init__(self, database) -> None:
        """
        Inits database of employeers. Table has 5 param: id, full_name, phone_number, email, and price\n
        :database: - file of the database
        """
        self.con = sql.connect(database)
        self.cur = self.con.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS employeer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    full_name TEXT,
                    phone_number TEXT,
                    email TEXT,
                    salary INT
            )
        """)
    
    def insert_data(self, full_name: str, phone_number: str, email: str, salary: int):
        """
        adds data to table "employeer"
        """
        self.cur.execute("""
            INSERT INTO employeer (full_name, phone_number, email, salary)
                VALUES (?, ?, ?, ?)
        """, (full_name, phone_number, email, salary))
        self.con.commit()
    
    def update_data(self, id: int, full_name: str, phone_number: str, email: str, salary: int):
        """
        updates data of table "employeer"
        """
        self.cur.execute("""
            UPDATE employeer
                SET
                    full_name = ?, 
                    phone_number = ?, 
                    email = ?,
                    salary = ?
                WHERE
                    id = ?
        """, (full_name, phone_number, email, salary, id))
        self.con.commit()
    
    def remove_data(self, id):
        """
        removes data from table "employeer"
        """
        self.cur.execute("""
            DELETE FROM employeer WHERE id = ?
        """, (id,))
        self.con.commit()
    
    def execute(self, __sql: str, __parameters):
        """
        For other commands to database\n
        Works as same as sqlite's execute()
        """
        return self.cur.execute(__sql, __parameters)
    
    def commit(self):
        """
        Works as same as sqlite's commit()
        """
        return self.con.commit()
