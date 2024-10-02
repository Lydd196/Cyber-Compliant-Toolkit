import customtkinter as ctk
import tkinter as tk

#Declare selectedOption variable globally so it can be accessed inside functions
selectedOption = None

#Procedure to check that an option has been selected and if it has not then notifies the user and blocks progress
def checkSelected():
    if selectedOption.get() == 0:
        noSelectLabel = ctk.CTkLabel(root, text="Please select an option")
        noSelectLabel.pack(pady=25)
    else:
        root.quit()

#Function to update compliance level based on user input for q1
def q1_compliance(compliance):
    if selectedOption.get() == 1:
        compliance = compliance - 0
    elif selectedOption.get() == 2:
        compliance = compliance - 5
    root.destroy()
    return compliance

#Function to update compliance level based on user input for q2
def q2_compliance(compliance):
    if selectedOption.get() == 1:
        compliance = compliance - 5
    elif selectedOption == 2:
        compliance = compliance - 0
    root.destroy()
    return compliance

#Function to update compliance level based on user input for q3
def q3_compliance(compliance):
    if selectedOption.get() == 1:
        compliance = compliance - 0
    elif selectedOption.get() == 2:
        compliance = compliance - 7
    root.destroy()
    return compliance

#Function to update compliance level based on user input for q4
def q4_compliance(compliance):
    if selectedOption.get() == 1:
        compliance = compliance - 0
    elif selectedOption.get() == 2:
        compliance = compliance - 0
    elif selectedOption.get() == 3:
        compliance = compliance - 3
    elif selectedOption.get() == 4:
        compliance = compliance - 6
    elif selectedOption.get() == 5:
        compliance = compliance - 10
    elif selectedOption.get() == 6:
        compliance = compliance - 0
    root.destroy()
    return compliance

#Page for q1
def q1(compliance, questionNumber):
    global root, selectedOption
    root = ctk.CTk()
    root.title("Question "+ str(questionNumber))
    root.geometry("1500x750")
    
    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    questionNumberLabel = ctk.CTkLabel(root, text="Question " + str(questionNumber) + "/50", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionLabel = ctk.CTkLabel(root, text="Do you ensure that data you hold of your clients are accurate and up to date?", font=questionFont)
    questionLabel.pack(pady=25)
    
    selectedOption = tk.IntVar()
    
    answer1radioButton = ctk.CTkRadioButton(root, text="Yes", font=normalFont, variable=selectedOption, value=1)
    answer1radioButton.pack(pady=15)

    answer2radioButton = ctk.CTkRadioButton(root, text="No", font=normalFont, variable=selectedOption, value=2)
    answer2radioButton.pack(pady=15)

    #Create submit button to check if an option has been selected and update compliance level
    submitButton = ctk.CTkButton(root, text="Submit", command=lambda: checkSelected(), font=normalFont)
    submitButton.pack(pady=15)

    root.mainloop()

    #Compliance gets updated and returns the result
    compliance = q1_compliance(compliance)
    return compliance

#Page for q2
def q2(compliance, questionNumber):
    global root, selectedOption
    root = ctk.CTk()
    root.title("Question "+ str(questionNumber))
    root.geometry("1500x750")
    
    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    questionNumberLabel = ctk.CTkLabel(root, text="Question " + str(questionNumber) + "/50", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionLabel = ctk.CTkLabel(root, text="Do you keep data longer than is necessary?", font=questionFont)
    questionLabel.pack(pady=25)
    
    selectedOption = tk.IntVar()

    answer1radioButton = ctk.CTkRadioButton(root, text="Yes", font=normalFont, variable=selectedOption, value=1)
    answer1radioButton.pack(pady=15)

    answer2radioButton = ctk.CTkRadioButton(root, text="No", font=normalFont, variable=selectedOption, value=2)
    answer2radioButton.pack(pady=15)

    #Create submit button to check if an option has been selected and update compliance level
    submitButton = ctk.CTkButton(root, text="Submit", command=lambda: checkSelected(), font=normalFont)
    submitButton.pack(pady=15)

    root.mainloop()

    #Compliance gets updated and returns the result
    compliance = q2_compliance(compliance)
    return compliance

#Page for q3
def q3(compliance, questionNumber):
    global root, selectedOption
    root = ctk.CTk()
    root.title("Question " + str(questionNumber))
    root.geometry("1500x750")
    
    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    questionNumberLabel = ctk.CTkLabel(root, text="Question " + str(questionNumber) + "/50", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionLabel = ctk.CTkLabel(root, text="Do you allow clients to request what data you hold on them?", font=questionFont)
    questionLabel.pack(pady=25)
    
    selectedOption = tk.IntVar()

    answer1radioButton = ctk.CTkRadioButton(root, text="Yes", font=normalFont, variable=selectedOption, value=1)
    answer1radioButton.pack(pady=15)

    answer2radioButton = ctk.CTkRadioButton(root, text="No", font=normalFont, variable=selectedOption, value=2)
    answer2radioButton.pack(pady=15)

    #Create submit button to check if an option has been selected and update compliance level
    submitButton = ctk.CTkButton(root, text="Submit", command=lambda: checkSelected(), font=normalFont)
    submitButton.pack(pady=15)

    root.mainloop()

    #Compliance gets updated and returns the result
    compliance = q3_compliance(compliance)
    return compliance

#Page for q4
def q4(compliance, questionNumber):
    global root, selectedOption
    root = ctk.CTk()
    root.title("Question " + str(questionNumber))
    root.geometry("1500x750")
    
    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    questionNumberLabel = ctk.CTkLabel(root, text="Question " + str(questionNumber) + "/50", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)
    
    questionLabel = ctk.CTkLabel(root, text="If your business processes sensitive data (such as ethnicity or health data);\n how often do you carry out Data Protection Impact Assessments (DPIAs)?", font=questionFont)
    questionLabel.pack(pady=25)
    
    selectedOption = tk.IntVar()

    answer1checkbox = ctk.CTkRadioButton(root, text="Every year", font=normalFont, variable=selectedOption, value=1)
    answer1checkbox.pack(pady=15)

    answer2checkbox = ctk.CTkRadioButton(root, text="Every 3 years", font=normalFont, variable=selectedOption, value=2)
    answer2checkbox.pack(pady=15)

    answer3checkbox = ctk.CTkRadioButton(root, text="Every 5 years", font=normalFont, variable=selectedOption , value=3)
    answer3checkbox.pack(pady=15)

    answer4checkbox = ctk.CTkRadioButton(root, text="Every 7+ years", font=normalFont, variable=selectedOption, value=4)
    answer4checkbox.pack(pady=15)

    answer5checkbox = ctk.CTkRadioButton(root, text="We do not carry out data protection impact assessments", font=normalFont, variable=selectedOption, value=5)
    answer5checkbox.pack(pady=15)

    answer6checkbox = ctk.CTkRadioButton(root, text="We do not process sensitive data", font=normalFont, variable=selectedOption, value=6)
    answer6checkbox.pack(pady=15)

    #Create submit button to check if an option has been selected and update compliance level
    submitButton = ctk.CTkButton(root, text="Submit", command=lambda: checkSelected(), font=normalFont)
    submitButton.pack(pady=15)

    root.mainloop()

    #Compliance gets updated and returns the result
    compliance = q4_compliance(compliance)
    return compliance
