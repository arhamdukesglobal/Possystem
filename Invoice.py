import tkinter
from tkinter import *
from PIL import Image, ImageTk

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
        Product_Frame1.place(x=10,y=110,width=500,height=550)

        pTitle=Label(Product_Frame1,text="All Products",font=("bahnschrift light semicondensed",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        Product_Frame2 = Frame(Product_Frame1,bd=2,relief=RIDGE,bg="white")
        Product_Frame2.place(x=2,y=42,width=450,height=90)

        lbl_search=Label(Product_Frame2,text="Search Product | By Name",font=("Aptos Display",15,"bold"),bg="white",fg="black").place(x=2,y=5)

        lbl_search=Label(Product_Frame2,text="Product Name",font=("Aptos Display",15,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(Product_Frame2,textvariable=self.var_search,font=("Aptos Display",15,"bold"),bg="lightyellow").place(x=150,y=47,width=150,height=22)
        btn_Search=Button(Product_Frame2,text="Search",font=("Aptos Display",15,"bold"),bg="#2196F3",fg="white",cursor="hand2").place(x=310,y=45,width=100,height=30)
        btn_show_all=Button(Product_Frame2,text="Show All",font=("Aptos Display",15,"bold"),bg="#083531",fg="white",cursor="hand2").place(x=310,y=10,width=100,height=30)



if __name__ == "__main__":
    root = Tk()
    obj = Invoice_Class(root)
    root.mainloop()
