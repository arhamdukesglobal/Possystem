from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class ProductClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+280+130")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        # ===============Variables================
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()  # This should match the database column name
        self.var_status = StringVar()
        
        # Initialize empty lists
        self.cat_list = []
        self.sup_list = []
        
        # ===========Title==========
        title = Label(self.root, text="Manage Product Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # ===========Product Frame==========
        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=40, width=450, height=400)

        lbl_category = Label(product_Frame, text="Category", font=("goudy old style", 15), bg="white").place(x=30, y=30)
        lbl_supplier = Label(product_Frame, text="Supplier", font=("goudy old style", 15), bg="white").place(x=30, y=80)
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style", 15), bg="white").place(x=30, y=130)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 15), bg="white").place(x=30, y=180)
        lbl_quantity = Label(product_Frame, text="Quantity", font=("goudy old style", 15), bg="white").place(x=30, y=230)
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style", 15), bg="white").place(x=30, y=280)

        # ===========Dropdowns and Entries==========
        self.cmb_category = ttk.Combobox(product_Frame, textvariable=self.var_cat, 
                                        state="readonly", justify=CENTER, font=("Times new Roman", 12))
        self.cmb_category.place(x=150, y=30, width=200)

        self.cmb_supplier = ttk.Combobox(product_Frame, textvariable=self.var_sup, 
                                        state="readonly", justify=CENTER, font=("Times new Roman", 12))
        self.cmb_supplier.place(x=150, y=80, width=200)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("Times new Roman", 12), bg="lightyellow")
        txt_name.place(x=150, y=130, width=200)

        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("Times new Roman", 12), bg="lightyellow")
        txt_price.place(x=150, y=180, width=200)

        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("Times new Roman", 12), bg="lightyellow")
        txt_qty.place(x=150, y=230, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, 
                                 values=("Active", "Inactive"), state="readonly", 
                                 justify=CENTER, font=("Times new Roman", 12))
        cmb_status.place(x=150, y=280, width=200)
        cmb_status.set("Active")

        # ===========Buttons==========
        btn_add = Button(product_Frame, text="Save", command=self.add, 
                        font=("Aptos", 12), bg="#2196f3", fg="White", cursor="hand2")
        btn_add.place(x=10, y=330, width=100, height=35)
        
        btn_update = Button(product_Frame, text="Update", command=self.update, 
                           font=("Aptos", 12), bg="#4caf50", fg="White", cursor="hand2")
        btn_update.place(x=120, y=330, width=100, height=35)
        
        btn_delete = Button(product_Frame, text="Delete", command=self.delete, 
                           font=("Aptos", 12), bg="#f44336", fg="White", cursor="hand2")
        btn_delete.place(x=230, y=330, width=100, height=35)
        
        btn_clear = Button(product_Frame, text="Clear", command=self.clear, 
                          font=("Aptos", 12), bg="#607d8b", fg="White", cursor="hand2")
        btn_clear.place(x=340, y=330, width=100, height=35)

        # ===========Search Frame==========
        SearchFrame = LabelFrame(self.root, text="Search Product", 
                                font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=40, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, 
                                 values=("Select", "Category", "Supplier", "Name"), 
                                 state="readonly", justify=CENTER, font=("Times new Roman", 12))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.set("Select")

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, 
                          font=("Aptos", 12), bg="lightyellow")
        txt_search.place(x=200, y=10, width=180)

        btn_search = Button(SearchFrame, text="Search", command=self.search, 
                           font=("Aptos", 12), bg="#4caf50", fg="White", cursor="hand2")
        btn_search.place(x=400, y=9, width=100, height=30)
        
        btn_showall = Button(SearchFrame, text="Show All", command=self.show, 
                            font=("Aptos", 12), bg="#2196f3", fg="White", cursor="hand2")
        btn_showall.place(x=510, y=9, width=100, height=30)

        # ===========Product Table Frame==========
        prod_frame = Frame(self.root, bd=3, relief=RIDGE)
        prod_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(prod_frame, orient=VERTICAL)
        scrollx = Scrollbar(prod_frame, orient=HORIZONTAL)

        # FIXED: Column names match database schema
        self.Product_Table = ttk.Treeview(prod_frame, columns=("pid", "Category", "Supplier", "Name", "Price", "Quantity", "Status"), 
                                         yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Product_Table.xview)
        scrolly.config(command=self.Product_Table.yview)

        self.Product_Table.heading("pid", text="Prod ID")
        self.Product_Table.heading("Category", text="Category")
        self.Product_Table.heading("Supplier", text="Supplier")
        self.Product_Table.heading("Name", text="Name")
        self.Product_Table.heading("Price", text="Price")
        self.Product_Table.heading("Quantity", text="Quantity")
        self.Product_Table.heading("Status", text="Status")

        self.Product_Table["show"] = "headings"
        self.Product_Table.column("pid", width=60)
        self.Product_Table.column("Category", width=100)
        self.Product_Table.column("Supplier", width=100)
        self.Product_Table.column("Name", width=120)
        self.Product_Table.column("Price", width=80)
        self.Product_Table.column("Quantity", width=80)
        self.Product_Table.column("Status", width=80)

        self.Product_Table.pack(fill=BOTH, expand=1)
        self.Product_Table.bind("<ButtonRelease-1>", self.get_data)
        
        # Initialize data
        self.fetch_cat_sup()
        self.show()
        self.generate_pid()

    def fetch_cat_sup(self):
        """Fetch active categories and suppliers from database"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Clear existing lists
            self.cat_list.clear()
            self.sup_list.clear()
            
            # Check if Category table has Status column
            try:
                # Try to check for Status column
                cur.execute("PRAGMA table_info(Category)")
                columns = [col[1] for col in cur.fetchall()]
                
                if 'Status' in columns:
                    cur.execute("SELECT Name FROM Category WHERE Status='Active' ORDER BY Name")
                else:
                    cur.execute("SELECT Name FROM Category ORDER BY Name")
            except:
                cur.execute("SELECT Name FROM Category ORDER BY Name")
            
            categories = cur.fetchall()
            self.cat_list = ["Select"] + [cat[0] for cat in categories]
            
            # Check if Supplier table has Status column
            try:
                cur.execute("PRAGMA table_info(Supplier)")
                columns = [col[1] for col in cur.fetchall()]
                
                if 'Status' in columns:
                    cur.execute("SELECT Name FROM Supplier WHERE Status='Active' ORDER BY Name")
                else:
                    cur.execute("SELECT Name FROM Supplier ORDER BY Name")
            except:
                cur.execute("SELECT Name FROM Supplier ORDER BY Name")
            
            suppliers = cur.fetchall()
            self.sup_list = ["Select"] + [sup[0] for sup in suppliers]
            
            # Update combobox values
            self.cmb_category['values'] = self.cat_list
            self.cmb_supplier['values'] = self.sup_list
            
            # Set default selection
            if self.cat_list:
                self.cmb_category.set("Select")
            if self.sup_list:
                self.cmb_supplier.set("Select")
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching data: {str(ex)}", parent=self.root)
            # Set default values on error
            self.cat_list = ["Select"]
            self.sup_list = ["Select"]
            self.cmb_category['values'] = self.cat_list
            self.cmb_supplier['values'] = self.sup_list
        finally:
            if 'con' in locals():
                con.close()

    def refresh_lists(self):
        """Refresh category and supplier lists"""
        self.fetch_cat_sup()

    def get_categories(self):
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            # Check if Status column exists
            cur.execute("PRAGMA table_info(Category)")
            columns = [col[1] for col in cur.fetchall()]
            
            if 'Status' in columns:
                cur.execute("SELECT Name FROM Category WHERE Status='Active'")
            else:
                cur.execute("SELECT Name FROM Category")
                
            rows = cur.fetchall()
            return ["Select"] + [row[0] for row in rows]
        except:
            return ["Select"]
        finally:
            if 'con' in locals():
                con.close()

    def get_suppliers(self):
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            # Check if Status column exists
            cur.execute("PRAGMA table_info(Supplier)")
            columns = [col[1] for col in cur.fetchall()]
            
            if 'Status' in columns:
                cur.execute("SELECT Name FROM Supplier WHERE Status='Active'")
            else:
                cur.execute("SELECT Name FROM Supplier")
                
            rows = cur.fetchall()
            return ["Select"] + [row[0] for row in rows]
        except:
            return ["Select"]
        finally:
            if 'con' in locals():
                con.close()

    def generate_pid(self):
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            cur.execute("SELECT MAX(pid) FROM product")
            max_id = cur.fetchone()[0]
            if max_id:
                self.var_pid.set(f"P{int(max_id) + 1:03d}")
            else:
                self.var_pid.set("P001")
        except:
            self.var_pid.set("P001")
        finally:
            if 'con' in locals():
                con.close()

    def add(self):
        if self.var_cat.get() == "Select" or self.var_sup.get() == "Select":
            messagebox.showerror("Error", "Category and Supplier are required", parent=self.root)
            return
            
        if not self.var_name.get() or not self.var_price.get() or not self.var_qty.get():
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            price = float(self.var_price.get())
            qty = int(self.var_qty.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and Quantity must be an integer", parent=self.root)
            return

        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Check if product with same name already exists
            cur.execute("SELECT * FROM product WHERE Name=?", (self.var_name.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Product already exists", parent=self.root)
                return

            # FIXED: Using correct column names that match database schema
            cur.execute("INSERT INTO product (Category, Supplier, Name, Price, Quantity, Status) VALUES (?, ?, ?, ?, ?, ?)",
                       (self.var_cat.get(), self.var_sup.get(), 
                        self.var_name.get(), price, qty, self.var_status.get()))
            con.commit()
            messagebox.showinfo("Success", "Product added successfully", parent=self.root)
            self.show()
            self.generate_pid()  # Regenerate new PID after add
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding product: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Select a product to update", parent=self.root)
            return
            
        if self.var_cat.get() == "Select" or self.var_sup.get() == "Select":
            messagebox.showerror("Error", "Category and Supplier are required", parent=self.root)
            return
            
        if not self.var_name.get() or not self.var_price.get() or not self.var_qty.get():
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            price = float(self.var_price.get())
            qty = int(self.var_qty.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and Quantity must be an integer", parent=self.root)
            return

        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Get the numeric part of PID (remove 'P' prefix)
            pid_num = int(self.var_pid.get()[1:]) if self.var_pid.get().startswith('P') else int(self.var_pid.get())
            
            # Check if product with same name exists for other product
            cur.execute("SELECT * FROM product WHERE Name=? AND pid!=?", 
                       (self.var_name.get(), pid_num))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Product name already exists for another product", parent=self.root)
                return

            # FIXED: Using correct column names
            cur.execute("UPDATE product SET Category=?, Supplier=?, Name=?, Price=?, Quantity=?, Status=? WHERE pid=?",
                       (self.var_cat.get(), self.var_sup.get(), self.var_name.get(), 
                        price, qty, self.var_status.get(), pid_num))
            con.commit()
            messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating product: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Select a product to delete", parent=self.root)
            return
            
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Get the numeric part of PID
            pid_num = int(self.var_pid.get()[1:]) if self.var_pid.get().startswith('P') else int(self.var_pid.get())
            
            confirm = messagebox.askyesno("Confirm", "Do you really want to delete this product?", parent=self.root)
            if confirm:
                cur.execute("DELETE FROM product WHERE pid=?", (pid_num,))
                con.commit()
                messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                self.clear()
                self.generate_pid()
        except Exception as ex:
            messagebox.showerror("Error", f"Error deleting product: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_status.set("Active")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.Product_Table.selection_remove(self.Product_Table.selection())
        self.generate_pid()

    def get_data(self, ev):
        f = self.Product_Table.focus()
        content = self.Product_Table.item(f)
        row = content['values']
        if row:
            self.var_pid.set(f"P{row[0]:03d}")
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])

    def show(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product ORDER BY pid")
            rows = cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                # Format PID with 'P' prefix for display
                formatted_row = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                self.Product_Table.insert('', END, values=formatted_row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading products: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        if self.var_searchby.get() == "Select":
            messagebox.showerror("Error", "Select search criteria", parent=self.root)
            return
            
        if not self.var_searchtxt.get().strip():
            self.show()
            return

        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            search_by = self.var_searchby.get()
            search_text = f"%{self.var_searchtxt.get().strip()}%"
            
            if search_by == "Category":
                cur.execute("SELECT * FROM product WHERE Category LIKE ?", (search_text,))
            elif search_by == "Supplier":
                cur.execute("SELECT * FROM product WHERE Supplier LIKE ?", (search_text,))
            elif search_by == "Name":
                cur.execute("SELECT * FROM product WHERE Name LIKE ?", (search_text,))
            
            rows = cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            
            if rows:
                for row in rows:
                    formatted_row = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    self.Product_Table.insert('', END, values=formatted_row)
            else:
                messagebox.showinfo("No Results", "No products found", parent=self.root)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()