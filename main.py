import customtkinter as ctk
import tkinter as tk
import questionhandler 

# Create the main window
root = ctk.CTk()
root.title("Cyber Law Compliance Toolkit")
root.geometry("1000x500")

# Initial compliance level as a percentage
compliancelevel = 100

# Start function for running the questions (starting the test)
def start():
    global compliancelevel

    # Get updated compliance level from previous questions and use them in the next questions
    compliancelevel = questionhandler.question1(compliancelevel)
    compliancelevel = questionhandler.question2(compliancelevel)

    titlelabel.configure(text="Your Results")
    descriptionlabel.destroy()
    startbutton.destroy()
    closebutton.destroy()
    
    # Display final compliance value as a percentage
    compliancetitlelabel = ctk.CTkLabel(root, text= "Final compliance level:", font=titlefont)
    compliancetitlelabel.pack(pady=15)

    compliancelevellabel = ctk.CTkLabel(root, text=str(compliancelevel) + "%", font=normalfont)
    compliancelevellabel.pack(pady=15)

    endbutton = ctk.CTkButton(root, text="End", command=close, font=normalfont)
    endbutton.pack(pady=15)

# Cancel function to not run the test and to close the program
def close():
    root.destroy()

titlefont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
normalfont = ctk.CTkFont(family="Times New Roman", size=18)
titlelabel= ctk.CTkLabel(root, text="Welcome to CyberComply: The Cyber Law Compliance Toolkit for Accountants", font=titlefont)
titlelabel.pack(pady=25)


descriptionlabel = ctk.CTkLabel(root, text="Find out how compliant your accountancy business is with cyber laws", font=normalfont)
descriptionlabel.pack(pady=15)

# Create start and close buttons
startbutton = ctk.CTkButton(root, text="Start", command=start, font=normalfont)
startbutton.pack(pady=15)

closebutton = ctk.CTkButton(root, text="Close", command=close, font=normalfont)
closebutton.pack(pady=15)

# Run the main loop
root.mainloop()

# Print final compliance score in the terminal (debugging purposes)
print("Final compliance level:", compliancelevel)
