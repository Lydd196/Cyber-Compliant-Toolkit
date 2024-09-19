import customtkinter as ctk
import tkinter as tk

# Declare variables globally so they can be accessed inside functions
var1, var2 = None, None

def deselect_other(selected_var, other_var):
    if selected_var.get() == 1:
        other_var.set(0)

def handle_answer1():
    deselect_other(var1, var2)

def handle_answer2():
    deselect_other(var2, var1)

def add_compliance(compliance):
    # Update compliance level based on user input
    if var1.get() == 1:
        compliance = compliance + 10
    elif var2.get() == 1:
        compliance = compliance + 5
    print("Updated compliance level:", compliance)
    root.destroy()
    return compliance

def question1(compliance):
    global root, var1, var2
    root = ctk.CTk()
    root.title("Question 1")
    root.geometry("1600x800")
    
    questionfont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalfont = ctk.CTkFont(family="Times New Roman", size=18)
    
    label_question = ctk.CTkLabel(root, text="What best describes your accountancy business?", font=questionfont)
    label_question.pack(pady=25)
    
    var1 = ctk.BooleanVar()
    var2 = ctk.BooleanVar()
    
    answer1check = ctk.CTkCheckBox(root, text="Self-Employed", font=normalfont, corner_radius=100, variable=var1, command=handle_answer1)
    answer1check.pack(pady=15)

    answer2check = ctk.CTkCheckBox(root, text="Accountancy Firm", font=normalfont, corner_radius=100, variable=var2, command=handle_answer2)
    answer2check.pack(pady=15)

    # Create submit button to update compliance level
    submit_button = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalfont)
    submit_button.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = add_compliance(compliance)
    return compliance
