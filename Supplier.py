from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
import re

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+280+180")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()
        
        # Create database and table if not exists
        self.setup_database()
        
        #===========================================
        # All Variables=========
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_SuppInv = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        #===searchFrame=====
        SearchFrame = LabelFrame(self.root, text="Search Supplier", font=("goudy old style", 12, "bold"), 
                                bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        #===options====
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, 
                                  values=["Select", "Invoice No", "Name", "Contact"], 
                                  state='readonly', font=("Times new Roman", 12))
        cmb_search.place(x=10, y=10, width=150)
        cmb_search.current(0)
        
        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, 
                          font=("Aptos", 15), bg="lightyellow")
        txt_search.place(x=170, y=10)
        
        btn_search = Button(SearchFrame, text="Search", command=self.search, 
                           font=("Aptos", 15), bg="#4caf50", fg="White", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        #===title====
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 15), 
                     bg="#0f4d7d", fg="white")
        title.place(x=50, y=100, width=1000)

        #===content====
        #====row1====
        lbl_SuppInv = Label(self.root, text="Invoice No", font=("goudy old style", 15), 
                           bg="white")
        lbl_SuppInv.place(x=50, y=150)
        
        txt_SuppInv = Entry(self.root, textvariable=self.var_SuppInv, 
                           font=("goudy old style", 15), bg="lightyellow", state='readonly')
        txt_SuppInv.place(x=150, y=150, width=180)
        
        #====row2=====
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), 
                        bg="white")
        lbl_name.place(x=50, y=190)
        
        txt_name = Entry(self.root, textvariable=self.var_name, 
                        font=("goudy old style", 15), bg="lightyellow")
        txt_name.place(x=150, y=190, width=180)

        #====row3=====
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), 
                           bg="white")
        lbl_contact.place(x=50, y=230)
        
        # Create contact entry with validation
        self.txt_contact = Entry(self.root, textvariable=self.var_contact, 
                                font=("goudy old style", 15), bg="lightyellow")
        self.txt_contact.place(x=150, y=230, width=180)
        
        # Bind the key release event for real-time validation
        self.txt_contact.bind('<KeyRelease>', self.validate_contact_length)

        #====row4=====
        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), 
                        bg="white")
        lbl_desc.place(x=50, y=270)
        
        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=150, y=270, width=300, height=60)

        #====buttons=====
        btn_add = Button(self.root, text="Save", command=self.add, 
                        font=("Aptos", 15), bg="#2196f3", fg="White", cursor="hand2")
        btn_add.place(x=500, y=340, width=110, height=28)
        
        btn_update = Button(self.root, text="Update", command=self.update, 
                           font=("Aptos", 15), bg="#4caf50", fg="White", cursor="hand2")
        btn_update.place(x=620, y=340, width=110, height=28)
        
        btn_delete = Button(self.root, text="Delete", command=self.delete, 
                           font=("Aptos", 15), bg="#f44336", fg="White", cursor="hand2")
        btn_delete.place(x=740, y=340, width=110, height=28)
        
        btn_clear = Button(self.root, text="Clear", command=self.clear, 
                          font=("Aptos", 15), bg="#607d8b", fg="White", cursor="hand2")
        btn_clear.place(x=860, y=340, width=110, height=28)

        #===Supplier Details====
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=380, relwidth=1, height=120)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(emp_frame, columns=("Invoice", "Name", "Contact", "Description"),
                                         yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        
        self.SupplierTable.heading("Invoice", text="Invoice No")
        self.SupplierTable.heading("Name", text="Name")
        self.SupplierTable.heading("Contact", text="Contact")
        self.SupplierTable.heading("Description", text="Description")
        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("Invoice", width=90)
        self.SupplierTable.column("Name", width=100)
        self.SupplierTable.column("Contact", width=100)
        self.SupplierTable.column("Description", width=100)

        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)
        
        self.show()
        self.generate_invoice_no()  # Generate initial invoice number

    def setup_database(self):
        """Create database and table if they don't exist"""
        try:
            db_path = 'Possystem.db'
            print(f"Connecting to database at: {os.path.abspath(db_path)}")
            
            con = sqlite3.connect(database=db_path)
            cur = con.cursor()
            
            # Create supplier table if it doesn't exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS Supplier (
                    SuppInv TEXT PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Contact TEXT NOT NULL,
                    Description TEXT
                )
            ''')
            con.commit()
            con.close()
            print("Database setup completed successfully")
        except Exception as ex:
            print(f"Error setting up database: {str(ex)}")
            messagebox.showerror("Database Error", f"Cannot setup database: {str(ex)}", parent=self.root)

    def generate_invoice_no(self):
        """Generate auto-incrementing invoice number"""
        con = sqlite3.connect(database='Possystem.db')
        cur = con.cursor()
        try:
            # Get the last invoice number from database
            cur.execute("SELECT SuppInv FROM Supplier ORDER BY SuppInv DESC LIMIT 1")
            result = cur.fetchone()
            
            if result:
                # Extract the numeric part and increment
                last_invoice = result[0]  # e.g., "S0001"
                # Extract only digits from the string
                numbers = re.findall(r'\d+', last_invoice)
                if numbers:
                    last_number = int(numbers[-1])  # Get the last number found
                    next_number = last_number + 1
                else:
                    next_number = 1
            else:
                # If no records exist, start from 1
                next_number = 1
            
            # Format as S followed by 4 digits with leading zeros
            next_invoice = f"S{next_number:04d}"
            self.var_SuppInv.set(next_invoice)
        except Exception as ex:
            # If there's any error, start from S0001
            self.var_SuppInv.set("S0001")
            print(f"Error generating invoice: {str(ex)}")
        finally:
            con.close()

    def validate_contact_length(self, event=None):
        """Automatically restrict contact input to 11 digits"""
        # Get current text and remove all non-digit characters
        current_text = self.var_contact.get()
        digits_only = re.sub(r'\D', '', current_text)
        
        # If we have more than 11 digits, truncate to 11
        if len(digits_only) > 11:
            digits_only = digits_only[:11]
            
            # Update the variable (this will trigger the entry to update)
            self.var_contact.set(digits_only)
            
            # Move cursor to end
            self.txt_contact.icursor(END)
            
            # Optionally, show a brief warning
            self.txt_contact.config(bg="#ffebee")  # Light red background
            self.root.after(500, lambda: self.txt_contact.config(bg="lightyellow"))
    
    def validate_contact_format(self, contact):
        """Validate that contact number is exactly 11 digits and contains only numbers"""
        # Remove any spaces, dashes, or other characters
        clean_contact = re.sub(r'\D', '', contact)
        
        # Check if it's exactly 11 digits
        if len(clean_contact) != 11:
            return False, "Contact number must be exactly 11 digits"
        
        # Check if it contains only numbers
        if not clean_contact.isdigit():
            return False, "Contact number must contain only numbers"
        
        # Optional: Check if it starts with a valid prefix (for Pakistan: 03)
        if not clean_contact.startswith('03'):
            # You can remove or modify this check based on your country's phone number format
            response = messagebox.askyesno("Warning", 
                "Contact number doesn't start with '03'. Do you want to continue?")
            if not response:
                return False, "Contact number validation cancelled"
        
        return True, clean_contact

    def add(self):
        con = sqlite3.connect(database='Possystem.db')
        cur = con.cursor()
        try:
            # Get the description text
            description = self.txt_desc.get('1.0', END).strip()
            
            # Check if all fields are filled
            errors = []
            if not self.var_name.get().strip():
                errors.append("Supplier Name")
            if not self.var_contact.get().strip():
                errors.append("Contact")
            
            if errors:
                error_msg = "The following fields are required:\n"
                for error in errors:
                    error_msg += f"- {error}\n"
                messagebox.showerror("Error", error_msg, parent=self.root)
                return
            
            # Validate contact number format
            contact = self.var_contact.get().strip()
            is_valid, validation_result = self.validate_contact_format(contact)
            if not is_valid:
                messagebox.showerror("Validation Error", validation_result, parent=self.root)
                return
            
            # Use the cleaned contact number
            cleaned_contact = validation_result
            
            # Get the current invoice number
            invoice_no = self.var_SuppInv.get()
            
            # Check if Invoice No already exists (just in case)
            cur.execute("SELECT * FROM Supplier WHERE SuppInv=?", (invoice_no,))
            row = cur.fetchone()
            if row is not None:
                # Regenerate invoice number if conflict
                self.generate_invoice_no()
                invoice_no = self.var_SuppInv.get()
                
                # Check again
                cur.execute("SELECT * FROM Supplier WHERE SuppInv=?", (invoice_no,))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice number conflict, please try again", parent=self.root)
                    return
            
            # Debug print
            print(f"Attempting to insert: Invoice={invoice_no}, Name={self.var_name.get().strip()}, Contact={cleaned_contact}")
            
            # Insert with auto-generated Invoice No
            cur.execute("INSERT INTO Supplier(SuppInv, Name, Contact, Description) VALUES(?, ?, ?, ?)", (
                invoice_no,
                self.var_name.get().strip(),
                cleaned_contact,
                description,
            ))
            con.commit()
            print("Insert successful!")
            messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
            self.show()
            self.clear()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Invoice number already exists or database constraint violated", parent=self.root)
        except sqlite3.Error as ex:
            messagebox.showerror("Database Error", f"Error adding supplier: {str(ex)}", parent=self.root)
            print(f"SQLite error: {str(ex)}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding supplier: {str(ex)}", parent=self.root)
            print(f"Add error: {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database='Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM Supplier ORDER BY SuppInv")
            rows = cur.fetchall()
            print(f"Found {len(rows)} records in database")
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                print(f"Adding to table: {row}")
                self.SupplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading data: {str(ex)}", parent=self.root)
            print(f"Show error: {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        try:
            f = self.SupplierTable.focus()
            content = self.SupplierTable.item(f)
            row = content['values']
            if row and len(row) >= 4:  # Check if row has data and has all 4 columns
                self.var_SuppInv.set(row[0])
                self.var_name.set(row[1])
                self.var_contact.set(row[2])
                self.txt_desc.delete('1.0', END)
                if row[3]:  # Check if description exists
                    self.txt_desc.insert(END, row[3])
        except Exception as ex:
            print(f"Error getting data: {str(ex)}")

    def update(self):
        con = sqlite3.connect(database='Possystem.db')
        cur = con.cursor()
        try:
            if not self.var_SuppInv.get():
                messagebox.showerror("Error", "Please select a supplier to update", parent=self.root)
                return
            
            # Get the description text
            description = self.txt_desc.get('1.0', END).strip()
            
            # Check if all fields are filled
            errors = []
            if not self.var_name.get().strip():
                errors.append("Supplier Name")
            if not self.var_contact.get().strip():
                errors.append("Contact")
            
            if errors:
                error_msg = "The following fields are required:\n"
                for error in errors:
                    error_msg += f"- {error}\n"
                messagebox.showerror("Error", error_msg, parent=self.root)
                return
            
            # Validate contact number format
            contact = self.var_contact.get().strip()
            is_valid, validation_result = self.validate_contact_format(contact)
            if not is_valid:
                messagebox.showerror("Validation Error", validation_result, parent=self.root)
                return
            
            # Use the cleaned contact number
            cleaned_contact = validation_result
            
            # Check if supplier exists
            cur.execute("SELECT * FROM Supplier WHERE SuppInv=?", (self.var_SuppInv.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Supplier not found in database", parent=self.root)
                return
            
            cur.execute("UPDATE Supplier SET Name=?, Contact=?, Description=? WHERE SuppInv=?", (
                self.var_name.get().strip(),
                cleaned_contact,
                description,
                self.var_SuppInv.get(),
            ))
            con.commit()
            messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating supplier: {str(ex)}", parent=self.root)
            print(f"Update error: {str(ex)}")
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database='Possystem.db')
        cur = con.cursor()
        try:
            if not self.var_SuppInv.get():
                messagebox.showerror("Error", "Please select a supplier to delete", parent=self.root)
                return
            
            # Check if supplier exists
            cur.execute("SELECT * FROM Supplier WHERE SuppInv=?", (self.var_SuppInv.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Supplier not found in database", parent=self.root)
                return
            
            op = messagebox.askyesno("Confirm", "Do you really want to delete this supplier?", parent=self.root)
            if op:
                cur.execute("DELETE FROM Supplier WHERE SuppInv=?", (self.var_SuppInv.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Supplier deleted successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error deleting supplier: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        # Generate new invoice number for next entry
        self.generate_invoice_no()
        self.show()

    def search(self):
        con = sqlite3.connect(database='Possystem.db')
        cur = con.cursor()
        try:
            search_by = self.var_searchby.get()
            search_text = self.var_searchtxt.get().strip()
            
            if not search_text:
                messagebox.showerror("Error", "Please enter search text", parent=self.root)
                self.show()  # Show all if search is empty
                return
            
            if search_by == "Select":
                messagebox.showerror("Error", "Please select a search option", parent=self.root)
                return
            
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            
            if search_by == "Invoice No":
                # Handle invoice number search with various formats
                if search_text.isdigit() and len(search_text) <= 4:
                    search_invoice = f"S{int(search_text):04d}"
                elif search_text.upper().startswith('S') and search_text[1:].isdigit() and len(search_text) <= 5:
                    search_invoice = f"S{int(search_text[1:]):04d}"
                else:
                    search_invoice = search_text
                
                cur.execute("SELECT * FROM Supplier WHERE SuppInv=?", (search_invoice,))
            elif search_by == "Name":
                cur.execute("SELECT * FROM Supplier WHERE Name LIKE ?", (f'%{search_text}%',))
            elif search_by == "Contact":
                # Clean the contact for search
                clean_search = re.sub(r'\D', '', search_text)
                cur.execute("SELECT * FROM Supplier WHERE Contact LIKE ?", (f'%{clean_search}%',))
            
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    self.SupplierTable.insert('', END, values=row)
            else:
                messagebox.showinfo("No Results", "No records found matching your search", parent=self.root)
                self.show()  # Show all if no record found
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    # First, create/verify the database
    try:
        con = sqlite3.connect('Possystem.db')
        cur = con.cursor()
        # Check if table exists with correct schema
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Supplier'")
        if not cur.fetchone():
            # Create table if doesn't exist
            cur.execute('''
                CREATE TABLE Supplier (
                    SuppInv TEXT PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Contact TEXT NOT NULL,
                    Description TEXT
                )
            ''')
            con.commit()
            print("Supplier table created successfully")
        con.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    # Now run the application
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()