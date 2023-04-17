import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.connection.commit()

    def read_data(self, table_name, columns="*", condition=""):
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def read_timesheet(self, date):
        query = f"SELECT entry FROM timesheet where timesheet.user_id = 1 and date(week) = '{date}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def write_timesheet(self, data):
        self.cursor.execute("Insert into timesheet (week,entry,user_id) values (?,?,?)", data)
        self.connection.commit()
    
    def update_timesheet(self, data):
        self.cursor.execute("Update timesheet set entry = ? where week = ?", data)
        self.connection.commit()

    def write_data(self, table_name, values):
        placeholders = ",".join("?" * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()

    def close(self):
        self.connection.close()
