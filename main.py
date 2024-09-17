import customtkinter as ctk
import tkinter as tk
import questionhandler 

#Create the main window
root = ctk.CTk()
root.title("Cyber Law Compliance Toolkit")
root.geometry("1000x500")

#Define start and close functions
def start():
    questionhandler.question1()
    root.destroy()
    
def cancel():
    root.destroy()

titlefont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
normalfont = ctk.CTkFont(family="Times New Roman", size=18)
label_title = ctk.CTkLabel(root, text="Welcome to CyberComply: The Cyber Law Compliance Toolkit for Accountants", font=titlefont)
label_title.pack(pady=25)

label_description = ctk.CTkLabel(root, text="Find out how compliant your accountancy business is with cyber laws", font=normalfont)
label_description.pack(pady=15)

#Create start and close buttons
start_button = ctk.CTkButton(root, text="Start", command=start, font=normalfont)
start_button.pack(pady=15)

close_button = ctk.CTkButton(root, text="Cancel", command=cancel, font=normalfont)
close_button.pack(pady=15)

#Run the main loop
root.mainloop()

