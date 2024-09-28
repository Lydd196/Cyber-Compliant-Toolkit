import customtkinter as ctk
import tkinter as tk

# Declare variables globally so they can be accessed inside functions
var1, var2 = None, None, 

def deselect_other(selected_var, other_var):
    if selected_var.get() == 1:
        other_var.set(0)

def handle_answer1():
    deselect_other(var1, var2)

def handle_answer2():
    deselect_other(var2, var1)

# Function to update compliance level based on user input
def q1compliance(compliance):
    if var1.get() == 1:
        compliance = compliance - 0
    elif var2.get() == 1:
        compliance = compliance - 5
    root.destroy()
    return compliance

# Function to update compliance level based on user input
def q2compliance(compliance):
    if var1.get() == 1:
        compliance = compliance - 5
    elif var2.get() == 1:
        compliance = compliance - 0
    root.destroy()
    return compliance

def q3compliance(compliance):
    if var1.get() == 1:
        compliance = compliance - 0
    elif var2.get() == 1:
        compliance = compliance - 7
    root.destroy()
    return compliance

def question1(compliance, questionnumber):
    global root, var1, var2
    root = ctk.CTk()
    root.title("Question "+ str(questionnumber))
    root.geometry("1500x750")
    
    questionfont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalfont = ctk.CTkFont(family="Times New Roman", size=18)

    questionnumberlabel = ctk.CTkLabel(root, text="Question " + str(questionnumber) + "/50", font=normalfont)
    questionnumberlabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionlabel = ctk.CTkLabel(root, text="Do you ensure that data you hold of your clients are accurate and up to date?", font=questionfont)
    questionlabel.pack(pady=25)
    
    var1 = ctk.BooleanVar()
    var2 = ctk.BooleanVar()
    
    answer1check = ctk.CTkCheckBox(root, text="Yes", font=normalfont, corner_radius=1, variable=var1, command=handle_answer1)
    answer1check.pack(pady=15)

    answer2check = ctk.CTkCheckBox(root, text="No", font=normalfont, corner_radius=1, variable=var2, command=handle_answer2)
    answer2check.pack(pady=15)

    # Create submit button to update compliance level
    submitbutton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalfont)
    submitbutton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q1compliance(compliance)
    return compliance

def question2(compliance, questionnumber):
    global root, var1, var2
    root = ctk.CTk()
    root.title("Question "+ str(questionnumber))
    root.geometry("1500x750")
    
    questionfont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalfont = ctk.CTkFont(family="Times New Roman", size=18)

    questionnumberlabel = ctk.CTkLabel(root, text="Question " + str(questionnumber) + "/50", font=normalfont)
    questionnumberlabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionlabel = ctk.CTkLabel(root, text="Do you keep data longer than is necessary?", font=questionfont)
    questionlabel.pack(pady=25)
    
    var1 = ctk.BooleanVar()
    var2 = ctk.BooleanVar()

    answer1check = ctk.CTkCheckBox(root, text="Yes", font=normalfont, corner_radius=1, variable=var1, command=handle_answer1)
    answer1check.pack(pady=15)

    answer2check = ctk.CTkCheckBox(root, text="No", font=normalfont, corner_radius=1, variable=var2, command=handle_answer2)
    answer2check.pack(pady=15)

    # Create submit button to update compliance level
    submitbutton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalfont)
    submitbutton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q2compliance(compliance)
    return compliance

def question3(compliance, questionnumber):
    global root, var1, var2
    root = ctk.CTk()
    root.title("Question " + str(questionnumber))
    root.geometry("1500x750")
    
    questionfont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalfont = ctk.CTkFont(family="Times New Roman", size=18)

    questionnumberlabel = ctk.CTkLabel(root, text="Question " + str(questionnumber) + "/50", font=normalfont)
    questionnumberlabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionlabel = ctk.CTkLabel(root, text="Do you allow clients to request what data you hold on them?", font=questionfont)
    questionlabel.pack(pady=25)
    
    var1 = ctk.BooleanVar()
    var2 = ctk.BooleanVar()

    answer1check = ctk.CTkCheckBox(root, text="Yes", font=normalfont, corner_radius=1, variable=var1, command=handle_answer1)
    answer1check.pack(pady=15)

    answer2check = ctk.CTkCheckBox(root, text="No", font=normalfont, corner_radius=1, variable=var2, command=handle_answer2)
    answer2check.pack(pady=15)

    # Create submit button to update compliance level
    submitbutton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalfont)
    submitbutton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q3compliance(compliance)
    return compliance
