#Employee.py
from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
from datetime import datetime
import re
from tkcalendar import DateEntry  # pip install tkcalendar

class EmployeeClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x550+280+180")  # Increased height for CNIC field
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()
        
        #===========================================
        # All Variables=========
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_EmpID = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_DOB = StringVar()
        self.var_DOJ = StringVar()
        self.var_email = StringVar()
        self.var_Password = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()
        self.var_cnic = StringVar()  # New variable for CNIC

        #===searchFrame=====
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #===options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","EmpID","Email","Name","Contact","CNIC"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt, font=("Aptos",15),bg="lightyellow").place(x=200, y=10)
        btn_search = Button(SearchFrame,text="Search",command=self.search, font=("Aptos",15),bg="#4caf50",fg="White",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #===title====
        title=Label(self.root,text="Employee Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #===content====
        #====row1====
        lbl_empid=Label(self.root,text="EmpID",font=("goudy old style",15),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",15),bg="white").place(x=350,y=150)
        lbl_cnic=Label(self.root,text="CNIC",font=("goudy old style",15),bg="white").place(x=750,y=150)  # Changed from Contact to CNIC

        # EmpID entry - starts with E followed by 4 digits
        self.txt_empid=Entry(self.root,textvariable=self.var_EmpID,font=("goudy old style",15),bg="lightyellow", state='readonly')
        self.txt_empid.place(x=150,y=150,width=180)
        
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        
        # CNIC entry - 13 digits with formatting
        self.cnic_entry = Entry(self.root, textvariable=self.var_cnic, font=("goudy old style",15), bg="lightyellow")
        self.cnic_entry.place(x=850,y=150,width=180)
        self.cnic_entry.bind('<KeyRelease>', self.validate_cnic)

        #====row2=====
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",15),bg="white").place(x=350,y=190)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=750,y=190)

        # Name entry
        self.txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow")
        self.txt_name.place(x=150,y=190,width=180)
        
        # DOB entry with calendar
        dob_frame = Frame(self.root, bg="lightyellow")
        dob_frame.place(x=500,y=190,width=180,height=30)
        self.dob_calendar = DateEntry(dob_frame, font=("goudy old style",12), bg="lightyellow", 
                                     date_pattern='dd/mm/yyyy', locale='en_GB')
        self.dob_calendar.pack(fill=BOTH, expand=True)
        self.dob_calendar.bind("<<DateEntrySelected>>", self.on_dob_select)
        
        # Contact entry
        self.contact_entry = Entry(self.root, textvariable=self.var_contact, font=("goudy old style",15), bg="lightyellow")
        self.contact_entry.place(x=850,y=190,width=180)
        self.contact_entry.bind('<KeyRelease>', self.validate_contact)

        #====row3=====
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lbl_doj=Label(self.root,text="Joining Date",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",15),bg="white").place(x=750,y=230)

        # Email entry
        self.txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow")
        self.txt_email.place(x=150,y=230,width=180)
        
        # DOJ entry with calendar
        doj_frame = Frame(self.root, bg="lightyellow")
        doj_frame.place(x=500,y=230,width=180,height=30)
        self.doj_calendar = DateEntry(doj_frame, font=("goudy old style",12), bg="lightyellow", 
                                     date_pattern='dd/mm/yyyy', locale='en_GB')
        self.doj_calendar.pack(fill=BOTH, expand=True)
        self.doj_calendar.bind("<<DateEntrySelected>>", self.on_doj_select)
        
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Employee"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #====row4=====
        lbl_address=Label(self.root,text="Address",font=("goudy old style",15),bg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salary",font=("goudy old style",15),bg="white").place(x=350,y=270)
        lbl_password=Label(self.root,text="Password",font=("goudy old style",15),bg="white").place(x=750,y=270)

        # Address entry
        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=180,height=60)
        
        # Salary entry
        self.salary_entry = Entry(self.root, textvariable=self.var_salary, font=("goudy old style",15), bg="lightyellow")
        self.salary_entry.place(x=500,y=270,width=180)
        
        # Password entry
        self.txt_pass=Entry(self.root,textvariable=self.var_Password,font=("goudy old style",15),bg="lightyellow", show="*")
        self.txt_pass.place(x=850,y=270,width=180)

        #====buttons=====
        btn_add = Button(self.root,text="Save",command=self.add, font=("Aptos",15),bg="#2196f3",fg="White",cursor="hand2").place(x=500,y=340,width=110,height=28)
        btn_update = Button(self.root,text="Update",command=self.update, font=("Aptos",15),bg="#4caf50",fg="White",cursor="hand2").place(x=620,y=340,width=110,height=28)
        btn_delete = Button(self.root,text="Delete",command=self.delete, font=("Aptos",15),bg="#f44336",fg="White",cursor="hand2").place(x=740,y=340,width=110,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear, font=("Aptos",15),bg="#607d8b",fg="White",cursor="hand2").place(x=860,y=340,width=110,height=28)

        #===Employee Details====
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=400,relwidth=1,height=120)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("EmpID","Name","Email","Gender","CNIC","Contact","DOB","DOJ","Password","UserType","Address","Salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        
        self.EmployeeTable.heading("EmpID",text="Emp ID")
        self.EmployeeTable.heading("Name",text="Name")
        self.EmployeeTable.heading("Email",text="Email")
        self.EmployeeTable.heading("Gender",text="Gender")
        self.EmployeeTable.heading("CNIC",text="CNIC")
        self.EmployeeTable.heading("Contact",text="Contact")
        self.EmployeeTable.heading("DOB",text="DOB")
        self.EmployeeTable.heading("DOJ",text="Joining Date")
        self.EmployeeTable.heading("Password",text="Password")
        self.EmployeeTable.heading("UserType",text="User Type")
        self.EmployeeTable.heading("Address",text="Address")
        self.EmployeeTable.heading("Salary",text="Salary")

        self.EmployeeTable["show"]="headings"
        self.EmployeeTable.column("EmpID",width=90)
        self.EmployeeTable.column("Name",width=100)
        self.EmployeeTable.column("Email",width=100)
        self.EmployeeTable.column("Gender",width=80)
        self.EmployeeTable.column("CNIC",width=120)
        self.EmployeeTable.column("Contact",width=100)
        self.EmployeeTable.column("DOB",width=80)
        self.EmployeeTable.column("DOJ",width=100)
        self.EmployeeTable.column("Password",width=80)
        self.EmployeeTable.column("UserType",width=80)
        self.EmployeeTable.column("Address",width=100)
        self.EmployeeTable.column("Salary",width=80)

        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        
        # Generate initial EmpID
        self.generate_emp_id()
        self.show()

    def on_dob_select(self, event):
        self.var_DOB.set(self.dob_calendar.get_date().strftime("%d/%m/%Y"))

    def on_doj_select(self, event):
        self.var_DOJ.set(self.doj_calendar.get_date().strftime("%d/%m/%Y"))

    def generate_emp_id(self):
        """Generate a new unique EmpID starting with E followed by 4 digits"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Create employee table if not exists
            cur.execute('''CREATE TABLE IF NOT EXISTS employee (
                        EmpID TEXT PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Email TEXT,
                        Gender TEXT,
                        CNIC TEXT UNIQUE,
                        Contact TEXT,
                        DOB TEXT,
                        DOJ TEXT,
                        Password TEXT,
                        UserType TEXT,
                        Address TEXT,
                        Salary TEXT)''')
            
            # Get the highest existing EmpID
            cur.execute("SELECT MAX(EmpID) FROM employee")
            result = cur.fetchone()
            max_id = result[0]
            
            if max_id and max_id.startswith('E'):
                try:
                    # Extract numeric part and increment
                    num_part = int(max_id[1:])
                    new_num = num_part + 1
                except:
                    new_num = 1
            else:
                new_num = 1
            
            # Format as E followed by 4 digits with leading zeros
            new_emp_id = f"E{new_num:04d}"
            self.var_EmpID.set(new_emp_id)
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error generating EmpID: {str(ex)}",parent=self.root)
            # Default to E0001 if there's an error
            self.var_EmpID.set("E0001")
        finally:
            con.close()

    def validate_cnic(self, event=None):
        """Format CNIC as XXXXX-XXXXXXX-X"""
        current_text = self.var_cnic.get()
        if current_text:
            # Remove non-digits
            digits = ''.join(filter(str.isdigit, current_text))
            if len(digits) > 13:
                digits = digits[:13]
            
            # Format with dashes
            if len(digits) > 0:
                formatted = digits
                if len(digits) > 5:
                    formatted = digits[:5] + '-' + digits[5:]
                if len(digits) > 12:
                    formatted = digits[:5] + '-' + digits[5:12] + '-' + digits[12:]
                self.var_cnic.set(formatted)
                self.cnic_entry.icursor(END)

    def validate_contact(self, event=None):
        """Validate Contact to accept exactly 11 digits"""
        current_text = self.var_contact.get()
        if current_text:
            # Remove non-digits
            digits = ''.join(filter(str.isdigit, current_text))
            if len(digits) > 11:
                digits = digits[:11]
            self.var_contact.set(digits)
            self.contact_entry.icursor(END)

    def validate_all_fields(self):
        """Validate that all required fields are filled"""
        errors = []
        
        # Check EmpID
        if not self.var_EmpID.get():
            errors.append("Employee ID is required")
        
        # Check Name
        if not self.var_name.get().strip():
            errors.append("Name is required")
        
        # Check Gender
        if self.var_gender.get() == "Select":
            errors.append("Please select Gender")
        
        # Check CNIC
        cnic = self.var_cnic.get().replace('-', '')
        if not cnic or len(cnic) != 13:
            errors.append("CNIC must be exactly 13 digits")
        
        # Check Contact
        contact = self.var_contact.get()
        if not contact or len(contact) != 11:
            errors.append("Contact must be exactly 11 digits")
        
        # Check Email
        if not self.var_email.get():
            errors.append("Email is required")
        else:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, self.var_email.get()):
                errors.append("Please enter a valid email address")
        
        # Check DOB
        if not self.var_DOB.get():
            errors.append("Date of Birth is required")
        
        # Check DOJ
        if not self.var_DOJ.get():
            errors.append("Joining Date is required")
        
        # Check User Type
        if not self.var_utype.get():
            errors.append("User Type is required")
        
        # Check Password
        if not self.var_Password.get():
            errors.append("Password is required")
        
        # Check Address
        if not self.txt_address.get('1.0', END).strip():
            errors.append("Address is required")
        
        # Check Salary
        if not self.var_salary.get():
            errors.append("Salary is required")
        else:
            try:
                float(self.var_salary.get())
            except:
                errors.append("Salary must be a valid number")
        
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors), parent=self.root)
            return False
        return True

    def add(self):
        if not self.validate_all_fields():
            return
            
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Check if EmpID already exists
            cur.execute("Select * from employee where EmpID=?",(self.var_EmpID.get(),))
            row = cur.fetchone()
            if row!=None:
                messagebox.showerror("Error","This Employee ID already assigned, try different",parent=self.root)
            else:
                # Check if CNIC already exists
                cnic_clean = self.var_cnic.get().replace('-', '')
                cur.execute("Select * from employee where CNIC=?",(cnic_clean,))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This CNIC already exists in the system",parent=self.root)
                    return
                
                # Clean CNIC (remove dashes)
                cnic_clean = self.var_cnic.get().replace('-', '')
                
                cur.execute("Insert into Employee(EmpID,Name,Email,Gender,CNIC,Contact,DOB,DOJ,Password,UserType,Address,Salary) values(?,?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_EmpID.get(),
                                        self.var_name.get(),
                                        self.var_email.get(),
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
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

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
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        if row:
            self.var_EmpID.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            
            # Set CNIC
            cnic = str(row[4])
            self.var_cnic.set(cnic)
            
            # Set contact
            contact = str(row[5])
            self.var_contact.set(contact)
            
            # Set dates
            self.var_DOB.set(row[6])
            self.var_DOJ.set(row[7])
            
            # Set DOB and DOJ in calendars
            try:
                dob_date = datetime.strptime(row[6], "%d/%m/%Y")
                self.dob_calendar.set_date(dob_date)
            except:
                pass
                
            try:
                doj_date = datetime.strptime(row[7], "%d/%m/%Y")
                self.doj_calendar.set_date(doj_date)
            except:
                pass
            
            self.var_Password.set(row[8])
            self.var_utype.set(row[9])
            self.txt_address.delete('1.0',END)
            self.txt_address.insert(END,row[10])
            self.var_salary.set(row[11])
            
            # Make EmpID editable for update
            self.txt_empid.config(state='normal')

    def update(self):
        if not self.validate_all_fields():
            return
            
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Check if EmpID exists
            cur.execute("Select * from employee where EmpID=?",(self.var_EmpID.get(),))
            row = cur.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
            else:
                # Check if CNIC already exists for another employee
                cnic_clean = self.var_cnic.get().replace('-', '')
                cur.execute("Select * from employee where CNIC=? AND EmpID!=?",(cnic_clean, self.var_EmpID.get()))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This CNIC already exists for another employee",parent=self.root)
                    return
                
                # Clean CNIC (remove dashes)
                cnic_clean = self.var_cnic.get().replace('-', '')
                
                cur.execute("Update employee set Name=?,Email=?,Gender=?,CNIC=?,Contact=?,DOB=?,DOJ=?,Password=?,UserType=?,Address=?,Salary=? where EmpID=?",(
                                        self.var_name.get(),
                                        self.var_email.get(),
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
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if not self.var_EmpID.get():
                messagebox.showerror("Error","Please select an employee to delete",parent=self.root)
            else:
                op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                if op==True:
                    cur.execute("delete from employee where EmpID=?",(self.var_EmpID.get(),))
                    con.commit()
                    messagebox.showinfo("Delete","Employee deleted successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
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

    def search(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search by option", parent=self.root)
                return

            if not self.var_searchtxt.get():
                messagebox.showerror("Error", "Search input is required", parent=self.root)
                return

            search_text = self.var_searchtxt.get()

            # Auto-fix EmpID input
            if self.var_searchby.get() == "EmpID" and not search_text.startswith("E"):
                search_text = "E" + search_text

            # Clean CNIC input
            if self.var_searchby.get() == "CNIC":
                search_text = search_text.replace("-", "")

            query = f"SELECT * FROM employee WHERE {self.var_searchby.get()} LIKE ?"
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
                messagebox.showinfo("Result", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()