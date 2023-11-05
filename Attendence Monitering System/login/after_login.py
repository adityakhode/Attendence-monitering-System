import customtkinter as ctk
import time
from popupcards import flexcards as cards
from databases_files import databases as db
from databases_files import attendence as attd


emails = None
name = None
with open("username.txt", "r") as file:
    # Read the first line
    emails = file.readline()
    name = db.get_name_by_value(emails)
    db.conn.close()
username = 'Hello ' + name
if attd.check_email_exists(emails):
    attd.insert_user(emails, name)
attd.display_users()




def frontend_initiliesd():
    # Selecting GUI theme - dark, light, system (for system default)
    ctk.set_appearance_mode("dark")

    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("dark-blue")

    apps = ctk.CTk()
    apps.geometry("{0}x{1}+0+0".format(apps.winfo_screenwidth(), apps.winfo_screenheight()))  # Open in full screen
    apps.title("Attendance")
    return apps

def structure():
    label = ctk.CTkLabel(master=apps, text=username)
    label.place(relx=0.01, rely=0.0, anchor="nw")

    date = time.strftime('%d / %m / %Y')
    label = ctk.CTkLabel(master=apps, text=date)
    label.place(relx=0.5, rely=0, anchor="n")
    
    # Create a horizontal line
    line = ctk.CTkCanvas(master=apps, width=apps.winfo_screenwidth(), height=2)
    line.create_rectangle(0, 0, apps.winfo_screenwidth(), 2, fill="blue")
    line.place(relx=0, rely=0.04, anchor="nw")  # Adjust the rely value to position the line
    
    # create a Create Button
    create_button = ctk.CTkButton(master=apps, text='Create_class +', command=create_class)
    create_button.place(relx=0.059, rely=0.075, anchor="center")
    
    # Create a vertical line
    vertical_line = ctk.CTkCanvas(master=apps, width=2, height=apps.winfo_screenheight(), background="red")
    vertical_line.place(relx=0.12, rely=0.04, anchor="nw")
    


def create_class():
    app   = cards.QApplication(cards.sys.argv)
    popup = cards.Addsubject()
    result= popup.exec()
    if result == cards.QDialog.Accepted:
        subject_name = popup.create_class_data()
        attd.insert_subject(subject_name,emails)
        attd.display_subjects()

apps = frontend_initiliesd()
structure()
apps.mainloop()
