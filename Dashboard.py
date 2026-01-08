from datetime import datetime
import tkinter
from tkinter import *
from PIL import Image, ImageTk
from Employee import EmployeeClass
from Supplier import SupplierClass
from Category import CategoryClass
# FIXED: Import the correct class name from Product.py
from Product import IntegratedInventorySystem as ProductClass
from InvoiceNew import Invoice_Class  # ADDED THIS LINE
from Sales import SalesClass
import sqlite3
from tkinter import messagebox
import time
import os
import datetime
import json
import hashlib
import os.path

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        
        # Hide main window initially
        self.root.withdraw()
        
        # User data file
        self.user_data_file = "user_data.json"
        self.current_user = None
        self.is_guest = False
        
        # Show login screen first
        self.show_login_screen()

    def init_main_window(self):
        """Initialize the main window after login"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show the window
        self.root.deiconify()
        
        # FIXED: Use try/except for missing images
        try:
            self.icon_title = PhotoImage(file="IMAGES/shopcartfinal.png")
        except:
            self.icon_title = None

        # Title bar frame
        title_frame = Frame(self.root, bg="#87CEEB", height=70)
        title_frame.place(x=0, y=0, relwidth=1)
        
        # Title label on left
        title = Label(
            title_frame,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("bahnschrift light semicondensed", 30, "bold"),  # Reduced font size
            bg="#87CEEB",
            fg="black",
            anchor="w",
            padx=20
        )
        title.pack(side=LEFT, fill=Y)
        
        # User info label in middle
        user_type = "Guest" if self.is_guest else "User"
        self.user_label = Label(
            title_frame,
            text=f"Logged in as: {self.current_user} ({user_type})",
            font=("Arial", 12),
            bg="#87CEEB",
            fg="white"
        )
        self.user_label.pack(side=LEFT, expand=True, padx=20)
        
        # Logout button on right
        logout_text = "Logout" if not self.is_guest else "Exit Guest Mode"
        Button(
            title_frame,
            text=logout_text,
            font=("Arial", 12, "bold"),
            bg="red" if not self.is_guest else "orange",
            fg="white",
            cursor="hand2",
            command=self.logout
        ).pack(side=RIGHT, padx=20)

        # Clock
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System     Date: --/--/----     Time: --:--:--",
            font=("bahnschrift light semicondensed", 15),
            bg="#A9A9A9",
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Left menu
        menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        menu_frame.place(x=0, y=120, width=200, height=580)  # Adjusted height

        # FIXED: Image loading
        try:
            logo = Image.open("IMAGES/inventory management logo.png")
            logo = logo.resize((200, 200), Image.LANCZOS)
            self.menu_logo_img = ImageTk.PhotoImage(logo)
        except:
            self.menu_logo_img = None

        Label(menu_frame, image=self.menu_logo_img).pack(side=TOP, fill=X)

        Label(menu_frame, text="MENU", font=("Impact", 20), bg="#B0C4DE").pack(side=TOP, fill=X)

        try:
            self.icon_side = PhotoImage(file="IMAGES/pointerarr.png")
        except:
            self.icon_side = None

        # Buttons - disable for guest if needed
        btn_state = NORMAL if not self.is_guest else DISABLED
        
        Button(menu_frame, text="Employee", command=self.Employee, image=self.icon_side,
               compound=LEFT, padx=5, anchor="w",
               font=("Aptos Display", 16, "bold"),  # Reduced font size
               bg="white", bd=6, cursor="hand2", state=btn_state).pack(side=TOP, fill=X)

        Button(menu_frame, text="Supplier", command=self.Supplier, image=self.icon_side,
               compound=LEFT, padx=5, anchor="w",
               font=("Aptos Display", 16, "bold"),
               bg="white", bd=6, cursor="hand2", state=btn_state).pack(side=TOP, fill=X)

#        Button(menu_frame, text="Stock / Inventory", command=self.Category, image=self.icon_side,
 #              compound=LEFT, padx=5, anchor="w",
#               font=("Aptos Display", 16, "bold"),
#               bg="white", bd=6, cursor="hand2", state=btn_state).pack(side=TOP, fill=X)#

        Button(menu_frame, text="Stock/Inventory",command=self.Product, image=self.icon_side,
               compound=LEFT, padx=5, anchor="w",
               font=("Aptos Display", 16, "bold"),
               bg="white", bd=6, cursor="hand2", state=btn_state).pack(side=TOP, fill=X)

        # ADDED INVOICE BUTTON HERE
        Button(menu_frame, text="Invoice",command=self.Invoice, image=self.icon_side,
               compound=LEFT, padx=5, anchor="w",
               font=("Aptos Display", 16, "bold"),
               bg="white", bd=6, cursor="hand2", state=btn_state).pack(side=TOP, fill=X)

        Button(menu_frame, text="Sales",command=self.Sales, image=self.icon_side,
               compound=LEFT, padx=5, anchor="w",
               font=("Aptos Display", 16, "bold"),
               bg="white", bd=6, cursor="hand2", state=btn_state).pack(side=TOP, fill=X)

        Button(menu_frame, text="Exit", image=self.icon_side,
               compound=LEFT, padx=5, anchor="w",
               font=("Aptos Display", 16, "bold"),
               bg="white", bd=6, cursor="hand2",
               command=self.root.destroy).pack(side=TOP, fill=X)

        # Dashboard boxes - show dummy data for guest
        if self.is_guest:
            self.lbl_employee = Label(self.root, text="Guest Mode\nDemo Dashboard",
                                      bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                      font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_employee.place(x=300, y=180, height=180, width=300)
            
            self.lbl_supplier = Label(self.root, text="Features Disabled\nSign up to access",
                                      bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                      font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_supplier.place(x=650, y=180, height=180, width=300)
            
            self.lbl_category = Label(self.root, text="Guest Account\nLimited Access",
                                      bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                      font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_category.place(x=1000, y=180, height=180, width=300)
            
            self.lbl_product = Label(self.root, text="Create Account\nFor Full Features",
                                     bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                     font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_product.place(x=475, y=400, height=180, width=300)
            
            # ADDED INVOICE DASHBOARD BOX FOR GUEST
            self.lbl_invoice = Label(self.root, text="Invoice System\nDisabled for Guest",
                                     bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                     font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_invoice.place(x=825, y=400, height=180, width=300)
            
            self.lbl_sales = Label(self.root, text="IMS Demo\nVersion 1.0",
                                   bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                   font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_sales.place(x=475, y=620, height=180, width=300)
        else:
            # Regular dashboard boxes for logged-in users
            self.lbl_employee = Label(self.root, text="Total Employees\n[ 0 ]",
                                      bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                      font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_employee.place(x=300, y=180, height=180, width=300)

            self.lbl_supplier = Label(self.root, text="Total Suppliers\n[ 0 ]",
                                      bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                      font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_supplier.place(x=650, y=180, height=180, width=300)

            self.lbl_category = Label(self.root, text="Total Categories\n[ 0 ]",
                                      bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                      font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_category.place(x=1000, y=180, height=180, width=300)

            self.lbl_product = Label(self.root, text="Total Products\n[ 0 ]",
                                     bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                     font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_product.place(x=475, y=400, height=180, width=300)

            # ADDED INVOICE DASHBOARD BOX FOR LOGGED-IN USERS
            self.lbl_invoice = Label(self.root, text="Invoices\n[ 0 ]",
                                     bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                     font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_invoice.place(x=825, y=400, height=180, width=300)

            self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]",
                                   bd=6.5, relief=RIDGE, bg="#404040", fg="white",
                                   font=("Contemporary Sans-Serif", 18, "bold"))
            self.lbl_sales.place(x=475, y=620, height=180, width=300)

        # Footer
        footer_text = "IMS - Inventory Management System | Demo Mode" if self.is_guest else "IMS - Inventory Management System | Developed by Dukes Tech Services\nFor any technical issue email: info@dukestechservices.com"
        
        Label(
            self.root,
            text=footer_text,
            font=("bahnschrift light semicondensed", 15),
            bg="#A9A9A9",
            fg="white"
        ).pack(side=BOTTOM, fill=X)

        if not self.is_guest:
            self.update_content()

    def show_login_screen(self):
        """Display login/signup screen"""
        login_window = Toplevel(self.root)
        login_window.title("Login - Inventory Management System")
        login_window.geometry("500x600+500+200")
        login_window.config(bg="#E6FBFF")
        login_window.resizable(False, False)
        
        # Make it modal
        login_window.grab_set()
        login_window.protocol("WM_DELETE_WINDOW", lambda: self.on_login_close(login_window))
        
        # Title
        Label(login_window, text="IMS LOGIN", font=("bahnschrift", 30, "bold"), 
              bg="#87CEEB", fg="black").pack(fill=X, pady=20)
        
        # Create notebook for tabs
        notebook = tkinter.ttk.Notebook(login_window)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Login Tab
        login_frame = Frame(notebook, bg="#E6FBFF")
        notebook.add(login_frame, text="Login")
        self.create_login_tab(login_frame, login_window)
        
        # Signup Tab
        signup_frame = Frame(notebook, bg="#E6FBFF")
        notebook.add(signup_frame, text="Sign Up")
        self.create_signup_tab(signup_frame, login_window)
        
        # Guest Tab
        guest_frame = Frame(notebook, bg="#E6FBFF")
        notebook.add(guest_frame, text="Guest Access")
        self.create_guest_tab(guest_frame, login_window)

    def create_login_tab(self, parent, login_window):
        """Create login tab content"""
        Label(parent, text="Username:", font=("Arial", 15), 
              bg="#E6FBFF").place(x=50, y=50)
        self.login_username = Entry(parent, font=("Arial", 15), bd=3)
        self.login_username.place(x=50, y=80, width=300)
        
        Label(parent, text="Password:", font=("Arial", 15), 
              bg="#E6FBFF").place(x=50, y=130)
        self.login_password = Entry(parent, font=("Arial", 15), bd=3, show="*")
        self.login_password.place(x=50, y=160, width=300)
        
        Button(parent, text="Login", font=("Arial", 15, "bold"),
               bg="green", fg="white", cursor="hand2",
               command=lambda: self.attempt_login(login_window)
               ).place(x=150, y=220, width=100, height=40)

    def create_signup_tab(self, parent, login_window):
        """Create signup tab content"""
        Label(parent, text="Choose Username:", font=("Arial", 15), 
              bg="#E6FBFF").place(x=50, y=30)
        self.signup_username = Entry(parent, font=("Arial", 15), bd=3)
        self.signup_username.place(x=50, y=60, width=300)
        
        Label(parent, text="Password:", font=("Arial", 15), 
              bg="#E6FBFF").place(x=50, y=100)
        self.signup_password = Entry(parent, font=("Arial", 15), bd=3, show="*")
        self.signup_password.place(x=50, y=130, width=300)
        
        Label(parent, text="Confirm Password:", font=("Arial", 15), 
              bg="#E6FBFF").place(x=50, y=170)
        self.signup_confirm = Entry(parent, font=("Arial", 15), bd=3, show="*")
        self.signup_confirm.place(x=50, y=200, width=300)
        
        Button(parent, text="Create Account", font=("Arial", 15, "bold"),
               bg="blue", fg="white", cursor="hand2",
               command=lambda: self.attempt_signup(login_window)
               ).place(x=150, y=250, width=150, height=40)

    def create_guest_tab(self, parent, login_window):
        """Create guest access tab"""
        Label(parent, text="Guest Access", font=("Arial", 20, "bold"), 
              bg="#E6FBFF").place(x=150, y=50)
        
        Label(parent, text="Access the system in demo mode:", 
              font=("Arial", 12), bg="#E6FBFF").place(x=50, y=100)
        
        Label(parent, text="• Limited functionality\n• No data saving\n• Demo data only\n• Perfect for testing", 
              font=("Arial", 11), bg="#E6FBFF", justify=LEFT).place(x=80, y=130)
        
        Button(parent, text="Enter as Guest", font=("Arial", 15, "bold"),
               bg="orange", fg="white", cursor="hand2",
               command=lambda: self.enter_as_guest(login_window)
               ).place(x=150, y=250, width=150, height=40)

    def attempt_login(self, login_window):
        """Handle login attempt"""
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password", 
                               parent=login_window)
            return
        
        if self.authenticate_user(username, password):
            self.current_user = username
            self.is_guest = False
            login_window.destroy()
            self.init_main_window()
            messagebox.showinfo("Welcome", f"Welcome back, {username}!", parent=self.root)
        else:
            messagebox.showerror("Error", "Invalid username or password", parent=login_window)

    def attempt_signup(self, login_window):
        """Handle signup attempt"""
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        
        if not username or not password or not confirm:
            messagebox.showerror("Error", "Please fill all fields", parent=login_window)
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match", parent=login_window)
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters", 
                               parent=login_window)
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", 
                               parent=login_window)
            return
        
        if self.user_exists(username):
            messagebox.showerror("Error", "Username already exists", parent=login_window)
            return
        
        if self.create_user(username, password):
            messagebox.showinfo("Success", "Account created successfully!", parent=login_window)
            # Auto login after signup
            self.current_user = username
            self.is_guest = False
            login_window.destroy()
            self.init_main_window()
            messagebox.showinfo("Welcome", f"Welcome, {username}!", parent=self.root)
        else:
            messagebox.showerror("Error", "Failed to create account", parent=login_window)

    def enter_as_guest(self, login_window):
        """Enter as guest user"""
        self.current_user = "Guest"
        self.is_guest = True
        login_window.destroy()
        self.init_main_window()
        messagebox.showinfo("Guest Mode", "You are now in guest mode with limited functionality.", 
                          parent=self.root)

    def user_exists(self, username):
        """Check if user exists"""
        if not os.path.exists(self.user_data_file):
            return False
        
        try:
            with open(self.user_data_file, 'r') as f:
                users = json.load(f)
                return username in users
        except:
            return False

    def create_user(self, username, password):
        """Create new user account"""
        users = {}
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    users = json.load(f)
            except:
                users = {}
        
        # Simple hash for password (use better methods in production)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users[username] = {
            'password_hash': password_hash,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        try:
            with open(self.user_data_file, 'w') as f:
                json.dump(users, f, indent=2)
            return True
        except:
            return False

    def authenticate_user(self, username, password):
        """Authenticate user"""
        if not os.path.exists(self.user_data_file):
            return False
        
        try:
            with open(self.user_data_file, 'r') as f:
                users = json.load(f)
                
            if username in users:
                stored_hash = users[username]['password_hash']
                input_hash = hashlib.sha256(password.encode()).hexdigest()
                return stored_hash == input_hash
        except:
            return False
        
        return False

    def on_login_close(self, login_window):
        """Handle login window close"""
        if messagebox.askyesno("Exit", "Close the application?", parent=login_window):
            login_window.destroy()
            self.root.destroy()
        else:
            login_window.grab_set()

    def logout(self):
        """Logout from current session"""
        if messagebox.askyesno("Confirm", "Logout from system?", parent=self.root):
            self.root.withdraw()
            self.current_user = None
            self.is_guest = False
            self.show_login_screen()

    # Window openers (only for logged-in users)
    def Employee(self):
        if not self.is_guest:
            self.new_win = Toplevel(self.root)
            self.new_obj = EmployeeClass(self.new_win)
        else:
            messagebox.showinfo("Guest Mode", "This feature is disabled in guest mode. Please sign up for full access.", parent=self.root)

    def Supplier(self):
        if not self.is_guest:
            self.new_win = Toplevel(self.root)
            self.new_obj = SupplierClass(self.new_win)
        else:
            messagebox.showinfo("Guest Mode", "This feature is disabled in guest mode. Please sign up for full access.", parent=self.root)

#    def Category(self):
#        if not self.is_guest:
#            self.new_win = Toplevel(self.root)
#            self.new_obj = CategoryClass(self.new_win)
#        else:
#            messagebox.showinfo("Guest Mode", "This feature is disabled in guest mode. Please sign up for full access.", parent=self.root)

    def Product(self):
        if not self.is_guest:
            self.new_win = Toplevel(self.root)
            self.new_obj = ProductClass(self.new_win)
        else:
            messagebox.showinfo("Guest Mode", "This feature is disabled in guest mode. Please sign up for full access.", parent=self.root)

    # ADDED INVOICE METHOD HERE
    def Invoice(self):
        if not self.is_guest:
            self.new_win = Toplevel(self.root)
            self.new_obj = Invoice_Class(self.new_win)
        else:
            messagebox.showinfo("Guest Mode", "This feature is disabled in guest mode. Please sign up for full access.", parent=self.root)

    def Sales(self):
        if not self.is_guest:
            self.new_win = Toplevel(self.root)
            self.new_obj = SalesClass(self.new_win)
        else:
            messagebox.showinfo("Guest Mode", "This feature is disabled in guest mode. Please sign up for full access.", parent=self.root)

    def update_content(self):
        """Update dashboard content for logged-in users"""
        if self.is_guest:
            return  # Don't update for guest users
            
        con=sqlite3.connect(database=r'Possystem.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from Product")
            product=cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n[ {str(len(product))} ]")

            cur.execute("Select * from Supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[ {str(len(supplier))} ]")

            cur.execute("Select * from Category")
            category=cur.fetchall()
            self.lbl_category.config(text=f"Total Categories\n[ {str(len(category))} ]")

            cur.execute("Select * from Employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f"Total Employees\n[ {str(len(employee))} ]")

            # ADDED INVOICE COUNT UPDATE
            # Assuming you have an 'invoices' table in your database
            # If not, you might need to create one or adjust this query
            try:
                cur.execute("Select * from invoices")
                invoices = cur.fetchall()
                self.lbl_invoice.config(text=f"Invoices\n[ {str(len(invoices))} ]")
            except:
                # If invoices table doesn't exist yet, show 0
                self.lbl_invoice.config(text="Invoices\n[ 0 ]")

            bill_count = len(os.listdir('bills')) if os.path.exists('bills') else 0
            self.lbl_sales.config(text=f"Total Sales\n[{str(bill_count)}]")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%I:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System     Date: {date_str}     Time: {time_str}")
        self.root.after(1000, self.update_content)

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()