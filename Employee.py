#Employee.py
from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
from datetime import datetime
import re

class EmployeeClass:
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

        #===searchFrame=====
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #===options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Email","Name","Contact"),state="readonly",justify=CENTER,font=("Times new Roman",15))
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
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=750,y=150)

        # EmpID entry - integer only
        self.txt_empid=Entry(self.root,textvariable=self.var_EmpID,font=("goudy old style",15),bg="lightyellow")
        self.txt_empid.place(x=150,y=150,width=180)
        self.txt_empid.bind('<KeyRelease>', self.validate_empid)
        
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        
        # Contact entry with country code placeholder and validation
        contact_frame = Frame(self.root, bg="lightyellow")
        contact_frame.place(x=850,y=150,width=180,height=30)
        
        lbl_country_code = Label(contact_frame, text="+92", font=("goudy old style",15), bg="lightyellow", fg="black")
        lbl_country_code.pack(side=LEFT, padx=(5,0))
        
        self.contact_entry = Entry(contact_frame, textvariable=self.var_contact, font=("goudy old style",15), bg="lightyellow", bd=0)
        self.contact_entry.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Add placeholder text
        self.contact_entry.insert(0, "XXXXXXXXXXX")
        self.contact_entry.config(fg="gray")
        
        # Bind events for placeholder and validation
        self.contact_entry.bind("<FocusIn>", self.on_contact_focus_in)
        self.contact_entry.bind("<FocusOut>", self.on_contact_focus_out)
        self.contact_entry.bind('<KeyRelease>', self.validate_contact)
        
        #====row2=====
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",15),bg="white").place(x=350,y=190)
        lbl_doj=Label(self.root,text="Joining Date",font=("goudy old style",15),bg="white").place(x=750,y=190)

        # Name entry - string only (alphabets and spaces)
        self.txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow")
        self.txt_name.place(x=150,y=190,width=180)
        self.txt_name.bind('<KeyRelease>', self.validate_name)
        
        # DOB entry with placeholder
        self.dob_entry = Entry(self.root, textvariable=self.var_DOB, font=("goudy old style",15), bg="lightyellow")
        self.dob_entry.place(x=500,y=190,width=180)
        self.dob_entry.insert(0, "DD/MM/YYYY")
        self.dob_entry.config(fg="gray")
        self.dob_entry.bind("<FocusIn>", lambda e: self.on_date_focus_in(e, "dob"))
        self.dob_entry.bind("<FocusOut>", lambda e: self.on_date_focus_out(e, "dob"))
        
        # DOJ entry with placeholder (renamed to Joining Date)
        self.doj_entry = Entry(self.root, textvariable=self.var_DOJ, font=("goudy old style",15), bg="lightyellow")
        self.doj_entry.place(x=850,y=190,width=180)
        self.doj_entry.insert(0, "DD/MM/YYYY")
        self.doj_entry.config(fg="gray")
        self.doj_entry.bind("<FocusIn>", lambda e: self.on_date_focus_in(e, "doj"))
        self.doj_entry.bind("<FocusOut>", lambda e: self.on_date_focus_out(e, "doj"))

        #====row3=====
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        #lbl_pass=Label(self.root,text="Password",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",15),bg="white").place(x=750,y=230)

        # Email entry - alphanumeric with @ and .
        self.txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow")
        self.txt_email.place(x=150,y=230,width=180)
        self.txt_email.bind('<FocusOut>', self.validate_email)
        
        # Password entry - removed as per requirement
        #self.txt_pass=Entry(self.root,textvariable=self.var_Password,font=("goudy old style",15),bg="lightyellow", show="*")
        #self.txt_pass.place(x=500,y=230,width=180)
        
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Employee"),state="readonly",justify=CENTER,font=("Times new Roman",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #====row4=====
        lbl_address=Label(self.root,text="Address",font=("goudy old style",15),bg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salary",font=("goudy old style",15),bg="white").place(x=500,y=270)

        # Address entry - alphanumeric with common punctuation
        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        
        # Salary entry with Rs prefix and formatting
        salary_frame = Frame(self.root, bg="lightyellow")
        salary_frame.place(x=600,y=270,width=180,height=30)
        
        lbl_rs = Label(salary_frame, text="Rs", font=("goudy old style",15), bg="lightyellow", fg="black")
        lbl_rs.pack(side=LEFT, padx=(5,0))
        
        self.salary_entry = Entry(salary_frame, textvariable=self.var_salary, font=("goudy old style",15), bg="lightyellow", bd=0)
        self.salary_entry.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.salary_entry.bind("<KeyRelease>", self.format_salary)
        self.salary_entry.bind("<FocusOut>", self.format_salary)
        self.salary_entry.bind('<KeyRelease>', self.validate_salary)

        #====buttons=====
        btn_add = Button(self.root,text="Save",command=self.add, font=("Aptos",15),bg="#2196f3",fg="White",cursor="hand2").place(x=500,y=340,width=110,height=28)
        btn_update = Button(self.root,text="Update",command=self.update, font=("Aptos",15),bg="#4caf50",fg="White",cursor="hand2").place(x=620,y=340,width=110,height=28)
        btn_delete = Button(self.root,text="Delete",command=self.delete, font=("Aptos",15),bg="#f44336",fg="White",cursor="hand2").place(x=740,y=340,width=110,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear, font=("Aptos",15),bg="#607d8b",fg="White",cursor="hand2").place(x=860,y=340,width=110,height=28)

        #===Employee Details====
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=380,relwidth=1,height=120)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("EmpID","Name","Email","Gender","Contact","DOB","DOJ","Password","UserType","Address","Salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        
        self.EmployeeTable.heading("EmpID",text="Emp ID")
        self.EmployeeTable.heading("Name",text="Name")
        self.EmployeeTable.heading("Email",text="Email")
        self.EmployeeTable.heading("Gender",text="Gender")
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
        self.EmployeeTable.column("Gender",width=100)
        self.EmployeeTable.column("Contact",width=100)
        self.EmployeeTable.column("DOB",width=100)
        self.EmployeeTable.column("DOJ",width=100)
        self.EmployeeTable.column("Password",width=100)
        self.EmployeeTable.column("UserType",width=100)
        self.EmployeeTable.column("Address",width=100)
        self.EmployeeTable.column("Salary",width=100)

        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        
        self.show()
#==================================================================

    def validate_empid(self, event=None):
        """Validate EmpID to accept only integers"""
        current_text = self.var_EmpID.get()
        if current_text:
            # Remove non-digits
            digits_only = ''.join(filter(str.isdigit, current_text))
            self.var_EmpID.set(digits_only)

    def validate_name(self, event=None):
        """Validate Name to accept only alphabets and spaces"""
        current_text = self.var_name.get()
        if current_text:
            # Allow only alphabets, spaces, and apostrophes
            filtered = ''.join([c for c in current_text if c.isalpha() or c.isspace() or c == "'" or c == "-"])
            if filtered != current_text:
                self.var_name.set(filtered)
                # Move cursor to end
                self.txt_name.icursor(END)

    def validate_contact(self, event=None):
        """Validate Contact to accept exactly 11 digits after +92"""
        current_text = self.var_contact.get()
        if current_text and current_text != "XXXXXXXXXXX":
            # Remove non-digits
            digits_only = ''.join(filter(str.isdigit, current_text))
            
            # Limit to 11 digits
            if len(digits_only) > 10:
                digits_only = digits_only[:10]
            
            self.var_contact.set(digits_only)
            # Move cursor to end
            self.contact_entry.icursor(END)

    def validate_email(self, event=None):
        """Validate Email format"""
        email = self.var_email.get()
        if email:
            # Basic email validation
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                messagebox.showwarning("Warning", "Please enter a valid email address", parent=self.root)
                self.txt_email.focus_set()

    def validate_salary(self, event=None):
        """Validate Salary to accept only numbers"""
        current_text = self.var_salary.get()
        if current_text:
            # Remove Rs prefix if present
            current_text = current_text.replace('Rs', '').strip()
            
            # Remove non-digits and decimal point
            filtered = ''.join([c for c in current_text if c.isdigit() or c == '.'])
            
            # Ensure only one decimal point
            if filtered.count('.') > 1:
                parts = filtered.split('.')
                filtered = parts[0] + '.' + ''.join(parts[1:])
            
            self.var_salary.set(filtered)

    def on_contact_focus_in(self, event):
        if self.var_contact.get() == "XXXXXXXXXXX":
            self.contact_entry.delete(0, END)
            self.contact_entry.config(fg="black")

    def on_contact_focus_out(self, event):
        if not self.var_contact.get():
            self.contact_entry.insert(0, "XXXXXXXXXXX")
            self.contact_entry.config(fg="gray")
        else:
            # Validate contact length
            contact = self.var_contact.get()
            if contact != "XXXXXXXXXXX" and len(contact) != 11:
                messagebox.showwarning("Warning", "Contact number must be exactly 11 digits", parent=self.root)
                self.contact_entry.focus_set()

    def on_date_focus_in(self, event, field):
        widget = event.widget
        if field == "dob":
            if self.var_DOB.get() == "DD/MM/YYYY":
                widget.delete(0, END)
                widget.config(fg="black")
        else:
            if self.var_DOJ.get() == "DD/MM/YYYY":
                widget.delete(0, END)
                widget.config(fg="black")

    def on_date_focus_out(self, event, field):
        widget = event.widget
        if field == "dob":
            if not self.var_DOB.get():
                widget.insert(0, "DD/MM/YYYY")
                widget.config(fg="gray")
            else:
                # Validate date format
                date_str = self.var_DOB.get()
                if self.validate_date(date_str):
                    # Format date as DD/MM/YYYY
                    try:
                        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                        self.var_DOB.set(date_obj.strftime("%d/%m/%Y"))
                    except:
                        pass
                else:
                    messagebox.showerror("Error", "Please enter date in DD/MM/YYYY format", parent=self.root)
        else:
            if not self.var_DOJ.get():
                widget.insert(0, "DD/MM/YYYY")
                widget.config(fg="gray")
            else:
                # Validate date format
                date_str = self.var_DOJ.get()
                if self.validate_date(date_str):
                    # Format date as DD/MM/YYYY
                    try:
                        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                        self.var_DOJ.set(date_obj.strftime("%d/%m/%Y"))
                    except:
                        pass
                else:
                    messagebox.showerror("Error", "Please enter date in DD/MM/YYYY format", parent=self.root)

    def validate_date(self, date_str):
        """Validate date in DD/MM/YYYY format"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def format_salary(self, event=None):
        """Format salary with commas for thousands and add Rs prefix"""
        try:
            salary_str = self.var_salary.get()
            if not salary_str:
                return
                
            # Remove any existing commas and Rs prefix
            salary_str = salary_str.replace('Rs', '').replace(',', '').strip()
            
            if salary_str and salary_str != "0":
                # Convert to integer and format with commas
                try:
                    # Handle decimal values
                    if '.' in salary_str:
                        salary_float = float(salary_str)
                        formatted = f"Rs {salary_float:,.2f}"
                    else:
                        salary_int = int(float(salary_str))
                        formatted = f"Rs {salary_int:,}"
                    
                    self.var_salary.set(formatted)
                except ValueError:
                    pass
        except Exception as e:
            print(f"Error formatting salary: {e}")

    def add(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Validation checks
            if self.var_EmpID.get()=="":
                messagebox.showerror("Error","Employee ID is required",parent=self.root)
                return
            elif not self.var_EmpID.get().isdigit():
                messagebox.showerror("Error","Employee ID must be a number",parent=self.root)
                return
            elif not self.var_name.get():
                messagebox.showerror("Error","Name is required",parent=self.root)
                return
            elif self.var_contact.get() not in ["", "XXXXXXXXXXX"] and len(self.var_contact.get()) != 11:
                messagebox.showerror("Error","Contact must be exactly 11 digits",parent=self.root)
                return
            elif not self.validate_date(self.var_DOB.get()) and self.var_DOB.get() != "DD/MM/YYYY":
                messagebox.showerror("Error","Please enter Date of Birth in DD/MM/YYYY format",parent=self.root)
                return
            elif not self.validate_date(self.var_DOJ.get()) and self.var_DOJ.get() != "DD/MM/YYYY":
                messagebox.showerror("Error","Please enter Joining Date in DD/MM/YYYY format",parent=self.root)
                return
            else:
                cur.execute("Select * from employee where EmpID=?",(self.var_EmpID.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID already assigned, try different",parent=self.root)
                else:
                    # Prepare contact number with country code
                    contact = self.var_contact.get()
                    if contact == "XXXXXXXXXXX":
                        contact = ""
                    elif contact and not contact.startswith("+92"):
                        contact = "+92" + contact
                    
                    # Prepare salary (remove Rs and commas for storage)
                    salary = self.var_salary.get()
                    if salary:
                        salary = salary.replace('Rs', '').replace(',', '').strip()
                    
                    # Prepare dates
                    dob = "" if self.var_DOB.get() == "DD/MM/YYYY" else self.var_DOB.get()
                    doj = "" if self.var_DOJ.get() == "DD/MM/YYYY" else self.var_DOJ.get()
                    
                    cur.execute("Insert into Employee(EmpID,Name,Email,Gender,Contact,DOB,DOJ,Password,UserType,Address,Salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                            self.var_EmpID.get(),
                                            self.var_name.get(),
                                            self.var_email.get(),
                                            self.var_gender.get(),
                                            contact,
                                            dob,
                                            doj,
                                            self.var_Password.get(),
                                            self.var_utype.get(),
                                            self.txt_address.get('1.0',END),
                                            salary,
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                # Format salary with Rs and commas for display
                if row[10]:  # Salary column
                    try:
                        salary = float(row[10])
                        if salary.is_integer():
                            formatted_salary = f"Rs {int(salary):,}"
                        else:
                            formatted_salary = f"Rs {salary:,.2f}"
                        formatted_row = list(row)
                        formatted_row[10] = formatted_salary
                        self.EmployeeTable.insert('',END,values=formatted_row)
                    except:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        if row:
            self.var_EmpID.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            
            # Set contact (remove +92 for editing if needed)
            contact = str(row[4])
            if contact.startswith("+92"):
                contact = contact[3:]  # Remove +92
            self.var_contact.set(contact)
            self.contact_entry.delete(0, END)
            self.contact_entry.insert(0, contact)
            self.contact_entry.config(fg="black")
            
            self.var_DOB.set(row[5])
            self.var_DOJ.set(row[6])
            self.var_Password.set(row[7])
            self.var_utype.set(row[8])
            self.txt_address.delete('1.0',END)
            self.txt_address.insert(END,row[9])
            
            # Format salary for display
            salary = str(row[10])
            if salary:
                try:
                    # Remove Rs prefix if present
                    salary = salary.replace('Rs', '').strip()
                    salary_float = float(salary)
                    if salary_float.is_integer():
                        self.var_salary.set(f"Rs {int(salary_float):,}")
                    else:
                        self.var_salary.set(f"Rs {salary_float:,.2f}")
                except:
                    self.var_salary.set(salary)
            else:
                self.var_salary.set("")

    def update(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Validation checks
            if self.var_EmpID.get()=="":
                messagebox.showerror("Error","Employee ID is required",parent=self.root)
                return
            elif not self.var_EmpID.get().isdigit():
                messagebox.showerror("Error","Employee ID must be a number",parent=self.root)
                return
            elif not self.var_name.get():
                messagebox.showerror("Error","Name is required",parent=self.root)
                return
            elif self.var_contact.get() not in ["", "XXXXXXXXXXX"] and len(self.var_contact.get()) != 11:
                messagebox.showerror("Error","Contact must be exactly 11 digits",parent=self.root)
                return
            elif not self.validate_date(self.var_DOB.get()) and self.var_DOB.get() != "DD/MM/YYYY":
                messagebox.showerror("Error","Please enter Date of Birth in DD/MM/YYYY format",parent=self.root)
                return
            elif not self.validate_date(self.var_DOJ.get()) and self.var_DOJ.get() != "DD/MM/YYYY":
                messagebox.showerror("Error","Please enter Joining Date in DD/MM/YYYY format",parent=self.root)
                return
            else:
                cur.execute("Select * from employee where EmpID=?",(self.var_EmpID.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    # Prepare contact number with country code
                    contact = self.var_contact.get()
                    if contact == "XXXXXXXXXXX":
                        contact = ""
                    elif contact and not contact.startswith("+92"):
                        contact = "+92" + contact
                    
                    # Prepare salary (remove Rs and commas for storage)
                    salary = self.var_salary.get()
                    if salary:
                        salary = salary.replace('Rs', '').replace(',', '').strip()
                    
                    # Prepare dates
                    dob = "" if self.var_DOB.get() == "DD/MM/YYYY" else self.var_DOB.get()
                    doj = "" if self.var_DOJ.get() == "DD/MM/YYYY" else self.var_DOJ.get()
                    
                    cur.execute("Update employee set Name=?,Email=?,Gender=?,Contact=?,DOB=?,DOJ=?,Password=?,UserType=?,Address=?,Salary=? where EmpID=?",(
                                            self.var_name.get(),
                                            self.var_email.get(),
                                            self.var_gender.get(),
                                            contact,
                                            dob,
                                            doj,
                                            self.var_Password.get(),
                                            self.var_utype.get(),
                                            self.txt_address.get('1.0',END),
                                            salary,
                                            self.var_EmpID.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_EmpID.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where EmpID=?",(self.var_EmpID.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where EmpID=?",(self.var_EmpID.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee deleted successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_EmpID.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.contact_entry.delete(0, END)
        self.contact_entry.insert(0, "XXXXXXXXXXX")
        self.contact_entry.config(fg="gray")
        self.var_DOB.set("")
        self.var_DOJ.set("")
        self.var_Password.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("Select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        # Format salary with Rs and commas for display
                        if row[10]:  # Salary column
                            try:
                                salary = float(row[10])
                                if salary.is_integer():
                                    formatted_salary = f"Rs {int(salary):,}"
                                else:
                                    formatted_salary = f"Rs {salary:,.2f}"
                                formatted_row = list(row)
                                formatted_row[10] = formatted_salary
                                self.EmployeeTable.insert('',END,values=formatted_row)
                            except:
                                self.EmployeeTable.insert('',END,values=row)
                        else:
                            self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)



if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()