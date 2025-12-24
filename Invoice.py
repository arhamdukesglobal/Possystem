import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class Invoice_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")

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
            anchor="n",
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout button
        Button(
            self.root,
            text="Logout",
            font=("Arial", 15, "bold"),
            bg="red",
            fg="white",
            cursor="hand2"
        ).place(x=1550, y=10, height=50, width=150)

        # Clock
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System     Date: --/--/----     Time: --:--:--",
            font=("bahnschrift light semicondensed", 15),
            bg="#A9A9A9",
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)


        #===========Product Frame===========
        self.var_search=StringVar()
        Product_Frame1 = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Product_Frame1.place(x=10,y=110,width=480,height=550)

        pTitle=Label(Product_Frame1,text="All Products",font=("bahnschrift light semicondensed",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        Product_Frame2 = Frame(Product_Frame1,bd=2,relief=RIDGE,bg="white")
        Product_Frame2.place(x=2,y=42,width=450,height=90)

        lbl_search=Label(Product_Frame2,text="Search Product | By Name",font=("Aptos Display",15,"bold"),bg="white",fg="black").place(x=2,y=5)

        lbl_search=Label(Product_Frame2,text="Product Name",font=("Aptos Display",15,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(Product_Frame2,textvariable=self.var_search,font=("Aptos Display",15,"bold"),bg="lightyellow").place(x=150,y=47,width=150,height=22)
        btn_Search=Button(Product_Frame2,text="Search",command=self.search,font=("Aptos Display",15,"bold"),bg="#2196F3",fg="white",cursor="hand2").place(x=310,y=45,width=100,height=30)
        btn_show_all=Button(Product_Frame2,text="Show All",command=self.show,font=("Aptos Display",15,"bold"),bg="#083531",fg="white",cursor="hand2").place(x=310,y=10,width=100,height=30)


        #==============Product Details Frame=============
        Product_Frame3 = Frame(Product_Frame1, bd=3, relief=RIDGE)
        Product_Frame3.place(x=2, y=140, width=450, height=375)

        scrolly = Scrollbar(Product_Frame3, orient=VERTICAL)
        scrollx = Scrollbar(Product_Frame3, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(Product_Frame3, columns=("pid", "Name", "Price", "Quantity", "Status"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
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
        #self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        lbl_note=Label(Product_Frame3,text="Note: 'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #===========Customer Frame===========
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        Customer_Frame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Customer_Frame.place(x=500,y=110,width=550,height=70)

        cTitle=Label(Customer_Frame,text="Customer Details",font=("bahnschrift light semicondensed",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(Customer_Frame,text="Customer Name",font=("Aptos Display",15,"bold"),bg="white").place(x=5,y=35)
        txt_name=Entry(Customer_Frame,textvariable=self.var_cname,font=("Aptos Display",15),bg="lightyellow").place(x=160,y=37,width=150,height=22)

        lbl_contact=Label(Customer_Frame,text="Contact No.",font=("Aptos Display",15,"bold"),bg="white").place(x=270,y=35)
        txt_contact=Entry(Customer_Frame,textvariable=self.var_contact,font=("Aptos Display",15),bg="lightyellow").place(x=380,y=37,width=140,height=22)

        Cal_Cart_Frame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=500,y=180,width=550,height=400)

        #========Calculator Frame=====
        self.var_cal_input=StringVar()
        Cal_Frame = Frame(Cal_Cart_Frame,bd=4,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=280,height=375)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=("Aptos Display",20,"bold"),width=21,bd=10,relief=GROOVE,state='readonly')
        txt_cal_input.grid(row=0,columnspan=20)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=5,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=5,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=5,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=5,cursor="hand2").grid(row=4,column=3)

        #========Cart Frame=====

        Cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        Cart_Frame.place(x=300, y=8, width=240, height=375)
        CartTitle=Label(Cart_Frame,text="Cart \t Total Products: [0]",font=("bahnschrift light semicondensed",15),bg="lightgray").pack(side=TOP,fill=X)


        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(Cart_Frame, columns=("pid", "Name", "Price", "Quantity", "Status"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid", text="Prod_ID")
        self.CartTable.heading("Name", text="Name")
        self.CartTable.heading("Price", text="Price")
        self.CartTable.heading("Quantity", text="Quantity")
        self.CartTable.heading("Status", text="Status")
        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("Name", width=100)
        self.CartTable.column("Price", width=90)
        self.CartTable.column("Quantity", width=40)
        self.CartTable.column("Status", width=90)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data)

        #========ADD Cart Widget Frame=====
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=500,y=580,width=550,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("Aptos Display",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("Aptos Display",15),bg="lightyellow",state='readonly').place(x=5,y=35, width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price",font=("Aptos Display",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("Aptos Display",15),bg="lightyellow",state='readonly').place(x=230,y=35, width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("Aptos Display",15),bg="white").place(x=400,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("Aptos Display",15),bg="lightyellow").place(x=400,y=35, width=120,height=22)

        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock [9999]",font=("Aptos Display",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",font=("Aptos Display",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",font=("Aptos Display",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)

        #=================billing Area===============
        billFrame = Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=1062,y=110,width=410,height=470)

        BTitle=Label(billFrame,text="Customer Bill Area",font=("bahnschrift light semicondensed",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #=================Billing Buttons Frame===============
        billMenuFrame = Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=1062,y=582,width=410,height=108)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("Aptos Display",12,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=3,y=3,width=120,height=50)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n[0]",font=("Aptos Display",12,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=125,y=3,width=120,height=50)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("Aptos Display",12,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=250,y=3,width=120,height=50)


        btn_print=Button(billMenuFrame,text="Print",cursor="hand2",font=("Aptos Display",12,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=3,y=57,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text="Clear all",cursor="hand2",font=("Aptos Display",12,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=125,y=57,width=120,height=50)

        btn_generate=Button(billMenuFrame,text="Generate Bill",cursor="hand2",font=("Aptos Display",12,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=250,y=57,width=120,height=50)


        Label(
            self.root,
            text="IMS - Inventory Management System | Developed by Dukes Tech Services\nFor any technical issue email: info@dukestechservices.com",
            font=("bahnschrift light semicondensed", 15),
            bg="#A9A9A9",
            fg="white"
        ).pack(side=BOTTOM, fill=X)

        self.show()

#================All Functions================
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'Possystem.db')
        cur=con.cursor()
        try:
            cur.execute("select pid, Name, Price, Quantity, Status from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'Possystem.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid, Name, Price, Quantity, Status from product where Name LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)


    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = self.ProductTable.item(f)
        row = content['values']



if __name__ == "__main__":
    root = Tk()
    obj = Invoice_Class(root)
    root.mainloop()