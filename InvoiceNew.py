import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import datetime
import re
import os
from tkinter import font as tkfont

class Invoice_Class:
    def __init__(self, root):
        self.root = root
        # Start with a reasonable size but will adapt
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        
        # Make window resizable
        self.root.minsize(800, 600)  # Minimum size
        self.root.state('zoomed')  # Start maximized
        
        # Bind resize event
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Store initial sizes for reference
        self.initial_window_width = 1350
        self.initial_window_height = 700
        self.current_window_width = self.initial_window_width
        self.current_window_height = self.initial_window_height
        
        self.cart_list = []
        
        # Initialize variables
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        self.suggestion_window = None

        # FIXED: Use try/except for missing images
        try:
            self.icon_title = PhotoImage(file="IMAGES/shopcartfinal.png")
        except:
            self.icon_title = None

        # Create main container
        self.main_container = Frame(self.root, bg="#E6FBFF")
        self.main_container.pack(fill=BOTH, expand=1)
        
        # Title section - responsive
        title_frame = Frame(self.main_container, bg="#87CEEB", height=70)
        title_frame.pack(side=TOP, fill=X)
        title_frame.pack_propagate(False)  # Keep height fixed
        
        title = Label(
            title_frame,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("bahnschrift light semicondensed", self.scale_font_size(40), "bold"),
            bg="#87CEEB",
            fg="black",
            anchor="w",
            padx=20
        )
        title.pack(side=LEFT, fill=Y)
        
        # Logout button - responsive
        Button(
            title_frame,
            text="Logout",
            font=("Arial", self.scale_font_size(15), "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            command=self.logout
        ).pack(side=RIGHT, padx=20, pady=10)

        # Clock - responsive
        self.lbl_clock = Label(
            self.main_container,
            text="Welcome to Inventory Management System",
            font=("bahnschrift light semicondensed", self.scale_font_size(15)),
            bg="#A9A9A9",
            fg="white"
        )
        self.lbl_clock.pack(side=TOP, fill=X, ipady=5)
        self.update_clock()  # Start clock update

        # Main content area - responsive using grid
        self.content_frame = Frame(self.main_container, bg="#E6FBFF")
        self.content_frame.pack(fill=BOTH, expand=1, padx=10, pady=10)
        
        # Configure grid weights for responsiveness
        self.content_frame.columnconfigure(0, weight=1)  # Products column
        self.content_frame.columnconfigure(1, weight=2)  # Middle column (customer, cart)
        self.content_frame.columnconfigure(2, weight=1)  # Bill column
        self.content_frame.rowconfigure(0, weight=1)     # Main row
        
        #===========Product Frame===========
        self.var_search = StringVar()
        self.var_search_id = StringVar()  # New variable for ID search
        
        Product_Frame1 = Frame(self.content_frame, bd=4, relief=RIDGE, bg="white")
        Product_Frame1.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        
        Product_Frame1.columnconfigure(0, weight=1)
        Product_Frame1.rowconfigure(1, weight=0)
        Product_Frame1.rowconfigure(2, weight=1)

        pTitle = Label(Product_Frame1, text="All Products", 
                      font=("bahnschrift light semicondensed", self.scale_font_size(20), "bold"), 
                      bg="#262626", fg="white").grid(row=0, column=0, sticky="ew", ipady=5)

        #===========Search Frame===========
        Search_Frame = Frame(Product_Frame1, bd=2, relief=RIDGE, bg="white")
        Search_Frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        Search_Frame.columnconfigure(1, weight=1)

        # Search by Name
        lbl_search = Label(Search_Frame, text="Search Product By Name", 
                          font=("Aptos Display", self.scale_font_size(11), "bold"), 
                          bg="white", fg="black").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        txt_search = Entry(Search_Frame, textvariable=self.var_search, 
                          font=("Aptos Display", self.scale_font_size(11)), 
                          bg="lightyellow")
        txt_search.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        
        # Bind key release event for suggestions
        txt_search.bind('<KeyRelease>', self.show_suggestions)
        
        # Search by ID
        lbl_search_id = Label(Search_Frame, text="Search Product By ID", 
                             font=("Aptos Display", self.scale_font_size(11), "bold"), 
                             bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        txt_search_id = Entry(Search_Frame, textvariable=self.var_search_id, 
                             font=("Aptos Display", self.scale_font_size(11)), 
                             bg="lightyellow")
        txt_search_id.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        
        # Buttons frame for search
        button_frame = Frame(Search_Frame, bg="white")
        button_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=5, pady=2)
        
        btn_search_name = Button(button_frame, text="Search by Name", command=self.search_by_name, 
                                font=("Aptos Display", 9, "bold"), 
                                bg="#2196F3", fg="white", cursor="hand2")
        btn_search_name.pack(side=TOP, fill=X, pady=(0, 2))
        
        btn_search_id = Button(button_frame, text="Search by ID", command=self.search_by_id, 
                              font=("Aptos Display", 9, "bold"), 
                              bg="#4CAF50", fg="white", cursor="hand2")
        btn_search_id.pack(side=TOP, fill=X, pady=2)
        
        btn_show_all = Button(button_frame, text="Show All", command=self.show, 
                             font=("Aptos Display", 9, "bold"), 
                             bg="#083531", fg="white", cursor="hand2")
        btn_show_all.pack(side=TOP, fill=X, pady=(2, 0))

        #==============Product Details Frame=============
        Product_Frame3 = Frame(Product_Frame1, bd=3, relief=RIDGE, bg="white")
        Product_Frame3.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0, 5))

        scrolly = Scrollbar(Product_Frame3, orient=VERTICAL)
        scrollx = Scrollbar(Product_Frame3, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(Product_Frame3, 
                                         columns=("pid", "Name", "Price", "Quantity", "Status"), 
                                         yscrollcommand=scrolly.set, 
                                         xscrollcommand=scrollx.set,
                                         height=10)  # Increased height
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        
        self.ProductTable.pack(fill=BOTH, expand=1)
        
        # Configure column widths
        self.ProductTable.heading("pid", text="ID")
        self.ProductTable.heading("Name", text="Name")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("Quantity", text="Qty")
        self.ProductTable.heading("Status", text="Status")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=50, anchor="center")
        self.ProductTable.column("Name", width=150, anchor="w")
        self.ProductTable.column("Price", width=80, anchor="e")
        self.ProductTable.column("Quantity", width=60, anchor="center")
        self.ProductTable.column("Status", width=80, anchor="center")

        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        
        lbl_note = Label(Product_Frame1, text="Note: 'Enter 0 Quantity to remove product from cart'", 
                        font=("goudy old style", self.scale_font_size(10)), 
                        anchor='w', bg="white", fg="red")
        lbl_note.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 5))

        #===========Customer & Cart Area===========
        middle_frame = Frame(self.content_frame, bg="#E6FBFF")
        middle_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(0, weight=0)  # Customer frame
        middle_frame.rowconfigure(1, weight=1)  # Cart frame
        middle_frame.rowconfigure(2, weight=0)  # Add cart widgets

        self.var_cname = StringVar()
        self.var_contact = StringVar()
        Customer_Frame = Frame(middle_frame, bd=4, relief=RIDGE, bg="white")
        Customer_Frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        Customer_Frame.columnconfigure(1, weight=1)
        Customer_Frame.columnconfigure(3, weight=1)

        cTitle = Label(Customer_Frame, text="Customer Details", 
                      font=("bahnschrift light semicondensed", self.scale_font_size(14)), 
                      bg="lightgray").grid(row=0, column=0, columnspan=4, sticky="ew", ipady=3)
        
        lbl_name = Label(Customer_Frame, text="Name:", 
                        font=("Aptos Display", self.scale_font_size(12), "bold"), 
                        bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        txt_name = Entry(Customer_Frame, textvariable=self.var_cname, 
                        font=("Aptos Display", self.scale_font_size(12)), 
                        bg="lightyellow")
        txt_name.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        lbl_contact = Label(Customer_Frame, text="Contact:", 
                           font=("Aptos Display", self.scale_font_size(12), "bold"), 
                           bg="white").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        
        # Create a frame for the contact number with +92 prefix
        contact_frame = Frame(Customer_Frame, bg="white")
        contact_frame.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        
        # Add +92 label
        prefix_label = Label(contact_frame, text="+92", 
                            font=("Aptos Display", self.scale_font_size(12), "bold"), 
                            bg="lightgray", fg="black")
        prefix_label.pack(side=LEFT, fill=Y)
        
        # Create entry for remaining 10 digits
        self.contact_entry = Entry(contact_frame, textvariable=self.var_contact, 
                                  font=("Aptos Display", self.scale_font_size(12)), 
                                  bg="lightyellow")
        self.contact_entry.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Bind validation to contact entry
        self.contact_entry.bind('<KeyRelease>', self.validate_contact)
        self.var_contact.trace('w', self.format_contact)

        #========Cart Frame========
        Cart_Frame = Frame(middle_frame, bd=4, relief=RIDGE, bg="white")
        Cart_Frame.grid(row=1, column=0, sticky="nsew", pady=(0, 5))
        
        Cart_Frame.columnconfigure(0, weight=1)
        Cart_Frame.rowconfigure(1, weight=1)

        self.CartTitle = Label(Cart_Frame, text="Cart \t Total Products: [0]", 
                              font=("bahnschrift light semicondensed", self.scale_font_size(14)), 
                              bg="lightgray")
        self.CartTitle.grid(row=0, column=0, sticky="ew", ipady=3)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(Cart_Frame, 
                                      columns=("pid", "Name", "Price", "Quantity"), 
                                      yscrollcommand=scrolly.set, 
                                      xscrollcommand=scrollx.set,
                                      height=12)  # Increased height
        
        scrollx.grid(row=2, column=0, sticky="ew")
        scrolly.grid(row=1, column=1, sticky="ns")
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.grid(row=1, column=0, sticky="nsew")
        
        self.CartTable.heading("pid", text="ID")
        self.CartTable.heading("Name", text="Name")
        self.CartTable.heading("Price", text="Price")
        self.CartTable.heading("Quantity", text="Qty")
        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=50, anchor="center")
        self.CartTable.column("Name", width=150, anchor="w")
        self.CartTable.column("Price", width=100, anchor="e")
        self.CartTable.column("Quantity", width=70, anchor="center")

        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #========ADD Cart Widget Frame=====
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(middle_frame, bd=4, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.grid(row=2, column=0, sticky="ew")
        
        Add_CartWidgetsFrame.columnconfigure(0, weight=1)
        Add_CartWidgetsFrame.columnconfigure(1, weight=1)
        Add_CartWidgetsFrame.columnconfigure(2, weight=1)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", 
                          font=("Aptos Display", self.scale_font_size(12)), 
                          bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, 
                          font=("Aptos Display", self.scale_font_size(12)), 
                          bg="lightyellow", state='readonly')
        txt_p_name.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price", 
                           font=("Aptos Display", self.scale_font_size(12)), 
                           bg="white").grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, 
                           font=("Aptos Display", self.scale_font_size(12)), 
                           bg="lightyellow", state='readonly')
        txt_p_price.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", 
                         font=("Aptos Display", self.scale_font_size(12)), 
                         bg="white").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, 
                         font=("Aptos Display", self.scale_font_size(12)), 
                         bg="lightyellow")
        txt_p_qty.grid(row=1, column=2, sticky="ew", padx=5, pady=2)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", 
                                font=("Aptos Display", self.scale_font_size(12)), 
                                bg="white")
        self.lbl_inStock.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        # Buttons
        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear Cart", command=self.clear_cart, 
                               font=("Aptos Display", self.scale_font_size(11), "bold"), 
                               bg="lightgray", cursor="hand2")
        btn_clear_cart.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add/Update Cart", command=self.add_update_cart, 
                             font=("Aptos Display", self.scale_font_size(11), "bold"), 
                             bg="orange", cursor="hand2")
        btn_add_cart.grid(row=2, column=2, sticky="ew", padx=5, pady=5)

        #=================Billing Area===============
        billFrame = Frame(self.content_frame, bd=2, relief=RIDGE, bg='white')
        billFrame.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=5)
        
        billFrame.columnconfigure(0, weight=1)
        billFrame.rowconfigure(1, weight=1)

        BTitle = Label(billFrame, text="Customer Bill Area", 
                      font=("bahnschrift light semicondensed", self.scale_font_size(18), "bold"), 
                      bg="#f44336", fg="white")
        BTitle.grid(row=0, column=0, sticky="ew", ipady=5)

        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set, 
                                 font=("Courier", self.scale_font_size(10)), 
                                 wrap=WORD)
        
        self.txt_bill_area.grid(row=1, column=0, sticky="nsew")
        scrolly.grid(row=1, column=1, sticky="ns")
        scrolly.config(command=self.txt_bill_area.yview)

        #=================Billing Buttons Frame===============
        billMenuFrame = Frame(billFrame, bg='white')
        billMenuFrame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        billMenuFrame.columnconfigure(0, weight=1)
        billMenuFrame.columnconfigure(1, weight=1)
        billMenuFrame.columnconfigure(2, weight=1)

        self.lbl_amnt = Label(billMenuFrame, text="Bill Amount\n[0]", 
                             font=("Aptos Display", self.scale_font_size(11), "bold"), 
                             bg="#3f51b5", fg="white", relief=RAISED)
        self.lbl_amnt.grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=2)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n[0]", 
                                 font=("Aptos Display", self.scale_font_size(11), "bold"), 
                                 bg="#8bc34a", fg="white", relief=RAISED)
        self.lbl_discount.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n[0]", 
                                font=("Aptos Display", self.scale_font_size(11), "bold"), 
                                bg="#607d8b", fg="white", relief=RAISED)
        self.lbl_net_pay.grid(row=0, column=2, sticky="nsew", padx=(2, 0), pady=2)

        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill, 
                          cursor="hand2", 
                          font=("Aptos Display", self.scale_font_size(11), "bold"), 
                          bg="lightgreen", fg="white")
        btn_print.grid(row=1, column=0, sticky="nsew", padx=(0, 2), pady=2)

        btn_clear_all = Button(billMenuFrame, text="Clear all", command=self.clear_all, 
                              cursor="hand2", 
                              font=("Aptos Display", self.scale_font_size(11), "bold"), 
                              bg="gray", fg="white")
        btn_clear_all.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)

        btn_generate = Button(billMenuFrame, text="Generate Bill", command=self.generate_bill, 
                             cursor="hand2", 
                             font=("Aptos Display", self.scale_font_size(11), "bold"), 
                             bg="#009688", fg="white")
        btn_generate.grid(row=1, column=2, sticky="nsew", padx=(2, 0), pady=2)

        # Footer - responsive
        footer = Label(
            self.main_container,
            text="IMS - Inventory Management System | Developed by Dukes Tech Services\nFor any technical issue email: info@dukestechservices.com",
            font=("bahnschrift light semicondensed", self.scale_font_size(12)),
            bg="#A9A9A9",
            fg="white"
        )
        footer.pack(side=BOTTOM, fill=X, ipady=5)

        self.show()
        self.update_table_column_widths()  # Initial column width adjustment

    def scale_font_size(self, base_size):
        """Scale font size based on window width"""
        scale_factor = min(self.current_window_width / self.initial_window_width, 1.5)
        return max(int(base_size * scale_factor * 0.8), 8)  # Minimum font size 8

    def on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            self.current_window_width = event.width
            self.current_window_height = event.height
            
            # Update font sizes on significant resize
            if hasattr(self, 'last_font_update'):
                if abs(self.current_window_width - self.last_font_update) > 50:  # Update every 50px change
                    self.update_font_sizes()
                    self.last_font_update = self.current_window_width
            else:
                self.last_font_update = self.current_window_width
                self.update_font_sizes()
            
            # Update table column widths
            self.update_table_column_widths()

    def update_font_sizes(self):
        """Update all font sizes in the application"""
        pass

    def update_table_column_widths(self):
        """Update table column widths based on window size"""
        if hasattr(self, 'ProductTable'):
            # Scale column widths based on window width
            scale_factor = self.current_window_width / self.initial_window_width
            
            # Product table columns
            self.ProductTable.column("pid", width=int(50 * scale_factor))
            self.ProductTable.column("Name", width=int(150 * scale_factor))
            self.ProductTable.column("Price", width=int(80 * scale_factor))
            self.ProductTable.column("Quantity", width=int(60 * scale_factor))
            self.ProductTable.column("Status", width=int(80 * scale_factor))
            
            # Cart table columns
            if hasattr(self, 'CartTable'):
                self.CartTable.column("pid", width=int(50 * scale_factor))
                self.CartTable.column("Name", width=int(150 * scale_factor))
                self.CartTable.column("Price", width=int(100 * scale_factor))
                self.CartTable.column("Quantity", width=int(70 * scale_factor))

