from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox,ttk
import sqlite3
class CategoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="white")
        self.root.focus_force()
        ########Variables===========
        self.var_CatID=StringVar()
        self.var_Name=StringVar()

        #===============title================
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_Name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width=300)

        btn_add=Button(self.root,text="ADD",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="DELETE",font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        #========Category Details===========

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.Category_Table=ttk.Treeview(cat_frame,columns=("CID","Name"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Category_Table.xview)
        scrolly.config(command=self.Category_Table.yview)

        self.Category_Table.heading("CID",text="Category ID")
        self.Category_Table.heading("Name",text="Name")
        self.Category_Table["show"]="headings"
        self.Category_Table.column("CID",width=90)
        self.Category_Table.column("Name",width=100)
        self.Category_Table.pack(fill=BOTH,expand=1)


if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()
