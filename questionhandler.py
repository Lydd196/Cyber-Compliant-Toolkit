import customtkinter as ctk
import tkinter as tk

# Declare variables globally so they can be accessed inside functions
var1, var2, var3, var4 = None, None, None, None

def deselect_other(selected_var, other_var):
    if selected_var.get() == 1:
        other_var.set(0)

def handle_answer1():
    deselect_other(var1, var2)

def handle_answer2():
    deselect_other(var2, var1)

def q1compliance(compliance):
    # Update compliance level based on user input
    if var1.get() == 1:
        compliance = compliance - 2
    elif var2.get() == 1:
        compliance = compliance - 5
    root.destroy()
    return compliance

def q2compliance(compliance):
    # Update compliance level based on user input
    if var1.get() == 0:
        compliance = compliance - 3
    if var2.get() == 0:
        compliance = compliance - 5
    if var3.get() == 0:
        compliance = compliance - 7
    if var4.get() == 0:
        compliance = compliance - 10
    root.destroy()
    return compliance

def question1(compliance):
    global root, var1, var2
    root = ctk.CTk()
    root.title("Question 1")
    root.geometry("1600x800")
    
    questionfont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalfont = ctk.CTkFont(family="Times New Roman", size=18)
    
    labelquestion = ctk.CTkLabel(root, text="What best describes your accountancy business?", font=questionfont)
    labelquestion.pack(pady=25)
    
    var1 = ctk.BooleanVar()
    var2 = ctk.BooleanVar()
    
    answer1check = ctk.CTkCheckBox(root, text="Self-Employed", font=normalfont, corner_radius=1, variable=var1, command=handle_answer1)
    answer1check.pack(pady=15)

    answer2check = ctk.CTkCheckBox(root, text="Accountancy Firm", font=normalfont, corner_radius=1, variable=var2, command=handle_answer2)
    answer2check.pack(pady=15)

    # Create submit button to update compliance level
    submitbutton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalfont)
    submitbutton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q1compliance(compliance)
    return compliance

def question2(compliance):
    global root, var1, var2, var3, var4
    root = ctk.CTk()
    root.title("Question 2")
    root.geometry("1600x800")
    
    questionfont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalfont = ctk.CTkFont(family="Times New Roman", size=18)
    
    labelquestion = ctk.CTkLabel(root, text="Which of the following is true in your business?", font=questionfont)
    labelquestion.pack(pady=25)
    
    var1 = ctk.BooleanVar()
    var2 = ctk.BooleanVar()
    var3 = ctk.BooleanVar()
    var4 = ctk.BooleanVar()
    
    answer1check = ctk.CTkCheckBox(root, text="You only collect client data that is relevant to accounts", font=normalfont, corner_radius=100, variable=var1)
    answer1check.pack(pady=15)

    answer2check = ctk.CTkCheckBox(root, text="You delete client data that is no longer necessary", font=normalfont, corner_radius=100, variable=var2)
    answer2check.pack(pady=15)

    answer3check = ctk.CTkCheckBox(root, text="You ensure that data is accurate and kept up to date", font=normalfont, corner_radius=100, variable=var3)
    answer3check.pack(pady=15)

    answer4check = ctk.CTkCheckBox(root, text="You ensure that data is handled and stored securely, ensuring that confidentiality, integrity and accessibility are not violated", font=normalfont, corner_radius=100, variable=var4)
    answer4check.pack(pady=15)


    # Create submit button to update compliance level
    submitbutton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalfont)
    submitbutton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q2compliance(compliance)
    return compliance
