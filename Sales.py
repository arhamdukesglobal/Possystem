from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+280+130")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()


        self.var_Invoice=StringVar()
        #========title=====
        lbl_title = Label(self.root, text="View Customer Invoice", font=("goudy old style", 30), bg="#389b91", fg="white", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice = Label(self.root,text="Invoice No.", font=("Arial Black", 15), bg="white").place(x=50, y=100)
        txt_invoice = Entry(self.root,textvariable=self.var_Invoice,text="Invoice No.", font=("Aptos", 15), bg="light yellow").place(x=190, y=100,width=180,height=28)

        btn_search = Button(self.root,text="Search",font=("Times New Roman", 15,"bold"), bg="#2196f3", fg="white",cursor = "hand2").place(x=400, y=100,width=120,height=28)
        btn_clear = Button(self.root,text="Clear",font=("Times New Roman", 15,"bold"), bg="lightgray",cursor = "hand2").place(x=530, y=100,width=120,height=28)


        #=======Sales List=======
        sales_Frame = Frame(self.root,bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=150, width=400, height=750)

        scrolly=Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sales_List = Listbox(sales_Frame, font=("goudy old style",15), bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)


        #=======Invoice Details=======
        Invoice_Frame = Frame(self.root,bd=3, relief=RIDGE)
        Invoice_Frame.place(x=500, y=150, width=450, height=750)

        lbl_title2 = Label(Invoice_Frame, text="Customer Bill Area", font=("goudy old style", 20), bg="orange").pack(side=TOP, fill=X)


        scrolly2=Scrollbar(Invoice_Frame, orient=VERTICAL)
        self.Invoice_area = Text(Invoice_Frame, font=("goudy old style",15), bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.Invoice_area.yview)
        self.Invoice_area.pack(fill=BOTH, expand=1)


        #======Image====
        self.bill_photo=Image.open("IMAGES/sales.png")
        self.bill_photo=self.bill_photo.resize((450,300), Image.ANTIALIAS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)




if __name__ == "__main__":
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()
