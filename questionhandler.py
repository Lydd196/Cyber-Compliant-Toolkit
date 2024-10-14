import customtkinter as ctk
import tkinter as tk
import json

noSelect = None
#Function to load questions from a json file
def loadQuestions(questionFile):
    with open(questionFile, 'r') as file:
        questionData = json.load(file)
    return questionData['questions']

#Function to show a question dynamically based on the loaded json file data
def showQuestion(root, questionData, compliance, questionNumber, questionAmount):
    global noSelect
    noSelect = False

    #Clear previous question elements
    for elements in root.winfo_children():
        elements.destroy()  
    root.title("Question " + str(questionNumber))

    questionFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold")
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)

    #Set question number
    questionNumberLabel = ctk.CTkLabel(root, text=f"Question {questionNumber}/{questionAmount}", font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.03, anchor=tk.E)

    #Set question text from json file
    questionLabel = ctk.CTkLabel(root, text=questionData['text'], font=questionFont)
    questionLabel.pack(pady=30)

    selectedOption = tk.IntVar()

    #Dynamically add answers as radio buttons
    optionNumber = 0
    while optionNumber < len(questionData['options']):
        answerRadioButton = ctk.CTkRadioButton(root, text=questionData['options'][optionNumber], font=normalFont, variable=selectedOption, value=optionNumber + 1)
        answerRadioButton.pack(pady=10)
        optionNumber = optionNumber + 1

    #Define submit button functionality, if no option is selected it notifies the user. If an option is selected the compliance is updated and moves onto next question
    def submit():
        global newCompliance, noSelect
        selected = selectedOption.get()
        if selected == 0 and noSelect == False:
            noSelectLabel = ctk.CTkLabel(root, text="Please select an option")
            noSelectLabel.pack(pady=10)
            noSelect = True
        elif selected != 0:
            newCompliance = updateCompliance(compliance, selected, questionData['deduction'])
            root.quit() 

    #Create submit button
    submitButton = ctk.CTkButton(root, text="Submit", command=submit, font=normalFont)
    submitButton.pack(pady=15)

    root.mainloop()

    #Updated compliance value is returned
    return newCompliance

#Function to update compliance level based on user input for each question
def updateCompliance(compliance, selectedOption, deduction):
    compliance = compliance + deduction[selectedOption - 1]
    return compliance