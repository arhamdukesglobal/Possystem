import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import datetime
import re

class Invoice_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.cart_list = []
        
        # Initialize variables
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0

        # FIXED: Use try/except for missing images
        try:
            self.icon_title = PhotoImage(file="IMAGES/shopcartfinal.png")
        except:
            self.icon_title = None

        title = Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("bahnschrift light semicondensed", 40, "bold"),
            bg="#87CEEB",
            fg="black",
            anchor="w",  # Changed to left align
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout button - FIXED: Moved to right side and added command
        Button(
            self.root,
            text="Logout",
            font=("Arial", 15, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            command=self.logout
        ).place(x=1200, y=10, height=50, width=150)  # Adjusted position

        # Clock - FIXED: Update time function
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System",
            font=("bahnschrift light semicondensed", 15),
            bg="#A9A9A9",
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_clock()  # Start clock update

        #===========Product Frame===========
        self.var_search = StringVar()
        Product_Frame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Product_Frame1.place(x=10, y=110, width=480, height=550)

        pTitle = Label(Product_Frame1, text="All Products", font=("bahnschrift light semicondensed", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)

        Product_Frame2 = Frame(Product_Frame1, bd=2, relief=RIDGE, bg="white")
        Product_Frame2.place(x=2, y=42, width=450, height=90)

        lbl_search = Label(Product_Frame2, text="Search Product | By Name", font=("Aptos Display", 15, "bold"), bg="white", fg="black").place(x=2, y=5)
        
        lbl_search2 = Label(Product_Frame2, text="Product Name", font=("Aptos Display", 15, "bold"), bg="white").place(x=5, y=45)
        txt_search = Entry(Product_Frame2, textvariable=self.var_search, font=("Aptos Display", 15, "bold"), bg="lightyellow").place(x=150, y=47, width=150, height=22)
        btn_Search = Button(Product_Frame2, text="Search", command=self.search, font=("Aptos Display", 15, "bold"), bg="#2196F3", fg="white", cursor="hand2").place(x=310, y=45, width=100, height=30)
        btn_show_all = Button(Product_Frame2, text="Show All", command=self.show, font=("Aptos Display", 15, "bold"), bg="#083531", fg="white", cursor="hand2").place(x=310, y=10, width=100, height=30)

        #==============Product Details Frame=============
        Product_Frame3 = Frame(Product_Frame1, bd=3, relief=RIDGE, bg="white")
        Product_Frame3.place(x=2, y=140, width=450, height=375)

        scrolly = Scrollbar(Product_Frame3, orient=VERTICAL)
        scrollx = Scrollbar(Product_Frame3, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(Product_Frame3, columns=("pid", "Name", "Price", "Quantity", "Status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        
        self.ProductTable.heading("pid", text="Prod_ID")
        self.ProductTable.heading("Name", text="Name")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("Quantity", text="Quantity")
        self.ProductTable.heading("Status", text="Status")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=40)
        self.ProductTable.column("Name", width=100)
        self.ProductTable.column("Price", width=100)
        self.ProductTable.column("Quantity", width=40)
        self.ProductTable.column("Status", width=90)

        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        lbl_note = Label(Product_Frame3, text="Note: 'Enter 0 Quantity to remove product from the cart'", font=("goudy old style", 12), anchor='w', bg="white", fg="red").pack(side=BOTTOM, fill=X)

        #===========Customer Frame===========
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        Customer_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Customer_Frame.place(x=500, y=110, width=550, height=70)

        cTitle = Label(Customer_Frame, text="Customer Details", font=("bahnschrift light semicondensed", 15), bg="lightgray").pack(side=TOP, fill=X)
        lbl_name = Label(Customer_Frame, text="Customer Name", font=("Aptos Display", 15, "bold"), bg="white").place(x=5, y=35)
        txt_name = Entry(Customer_Frame, textvariable=self.var_cname, font=("Aptos Display", 15), bg="lightyellow").place(x=160, y=37, width=150, height=22)

        lbl_contact = Label(Customer_Frame, text="Contact No.", font=("Aptos Display", 15, "bold"), bg="white").place(x=270, y=35)
        
        # Create a frame for the contact number with +92 prefix
        contact_frame = Frame(Customer_Frame, bg="white")
        contact_frame.place(x=380, y=35, width=140, height=25)
        
        # Add +92 label
        prefix_label = Label(contact_frame, text="+92", font=("Aptos Display", 15, "bold"), bg="lightgray", fg="black")
        prefix_label.pack(side=LEFT, fill=Y)
        
        # Create entry for remaining 10 digits
        self.contact_entry = Entry(contact_frame, textvariable=self.var_contact, font=("Aptos Display", 15), bg="lightyellow", width=10)
        self.contact_entry.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Bind validation to contact entry
        self.contact_entry.bind('<KeyRelease>', self.validate_contact)
        self.var_contact.trace('w', self.format_contact)

        Cal_Cart_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=500, y=180, width=550, height=400)

        #========Calculator Frame=====
        self.var_cal_input = StringVar()
        Cal_Frame = Frame(Cal_Cart_Frame, bd=4, relief=RIDGE, bg="white")
        Cal_Frame.place(x=5, y=10, width=280, height=375)

        txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, font=("Aptos Display", 20, "bold"), width=21, bd=10, relief=GROOVE, state='readonly')
        txt_cal_input.grid(row=0, columnspan=20)

        # Calculator buttons
        btn_7 = Button(Cal_Frame, text='7', font=('arial', 15, 'bold'), command=lambda: self.get_input('7'), bd=5, width=4, pady=5, cursor="hand2").grid(row=1, column=0)
        btn_8 = Button(Cal_Frame, text='8', font=('arial', 15, 'bold'), command=lambda: self.get_input('8'), bd=5, width=4, pady=5, cursor="hand2").grid(row=1, column=1)
        btn_9 = Button(Cal_Frame, text='9', font=('arial', 15, 'bold'), command=lambda: self.get_input('9'), bd=5, width=4, pady=5, cursor="hand2").grid(row=1, column=2)
        btn_sum = Button(Cal_Frame, text='+', font=('arial', 15, 'bold'), command=lambda: self.get_input('+'), bd=5, width=4, pady=5, cursor="hand2").grid(row=1, column=3)

        btn_4 = Button(Cal_Frame, text='4', font=('arial', 15, 'bold'), command=lambda: self.get_input('4'), bd=5, width=4, pady=5, cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(Cal_Frame, text='5', font=('arial', 15, 'bold'), command=lambda: self.get_input('5'), bd=5, width=4, pady=5, cursor="hand2").grid(row=2, column=1)
        btn_6 = Button(Cal_Frame, text='6', font=('arial', 15, 'bold'), command=lambda: self.get_input('6'), bd=5, width=4, pady=5, cursor="hand2").grid(row=2, column=2)
        btn_sub = Button(Cal_Frame, text='-', font=('arial', 15, 'bold'), command=lambda: self.get_input('-'), bd=5, width=4, pady=5, cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(Cal_Frame, text='1', font=('arial', 15, 'bold'), command=lambda: self.get_input('1'), bd=5, width=4, pady=5, cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(Cal_Frame, text='2', font=('arial', 15, 'bold'), command=lambda: self.get_input('2'), bd=5, width=4, pady=5, cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(Cal_Frame, text='3', font=('arial', 15, 'bold'), command=lambda: self.get_input('3'), bd=5, width=4, pady=5, cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(Cal_Frame, text='*', font=('arial', 15, 'bold'), command=lambda: self.get_input('*'), bd=5, width=4, pady=5, cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(Cal_Frame, text='0', font=('arial', 15, 'bold'), command=lambda: self.get_input('0'), bd=5, width=4, pady=5, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(Cal_Frame, text='C', font=('arial', 15, 'bold'), command=self.clear_cal, bd=5, width=4, pady=5, cursor="hand2").grid(row=4, column=1)
        btn_eq = Button(Cal_Frame, text='=', font=('arial', 15, 'bold'), command=self.perform_cal, bd=5, width=4, pady=5, cursor="hand2").grid(row=4, column=2)
        btn_div = Button(Cal_Frame, text='/', font=('arial', 15, 'bold'), command=lambda: self.get_input('/'), bd=5, width=4, pady=5, cursor="hand2").grid(row=4, column=3)

        #========Cart Frame=====
        Cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE, bg="white")
        Cart_Frame.place(x=300, y=8, width=240, height=375)
        self.CartTitle = Label(Cart_Frame, text="Cart \t Total Products: [0]", font=("bahnschrift light semicondensed", 15), bg="lightgray")
        self.CartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(Cart_Frame, columns=("pid", "Name", "Price", "Quantity"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid", text="Prod_ID")
        self.CartTable.heading("Name", text="Name")
        self.CartTable.heading("Price", text="Price")
        self.CartTable.heading("Quantity", text="Quantity")
        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("Name", width=90)
        self.CartTable.column("Price", width=90)
        self.CartTable.column("Quantity", width=40)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #========ADD Cart Widget Frame=====
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=500, y=580, width=550, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("Aptos Display", 15), bg="white").place(x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("Aptos Display", 15), bg="lightyellow", state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price", font=("Aptos Display", 15), bg="white").place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("Aptos Display", 15), bg="lightyellow", state='readonly').place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("Aptos Display", 15), bg="white").place(x=400, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("Aptos Display", 15), bg="lightyellow").place(x=400, y=35, width=120, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("Aptos Display", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        # Clear Cart button - FIXED: Added command
        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear Cart", command=self.clear_cart, font=("Aptos Display", 15, "bold"), bg="lightgray", cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update Cart", command=self.add_update_cart, font=("Aptos Display", 15, "bold"), bg="orange", cursor="hand2").place(x=340, y=70, width=180, height=30)

        #=================billing Area===============
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=1062, y=110, width=410, height=470)

        BTitle = Label(billFrame, text="Customer Bill Area", font=("bahnschrift light semicondensed", 20, "bold"), bg="#f44336", fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set, font=("Courier", 10))
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #=================Billing Buttons Frame===============
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=1062, y=582, width=410, height=108)

        self.lbl_amnt = Label(billMenuFrame, text="Bill Amount\n[0]", font=("Aptos Display", 12, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=3, y=3, width=120, height=50)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n[0]", font=("Aptos Display", 12, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=125, y=3, width=120, height=50)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n[0]", font=("Aptos Display", 12, "bold"), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=250, y=3, width=120, height=50)

        # FIXED: Added commands to buttons
        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill, cursor="hand2", font=("Aptos Display", 12, "bold"), bg="lightgreen", fg="white")
        btn_print.place(x=3, y=57, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text="Clear all", command=self.clear_all, cursor="hand2", font=("Aptos Display", 12, "bold"), bg="gray", fg="white")
        btn_clear_all.place(x=125, y=57, width=120, height=50)

        btn_generate = Button(billMenuFrame, text="Generate Bill", command=self.generate_bill, cursor="hand2", font=("Aptos Display", 12, "bold"), bg="#009688", fg="white")
        btn_generate.place(x=250, y=57, width=120, height=50)

        Label(
            self.root,
            text="IMS - Inventory Management System | Developed by Dukes Tech Services\nFor any technical issue email: info@dukestechservices.com",
            font=("bahnschrift light semicondensed", 15),
            bg="#A9A9A9",
            fg="white"
        ).pack(side=BOTTOM, fill=X)

        self.show()

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

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        try:
            result = self.var_cal_input.get()
            if result:
                calculated = eval(result)
                self.var_cal_input.set(str(calculated))
        except:
            messagebox.showerror("Error", "Invalid calculation", parent=self.root)
            self.var_cal_input.set('')

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

    def search(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("select pid, Name, Price, Quantity, Status from product where Name LIKE '%"+self.var_search.get()+"%' and Status='Active'")
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
        """FIXED: Properly add or update items in cart"""
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
            for i, row in enumerate(self.cart_list):
                if self.var_pid.get() == row[0]:
                    present = True
                    index_ = i
                    break

            if present:
                if qty == 0:
                    # Remove from cart
                    self.cart_list.pop(index_)
                    messagebox.showinfo("Success", "Product removed from cart", parent=self.root)
                else:
                    # Update quantity and price
                    self.cart_list[index_][3] = str(qty)
                    self.cart_list[index_][2] = str(total_price)
                    messagebox.showinfo("Success", "Cart updated successfully", parent=self.root)
            else:
                if qty > 0:
                    # Add new item to cart
                    cart_data = [self.var_pid.get(), self.var_pname.get(), str(total_price), str(qty), str(stock)]
                    self.cart_list.append(cart_data)
                    messagebox.showinfo("Success", "Product added to cart", parent=self.root)
                else:
                    messagebox.showerror("Error", "Quantity must be > 0 to add to cart", parent=self.root)
                    return

            self.show_cart()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

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
        
        # Update labels with formatted values - CHANGED $ to Rs.
        self.lbl_amnt.config(text=f'Bill Amount\nRs.{self.bill_amnt:.2f}')
        self.lbl_discount.config(text=f'Discount\nRs.{self.discount:.2f}')
        self.lbl_net_pay.config(text=f'Net Pay\nRs.{self.net_pay:.2f}')
        self.CartTitle.config(text=f"Cart \t Total Products: [{len(self.cart_list)}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                # Display only: pid, name, total price, quantity - CHANGED $ to Rs.
                self.CartTable.insert('', END, values=(row[0], row[1], f"Rs.{float(row[2]):.2f}", row[3]))
            self.bill_updates()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Customer details are required", parent=self.root)
            return
        
        # Validate contact number
        contact = self.var_contact.get().strip()
        if len(contact) != 10 or not contact.isdigit():
            messagebox.showerror("Error", "Contact number must be exactly 10 digits\nExample: 3001234567", parent=self.root)
            self.contact_entry.focus()
            return
            
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please add product to the cart", parent=self.root)
            return
        else:
            # Generate a new invoice number each time
            self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
            
            # Update database quantities
            self.update_product_quantities()
            
            messagebox.showinfo("Success", f"Bill generated successfully\nBill No.: {str(self.invoice)}", parent=self.root)        

    def update_product_quantities(self):
        """Update product quantities in the database after bill generation"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            for item in self.cart_list:
                pid = item[0]
                qty_sold = int(item[3])
                
                # Get current quantity from database
                cur.execute("SELECT Quantity FROM product WHERE pid=?", (pid,))
                current_qty = cur.fetchone()[0]
                
                # Calculate new quantity
                new_qty = current_qty - qty_sold
                
                # Update database
                cur.execute("UPDATE product SET Quantity=? WHERE pid=?", (new_qty, pid))
                
                # If quantity becomes 0, update status to Inactive
                if new_qty == 0:
                    cur.execute("UPDATE product SET Status='Inactive' WHERE pid=?", (pid,))
            
            con.commit()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating inventory: {str(ex)}", parent=self.root)
            con.rollback()
        finally:
            con.close()

    def bill_top(self):
        # Don't generate invoice number here - it's generated in generate_bill()
        bill_top_temp = f'''
    \t\tXYZ Inventory
    \t Phone No. +923*******63 , Lahore-54000
    {str("="*47)}
    Customer Name: {self.var_cname.get()}
    Phone No. : {self.get_contact_for_bill()}
    Bill No. : {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
    {str("="*47)}
    Product Name\t\tQTY\tPrice
    {str("="*47)}
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
            
            # Format the line with proper spacing - CHANGED $ to Rs.
            line = f" {product_name[:20]:20} {qty:>5} Rs.{price_per_item:>8.2f}\n"
            self.txt_bill_area.insert(END, line)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt:.2f}
 Discount (5%)\t\t\t\tRs.{self.discount:.2f}
{str("-"*47)}
 Net Pay\t\t\t\tRs.{self.net_pay:.2f}
{str("="*47)}
\n\tThank you for your purchase!
\t      Please visit again!
'''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        """Clear the cart"""
        if messagebox.askyesno("Confirm", "Clear all items from cart?", parent=self.root):
            self.cart_list.clear()
            self.show_cart()
            self.txt_bill_area.delete('1.0', END)
            messagebox.showinfo("Success", "Cart cleared", parent=self.root)

    def clear_all(self):
        """Clear everything: cart, customer details, bill"""
        if messagebox.askyesno("Confirm", "Clear all data?", parent=self.root):
            self.cart_list.clear()
            self.var_cname.set('')
            self.var_contact.set('')
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
            messagebox.showinfo("Success", "All data cleared", parent=self.root)

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