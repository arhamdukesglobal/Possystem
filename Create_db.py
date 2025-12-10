import sqlite3
def Create_db():
    con = sqlite3.connect(database=r'Possystem.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Employee(EmpID INTEGER PRIMARY KEY AUTOINCREMENT,Name text,Email text,Gender text,Contact text,DOB text,DOJ text,Password text,UserType text,Address text,Salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Supplier(SuppInv INTEGER PRIMARY KEY AUTOINCREMENT,Name text,Contact text,Description text)")
    con.commit()


Create_db()