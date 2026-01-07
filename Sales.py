from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import re

class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+50+50")
        self.root.title("Inventory Management System | Developed by Dukes Tech Services")
        self.root.config(bg="#E6FBFF")
        self.root.focus_force()
        
        # Make window resizable
        self.root.minsize(1100, 600)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.Invoice_List = []
        self.var_Invoice = StringVar()
        
        #========Main Container========
        main_container = Frame(self.root, bg="#E6FBFF")
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Configure grid weights for responsiveness
        main_container.columnconfigure(0, weight=0)  # Left frame (invoices list)
        main_container.columnconfigure(1, weight=1)  # Middle frame (invoice display)
        main_container.columnconfigure(2, weight=0)  # Right frame (image)
        main_container.rowconfigure(0, weight=0)     # Header
        main_container.rowconfigure(1, weight=0)     # Search area
        main_container.rowconfigure(2, weight=1)     # Content area
        
        #========Header========
        header_frame = Frame(main_container, bg="#389b91", height=80)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 10))
        header_frame.grid_propagate(False)
        header_frame.columnconfigure(0, weight=1)
        
        lbl_title = Label(header_frame, text="View Customer Invoice", 
                         font=("goudy old style", 30), bg="#389b91", 
                         fg="white")
        lbl_title.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        #========Search Area========
        search_frame = Frame(main_container, bg="white", bd=2, relief=RIDGE)
        search_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 10), ipady=10)
        search_frame.columnconfigure(1, weight=1)
        
        lbl_invoice = Label(search_frame, text="Invoice No.", 
                           font=("Arial Black", 14), bg="white")
        lbl_invoice.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        # Entry with autocomplete
        self.txt_invoice = Entry(search_frame, textvariable=self.var_Invoice, 
                                font=("Aptos", 14), bg="light yellow")
        self.txt_invoice.grid(row=0, column=1, sticky="ew", padx=10, pady=10, ipady=5)
        
        # Listbox for suggestions - will be positioned absolutely
        self.suggestion_listbox = Listbox(search_frame, font=("Aptos", 12), 
                                          bg="lightyellow", selectmode=SINGLE)
        self.suggestion_listbox.bind('<<ListboxSelect>>', self.fill_entry_from_suggestion)
        
        # Bind events for suggestions
        self.txt_invoice.bind('<KeyRelease>', self.show_suggestions)
        self.txt_invoice.bind('<FocusOut>', lambda e: self.root.after(100, self.hide_suggestions))
        
        btn_search = Button(search_frame, text="Search", command=self.search,
                           font=("Times New Roman", 14, "bold"), bg="#2196f3", 
                           fg="white", cursor="hand2", padx=20)
        btn_search.grid(row=0, column=2, padx=10, pady=10, ipady=5)
        
        btn_clear = Button(search_frame, text="Clear", command=self.clear,
                          font=("Times New Roman", 14, "bold"), bg="lightgray",
                          cursor="hand2", padx=20)
        btn_clear.grid(row=0, column=3, padx=(0, 20), pady=10, ipady=5)
        
        #========Content Area========
        content_frame = Frame(main_container, bg="#E6FBFF")
        content_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 40))
        content_frame.columnconfigure(0, weight=0)  # Invoice list
        content_frame.columnconfigure(1, weight=1)  # Invoice display
        content_frame.columnconfigure(2, weight=0)  # Image
        content_frame.rowconfigure(0, weight=1)
        
        #=======Sales List=======
        sales_container = Frame(content_frame, bg="white", bd=2, relief=RIDGE)
        sales_container.grid(row=0, column=0, sticky="nsew", padx=(5, 10), pady=5)
        sales_container.columnconfigure(0, weight=1)
        sales_container.rowconfigure(1, weight=1)
        
        lbl_sales_title = Label(sales_container, text="Available Invoices", 
                               font=("goudy old style", 16, "bold"), 
                               bg="orange", fg="white", anchor="w")
        lbl_sales_title.grid(row=0, column=0, sticky="ew", padx=10, pady=5, ipady=5)
        
        list_frame = Frame(sales_container, bg="white")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        scrolly = Scrollbar(list_frame, orient=VERTICAL)
        self.Sales_List = Listbox(list_frame, font=("goudy old style", 12), 
                                 bg="white", yscrollcommand=scrolly.set, 
                                 selectmode=SINGLE, activestyle="none")
        scrolly.config(command=self.Sales_List.yview)
        scrolly.grid(row=0, column=1, sticky="ns")
        self.Sales_List.grid(row=0, column=0, sticky="nsew")
        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)
        
        # Set minimum and preferred width for sales container
        sales_container.config(width=300)
        sales_container.grid_propagate(False)

        #=======Invoice Details=======
        invoice_container = Frame(content_frame, bg="white", bd=2, relief=RIDGE)
        invoice_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        invoice_container.columnconfigure(0, weight=1)
        invoice_container.rowconfigure(1, weight=1)
        
        lbl_invoice_title = Label(invoice_container, text="Customer Bill Area", 
                                 font=("goudy old style", 18, "bold"), 
                                 bg="orange", fg="white", anchor="w")
        lbl_invoice_title.grid(row=0, column=0, sticky="ew", padx=10, pady=5, ipady=5)
        
        text_frame = Frame(invoice_container, bg="white")
        text_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        scrolly2 = Scrollbar(text_frame, orient=VERTICAL)
        scrollx2 = Scrollbar(text_frame, orient=HORIZONTAL)
        
        self.Invoice_area = Text(text_frame, bg="lightyellow", 
                                font=("Courier", 12),
                                wrap=NONE,
                                yscrollcommand=scrolly2.set,
                                xscrollcommand=scrollx2.set)
        
        scrolly2.config(command=self.Invoice_area.yview)
        scrollx2.config(command=self.Invoice_area.xview)
        
        self.Invoice_area.grid(row=0, column=0, sticky="nsew")
        scrolly2.grid(row=0, column=1, sticky="ns")
        scrollx2.grid(row=1, column=0, sticky="ew", columnspan=2)

        #======Image Area=======
        try:
            self.bill_photo = Image.open("IMAGES/cat2.jpg")
            self.bill_photo = self.bill_photo.resize((350, 350), Image.LANCZOS)
            self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
            
            image_container = Frame(content_frame, bg="white", bd=2, relief=RIDGE)
            image_container.grid(row=0, column=2, sticky="nsew", padx=(10, 5), pady=5)
            image_container.columnconfigure(0, weight=1)
            image_container.rowconfigure(1, weight=1)
            
            lbl_image_title = Label(image_container, text="Invoice Preview", 
                                   font=("goudy old style", 16, "bold"), 
                                   bg="orange", fg="white", anchor="w")
            lbl_image_title.grid(row=0, column=0, sticky="ew", padx=10, pady=5, ipady=5)
            
            lbl_image = Label(image_container, image=self.bill_photo, bd=0, bg="white")
            lbl_image.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            
            # Set fixed size for image container
            image_container.config(width=370, height=400)
            image_container.grid_propagate(False)
            
        except Exception as e:
            print(f"Image error: {e}")
            # Create placeholder frame if image not found
            image_container = Frame(content_frame, bg="white", bd=2, relief=RIDGE, 
                                  width=370, height=400)
            image_container.grid(row=0, column=2, sticky="nsew", padx=(10, 5), pady=5)
            image_container.grid_propagate(False)
            
            lbl_image_title = Label(image_container, text="Invoice Preview", 
                                   font=("goudy old style", 16, "bold"), 
                                   bg="orange", fg="white", anchor="w")
            lbl_image_title.grid(row=0, column=0, sticky="ew", padx=10, pady=5, ipady=5)
            
            lbl_no_image = Label(image_container, text="Preview Image\nNot Available", 
                                font=("Arial", 14), bg="white", fg="gray")
            lbl_no_image.place(relx=0.5, rely=0.5, anchor=CENTER)

        #======Status Bar========
        self.status_bar = Label(main_container, text="Total Invoices: 0 | Ready", 
                               font=("Arial", 12), bg="#389b91", fg="white", 
                               bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=(5, 0))
        
        # Bind window resize event
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Initial show
        self.show()

    def on_window_resize(self, event=None):
        """Handle window resize for responsive design"""
        # Update suggestion listbox position if visible
        if self.suggestion_listbox.winfo_ismapped():
            self.position_suggestions()

    def position_suggestions(self):
        """Position suggestion listbox below the entry field"""
        # Get entry widget position in screen coordinates
        entry_x = self.txt_invoice.winfo_rootx()
        entry_y = self.txt_invoice.winfo_rooty()
        entry_width = self.txt_invoice.winfo_width()
        entry_height = self.txt_invoice.winfo_height()
        
        # Position listbox below entry
        self.suggestion_listbox.place(x=0, y=entry_height, 
                                     width=entry_width, 
                                     height=min(150, self.suggestion_listbox.size() * 25))

    def show_suggestions(self, event=None):
        """Show autocomplete suggestions based on input"""
        search_term = self.var_Invoice.get().strip().lower()
        
        if not search_term:
            self.hide_suggestions()
            return
        
        # Filter invoices that match the search term
        suggestions = [inv for inv in self.Invoice_List if search_term in inv.lower()]
        
        if not suggestions:
            self.hide_suggestions()
            return
        
        # Update suggestion listbox
        self.suggestion_listbox.delete(0, END)
        for suggestion in suggestions[:8]:  # Limit to 8 suggestions
            self.suggestion_listbox.insert(END, suggestion)
        
        # Show and position the suggestion listbox
        self.position_suggestions()
        self.suggestion_listbox.lift()  # Bring to front

    def hide_suggestions(self):
        """Hide suggestion listbox"""
        if self.suggestion_listbox.winfo_ismapped():
            self.suggestion_listbox.place_forget()

    def fill_entry_from_suggestion(self, event):
        """Fill the entry field when a suggestion is selected"""
        try:
            selection = self.suggestion_listbox.curselection()
            if selection:
                selected_invoice = self.suggestion_listbox.get(selection[0])
                self.var_Invoice.set(selected_invoice)
                self.hide_suggestions()
                # Auto-search when suggestion is selected
                self.search()
        except:
            pass

    def show(self):
        """Load all invoice files from bills directory"""
        del self.Invoice_List[:]
        self.Sales_List.delete(0, END)
        
        # Check if bills directory exists
        if not os.path.exists('bills'):
            os.makedirs('bills')
            self.Sales_List.insert(END, "No invoices found")
            self.status_bar.config(text="Total Invoices: 0 | No invoices found")
            return
        
        try:
            # Get all .txt files from bills directory
            invoice_files = [f for f in os.listdir('bills') if f.endswith('.txt')]
            
            if not invoice_files:
                self.Sales_List.insert(END, "No invoices found")
                self.status_bar.config(text="Total Invoices: 0 | No invoices found")
                return
            
            # Sort invoices numerically if they contain numbers
            invoice_files.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
            
            for file_name in invoice_files:
                # Extract invoice number (remove .txt extension)
                invoice_no = file_name.replace('.txt', '')
                self.Sales_List.insert(END, invoice_no)
                self.Invoice_List.append(invoice_no)
            
            self.status_bar.config(text=f"Total Invoices: {len(self.Invoice_List)} | Ready")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading invoices: {str(e)}", parent=self.root)
            self.status_bar.config(text=f"Error loading invoices")

    def get_data(self, ev):
        """Display selected invoice details"""
        try:
            selection = self.Sales_List.curselection()
            if not selection:
                return
                
            file_name = self.Sales_List.get(selection[0])
            
            # Check if it's the "No invoices found" message
            if file_name == "No invoices found":
                return
            
            self.display_invoice(file_name)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading invoice: {str(e)}", parent=self.root)

    def display_invoice(self, invoice_no):
        """Display invoice content"""
        self.Invoice_area.delete('1.0', END)
        
        file_path = f'bills/{invoice_no}.txt'
        
        if not os.path.exists(file_path):
            self.Invoice_area.insert(END, f"Invoice {invoice_no} not found!")
            return
        
        try:
            with open(file_path, 'r') as fp:
                content = fp.read()
                self.Invoice_area.insert(END, content)
                
                # Highlight the invoice in the list
                self.highlight_invoice_in_list(invoice_no)
                
                # Update status bar
                self.status_bar.config(text=f"Displaying Invoice: {invoice_no}")
                
        except Exception as e:
            self.Invoice_area.insert(END, f"Error reading invoice: {str(e)}")

    def highlight_invoice_in_list(self, invoice_no):
        """Highlight the selected invoice in the listbox"""
        for i in range(self.Sales_List.size()):
            if self.Sales_List.get(i) == invoice_no:
                self.Sales_List.selection_clear(0, END)
                self.Sales_List.selection_set(i)
                self.Sales_List.see(i)
                break

    def search(self):
        """Search for invoice by number"""
        invoice_no = self.var_Invoice.get().strip()
        
        if not invoice_no:
            messagebox.showerror("Error", "Invoice No. is required", parent=self.root)
            return
        
        # Hide suggestions
        self.hide_suggestions()
        
        # Check if invoice exists in our list
        if invoice_no in self.Invoice_List:
            self.display_invoice(invoice_no)
            # Also update the entry to show full invoice number
            self.var_Invoice.set(invoice_no)
        else:
            # Try to find similar invoices
            similar = [inv for inv in self.Invoice_List if invoice_no.lower() in inv.lower()]
            if similar:
                # If similar invoices found, show them in suggestions
                self.suggestion_listbox.delete(0, END)
                for inv in similar[:8]:
                    self.suggestion_listbox.insert(END, inv)
                
                self.position_suggestions()
                self.suggestion_listbox.lift()
                
                messagebox.showinfo("Info", f"Found {len(similar)} similar invoices. Select from suggestions.", 
                                  parent=self.root)
            else:
                messagebox.showerror("Error", f"Invoice No. '{invoice_no}' not found", parent=self.root)
                self.Invoice_area.delete('1.0', END)
                self.Invoice_area.insert(END, f"Invoice '{invoice_no}' not found!")

    def clear(self):
        """Clear all fields"""
        self.var_Invoice.set("")
        self.Invoice_area.delete('1.0', END)
        self.hide_suggestions()
        self.Sales_List.selection_clear(0, END)
        self.status_bar.config(text=f"Total Invoices: {len(self.Invoice_List)} | Ready")


if __name__ == "__main__":
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()