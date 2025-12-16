import sqlite3

def create_database():
    con = sqlite3.connect("Possystem.db")
    cur = con.cursor()

    # Supplier table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Supplier("
        "SuppInv INTEGER PRIMARY KEY AUTOINCREMENT,"
        "Name TEXT," 
        "Contact TEXT,"
        "Description TEXT)"
    )

    # Employee table
    cur.execute('''CREATE TABLE IF NOT EXISTS Employee (
                EmpID TEXT PRIMARY KEY,
                Name TEXT NOT NULL,
                Email TEXT,
                Gender TEXT,
                CNIC TEXT UNIQUE,
                Contact TEXT,
                DOB TEXT,
                DOJ TEXT,
                Password TEXT,
                UserType TEXT,
                Address TEXT,
                Salary TEXT)''')
    

    cur.execute("CREATE TABLE IF NOT EXISTS Category(CID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT)")
    con.commit()
    

    con.commit()
    con.close()
    print("Database and all tables created successfully!")


if __name__ == "__main__":
    create_database()