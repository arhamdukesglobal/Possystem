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

    # Product table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Product("
        "SuppInv INTEGER PRIMARY KEY AUTOINCREMENT,"
        "ProdID TEXT,"
        "ProdName TEXT,"
        "Quantity INTEGER,"
        "Price REAL,"
        "SupplierID INTEGER,"
        "FOREIGN KEY (SupplierID) REFERENCES Supplier(SuppInv))"
    )

    # Sales table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Sales("
        "SalesID INTEGER PRIMARY KEY AUTOINCREMENT,"
        "ProdID TEXT,"
        "Quantity INTEGER,"
        "Total REAL,"
        "Date TEXT)"
    )

    con.commit()
    con.close()


if __name__ == "__main__":
    create_database()
