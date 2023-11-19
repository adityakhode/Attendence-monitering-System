import smtplib
import subprocess
import customtkinter as ctk
import tkinter.messagebox as tkmb
from email.mime.text import MIMEText
from databases_files import databases as db
from email.mime.multipart import MIMEMultipart

# Define the name, email, and phone entry fields as global variables
user_entry             = None
user_pass              = None
name_entry             = None
email_entry            = None
phone_entry            = None
complete_login_button  = None
complete_signup_button = None
login_button           = None
signup_button          = None
or_label               = None
back_button            = None
checkbox_value         = None
checkbox               = None


def frontend_initiliesd():
    # Selecting GUI theme - dark, light, system (for system default)
    ctk.set_appearance_mode("dark")

    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))  # Open in full screen
    app.title("Attendence")
    return app

def loginpage(app):
    global login_button, signup_button, or_label
    
    if back_button:
        back_button.place_forget()
        
    label = ctk.CTkLabel(master=app, text='Welcome')
    label.place(relx=0.5, rely=0.3, anchor="center")

    login_button = ctk.CTkButton(master=app, text='Login', command=lambda: login_or_signup("login"))
    login_button.place(relx=0.42, rely=0.45, anchor="center")

    or_label = ctk.CTkLabel(master=app, text='Or')
    or_label.place(relx=0.5, rely=0.45, anchor="center")

    signup_button = ctk.CTkButton(master=app, text='Signup', command=lambda: login_or_signup("signup"))
    signup_button.place(relx=0.58, rely=0.45, anchor="center")

def login_or_signup(action):    
    global user_entry, user_pass, name_entry, email_entry, phone_entry, complete_login_button, complete_signup_button, login_button, signup_button, or_label, back_button, checkbox_value,checkbox
    
    if action == "login":
        login_button.place_forget()
        signup_button.place_forget()
        or_label.place_forget()
        
        user_entry = ctk.CTkEntry(master=app, placeholder_text="Username")
        user_entry.place(relx=0.5, rely=0.4, anchor="center")

        user_pass = ctk.CTkEntry(master=app, placeholder_text="Password", show="*")
        user_pass.place(relx=0.5, rely=0.5, anchor="center")
        
        complete_login_button = ctk.CTkButton(master=app, text='Login', command=login)
        complete_login_button.place(relx=0.5, rely=0.6, anchor="center")

        back_button = ctk.CTkButton(master=app, text='Back', command=back)
        back_button.place(relx=0.5, rely=0.7, anchor="center")
        
    elif action == "signup":
        login_button.place_forget()
        signup_button.place_forget()
        or_label.place_forget()
        
        name_entry = ctk.CTkEntry(master=app, placeholder_text="Name")
        name_entry.place(relx=0.5, rely=0.2, anchor="center")
        
        user_pass = ctk.CTkEntry(master=app, placeholder_text="Password", show="*")
        user_pass.place(relx=0.5, rely=0.3, anchor="center")
        
        email_entry = ctk.CTkEntry(master=app, placeholder_text="Email")
        email_entry.place(relx=0.5, rely=0.4, anchor="center")
        
        phone_entry = ctk.CTkEntry(master=app, placeholder_text="Phone Number")
        phone_entry.place(relx=0.5, rely=0.5, anchor="center")
        
        complete_signup_button = ctk.CTkButton(master=app, text='Complete Signup', command=complete_signup)
        complete_signup_button.place(relx=0.5, rely=0.6, anchor="center")
        
        back_button = ctk.CTkButton(master=app, text='Back', command=back)
        back_button.place(relx=0.5, rely=0.8, anchor="center")
        
        checkbox_value = ctk.StringVar(value="off")
        checkbox = ctk.CTkCheckBox(master=app, text="Signup as GFM", variable=checkbox_value, onvalue="on", offvalue="off")
        checkbox.place(relx=0.5, rely=0.7, anchor="center")

def complete_signup():
    
    global name_entry, email_entry, phone_entry, user_pass  # Define them as global
    password = user_pass.get()
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    if checkbox_value.get() == "off":
        role = "no"
    else :
        role = "yes"
        
    if name and is_valid_phone_number(phone) and has_valid_email_domain(email):
        subprocess.run(['python', 'databases.py'])
        db.insert_user_table(name, phone, email, password,role)
        db.display()
        # Display a success message
        tkmb.showinfo(title="Signup Successful", message=f"User {name} with email {email} and phone number {phone} has been registered successfully!")
        send_email(email,name)
        
def login():
    global user_entry, user_pass
    entered_username = user_entry.get()  # Get the user-entered username
    validate_username = db.check_name_exists(entered_username)
    entered_password = user_pass.get()  # Get the user-entered password
    validate_password = db.check_password_exists(entered_password)


    if validate_username and validate_password:
        with open("username.txt", "w") as file:
            file.write(db.get_email_id_by_value(entered_username))
            file.close()
        db.conn.commit()
        from login import after_login
        
        
    else:
        tkmb.showerror(title="Login Failed", message="Invalid Username or password")

def back():
    if user_entry:
        user_entry.place_forget()
    if user_pass:
        user_pass.place_forget()
    if complete_login_button:
        complete_login_button.place_forget()
    if complete_signup_button:
        complete_signup_button.place_forget()
    if name_entry:
        name_entry.place_forget()
    if email_entry:
        email_entry.place_forget()
    if phone_entry:
        phone_entry.place_forget()
    if checkbox:
        checkbox.place_forget()     
    loginpage(app)
 
def is_valid_phone_number(phone_number):
    try:
        phone_number = int(phone_number)

        if len(str(phone_number)) == 10:
            return True
        else:
            tkmb.showinfo(title="Error", message="Enter the correct details")
    except ValueError:
        tkmb.showinfo(title="Error", message="Enter the correct details")
   
def has_valid_email_domain(email):
    if email.endswith("@moderncoe.edu.in"):
        return True
    else:
        tkmb.showinfo(title="Error", message="Enter the correct details")

def send_email(receiver_email,name):
    # Sender and receiver email addresses
    sender_email = "aditya_khode_entc@moderncoe.edu.in"  # Replace with your email address
    password = "Aditya1996"  # Replace with your email password

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Welcome to Attendance Monitoring System"

    # Add the welcome message
    welcome_message = "Hello" + name + """
    Welcome to the Attendance Monitoring System app! We are delighted to have you on board.

    Thank you for joining our community.

    Best regards,
    Aditya
    """

    message.attach(MIMEText(welcome_message, "plain"))

    # Establish a connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Start TLS for security
        server.starttls()

        # Login to the email account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

    print(f"Welcome email sent to {receiver_email} successfully.")

       
app = frontend_initiliesd()
loginpage(app)
app.mainloop()
