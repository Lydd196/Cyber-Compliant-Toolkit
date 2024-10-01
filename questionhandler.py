import customtkinter as ctk
import tkinter as tk

# Declare variables globally so they can be accessed inside functions
ans1, ans2 = None, None, 

def deselect_other(selectedAns, otherAns):
    if selectedAns.get() == 1:
        otherAns.set(0)

def handle_answer1():
    deselect_other(ans1, ans2)

def handle_answer2():
    deselect_other(ans2, ans1)

# Function to update compliance level based on user input
def q1_compliance(compliance):
    if ans1.get() == 1:
        compliance = compliance - 0
    elif ans2.get() == 1:
        compliance = compliance - 5
    root.destroy()
    return compliance

# Function to update compliance level based on user input
def q2_compliance(compliance):
    if ans1.get() == 1:
        compliance = compliance - 5
    elif ans2.get() == 1:
        compliance = compliance - 0
    root.destroy()
    return compliance

def q3_compliance(compliance):
    if ans1.get() == 1:
        compliance = compliance - 0
    elif ans2.get() == 1:
        compliance = compliance - 7
    root.destroy()
    return compliance

def q1(compliance, questionNumber):
    global root, ans1, ans2
    root = ctk.CTk()
    root.title("Question "+ str(questionNumber))
    root.geometry("1500x750")
    
    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    questionNumberLabel = ctk.CTkLabel(root, text="Question " + str(questionNumber) + "/50", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionLabel = ctk.CTkLabel(root, text="Do you ensure that data you hold of your clients are accurate and up to date?", font=questionFont)
    questionLabel.pack(pady=25)
    
    ans1 = ctk.BooleanVar()
    ans2 = ctk.BooleanVar()
    
    answer1checkbox = ctk.CTkCheckBox(root, text="Yes", font=normalFont, corner_radius=1, variable=ans1, command=handle_answer1)
    answer1checkbox.pack(pady=15)

    answer2checkbox = ctk.CTkCheckBox(root, text="No", font=normalFont, corner_radius=1, variable=ans2, command=handle_answer2)
    answer2checkbox.pack(pady=15)

    # Create submit button to update compliance level
    submitButton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalFont)
    submitButton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q1_compliance(compliance)
    return compliance

def q2(compliance, questionNumber):
    global root, ans1, ans2
    root = ctk.CTk()
    root.title("Question "+ str(questionNumber))
    root.geometry("1500x750")
    
    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    questionNumberLabel = ctk.CTkLabel(root, text="Question " + str(questionNumber) + "/50", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionLabel = ctk.CTkLabel(root, text="Do you keep data longer than is necessary?", font=questionFont)
    questionLabel.pack(pady=25)
    
    ans1 = ctk.BooleanVar()
    ans2 = ctk.BooleanVar()

    answer1checkbox = ctk.CTkCheckBox(root, text="Yes", font=normalFont, corner_radius=1, variable=ans1, command=handle_answer1)
    answer1checkbox.pack(pady=15)

    answer2checkbox = ctk.CTkCheckBox(root, text="No", font=normalFont, corner_radius=1, variable=ans2, command=handle_answer2)
    answer2checkbox.pack(pady=15)

    # Create submit button to update compliance level
    submitButton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalFont)
    submitButton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q2_compliance(compliance)
    return compliance

def q3(compliance, questionNumber):
    global root, ans1, ans2
    root = ctk.CTk()
    root.title("Question " + str(questionNumber))
    root.geometry("1500x750")
    
    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    questionNumberLabel = ctk.CTkLabel(root, text="Question " + str(questionNumber) + "/50", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionLabel = ctk.CTkLabel(root, text="Do you allow clients to request what data you hold on them?", font=questionFont)
    questionLabel.pack(pady=25)
    
    ans1 = ctk.BooleanVar()
    ans2 = ctk.BooleanVar()

    answer1checkbox = ctk.CTkCheckBox(root, text="Yes", font=normalFont, corner_radius=1, variable=ans1, command=handle_answer1)
    answer1checkbox.pack(pady=15)

    answer2checkbox = ctk.CTkCheckBox(root, text="No", font=normalFont, corner_radius=1, variable=ans2, command=handle_answer2)
    answer2checkbox.pack(pady=15)

    # Create submit button to update compliance level
    submitButton = ctk.CTkButton(root, text="Submit", command=lambda: root.quit(), font=normalFont)
    submitButton.pack(pady=15)

    # Run the main loop (this halts until root.quit() is called)
    root.mainloop()

    # After root.quit(), the function continues. Use the result.
    compliance = q3_compliance(compliance)
    return compliance
