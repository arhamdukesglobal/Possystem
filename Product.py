from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class ProductClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x550+280+180")  # Increased height for CNIC field
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()


        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        #===============Variables================
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        product_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="White")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #=========Title==========
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_quantity=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=310)


        #===options====
        cmb_search=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=("Select"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_search.place(x=150,y=60,width=200)
        cmb_search.current(0)

        cmb_supplier=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=("Select"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_supplier.place(x=150,y=110,width=200)
        cmb_supplier.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("Times new Roman",15),bg="lightyellow").place(x=150,y=160,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("Times new Roman",15),bg="lightyellow").place(x=150,y=210,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("Times new Roman",15),bg="lightyellow").place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        #====buttons=====
        btn_add = Button(product_Frame,text="Save",command=self.add, font=("Aptos",15),bg="#2196f3",fg="White",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update = Button(product_Frame,text="Update",command=self.update, font=("Aptos",15),bg="#4caf50",fg="White",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete = Button(product_Frame,text="Delete",command=self.delete, font=("Aptos",15),bg="#f44336",fg="White",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear = Button(product_Frame,text="Clear",command=self.clear, font=("Aptos",15),bg="#607d8b",fg="White",cursor="hand2").place(x=340,y=400,width=100,height=40)


        #===searchFrame=====
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #===options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt, font=("Aptos",15),bg="lightyellow").place(x=200, y=10)
        btn_search = Button(SearchFrame,text="Search",command=self.search, font=("Aptos",15),bg="#4caf50",fg="White",cursor="hand2").place(x=410,y=9,width=150,height=30)


    def add(self):
        if not self.validate_all_fields():
            return
            
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Check if EmpID already exists
            cur.execute("Select * from employee where EmpID=?",(self.var_EmpID.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error","This Employee ID already assigned, try different",parent=self.root)
                return
            
            # Check if CNIC already exists
            cnic_clean = self.var_cnic.get().replace('-', '')
            cur.execute("Select * from employee where CNIC=?",(cnic_clean,))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error","This CNIC already exists in the system",parent=self.root)
                return
            
            # Check if Email already exists
            cur.execute("Select * from employee where Email=?",(self.var_email.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error","This Email already exists in the system",parent=self.root)
                return
            
            cur.execute("Insert into Employee(EmpID,Name,Email,Gender,CNIC,Contact,DOB,DOJ,Password,UserType,Address,Salary) values(?,?,?,?,?,?,?,?,?,?,?,?)",(
                                    self.var_EmpID.get(),
                                    self.var_name.get().strip(),
                                    self.var_email.get().strip(),
                                    self.var_gender.get(),
                                    cnic_clean,
                                    self.var_contact.get(),
                                    self.var_DOB.get(),
                                    self.var_DOJ.get(),
                                    self.var_Password.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get('1.0',END).strip(),
                                    self.var_salary.get(),
            ))
            con.commit()
            messagebox.showinfo("Success","Employee added successfully",parent=self.root)
            self.show()
            self.clear()  # Clear form and generate new EmpID
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                if "CNIC" in str(e):
                    messagebox.showerror("Error","CNIC already exists in the system",parent=self.root)
                elif "Email" in str(e):
                    messagebox.showerror("Error","Email already exists in the system",parent=self.root)
            else:
                messagebox.showerror("Error",f"Database error: {str(e)}",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
        finally:
            con.close()

    def update(self):
        if not self.validate_all_fields():
            return
            
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Check if EmpID exists
            cur.execute("Select * from employee where EmpID=?",(self.var_EmpID.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                return
            
            # Check if CNIC already exists for another employee
            cnic_clean = self.var_cnic.get().replace('-', '')
            cur.execute("Select * from employee where CNIC=? AND EmpID!=?",(cnic_clean, self.var_EmpID.get()))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error","This CNIC already exists for another employee",parent=self.root)
                return
            
            # Check if Email already exists for another employee
            cur.execute("Select * from employee where Email=? AND EmpID!=?",(self.var_email.get(), self.var_EmpID.get()))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error","This Email already exists for another employee",parent=self.root)
                return
            
            cur.execute("Update employee set Name=?,Email=?,Gender=?,CNIC=?,Contact=?,DOB=?,DOJ=?,Password=?,UserType=?,Address=?,Salary=? where EmpID=?",(
                                    self.var_name.get().strip(),
                                    self.var_email.get().strip(),
                                    self.var_gender.get(),
                                    cnic_clean,
                                    self.var_contact.get(),
                                    self.var_DOB.get(),
                                    self.var_DOJ.get(),
                                    self.var_Password.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get('1.0',END).strip(),
                                    self.var_salary.get(),
                                    self.var_EmpID.get(),
            ))
            con.commit()
            messagebox.showinfo("Success","Employee updated successfully",parent=self.root)
            self.show()
            self.txt_empid.config(state='readonly')  # Make read-only again
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                messagebox.showerror("Error","Duplicate entry. CNIC or Email already exists for another employee.",parent=self.root)
            else:
                messagebox.showerror("Error",f"Database error: {str(e)}",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error updating employee: {str(ex)}",parent=self.root)
        finally:
            con.close()

    def delete(self):
        if not self.var_EmpID.get():
            messagebox.showerror("Error","Please select an employee to delete",parent=self.root)
            return
            
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirm","Do you really want to delete this employee?",parent=self.root)
            if op:
                cur.execute("DELETE FROM employee WHERE EmpID=?",(self.var_EmpID.get(),))
                con.commit()
                if cur.rowcount > 0:
                    messagebox.showinfo("Delete","Employee deleted successfully",parent=self.root)
                    self.clear()
                else:
                    messagebox.showerror("Error","Employee not found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error deleting employee: {str(ex)}",parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_cnic.set("")
        self.var_contact.set("")
        self.var_DOB.set("")
        self.var_DOJ.set("")
        self.var_Password.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        
        # Reset calendars to today's date
        today = datetime.now()
        self.dob_calendar.set_date(today)
        self.doj_calendar.set_date(today)
        
        # Generate new EmpID
        self.generate_emp_id()
        self.show()
        self.txt_empid.config(state='readonly')


    def show(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from employee ORDER BY EmpID")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                # Format CNIC for display
                formatted_row = list(row)
                if row[4]:  # CNIC column
                    cnic = str(row[4])
                    if len(cnic) == 13:
                        formatted_cnic = f"{cnic[:5]}-{cnic[5:12]}-{cnic[12:]}"
                        formatted_row[4] = formatted_cnic
                
                self.EmployeeTable.insert('',END,values=formatted_row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error displaying data: {str(ex)}",parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search by option", parent=self.root)
                return

            if not self.var_searchtxt.get().strip():
                messagebox.showerror("Error", "Search input is required", parent=self.root)
                return

            search_text = self.var_searchtxt.get().strip()
            search_column = self.var_searchby.get()

            # Auto-fix EmpID input
            if search_column == "EmpID" and not search_text.startswith("E"):
                search_text = "E" + search_text

            # Clean CNIC input
            if search_column == "CNIC":
                search_text = search_text.replace("-", "")

            # Use parameterized query to prevent SQL injection
            query = f"SELECT * FROM employee WHERE {search_column} LIKE ?"
            cur.execute(query, ("%" + search_text + "%",))
            rows = cur.fetchall()

            self.EmployeeTable.delete(*self.EmployeeTable.get_children())

            if rows:
                for row in rows:
                    formatted_row = list(row)
                    # Format CNIC for display
                    if row[4] and len(row[4]) == 13:
                        formatted_row[4] = f"{row[4][:5]}-{row[4][5:12]}-{row[4][12:]}"
                    self.EmployeeTable.insert("", END, values=formatted_row)
            else:
                messagebox.showinfo("Result", "No records found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error searching: {str(ex)}", parent=self.root)
        finally:
            con.close()






if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()