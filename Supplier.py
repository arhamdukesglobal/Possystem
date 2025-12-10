from tkinter import*
from tkinter import ttk,messagebox
import sqlite3

class SupplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+280+180")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()
        
        #===========================================
        # All Variables=========
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_SuppInv = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        #===searchFrame=====
        SearchFrame=LabelFrame(self.root,text="Search Supplier",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #===options====
        lbl_search=Label(SearchFrame,text="Search By Invoice No",bg="white",font=("Times new Roman",15))
        lbl_search.place(x=10,y=10)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt, font=("Aptos",15),bg="lightyellow").place(x=200, y=10)
        btn_search = Button(SearchFrame,text="Search",command=self.search, font=("Aptos",15),bg="#4caf50",fg="White",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #===title====
        title=Label(self.root,text="Supplier Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #===content====
        #====row1====
        lbl_SuppInv=Label(self.root,text="Invoice No",font=("goudy old style",15),bg="white").place(x=50,y=150)
        # Changed: Made it editable (removed state='readonly')
        txt_SuppInv=Entry(self.root,textvariable=self.var_SuppInv,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)
        
        #====row2=====
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)

        #====row3=====
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=230)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)

        #====row4=====
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=270)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=150,y=270,width=300,height=60)

        #====buttons=====
        btn_add = Button(self.root,text="Save",command=self.add, font=("Aptos",15),bg="#2196f3",fg="White",cursor="hand2").place(x=500,y=340,width=110,height=28)
        btn_update = Button(self.root,text="Update",command=self.update, font=("Aptos",15),bg="#4caf50",fg="White",cursor="hand2").place(x=620,y=340,width=110,height=28)
        btn_delete = Button(self.root,text="Delete",command=self.delete, font=("Aptos",15),bg="#f44336",fg="White",cursor="hand2").place(x=740,y=340,width=110,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear, font=("Aptos",15),bg="#607d8b",fg="White",cursor="hand2").place(x=860,y=340,width=110,height=28)

        #===Supplier Details====
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=380,relwidth=1,height=120)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(emp_frame,columns=("Invoice","Name","Contact","Description"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        
        self.SupplierTable.heading("Invoice",text="Invoice No")
        self.SupplierTable.heading("Name",text="Name")
        self.SupplierTable.heading("Contact",text="Contact")
        self.SupplierTable.heading("Description",text="Description")
        self.SupplierTable["show"]="headings"

        self.SupplierTable.column("Invoice",width=90)
        self.SupplierTable.column("Name",width=100)
        self.SupplierTable.column("Contact",width=100)
        self.SupplierTable.column("Description",width=100)

        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
        
        self.show()

    def add(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Check if Invoice No is provided (since it's now mandatory)
            if self.var_SuppInv.get()=="":
                messagebox.showerror("Error","Supplier Invoice must be required",parent=self.root)
            elif self.var_name.get()=="" or self.var_contact.get()=="":
                messagebox.showerror("Error","Name and Contact are required fields",parent=self.root)
            else:
                # Check if Invoice No already exists
                cur.execute("Select * from supplier where SuppInv=?",(self.var_SuppInv.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Supplier Invoice already exists, try different",parent=self.root)
                else:
                    # Insert with manual Invoice No
                    cur.execute("Insert into Supplier(SuppInv,Name,Contact,Description) values(?,?,?,?)",(
                                                self.var_SuppInv.get(),
                                                self.var_name.get(),
                                                self.var_contact.get(),
                                                self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from Supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        if row:  # Check if row has data
            self.var_SuppInv.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.txt_desc.delete('1.0',END)
            self.txt_desc.insert(END,row[3])

    def update(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_SuppInv.get()=="":
                messagebox.showerror("Error","Please select a supplier to update",parent=self.root)
            else:
                cur.execute("Update Supplier set Name=?,Contact=?,Description=? where SuppInv=?",(
                                            self.var_name.get(),
                                            self.var_contact.get(),
                                            self.txt_desc.get('1.0',END),
                                            self.var_SuppInv.get(),
                ))
                con.commit()
                messagebox.showinfo("Success","Supplier updated successfully",parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_SuppInv.get()=="":
                messagebox.showerror("Error","Please select a supplier to delete",parent=self.root)
            else:
                op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                if op==True:
                    cur.execute("delete from Supplier where SuppInv=?",(self.var_SuppInv.get(),))
                    con.commit()
                    messagebox.showinfo("Delete","Supplier deleted successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_SuppInv.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Supplier Invoice should be required",parent=self.root)
                self.show()  # Show all if search is empty
            else:
                cur.execute("Select * from Supplier where SuppInv=?",(self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
                    self.show()  # Show all if no record found
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()