import customtkinter as ctk
import tkinter as tk

def deselect_other(selected_var, other_var):
    if selected_var.get() == 1:
        other_var.set(0)

def handle_answer1():
    deselect_other(var1, var2)

def handle_answer2():
    deselect_other(var2, var1)

def question1():
    root = ctk.CTk()
    root.title("Question 1")
    root.geometry("1600x800")
    questionfont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalfont = ctk.CTkFont(family="Times New Roman", size=18)
    label_question = ctk.CTkLabel(root, text="What best descibes your accountancy business?", font=questionfont)
    label_question.pack(pady=25)
    
    global var1, var2
    var1 = ctk.BooleanVar()
    var2 = ctk.BooleanVar()
    
    answer1check = ctk.CTkCheckBox(root, text="Self-Employed", font=normalfont, corner_radius=100, variable=var1, command=handle_answer1)
    answer1check.pack(pady=15)

    answer2check = ctk.CTkCheckBox(root, text="Accountancy Firm", font=normalfont, corner_radius=100, variable=var2, command=handle_answer2)
    answer2check.pack(pady=15)

    #Create start and close buttons
    submit_button = ctk.CTkButton(root, text="Submit", font=normalfont)
    submit_button.pack(pady=15)

    #Run the main loop
    root.mainloop()



