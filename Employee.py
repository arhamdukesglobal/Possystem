#Employee.py
from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
from datetime import datetime
import re
from tkcalendar import DateEntry  # pip install tkcalendar
import os
import locale

class EmployeeClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x550+280+180")  # Increased height for CNIC field
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()
        
        # Initialize database - ensure Employee table exists
        self.initialize_database()
        
        #===========================================
        # All Variables=========
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_EmpID = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar(value="+92")  # Set default value for contact
        self.var_name = StringVar()
        self.var_DOB = StringVar()
        self.var_DOJ = StringVar()
        self.var_email = StringVar()
        self.var_salary = StringVar()
        self.var_cnic = StringVar()  # New variable for CNIC

        #===searchFrame=====
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #===options====
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","EmpID","Name","Contact","CNIC"),state="readonly",justify=CENTER,font=("Times new Roman",15))
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
        lbl_contact=Label(self.root,text="Contact No.",font=("goudy old style",15),bg="white").place(x=750,y=190)

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
        
        # Contact entry with +92 fixed prefix
        contact_frame = Frame(self.root, bg="lightyellow")
        contact_frame.place(x=850,y=190,width=180,height=30)
        
        # Label with fixed +92
        contact_label = Label(contact_frame, text="+92", font=("goudy old style",15), bg="lightyellow", fg="gray")
        contact_label.pack(side=LEFT)
        
        # Entry for remaining 10 digits
        self.contact_entry = Entry(contact_frame, textvariable=self.var_contact, font=("goudy old style",15), 
                                  bg="lightyellow", justify=LEFT)
        self.contact_entry.pack(side=LEFT, fill=BOTH, expand=True)
        self.contact_entry.bind('<KeyRelease>', self.validate_contact)
        
        # Set initial value and bind focus event
        self.var_contact.set("")
        self.contact_entry.bind('<FocusIn>', self.on_contact_focus)

        #====row3=====
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lbl_doj=Label(self.root,text="Joining Date",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lbl_salary=Label(self.root,text="Salary",font=("goudy old style",15),bg="white").place(x=750,y=230)  # Moved salary here

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
        
        # Salary entry with Rs prefix and comma formatting
        salary_frame = Frame(self.root, bg="lightyellow")
        salary_frame.place(x=850,y=230,width=180,height=30)
        
        # Label with Rs prefix
        salary_label = Label(salary_frame, text="Rs ", font=("goudy old style",15), bg="lightyellow", fg="gray")
        salary_label.pack(side=LEFT)
        
        # Entry for salary with comma formatting
        self.salary_entry = Entry(salary_frame, textvariable=self.var_salary, font=("goudy old style",15), 
                                 bg="lightyellow", justify=RIGHT)
        self.salary_entry.pack(side=LEFT, fill=BOTH, expand=True)
        self.salary_entry.bind('<KeyRelease>', self.format_salary)
        self.salary_entry.bind('<FocusOut>', self.format_salary_final)

        #====row4=====
        lbl_address=Label(self.root,text="Address",font=("goudy old style",15),bg="white").place(x=50,y=270)

        # Address entry - expanded to take more space
        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=700,height=60)  # Expanded width

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

        # Removed Password and UserType columns
        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("EmpID","Name","Email","Gender","CNIC","Contact","DOB","DOJ","Address","Salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
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
        self.EmployeeTable.column("Address",width=150)
        self.EmployeeTable.column("Salary",width=100)

        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        
        # Generate initial EmpID and show data
        self.generate_emp_id()
        self.show()

    def initialize_database(self):
        """Ensure the Employee table exists in the database with new structure"""
        try:
            con = sqlite3.connect(database=r'Possystem.db')
            cur = con.cursor()
            
            # Check if old table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Employee'")
            table_exists = cur.fetchone()
            
            if table_exists:
                # Check if old table has Password and UserType columns
                cur.execute("PRAGMA table_info(Employee)")
                columns = [col[1] for col in cur.fetchall()]
                
                if 'Password' in columns and 'UserType' in columns:
                    # Create new table without Password and UserType
                    cur.execute('''CREATE TABLE IF NOT EXISTS Employee_new (
                                EmpID TEXT PRIMARY KEY,
                                Name TEXT NOT NULL,
                                Email TEXT,
                                Gender TEXT,
                                CNIC TEXT UNIQUE,
                                Contact TEXT,
                                DOB TEXT,
                                DOJ TEXT,
                                Address TEXT,
                                Salary TEXT)''')
                    
                    # Copy data from old table to new table (excluding Password and UserType)
                    cur.execute('''INSERT INTO Employee_new (EmpID, Name, Email, Gender, CNIC, Contact, DOB, DOJ, Address, Salary)
                                SELECT EmpID, Name, Email, Gender, CNIC, Contact, DOB, DOJ, Address, Salary 
                                FROM Employee''')
                    
                    # Drop old table
                    cur.execute("DROP TABLE Employee")
                    
                    # Rename new table to Employee
                    cur.execute("ALTER TABLE Employee_new RENAME TO Employee")
                    
                    messagebox.showinfo("Database Update", "Employee table structure updated successfully. Password and UserType fields have been removed.")
                else:
                    # Table already has new structure, just ensure it exists
                    cur.execute('''CREATE TABLE IF NOT EXISTS Employee (
                                EmpID TEXT PRIMARY KEY,
                                Name TEXT NOT NULL,
                                Email TEXT,
                                Gender TEXT,
                                CNIC TEXT UNIQUE,
                                Contact TEXT,
                                DOB TEXT,
                                DOJ TEXT,
                                Address TEXT,
                                Salary TEXT)''')
            else:
                # Create table with new structure
                cur.execute('''CREATE TABLE IF NOT EXISTS Employee (
                            EmpID TEXT PRIMARY KEY,
                            Name TEXT NOT NULL,
                            Email TEXT,
                            Gender TEXT,
                            CNIC TEXT UNIQUE,
                            Contact TEXT,
                            DOB TEXT,
                            DOJ TEXT,
                            Address TEXT,
                            Salary TEXT)''')
            
            con.commit()
            con.close()
        except Exception as e:
            print(f"Error initializing database: {e}")

    def on_dob_select(self, event):
        self.var_DOB.set(self.dob_calendar.get_date().strftime("%d/%m/%Y"))
        # Automatically validate dates after DOB selection
        if self.var_DOB.get() and self.var_DOJ.get():
            self.validate_dates()

    def on_doj_select(self, event):
        self.var_DOJ.set(self.doj_calendar.get_date().strftime("%d/%m/%Y"))
        # Automatically validate dates after DOJ selection
        if self.var_DOB.get() and self.var_DOJ.get():
            self.validate_dates()

    def validate_dates(self):
        """Validate that DOB year is always smaller than DOJ year"""
        try:
            dob_str = self.var_DOB.get()
            doj_str = self.var_DOJ.get()
            
            if dob_str and doj_str:
                dob_date = datetime.strptime(dob_str, "%d/%m/%Y")
                doj_date = datetime.strptime(doj_str, "%d/%m/%Y")
                
                # Check if DOB is after or equal to DOJ
                if dob_date >= doj_date:
                    messagebox.showwarning("Date Validation", 
                                         "Date of Birth must be earlier than Joining Date.\n"
                                         "Please adjust the dates.", parent=self.root)
                    return False
                
                # Check if employee is at least 18 years old at joining
                age_at_joining = doj_date.year - dob_date.year
                if age_at_joining < 18:
                    messagebox.showwarning("Age Validation",
                                         "Employee must be at least 18 years old at joining date.\n"
                                         "Please adjust the dates.", parent=self.root)
                    return False
            return True
        except ValueError:
            return True  # If dates are not properly formatted, skip validation

    def on_contact_focus(self, event):
        """Set cursor to the beginning of the entry when focused"""
        self.contact_entry.icursor(0)

    def format_salary(self, event=None):
        """Format salary with commas as user types"""
        # Get current value without formatting
        current_value = self.salary_entry.get()
        
        # Remove all non-digit characters except decimal point
        if current_value:
            # Remove Rs prefix if present
            current_value = current_value.replace('Rs', '').strip()
            
            # Remove all commas for processing
            digits = ''.join(filter(lambda x: x.isdigit() or x == '.', current_value))
            
            # Limit to 2 decimal places
            if '.' in digits:
                parts = digits.split('.')
                if len(parts) > 1:
                    digits = parts[0] + '.' + parts[1][:2]
            
            # Format with commas for thousands
            if digits:
                try:
                    # Format the number with commas
                    formatted = self.format_number_with_commas(digits)
                    if formatted != current_value:
                        self.var_salary.set(formatted)
                        # Move cursor to end
                        self.salary_entry.icursor(len(formatted))
                except:
                    pass

    def format_salary_final(self, event=None):
        """Final formatting when focus leaves salary field"""
        current_value = self.var_salary.get()
        if current_value:
            # Remove Rs prefix and commas for processing
            clean_value = current_value.replace('Rs', '').replace(',', '').strip()
            
            if clean_value:
                try:
                    # Format with commas and add Rs prefix
                    formatted = self.format_number_with_commas(clean_value)
                    self.var_salary.set(formatted)
                except:
                    pass

    def format_number_with_commas(self, value):
        """Format a number string with commas for thousands"""
        try:
            # If it's a decimal number
            if '.' in value:
                parts = value.split('.')
                integer_part = parts[0]
                decimal_part = parts[1] if len(parts) > 1 else ''
                
                # Format integer part with commas
                if integer_part:
                    integer_part = '{:,}'.format(int(integer_part))
                
                # Combine parts
                result = integer_part
                if decimal_part:
                    result += '.' + decimal_part
            else:
                # Format whole number
                result = '{:,}'.format(int(value))
            
            return result
        except:
            return value

    def generate_emp_id(self):
        """Generate a new unique EmpID starting with E followed by 4 digits"""
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            # Ensure table exists (should already exist from initialize_database)
            cur.execute('''CREATE TABLE IF NOT EXISTS Employee (
                        EmpID TEXT PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Email TEXT,
                        Gender TEXT,
                        CNIC TEXT UNIQUE,
                        Contact TEXT,
                        DOB TEXT,
                        DOJ TEXT,
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
                except ValueError:
                    # If the ID format is wrong, start from 1
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
                # Move cursor to end
                self.cnic_entry.icursor(len(formatted))

    def validate_contact(self, event=None):
        """Validate Contact to accept exactly 10 digits after +92"""
        current_text = self.var_contact.get()
        if current_text:
            # Remove non-digits
            digits = ''.join(filter(str.isdigit, current_text))
            if len(digits) > 10:
                digits = digits[:10]
            self.var_contact.set(digits)
            # Move cursor to end
            self.contact_entry.icursor(len(digits))

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
        if not contact or len(contact) != 10:
            errors.append("Contact must be exactly 10 digits after +92")
        else:
            # Add +92 prefix for validation
            full_contact = "+92" + contact
            if not re.match(r'^\+92[0-9]{10}$', full_contact):
                errors.append("Contact must be in format +92XXXXXXXXXX")
        
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
        else:
            # Validate dates
            if not self.validate_dates():
                errors.append("Date of Birth must be earlier than Joining Date")
        
        # Check Address
        if not self.txt_address.get('1.0', END).strip():
            errors.append("Address is required")
        
        # Check Salary
        salary_value = self.var_salary.get().replace(',', '').replace('Rs', '').strip()
        if not salary_value:
            errors.append("Salary is required")
        else:
            try:
                salary_val = float(salary_value)
                if salary_val <= 0:
                    errors.append("Salary must be greater than 0")
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
            
            # Format contact with +92 prefix
            contact_full = "+92" + self.var_contact.get()
            
            # Clean salary value
            salary_clean = self.var_salary.get().replace(',', '').replace('Rs', '').strip()
            
            # Insert employee data
            cur.execute("Insert into Employee(EmpID,Name,Email,Gender,CNIC,Contact,DOB,DOJ,Address,Salary) values(?,?,?,?,?,?,?,?,?,?)",(
                                    self.var_EmpID.get(),
                                    self.var_name.get().strip(),
                                    self.var_email.get().strip(),
                                    self.var_gender.get(),
                                    cnic_clean,
                                    contact_full,
                                    self.var_DOB.get(),
                                    self.var_DOJ.get(),
                                    self.txt_address.get('1.0',END).strip(),
                                    salary_clean,
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

    def show(self):
        con = sqlite3.connect(database=r'Possystem.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from employee ORDER BY EmpID")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                formatted_row = list(row)
                
                # Format CNIC for display
                if row[4]:  # CNIC column
                    cnic = str(row[4])
                    if len(cnic) == 13:
                        formatted_cnic = f"{cnic[:5]}-{cnic[5:12]}-{cnic[12:]}"
                        formatted_row[4] = formatted_cnic
                
                # Format salary with Rs prefix and commas
                if row[9]:  # Salary column (now at index 9)
                    try:
                        salary_value = float(row[9])
                        formatted_salary = "Rs " + '{:,.2f}'.format(salary_value)
                        formatted_row[9] = formatted_salary
                    except:
                        formatted_row[9] = row[9]
                
                self.EmployeeTable.insert('',END,values=formatted_row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error displaying data: {str(ex)}",parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        if not f:
            return
            
        content = self.EmployeeTable.item(f)
        row = content['values']
        if row:
            self.var_EmpID.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            
            # Set CNIC
            cnic = str(row[4])
            self.var_cnic.set(cnic)
            
            # Set contact (remove +92 prefix for display)
            contact = str(row[5])
            if contact.startswith('+92'):
                contact = contact[3:]  # Remove +92 prefix
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
            
            # Set Address
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[8])
            
            # Set salary (remove Rs prefix for editing)
            salary = str(row[9])
            if salary.startswith('Rs'):
                salary = salary[2:].strip()  # Remove Rs prefix
            self.var_salary.set(salary)
            
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
            
            # Format contact with +92 prefix
            contact_full = "+92" + self.var_contact.get()
            
            # Clean salary value
            salary_clean = self.var_salary.get().replace(',', '').replace('Rs', '').strip()
            
            cur.execute("Update employee set Name=?,Email=?,Gender=?,CNIC=?,Contact=?,DOB=?,DOJ=?,Address=?,Salary=? where EmpID=?",(
                                    self.var_name.get().strip(),
                                    self.var_email.get().strip(),
                                    self.var_gender.get(),
                                    cnic_clean,
                                    contact_full,
                                    self.var_DOB.get(),
                                    self.var_DOJ.get(),
                                    self.txt_address.get('1.0',END).strip(),
                                    salary_clean,
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
        self.var_contact.set("")  # Clear contact (only 10 digits part)
        self.var_DOB.set("")
        self.var_DOJ.set("")
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
            
            # For contact search, add +92 prefix
            if search_column == "Contact":
                if not search_text.startswith('+92'):
                    search_text = "+92" + search_text

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
                    # Format salary with Rs prefix and commas
                    if row[9]:
                        try:
                            salary_value = float(row[9])
                            formatted_row[9] = "Rs " + '{:,.2f}'.format(salary_value)
                        except:
                            pass
                    self.EmployeeTable.insert("", END, values=formatted_row)
            else:
                messagebox.showinfo("Result", "No records found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error searching: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()