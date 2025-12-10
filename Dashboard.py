import tkinter
from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from Employee import EmployeeClass
from Supplier import SupplierClass
class IMS:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        #===title=====
        self.icon_title=PhotoImage(file="IMAGES/shopcartfinal.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound = LEFT,font=("bahnschrift light semicondensed",40,"bold"),bg="#87CEEB",fg="black",anchor="n",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #===btn_logout=====
        btn_logout=Button(self.root,text="Logout",font=("Arial",15,"bold"),bg="red",cursor="hand2").place(x=1500,y=10,height=50,width=150)
        #===clock=====
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date DD-MM-YYYY\t\t Time: HH:MM:SS",font=("bahnschrift light semicondensed",15),bg="#A9A9A9",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #===left menu=====
        self.menulogo=Image.open("IMAGES/inventory management logo.png")
        self.menulogo=self.menulogo.resize((200,200),Image.LANCZOS)
        self.menulogo=ImageTk.PhotoImage(self.menulogo)

        Leftmenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Leftmenu.place(x=0,y=120,width=200,height=650)

        lbl_menulogo = Label(Leftmenu,image = self.menulogo)
        lbl_menulogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="IMAGES/pointerarr.png")
        lbl_menu=Label(Leftmenu,text="MENU",font=("Impact",20),bg="#B0C4DE").pack(side = TOP,fill = X)

        btn_employee=Button(Leftmenu,text="Employee",command=self.Employee,image = self.icon_side,compound = LEFT,padx=5,anchor="w",font=("Aptos Display",20,"bold"),bg="White",bd=6,cursor="hand2").pack(side = TOP,fill = X)
        btn_supplier=Button(Leftmenu,text="Supplier",command=self.Supplier,image = self.icon_side,compound = LEFT,padx=5,anchor="w",font=("Aptos Display",20,"bold"),bg="White",bd=6,cursor="hand2").pack(side = TOP,fill = X)
        btn_category=Button(Leftmenu,text="Category",image = self.icon_side,compound = LEFT,padx=5,anchor="w",font=("Aptos Display",20,"bold"),bg="White",bd=6,cursor="hand2").pack(side = TOP,fill = X)
        btn_product=Button(Leftmenu,text="Product",image = self.icon_side,compound = LEFT,padx=5,anchor="w",font=("Aptos Display",20,"bold"),bg="White",bd=6,cursor="hand2").pack(side = TOP,fill = X)
        btn_sales=Button(Leftmenu,text="Sales",image = self.icon_side,compound = LEFT,padx=5,anchor="w",font=("Aptos Display",20,"bold"),bg="White",bd=6,cursor="hand2").pack(side = TOP,fill = X)
        btn_exit=Button(Leftmenu,text="Exit",image = self.icon_side,compound = LEFT,padx=5,anchor="w",font=("Aptos Display",20,"bold"),bg="White",bd=6,cursor="hand2").pack(side = TOP,fill = X)
        

        #===content====
        self.lbl_employee = Label(self.root,text="Total Employees\n[ 0 ]",bd=6.5,relief=RIDGE,bg = "#404040",fg = "white",font = ("Contemporary Sans-Serif",20,"bold"))
        self.lbl_employee.place(x=420,y=180,height=180,width=375)

        self.lbl_supplier = Label(self.root,text="Total Suppliers\n[ 0 ]",bd=6.5,relief=RIDGE,bg = "#404040",fg = "white",font = ("Contemporary Sans-Serif",20,"bold"))
        self.lbl_supplier.place(x=800,y=180,height=180,width=375)

        self.lbl_category = Label(self.root,text="Total Categories\n[ 0 ]",bd=6.5,relief=RIDGE,bg = "#404040",fg = "white",font = ("Contemporary Sans-Serif",20,"bold"))
        self.lbl_category.place(x=1180,y=180,height=180,width=375)

        self.lbl_product = Label(self.root,text="Total Products\n[ 0 ]",bd=6.5,relief=RIDGE,bg = "#404040",fg = "white",font = ("Contemporary Sans-Serif",20,"bold"))
        self.lbl_product.place(x=610,y=380,height=180,width=375)

        self.lbl_sales = Label(self.root,text="Total Sales\n[ 0 ]",bd=6.5,relief=RIDGE,bg = "#404040",fg = "white",font = ("Contemporary Sans-Serif",20,"bold"))
        self.lbl_sales.place(x=990,y=380,height=180,width=375)

        #===footer=====
        lbl_footer=Label(self.root,text="IMS - Inventory Management System | Developed by Dukes Tech Services\nFor any Technical Issue email at: info@dukestechservices.com",font=("bahnschrift light semicondensed",15),bg="#A9A9A9",fg="white").pack(side=BOTTOM,fill=X)
#==============================================================================================================================

    def Employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win)

    def Supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierClass(self.new_win)

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()

 