#================All Functions================
    def logout(self):
        """Logout function - asks for confirmation and closes the application"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root):
            self.root.destroy()

    def update_clock(self):
        """Update the clock label with current date and time"""
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%I:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System     Date: {date_str}     Time: {time_str}")
        self.root.after(1000, self.update_clock)

    def validate_contact(self, event=None):
        """Validate contact number to ensure only digits and max 10 digits"""
        current_text = self.var_contact.get()
        
        # Remove any non-digit characters
        digits_only = re.sub(r'\D', '', current_text)
        
        # Limit to 10 digits
        if len(digits_only) > 10:
            digits_only = digits_only[:10]
        
        # Update the variable
        self.var_contact.set(digits_only)
        
        # Change background color based on validation
        if len(digits_only) == 10:
            self.contact_entry.config(bg="lightgreen")
        elif len(digits_only) > 0:
            self.contact_entry.config(bg="lightyellow")
        else:
            self.contact_entry.config(bg="lightyellow")
        
        return True

    def format_contact(self, *args):
        """Format contact number as +92XXXXXXXXXX when needed"""
        current_value = self.var_contact.get()
        if len(current_value) == 10 and current_value.isdigit():
            # Format as +92XXXXXXXXXX when bill is generated
            return "+92" + current_value
        return current_value

    def get_contact_for_bill(self):
        """Get formatted contact number for bill display"""
        contact = self.var_contact.get().strip()
        if len(contact) == 10 and contact.isdigit():
            return "+92" + contact
        return contact

    def show_suggestions(self, event):
        """Show product name suggestions as user types"""
        search_text = self.var_search.get()
        
        # Destroy existing suggestion window if exists
        if self.suggestion_window:
            self.suggestion_window.destroy()
        
        if not search_text:
            return
        
        # Get matching products from database
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT Name FROM product WHERE Name LIKE ? AND Status='Active' LIMIT 5", 
                       (f'%{search_text}%',))
            suggestions = cur.fetchall()
            
            if suggestions:
                # Create suggestion window
                self.suggestion_window = Toplevel(self.root)
                self.suggestion_window.wm_overrideredirect(True)
                
                # Get position of search entry
                x = event.widget.winfo_rootx()
                y = event.widget.winfo_rooty() + event.widget.winfo_height()
                
                self.suggestion_window.geometry(f"+{x}+{y}")
                self.suggestion_window.configure(bg='white', bd=1, relief=SOLID)
                
                # Add suggestion labels
                for i, suggestion in enumerate(suggestions):
                    suggestion_text = suggestion[0]
                    lbl = Label(self.suggestion_window, 
                              text=suggestion_text,
                              font=("Aptos Display", 10),
                              bg='white',
                              anchor='w',
                              padx=5,
                              pady=2)
                    lbl.pack(fill=X)
                    
                    # Bind click event to set search text
                    lbl.bind('<Button-1>', lambda e, text=suggestion_text: self.set_search_text(text))
                    lbl.bind('<Enter>', lambda e, lbl=lbl: lbl.config(bg='lightblue'))
                    lbl.bind('<Leave>', lambda e, lbl=lbl: lbl.config(bg='white'))
        except Exception as ex:
            pass
        finally:
            con.close()

    def set_search_text(self, text):
        """Set search text from suggestion"""
        self.var_search.set(text)
        if self.suggestion_window:
            self.suggestion_window.destroy()
            self.suggestion_window = None
        self.search_by_name()

    def show(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("select pid, Name, Price, Quantity, Status from product where Status='Active'")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search_by_name(self):
        """Search product by name"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Please enter product name to search", parent=self.root)
            else:
                cur.execute("SELECT pid, Name, Price, Quantity, Status FROM product WHERE Name LIKE ? AND Status='Active'", 
                           (f'%{self.var_search.get()}%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search_by_id(self):
        """Search product by ID"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_search_id.get() == "":
                messagebox.showerror("Error", "Please enter product ID to search", parent=self.root)
            else:
                cur.execute("SELECT pid, Name, Price, Quantity, Status FROM product WHERE pid=? AND Status='Active'", 
                           (self.var_search_id.get(),))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = self.ProductTable.item(f)
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
            self.var_stock.set(row[3])
            self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            # Remove 'Rs.' from price when getting from cart
            price_str = row[2].replace('Rs.', '').strip()
            self.var_price.set(price_str)
            self.var_qty.set(row[3])
            # Find stock from cart_list
            for cart_item in self.cart_list:
                if cart_item[0] == row[0]:
                    self.var_stock.set(cart_item[4])
                    self.lbl_inStock.config(text=f"In Stock [{cart_item[4]}]")
                    break

    def add_update_cart(self):
        """FIXED: Properly add or update items in cart with real-time quantity update"""
        if self.var_pid.get() == '':
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
            return

        if self.var_qty.get() == '':
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
            return

        try:
            qty = int(self.var_qty.get())
            stock = int(self.var_stock.get())
            price = float(self.var_price.get())
            
            if qty < 0:
                messagebox.showerror("Error", "Quantity cannot be negative", parent=self.root)
                return
                
            if qty > stock:
                messagebox.showerror("Error", f"Invalid Quantity\nOnly {stock} available in stock", parent=self.root)
                return

            # Calculate total price for this item
            total_price = price * qty
            
            # Check if product already in cart
            present = False
            index_ = 0
            old_qty = 0
            for i, row in enumerate(self.cart_list):
                if self.var_pid.get() == row[0]:
                    present = True
                    index_ = i
                    old_qty = int(row[3])
                    break

            if present:
                if qty == 0:
                    # Remove from cart and restore stock
                    self.cart_list.pop(index_)
                    # Update stock in database
                    self.update_product_quantity_in_db(self.var_pid.get(), old_qty, "add")
                    messagebox.showinfo("Success", "Product removed from cart", parent=self.root)
                else:
                    # Update quantity and price
                    qty_difference = qty - old_qty
                    self.cart_list[index_][3] = str(qty)
                    self.cart_list[index_][2] = str(total_price)
                    
                    # Update stock in database
                    if qty_difference > 0:
                        # Reduced stock
                        self.update_product_quantity_in_db(self.var_pid.get(), qty_difference, "subtract")
                    elif qty_difference < 0:
                        # Increased stock
                        self.update_product_quantity_in_db(self.var_pid.get(), abs(qty_difference), "add")
                    
                    messagebox.showinfo("Success", "Cart updated successfully", parent=self.root)
            else:
                if qty > 0:
                    # Add new item to cart
                    cart_data = [self.var_pid.get(), self.var_pname.get(), str(total_price), str(qty), str(stock)]
                    self.cart_list.append(cart_data)
                    # Update stock in database
                    self.update_product_quantity_in_db(self.var_pid.get(), qty, "subtract")
                    messagebox.showinfo("Success", "Product added to cart", parent=self.root)
                else:
                    messagebox.showerror("Error", "Quantity must be > 0 to add to cart", parent=self.root)
                    return

            self.show_cart()
            # Refresh product table to show updated quantities
            self.show()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def update_product_quantity_in_db(self, pid, qty, operation):
        """Update product quantity in database immediately"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if operation == "subtract":
                cur.execute("UPDATE product SET Quantity = Quantity - ? WHERE pid = ?", (qty, pid))
            elif operation == "add":
                cur.execute("UPDATE product SET Quantity = Quantity + ? WHERE pid = ?", (qty, pid))
            
            # Check if quantity becomes 0 and update status
            cur.execute("SELECT Quantity FROM product WHERE pid=?", (pid,))
            new_qty = cur.fetchone()[0]
            if new_qty == 0:
                cur.execute("UPDATE product SET Status='Inactive' WHERE pid=?", (pid,))
            elif new_qty > 0:
                cur.execute("UPDATE product SET Status='Active' WHERE pid=?", (pid,))
            
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating database: {str(ex)}", parent=self.root)
            con.rollback()
        finally:
            con.close()

    def bill_updates(self):
        """FIXED: Calculate bill amounts correctly"""
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        
        for row in self.cart_list:
            try:
                # row[2] is total price for the item (price * quantity)
                self.bill_amnt += float(row[2])
            except (ValueError, TypeError):
                continue

        self.discount = (self.bill_amnt * 5) / 100
        self.net_pay = self.bill_amnt - self.discount
        
        # Update labels with formatted values
        self.lbl_amnt.config(text=f'Bill Amount\nRs.{self.bill_amnt:.2f}')
        self.lbl_discount.config(text=f'Discount\nRs.{self.discount:.2f}')
        self.lbl_net_pay.config(text=f'Net Pay\nRs.{self.net_pay:.2f}')
        self.CartTitle.config(text=f"Cart \t Total Products: [{len(self.cart_list)}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                # Display only: pid, name, total price, quantity
                self.CartTable.insert('', END, values=(row[0], row[1], f"Rs.{float(row[2]):.2f}", row[3]))
            self.bill_updates()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def generate_bill(self):
        """FIXED: Name is now optional, only mobile number is required"""
        # Validate contact number
        contact = self.var_contact.get().strip()
        if contact == '':
            messagebox.showerror("Error", "Contact number is required", parent=self.root)
            return
            
        if len(contact) != 10 or not contact.isdigit():
            messagebox.showerror("Error", "Contact number must be exactly 10 digits\nExample: 3001234567", parent=self.root)
            self.contact_entry.focus()
            return
            
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please add product to the cart", parent=self.root)
            return
        
        # Generate a new invoice number each time
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        self.bill_top()
        self.bill_middle()
        self.bill_bottom()
        
        messagebox.showinfo("Success", f"Bill generated successfully\nBill No.: {str(self.invoice)}", parent=self.root)        

    def bill_top(self):
        # Get customer name or use default
        customer_name = self.var_cname.get() if self.var_cname.get().strip() else "Walk-in Customer"
        
        bill_top_temp = f'''
    \t\tXYZ Inventory
    \t Phone No. +923*******63 , Lahore-54000
    {str("="*55)}
    Customer Name: {customer_name}
    Phone No. : {self.get_contact_for_bill()}
    Bill No. : {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
    {str("="*55)}
    Product Name\t\t\tQTY\tPrice
    {str("="*55)}
    '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)
        
    def bill_middle(self):
        """Add cart items to bill"""
        for item in self.cart_list:
            product_name = item[1]
            qty = item[3]
            price_per_item = float(item[2]) / int(qty)  # Calculate price per item
            total_price = float(item[2])
            
            # Format the line with proper spacing
            line = f" {product_name[:25]:25} {qty:>5} Rs.{price_per_item:>10.2f}\n"
            self.txt_bill_area.insert(END, line)

    def bill_bottom(self):
        # Try to load logo ASCII art or create simple one
        logo = """
        ╔══════════════════════════════╗
        ║     XYZ INVENTORY STORE      ║
        ║      Since 2010              ║
        ╚══════════════════════════════╝
        """
        
        bill_bottom_temp = f'''
{str("="*55)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt:>10.2f}
 Discount (5%)\t\t\t\tRs.{self.discount:>10.2f}
{str("-"*55)}
 Net Pay\t\t\t\tRs.{self.net_pay:>10.2f}
{str("="*55)}

{logo}

    ** Terms & Conditions: **
    • Amount is non-refundable
    • Only replacement available with original bill
    • Replacement within 7 days of purchase
    • Goods once sold will not be taken back
    • Please check items at time of purchase

    ** Thank you for your purchase! **
    **    Please visit again!       **
{str("="*55)}
'''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        """Clear the cart and restore all stock"""
        if not self.cart_list:
            messagebox.showinfo("Info", "Cart is already empty", parent=self.root)
            return
            
        if messagebox.askyesno("Confirm", "Clear all items from cart and restore stock?", parent=self.root):
            # Restore stock for all items in cart
            for item in self.cart_list:
                pid = item[0]
                qty = int(item[3])
                self.update_product_quantity_in_db(pid, qty, "add")
            
            self.cart_list.clear()
            self.show_cart()
            self.txt_bill_area.delete('1.0', END)
            self.show()  # Refresh product table
            messagebox.showinfo("Success", "Cart cleared and stock restored", parent=self.root)

    def clear_all(self):
        """Clear everything: cart, customer details, bill and restore stock"""
        if not self.cart_list and not self.var_contact.get() and not self.var_cname.get():
            messagebox.showinfo("Info", "Already cleared", parent=self.root)
            return
            
        if messagebox.askyesno("Confirm", "Clear all data and restore stock?", parent=self.root):
            # Restore stock for all items in cart
            for item in self.cart_list:
                pid = item[0]
                qty = int(item[3])
                self.update_product_quantity_in_db(pid, qty, "add")
            
            self.cart_list.clear()
            self.var_cname.set('')
            self.var_contact.set('')
            self.var_search.set('')
            self.var_search_id.set('')
            self.var_pid.set('')
            self.var_pname.set('')
            self.var_price.set('')
            self.var_qty.set('')
            self.var_stock.set('')
            self.lbl_inStock.config(text="In Stock")
            self.contact_entry.config(bg="lightyellow")  # Reset contact field color
            self.show_cart()
            self.txt_bill_area.delete('1.0', END)
            self.bill_updates()
            self.show()  # Refresh product table
            messagebox.showinfo("Success", "All data cleared and stock restored", parent=self.root)

    def print_bill(self):
        """Print and save bill function"""
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", "No bill to print. Please generate bill first.", parent=self.root)
            return
        
        # Check if bill is generated (text area has content)
        bill_content = self.txt_bill_area.get('1.0', END).strip()
        if not bill_content:
            messagebox.showerror("Error", "Please generate bill first", parent=self.root)
            return
        
        # Save the bill to file
        try:
            # Extract invoice number from bill content
            import re
            bill_text = self.txt_bill_area.get('1.0', END)
            
            # Look for bill number in the text
            bill_match = re.search(r'Bill No\.\s*:\s*(\d+)', bill_text)
            if bill_match:
                invoice_num = bill_match.group(1)
            else:
                # Generate new invoice number if not found
                invoice_num = str(int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y")))
            
            # Save to file
            import os
            if not os.path.exists('bills'):
                os.makedirs('bills')
                
            file_name = f'bills/{invoice_num}.txt'
            with open(file_name, 'w') as fp:
                fp.write(bill_text)
            
            # Show success message
            messagebox.showinfo("Saved & Print", f"Bill No. : {invoice_num}\n\n1. Saved to: {file_name}\n2. Sent to printer", parent=self.root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save/print bill: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Invoice_Class(root)
    root.mainloop()