from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import locale

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
        self.var_qty = StringVar()
        self.var_status = StringVar()
        
        # Price variables
        self.price_without_format = ""  # Store raw price without commas
        
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
        lbl_product_name = Label(product_Frame, text="Prod Name", font=("goudy old style", 15), bg="white").place(x=30, y=130)
        lbl_price = Label(product_Frame, text="Prod Price", font=("goudy old style", 15), bg="white").place(x=30, y=180)
        lbl_quantity = Label(product_Frame, text="Prod Quantity", font=("goudy old style", 15), bg="white").place(x=30, y=230)
        lbl_status = Label(product_Frame, text="Prod Status", font=("goudy old style", 15), bg="white").place(x=30, y=280)

        # ===========Dropdowns and Entries==========
        self.cmb_category = ttk.Combobox(product_Frame, textvariable=self.var_cat, 
                                        state="readonly", justify=CENTER, font=("Times new Roman", 12))
        self.cmb_category.place(x=150, y=30, width=200)

        self.cmb_supplier = ttk.Combobox(product_Frame, textvariable=self.var_sup, 
                                        state="readonly", justify=CENTER, font=("Times new Roman", 12))
        self.cmb_supplier.place(x=150, y=80, width=200)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("Times new Roman", 12), bg="lightyellow")
        txt_name.place(x=150, y=130, width=200)

        # Price frame with Rs symbol
        price_frame = Frame(product_Frame, bg="white")
        price_frame.place(x=150, y=180, width=200, height=30)
        
        # Rs label
        rs_label = Label(price_frame, text="Rs.", font=("Times new Roman", 12, "bold"), bg="white")
        rs_label.pack(side=LEFT, padx=(0, 5))
        
        # Price entry with comma formatting
        self.txt_price = Entry(price_frame, font=("Times new Roman", 12), bg="lightyellow", justify=RIGHT)
        self.txt_price.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        # Bind events for comma formatting
        self.txt_price.bind('<KeyRelease>', self.format_price_with_commas)
        self.txt_price.bind('<FocusIn>', self.on_price_focus_in)
        self.txt_price.bind('<FocusOut>', self.on_price_focus_out)

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

    def format_price_with_commas(self, event=None):
        """Format price with commas as user types"""
        try:
            # Get current text and cursor position
            current_text = self.txt_price.get()
            cursor_pos = self.txt_price.index(INSERT)
            
            # Remove existing commas and non-numeric characters except decimal point
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
            
            # Save the raw price (without commas)
            self.price_without_format = clean_text
            
            # Format with commas
            if clean_text:
                # Split integer and decimal parts
                if '.' in clean_text:
                    integer_part, decimal_part = clean_text.split('.')
                else:
                    integer_part = clean_text
                    decimal_part = ''
                
                # Add commas to integer part
                formatted_integer = ''
                for i, digit in enumerate(reversed(integer_part)):
                    if i > 0 and i % 3 == 0:
                        formatted_integer = ',' + formatted_integer
                    formatted_integer = digit + formatted_integer
                
                # Combine integer and decimal parts
                formatted_price = formatted_integer
                if decimal_part:
                    formatted_price += '.' + decimal_part
                
                # Update the entry
                self.txt_price.delete(0, END)
                self.txt_price.insert(0, formatted_price)
                
                # Try to restore cursor position
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
            # Clear existing lists
            self.cat_list.clear()
            self.sup_list.clear()
            
            # Check if Category table has Status column
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
        """Generate the next available PID (not based on max, but based on gaps)"""
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            cur.execute("SELECT pid FROM product ORDER BY pid")
            rows = cur.fetchall()
            
            if not rows:
                self.var_pid.set("001")
                return
            
            # Convert all pids to integers (they might be strings or integers)
            existing_ids = []
            for row in rows:
                try:
                    # Convert to int whether it's string or already int
                    pid_value = int(row[0]) if row[0] is not None else 0
                    existing_ids.append(pid_value)
                except (ValueError, TypeError):
                    # Skip invalid entries
                    continue
            
            if not existing_ids:
                self.var_pid.set("001")
                return
            
            # Look for gaps in the sequence
            for i in range(1, len(existing_ids) + 2):  # +2 to go one beyond current max
                if i not in existing_ids:
                    self.var_pid.set(f"{i:03d}")
                    return
                    
            # If no gaps found, use next number after max
            self.var_pid.set(f"{max(existing_ids) + 1:03d}")
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating PID: {str(ex)}", parent=self.root)
            self.var_pid.set("001")
        finally:
            if 'con' in locals():
                con.close()

    def add(self):
        if self.var_cat.get() == "Select" or self.var_sup.get() == "Select":
            messagebox.showerror("Error", "Category and Supplier are required", parent=self.root)
            return
            
        if not self.var_name.get() or not self.txt_price.get() or not self.var_qty.get():
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
            cur.execute("SELECT * FROM product WHERE Name=?", (self.var_name.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Product already exists", parent=self.root)
                return

            # Use the generated PID
            pid_value = self.var_pid.get().lstrip('0') or '0'  # Remove leading zeros
            if not pid_value.isdigit():
                pid_value = '0'
                
            # Insert with the specified PID
            cur.execute("INSERT INTO product (pid, Category, Supplier, Name, Price, Quantity, Status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (int(pid_value), self.var_cat.get(), self.var_sup.get(), 
                        self.var_name.get(), price, qty, self.var_status.get()))
            con.commit()
            messagebox.showinfo("Success", "Product added successfully", parent=self.root)
            self.show()
            self.generate_pid()  # Generate next available PID
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
            
        if not self.var_name.get() or not self.txt_price.get() or not self.var_qty.get():
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
            # Get the PID (it's already stored as integer in database)
            pid_value = self.var_pid.get().lstrip('0') or '0'
            if not pid_value.isdigit():
                messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                return
                
            pid_num = int(pid_value)
            
            # Check if product with same name exists for other product
            cur.execute("SELECT * FROM product WHERE Name=? AND pid!=?", 
                       (self.var_name.get(), pid_num))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Product name already exists for another product", parent=self.root)
                return

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
            # Get the PID
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
                self.clear()
                # After deletion, we need to regenerate IDs for the remaining products
                self.renumber_pids()
                self.generate_pid()  # Generate new PID for next addition
                self.show()  # Refresh the display
        except Exception as ex:
            messagebox.showerror("Error", f"Error deleting product: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def renumber_pids(self):
        """Renumber all product IDs sequentially starting from 1"""
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            
            # Get all products ordered by current pid
            cur.execute("SELECT * FROM product ORDER BY pid")
            rows = cur.fetchall()
            
            # Renumber sequentially starting from 1
            for new_pid, row in enumerate(rows, 1):
                cur.execute("UPDATE product SET pid=? WHERE pid=?", (new_pid, row[0]))
            
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error renumbering products: {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

    def clear(self):
        self.var_name.set("")
        self.txt_price.delete(0, END)
        self.var_qty.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_status.set("Active")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.Product_Table.selection_remove(self.Product_Table.selection())
        self.generate_pid()
        self.price_without_format = ""

    def get_data(self, ev):
        f = self.Product_Table.focus()
        content = self.Product_Table.item(f)
        row = content['values']
        if row:
            # Display PID without formatting
            pid_value = row[0]
            # Convert to string and pad with zeros if needed
            self.var_pid.set(f"{int(pid_value):03d}")
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            
            # Format price with commas for display
            try:
                price_value = float(row[4])
                # Format with commas
                formatted_price = f"{price_value:,.2f}"
                self.txt_price.delete(0, END)
                self.txt_price.insert(0, formatted_price.replace('.00', ''))
            except:
                self.txt_price.delete(0, END)
                self.txt_price.insert(0, row[4])
                
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
                # Format PID with leading zeros for display
                formatted_pid = f"{row[0]:03d}"
                
                # Format price with commas for display
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
                    
                    # Format price with commas for display
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


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()