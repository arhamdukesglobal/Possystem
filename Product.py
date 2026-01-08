from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import locale

class IntegratedInventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x700+100+50")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # ========== Variables for Category ==========
        self.var_CatID = StringVar()
        self.var_CatName = StringVar()
        
        # ========== Variables for Product ==========
        self.var_pid = StringVar()
        self.var_ProdCat = StringVar()
        self.var_sup = StringVar()
        self.var_prod_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        
        # Price formatting variable
        self.price_without_format = ""
        
        # Lists for dropdowns
        self.cat_list = []
        self.sup_list = []
        
        # ========== Title ==========
        lbl_title = Label(self.root, text="Inventory Management System", 
                         font=("goudy old style", 30), bg="#184a45", 
                         fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)
        
        # ========== Main Container Frames ==========
        # Left Frame for Category Management
        left_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        left_frame.place(x=10, y=100, width=500, height=580)
        
        # Right Frame for Product Management
        right_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        right_frame.place(x=520, y=100, width=770, height=580)
        
        # ========== CATEGORY SECTION (Left Frame) ==========
        cat_title = Label(left_frame, text="Manage Categories", 
                         font=("goudy old style", 18, "bold"), 
                         bg="#184a45", fg="white")
        cat_title.pack(side=TOP, fill=X)
        
        # Category Entry Section
        cat_entry_frame = Frame(left_frame, bg="white", padx=10, pady=10)
        cat_entry_frame.pack(fill=X, padx=10, pady=10)
        
        lbl_cat_name = Label(cat_entry_frame, text="Category Name", 
                            font=("goudy old style", 14), bg="white")
        lbl_cat_name.grid(row=0, column=0, sticky=W, pady=5)
        
        txt_cat_name = Entry(cat_entry_frame, textvariable=self.var_CatName, 
                            font=("goudy old style", 14), bg="lightyellow", width=25)
        txt_cat_name.grid(row=0, column=1, pady=5, padx=10)
        
        # Category Buttons
        cat_btn_frame = Frame(left_frame, bg="white", padx=10, pady=10)
        cat_btn_frame.pack(fill=X, padx=10)
        
        btn_add_cat = Button(cat_btn_frame, text="ADD CATEGORY", command=self.add_category,
                           font=("goudy old style", 12), bg="#4caf50", 
                           fg="white", cursor="hand2", width=15)
        btn_add_cat.grid(row=0, column=0, padx=5, pady=5)
        
        btn_delete_cat = Button(cat_btn_frame, text="DELETE", command=self.delete_category,
                              font=("goudy old style", 12), bg="#f44336", 
                              fg="white", cursor="hand2", width=15)
        btn_delete_cat.grid(row=0, column=1, padx=5, pady=5)
        
        btn_clear_cat = Button(cat_btn_frame, text="CLEAR", command=self.clear_category,
                             font=("goudy old style", 12), bg="#607d8b", 
                             fg="white", cursor="hand2", width=15)
        btn_clear_cat.grid(row=0, column=2, padx=5, pady=5)
        
        # Categories List
        cat_list_frame = Frame(left_frame, bg="white", bd=2, relief=RIDGE)
        cat_list_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        scrolly_cat = Scrollbar(cat_list_frame, orient=VERTICAL)
        scrollx_cat = Scrollbar(cat_list_frame, orient=HORIZONTAL)
        
        self.Category_Table = ttk.Treeview(cat_list_frame, columns=("CID", "Name"),
                                          yscrollcommand=scrolly_cat.set,
                                          xscrollcommand=scrollx_cat.set)
        
        scrollx_cat.pack(side=BOTTOM, fill=X)
        scrolly_cat.pack(side=RIGHT, fill=Y)
        scrollx_cat.config(command=self.Category_Table.xview)
        scrolly_cat.config(command=self.Category_Table.yview)
        
        self.Category_Table.heading("CID", text="ID")
        self.Category_Table.heading("Name", text="Category Name")
        self.Category_Table["show"] = "headings"
        self.Category_Table.column("CID", width=50, anchor=CENTER)
        self.Category_Table.column("Name", width=200)
        self.Category_Table.pack(fill=BOTH, expand=True)
        self.Category_Table.bind("<ButtonRelease-1>", self.get_category_data)
        
        # ========== PRODUCT SECTION (Right Frame) ==========
        prod_title = Label(right_frame, text="Manage Products", 
                          font=("goudy old style", 18, "bold"), 
                          bg="#0f4d7d", fg="white")
        prod_title.pack(side=TOP, fill=X)
        
        # Product Entry Frame
        prod_entry_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE, padx=10, pady=10)
        prod_entry_frame.place(x=10, y=50, width=750, height=250)
        
        # Product Entry Fields
        lbl_category = Label(prod_entry_frame, text="Category", 
                            font=("goudy old style", 12), bg="white")
        lbl_category.grid(row=0, column=0, sticky=W, pady=5)
        
        self.cmb_category = ttk.Combobox(prod_entry_frame, textvariable=self.var_ProdCat,
                                        state="readonly", font=("Times new Roman", 12), width=25)
        self.cmb_category.grid(row=0, column=1, pady=5, padx=5)
        
        lbl_supplier = Label(prod_entry_frame, text="Supplier", 
                            font=("goudy old style", 12), bg="white")
        lbl_supplier.grid(row=0, column=2, sticky=W, pady=5, padx=10)
        
        self.cmb_supplier = ttk.Combobox(prod_entry_frame, textvariable=self.var_sup,
                                        state="readonly", font=("Times new Roman", 12), width=25)
        self.cmb_supplier.grid(row=0, column=3, pady=5, padx=5)
        
        lbl_product_name = Label(prod_entry_frame, text="Product Name", 
                                font=("goudy old style", 12), bg="white")
        lbl_product_name.grid(row=1, column=0, sticky=W, pady=5)
        
        txt_prod_name = Entry(prod_entry_frame, textvariable=self.var_prod_name,
                             font=("Times new Roman", 12), bg="lightyellow", width=28)
        txt_prod_name.grid(row=1, column=1, pady=5, padx=5)
        
        lbl_price = Label(prod_entry_frame, text="Price", 
                         font=("goudy old style", 12), bg="white")
        lbl_price.grid(row=1, column=2, sticky=W, pady=5, padx=10)
        
        # Price frame with Rs symbol
        price_frame = Frame(prod_entry_frame, bg="white")
        price_frame.grid(row=1, column=3, pady=5, padx=5, sticky=W)
        
        rs_label = Label(price_frame, text="Rs.", 
                        font=("Times new Roman", 12, "bold"), bg="white")
        rs_label.pack(side=LEFT, padx=(0, 5))
        
        self.txt_price = Entry(price_frame, font=("Times new Roman", 12), 
                              bg="lightyellow", justify=RIGHT, width=24)
        self.txt_price.pack(side=LEFT)
        
        # Bind price formatting events
        self.txt_price.bind('<KeyRelease>', self.format_price_with_commas)
        self.txt_price.bind('<FocusIn>', self.on_price_focus_in)
        self.txt_price.bind('<FocusOut>', self.on_price_focus_out)
        
        lbl_quantity = Label(prod_entry_frame, text="Quantity", 
                            font=("goudy old style", 12), bg="white")
        lbl_quantity.grid(row=2, column=0, sticky=W, pady=5)
        
        txt_qty = Entry(prod_entry_frame, textvariable=self.var_qty,
                       font=("Times new Roman", 12), bg="lightyellow", width=28)
        txt_qty.grid(row=2, column=1, pady=5, padx=5)
        
        lbl_status = Label(prod_entry_frame, text="Status", 
                          font=("goudy old style", 12), bg="white")
        lbl_status.grid(row=2, column=2, sticky=W, pady=5, padx=10)
        
        cmb_status = ttk.Combobox(prod_entry_frame, textvariable=self.var_status,
                                 values=("Active", "Inactive"), state="readonly",
                                 font=("Times new Roman", 12), width=26)
        cmb_status.grid(row=2, column=3, pady=5, padx=5)
        cmb_status.set("Active")
        
        lbl_pid = Label(prod_entry_frame, text="Product ID", 
                       font=("goudy old style", 12), bg="white")
        lbl_pid.grid(row=3, column=0, sticky=W, pady=5)
        
        txt_pid = Entry(prod_entry_frame, textvariable=self.var_pid,
                       font=("Times new Roman", 12), bg="lightyellow", 
                       state="readonly", width=28)
        txt_pid.grid(row=3, column=1, pady=5, padx=5)
        
        # Product Buttons
        prod_btn_frame = Frame(prod_entry_frame, bg="white")
        prod_btn_frame.grid(row=3, column=2, columnspan=2, pady=10, sticky=E)
        
        btn_add_prod = Button(prod_btn_frame, text="SAVE", command=self.add_product,
                            font=("Aptos", 11), bg="#2196f3", 
                            fg="White", cursor="hand2", width=10)
        btn_add_prod.grid(row=0, column=0, padx=3)
        
        btn_update_prod = Button(prod_btn_frame, text="UPDATE", command=self.update_product,
                               font=("Aptos", 11), bg="#4caf50", 
                               fg="White", cursor="hand2", width=10)
        btn_update_prod.grid(row=0, column=1, padx=3)
        
        btn_delete_prod = Button(prod_btn_frame, text="DELETE", command=self.delete_product,
                               font=("Aptos", 11), bg="#f44336", 
                               fg="White", cursor="hand2", width=10)
        btn_delete_prod.grid(row=0, column=2, padx=3)
        
        btn_clear_prod = Button(prod_btn_frame, text="CLEAR", command=self.clear_product,
                              font=("Aptos", 11), bg="#607d8b", 
                              fg="White", cursor="hand2", width=10)
        btn_clear_prod.grid(row=0, column=3, padx=3)
        
        # Search Frame
        search_frame = LabelFrame(right_frame, text="Search Product", 
                                 font=("goudy old style", 12, "bold"), 
                                 bd=2, relief=RIDGE, bg="white")
        search_frame.place(x=10, y=310, width=750, height=70)
        
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_searchby,
                                 values=("Select", "Category", "Supplier", "Name"),
                                 state="readonly", font=("Times new Roman", 12), width=15)
        cmb_search.place(x=10, y=10, width=150)
        cmb_search.set("Select")
        
        txt_search = Entry(search_frame, textvariable=self.var_searchtxt,
                          font=("Aptos", 12), bg="lightyellow", width=20)
        txt_search.place(x=180, y=10, width=200)
        
        btn_search = Button(search_frame, text="SEARCH", command=self.search_product,
                           font=("Aptos", 12), bg="#4caf50", 
                           fg="White", cursor="hand2", width=10)
        btn_search.place(x=400, y=8, height=30)
        
        btn_showall = Button(search_frame, text="SHOW ALL", command=self.show_products,
                            font=("Aptos", 12), bg="#2196f3", 
                            fg="White", cursor="hand2", width=10)
        btn_showall.place(x=510, y=8, height=30)
        
        # Products Table
        prod_table_frame = Frame(right_frame, bd=3, relief=RIDGE, bg="white")
        prod_table_frame.place(x=10, y=390, width=750, height=180)
        
        scrolly_prod = Scrollbar(prod_table_frame, orient=VERTICAL)
        scrollx_prod = Scrollbar(prod_table_frame, orient=HORIZONTAL)
        
        self.Product_Table = ttk.Treeview(prod_table_frame, 
                                         columns=("pid", "Category", "Supplier", "Name", "Price", "Quantity", "Status"),
                                         yscrollcommand=scrolly_prod.set,
                                         xscrollcommand=scrollx_prod.set)
        
        scrollx_prod.pack(side=BOTTOM, fill=X)
        scrolly_prod.pack(side=RIGHT, fill=Y)
        scrollx_prod.config(command=self.Product_Table.xview)
        scrolly_prod.config(command=self.Product_Table.yview)
        
        self.Product_Table.heading("pid", text="ID")
        self.Product_Table.heading("Category", text="Category")
        self.Product_Table.heading("Supplier", text="Supplier")
        self.Product_Table.heading("Name", text="Product Name")
        self.Product_Table.heading("Price", text="Price")
        self.Product_Table.heading("Quantity", text="Qty")
        self.Product_Table.heading("Status", text="Status")
        
        self.Product_Table["show"] = "headings"
        self.Product_Table.column("pid", width=50, anchor=CENTER)
        self.Product_Table.column("Category", width=100)
        self.Product_Table.column("Supplier", width=100)
        self.Product_Table.column("Name", width=150)
        self.Product_Table.column("Price", width=80, anchor=E)
        self.Product_Table.column("Quantity", width=60, anchor=CENTER)
        self.Product_Table.column("Status", width=80, anchor=CENTER)
        
        self.Product_Table.pack(fill=BOTH, expand=True)
        self.Product_Table.bind("<ButtonRelease-1>", self.get_product_data)
        
        # Initialize data
        self.show_categories()
        self.fetch_cat_sup()
        self.generate_pid()
        self.show_products()
        
        # Bind category selection event
        self.Category_Table.bind("<<TreeviewSelect>>", self.on_category_select)
        
    # ========== CATEGORY METHODS ==========
    
    def get_next_category_id(self):
        """Get the next available category ID starting from 1"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT CID FROM Category ORDER BY CID")
            rows = cur.fetchall()
            
            if not rows:
                return 1
            
            ids = [row[0] for row in rows]
            
            for i in range(1, len(ids) + 2):
                if i not in ids:
                    return i
                    
            return len(ids) + 1
        finally:
            con.close()
    
    def add_category(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_CatName.get() == "":
                messagebox.showerror("Error", "Category Name is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM Category WHERE Name=?", (self.var_CatName.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already exists", parent=self.root)
                else:
                    next_id = self.get_next_category_id()
                    cur.execute("INSERT INTO Category (CID, Name) VALUES(?, ?)", 
                               (next_id, self.var_CatName.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                    self.show_categories()
                    self.fetch_cat_sup()  # Refresh category dropdown
                    self.var_CatName.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def show_categories(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM Category ORDER BY CID")
            rows = cur.fetchall()
            self.Category_Table.delete(*self.Category_Table.get_children())
            for row in rows:
                self.Category_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading categories: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def get_category_data(self, ev):
        try:
            selected_item = self.Category_Table.selection()[0]
            row = self.Category_Table.item(selected_item, 'values')
            if row:
                self.var_CatID.set(row[0])
                self.var_CatName.set(row[1])
        except IndexError:
            pass
    
    def delete_category(self):
        con = sqlite3.connect(database='Possystem.db')
        cur = con.cursor()
        try:
            if not self.var_CatID.get():
                messagebox.showerror("Error", "Please select a category to delete", parent=self.root)
            else:
                # Check if category has products
                cur.execute("SELECT COUNT(*) FROM product WHERE Category=?", 
                           (self.var_CatName.get(),))
                product_count = cur.fetchone()[0]
                
                if product_count > 0:
                    messagebox.showerror("Error", 
                                       f"Cannot delete category. It has {product_count} product(s) associated with it.\nPlease delete or reassign the products first.", 
                                       parent=self.root)
                    return
                
                op = messagebox.askyesno("Confirm", 
                                        "Do you really want to delete this category?", 
                                        parent=self.root)
                if op:
                    delete_id = int(self.var_CatID.get())
                    cur.execute("DELETE FROM Category WHERE CID=?", (delete_id,))
                    
                    # Decrement all higher IDs by 1
                    cur.execute("SELECT CID FROM Category WHERE CID > ? ORDER BY CID", (delete_id,))
                    higher_ids = cur.fetchall()
                    
                    for old_id in higher_ids:
                        new_id = old_id[0] - 1
                        cur.execute("UPDATE Category SET CID = ? WHERE CID = ?", (new_id, old_id[0]))
                    
                    con.commit()
                    messagebox.showinfo("Delete", "Category deleted successfully", parent=self.root)
                    self.show_categories()
                    self.fetch_cat_sup()  # Refresh category dropdown
                    self.var_CatID.set("")
                    self.var_CatName.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def clear_category(self):
        self.var_CatID.set("")
        self.var_CatName.set("")
        self.Category_Table.selection_remove(self.Category_Table.selection())
    
    def on_category_select(self, event):
        """When a category is selected, show products under that category"""
        try:
            selected_item = self.Category_Table.selection()[0]
            row = self.Category_Table.item(selected_item, 'values')
            if row:
                category_name = row[1]
                self.var_ProdCat.set(category_name)
                self.show_products_by_category(category_name)
        except IndexError:
            pass
    
    # ========== PRODUCT METHODS ==========
    
    def format_price_with_commas(self, event=None):
        """Format price with commas as user types"""
        try:
            current_text = self.txt_price.get()
            cursor_pos = self.txt_price.index(INSERT)
            
            clean_text = ''
            has_decimal = False
            for char in current_text:
                if char.isdigit():
                    clean_text += char
                elif char == '.' and not has_decimal:
                    clean_text += char
                    has_decimal = True
                elif char == ',':
                    continue
            
            self.price_without_format = clean_text
            
            if clean_text:
                if '.' in clean_text:
                    integer_part, decimal_part = clean_text.split('.')
                else:
                    integer_part = clean_text
                    decimal_part = ''
                
                formatted_integer = ''
                for i, digit in enumerate(reversed(integer_part)):
                    if i > 0 and i % 3 == 0:
                        formatted_integer = ',' + formatted_integer
                    formatted_integer = digit + formatted_integer
                
                formatted_price = formatted_integer
                if decimal_part:
                    formatted_price += '.' + decimal_part
                
                self.txt_price.delete(0, END)
                self.txt_price.insert(0, formatted_price)
                
                try:
                    self.txt_price.icursor(cursor_pos)
                except:
                    pass
        except Exception as e:
            print(f"Error formatting price: {e}")
    
    def on_price_focus_in(self, event=None):
        """When price field gets focus, store current value"""
        self.price_without_format = self.txt_price.get().replace(',', '')
    
    def on_price_focus_out(self, event=None):
        """When price field loses focus, ensure proper formatting"""
        self.format_price_with_commas()
    
    def get_price_value(self):
        """Get the numeric price value from the formatted field"""
        try:
            price_text = self.txt_price.get().replace(',', '')
            if not price_text:
                return None
            return float(price_text)
        except ValueError:
            return None
    
    def fetch_cat_sup(self):
        """Fetch active categories and suppliers from database"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            self.cat_list.clear()
            self.sup_list.clear()
            
            # Fetch categories
            try:
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
            
            # Fetch suppliers
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
            
            if self.cat_list:
                self.cmb_category.set("Select")
            if self.sup_list:
                self.cmb_supplier.set("Select")
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching data: {str(ex)}", parent=self.root)
            self.cat_list = ["Select"]
            self.sup_list = ["Select"]
            self.cmb_category['values'] = self.cat_list
            self.cmb_supplier['values'] = self.sup_list
        finally:
            con.close()
    
    def generate_pid(self):
        """Generate the next available Product ID"""
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            cur.execute("SELECT pid FROM product ORDER BY pid")
            rows = cur.fetchall()
            
            if not rows:
                self.var_pid.set("001")
                return
            
            existing_ids = []
            for row in rows:
                try:
                    pid_value = int(row[0]) if row[0] is not None else 0
                    existing_ids.append(pid_value)
                except (ValueError, TypeError):
                    continue
            
            if not existing_ids:
                self.var_pid.set("001")
                return
            
            for i in range(1, len(existing_ids) + 2):
                if i not in existing_ids:
                    self.var_pid.set(f"{i:03d}")
                    return
                    
            self.var_pid.set(f"{max(existing_ids) + 1:03d}")
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating PID: {str(ex)}", parent=self.root)
            self.var_pid.set("001")
        finally:
            con.close()
    
    def add_product(self):
        if self.var_ProdCat.get() == "Select" or self.var_sup.get() == "Select":
            messagebox.showerror("Error", "Category and Supplier are required", parent=self.root)
            return
            
        if not self.var_prod_name.get() or not self.txt_price.get() or not self.var_qty.get():
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            price = self.get_price_value()
            if price is None:
                messagebox.showerror("Error", "Invalid price format", parent=self.root)
                return
                
            qty = int(self.var_qty.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and Quantity must be an integer", parent=self.root)
            return

        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Check if product with same name already exists
            cur.execute("SELECT * FROM product WHERE Name=?", (self.var_prod_name.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Product already exists", parent=self.root)
                return

            pid_value = self.var_pid.get().lstrip('0') or '0'
            if not pid_value.isdigit():
                pid_value = '0'
                
            cur.execute("INSERT INTO product (pid, Category, Supplier, Name, Price, Quantity, Status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (int(pid_value), self.var_ProdCat.get(), self.var_sup.get(), 
                        self.var_prod_name.get(), price, qty, self.var_status.get()))
            con.commit()
            messagebox.showinfo("Success", "Product added successfully", parent=self.root)
            self.show_products()
            self.generate_pid()
            self.clear_product()
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding product: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def update_product(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Select a product to update", parent=self.root)
            return
            
        if self.var_ProdCat.get() == "Select" or self.var_sup.get() == "Select":
            messagebox.showerror("Error", "Category and Supplier are required", parent=self.root)
            return
            
        if not self.var_prod_name.get() or not self.txt_price.get() or not self.var_qty.get():
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            price = self.get_price_value()
            if price is None:
                messagebox.showerror("Error", "Invalid price format", parent=self.root)
                return
                
            qty = int(self.var_qty.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and Quantity must be an integer", parent=self.root)
            return

        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            pid_value = self.var_pid.get().lstrip('0') or '0'
            if not pid_value.isdigit():
                messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                return
                
            pid_num = int(pid_value)
            
            cur.execute("SELECT * FROM product WHERE Name=? AND pid!=?", 
                       (self.var_prod_name.get(), pid_num))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Product name already exists for another product", parent=self.root)
                return

            cur.execute("UPDATE product SET Category=?, Supplier=?, Name=?, Price=?, Quantity=?, Status=? WHERE pid=?",
                       (self.var_ProdCat.get(), self.var_sup.get(), self.var_prod_name.get(), 
                        price, qty, self.var_status.get(), pid_num))
            con.commit()
            messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
            self.show_products()
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating product: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def delete_product(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Select a product to delete", parent=self.root)
            return
            
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            pid_value = self.var_pid.get().lstrip('0') or '0'
            if not pid_value.isdigit():
                messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                return
                
            pid_num = int(pid_value)
            
            confirm = messagebox.askyesno("Confirm", "Do you really want to delete this product?", parent=self.root)
            if confirm:
                cur.execute("DELETE FROM product WHERE pid=?", (pid_num,))
                con.commit()
                messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                self.clear_product()
                self.renumber_pids()
                self.generate_pid()
                self.show_products()
        except Exception as ex:
            messagebox.showerror("Error", f"Error deleting product: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def renumber_pids(self):
        """Renumber all product IDs sequentially starting from 1"""
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            
            cur.execute("SELECT * FROM product ORDER BY pid")
            rows = cur.fetchall()
            
            for new_pid, row in enumerate(rows, 1):
                cur.execute("UPDATE product SET pid=? WHERE pid=?", (new_pid, row[0]))
            
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error renumbering products: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def clear_product(self):
        self.var_prod_name.set("")
        self.txt_price.delete(0, END)
        self.var_qty.set("")
        self.var_ProdCat.set("Select")
        self.var_sup.set("Select")
        self.var_status.set("Active")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.Product_Table.selection_remove(self.Product_Table.selection())
        self.generate_pid()
        self.price_without_format = ""
    
    def get_product_data(self, ev):
        f = self.Product_Table.focus()
        content = self.Product_Table.item(f)
        row = content['values']
        if row:
            pid_value = row[0]
            self.var_pid.set(f"{int(pid_value):03d}")
            self.var_ProdCat.set(row[1])
            self.var_sup.set(row[2])
            self.var_prod_name.set(row[3])
            
            try:
                # Extract numeric price from formatted string
                price_str = row[4].replace('Rs.', '').replace(',', '').strip()
                price_value = float(price_str)
                formatted_price = f"{price_value:,.2f}"
                self.txt_price.delete(0, END)
                self.txt_price.insert(0, formatted_price.replace('.00', ''))
            except:
                self.txt_price.delete(0, END)
                self.txt_price.insert(0, row[4])
                
            self.var_qty.set(row[5])
            self.var_status.set(row[6])
    
    def show_products(self):
        """Show all products"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product ORDER BY pid")
            rows = cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                formatted_pid = f"{row[0]:03d}"
                
                try:
                    formatted_price = f"Rs.{row[4]:,.2f}"
                except:
                    formatted_price = f"Rs.{row[4]}"
                
                formatted_row = (formatted_pid, row[1], row[2], row[3], formatted_price, row[5], row[6])
                self.Product_Table.insert('', END, values=formatted_row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading products: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def show_products_by_category(self, category_name):
        """Show products filtered by category"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product WHERE Category=? ORDER BY pid", (category_name,))
            rows = cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                formatted_pid = f"{row[0]:03d}"
                
                try:
                    formatted_price = f"Rs.{row[4]:,.2f}"
                except:
                    formatted_price = f"Rs.{row[4]}"
                
                formatted_row = (formatted_pid, row[1], row[2], row[3], formatted_price, row[5], row[6])
                self.Product_Table.insert('', END, values=formatted_row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading products: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def search_product(self):
        if self.var_searchby.get() == "Select":
            messagebox.showerror("Error", "Select search criteria", parent=self.root)
            return
            
        if not self.var_searchtxt.get().strip():
            self.show_products()
            return

        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            search_by = self.var_searchby.get()
            search_text = f"%{self.var_searchtxt.get().strip()}%"
            
            if search_by == "Category":
                cur.execute("SELECT * FROM product WHERE Category LIKE ? ORDER BY pid", (search_text,))
            elif search_by == "Supplier":
                cur.execute("SELECT * FROM product WHERE Supplier LIKE ? ORDER BY pid", (search_text,))
            elif search_by == "Name":
                cur.execute("SELECT * FROM product WHERE Name LIKE ? ORDER BY pid", (search_text,))
            
            rows = cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            
            if rows:
                for row in rows:
                    formatted_pid = f"{row[0]:03d}"
                    
                    try:
                        formatted_price = f"Rs.{row[4]:,.2f}"
                    except:
                        formatted_price = f"Rs.{row[4]}"
                    
                    formatted_row = (formatted_pid, row[1], row[2], row[3], formatted_price, row[5], row[6])
                    self.Product_Table.insert('', END, values=formatted_row)
            else:
                messagebox.showinfo("No Results", "No products found", parent=self.root)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching: {str(ex)}", parent=self.root)
        finally:
            con.close()


# Add this alias at the end of Product.py to make it compatible with Dashboard.py
ProductClass = IntegratedInventorySystem


if __name__ == "__main__":
    root = Tk()
    obj = IntegratedInventorySystem(root)
    root.mainloop()