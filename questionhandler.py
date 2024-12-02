import customtkinter as ctk
import tkinter as tk
import json
import webbrowser

#Initialise noSelect so it can be accessed by functions
noSelect = None
goBackCondition = None
gdprAverage = 0
misuseAverage = 0
fraudAverage = 0
wrongList = []

#Function to open url from json file in browser
def openUrl(link):
   webbrowser.open_new_tab(link)

#Function to clear previous question elements
def clearElements(window):
    for elements in window.winfo_children():
        elements.destroy() 

#Function to load questions from a json file
def loadQuestions(questionFile):
    with open(questionFile, 'r') as file:
        questionData = json.load(file)
    return questionData["questions"]

def loadWrongQuestions(questionFile, wrongList):
    with open(questionFile, 'r') as file:
        oldQuestionData = json.load(file)
    newQuestionData = [question for question in oldQuestionData["questions"] if question["id"] in wrongList]
    return newQuestionData

#Function to update compliance level based on user input for each question
def updateCompliance(compliance, selectedOption, deduction):
    compliance = compliance + deduction[selectedOption - 1]
    if compliance < 0:
        compliance = 0
    return compliance

#Function to create/update a rolling average of the compliance loss for each of the laws
def averageLossUpdate(newCompliance, oldCompliance, questionType):
    global gdprAverage, misuseAverage, fraudAverage
    complianceDifference = oldCompliance - newCompliance
    if questionType == "UK GDPR":
        gdprAverage = gdprAverage + (complianceDifference/20)
    elif questionType == "Computer Misuse Act":
        misuseAverage = misuseAverage + (complianceDifference/6)
    elif questionType == "The Fraud Act":
        fraudAverage = fraudAverage + (complianceDifference/2)

#Function to return external info used in main.py. including a list of all of the three final average loss values and the list of questions the user got wrong
def returnExternalInfo():
    return [gdprAverage, misuseAverage, fraudAverage, wrongList]

#Function to show a question dynamically based on the loaded json file data
def showQuestion(window, questionData, compliance, questionNumber, questionAmount):
    global noSelect
    noSelect = False

    #Remove all the elements to prepare the next question and change window title
    clearElements(window)
    window.title("Question " + str(questionNumber))

    #Set fonts
    questionFont = ctk.CTkFont(family="Helvetic", size=23, weight="bold")
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)
    linkFont = ctk.CTkFont(family="Helvetic", slant="italic", underline=True, size=18)

    #Set question number
    questionNumberLabel = ctk.CTkLabel(window, text="Question " + str(questionNumber) + "/" + str(questionAmount), font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.02, anchor=tk.E)

    #Set question text from json file
    questionLabel = ctk.CTkLabel(window, text=questionData["text"], font=questionFont)
    questionLabel.pack(pady=30)

    #The selected option is stored as an int, first radiobutton is value 1, second radiobutton is value 2, etc.
    selectedOption = tk.IntVar()

    #Dynamically add answers as radio buttons
    optionNumber = 1
    while optionNumber <= len(questionData["options"]):
        answerRadioButton = ctk.CTkRadioButton(window, text=questionData["options"][optionNumber-1], font=normalFont, variable=selectedOption, value=optionNumber)
        answerRadioButton.pack(pady=10)
        optionNumber = optionNumber + 1

    #Define submit button functionality, if no option is selected it notifies the user. If an option is selected the compliance is updated and moves onto next question
    def submit():
        global newCompliance, noSelect
        optionSelected = selectedOption.get()
        if optionSelected == 0 and noSelect == False:
            noSelectLabel = ctk.CTkLabel(window, text="Please select an option")
            noSelectLabel.pack(pady=7.5)
            noSelect = True
        elif optionSelected != 0:
            newCompliance = updateCompliance(compliance, optionSelected, questionData['deduction'])
            averageLossUpdate(newCompliance, compliance, questionData["law"])
            if newCompliance != compliance:
                wrongList.append(questionData["id"])
            window.quit() 

    #Create submit button
    submitButton = ctk.CTkButton(window, text="Submit", command=submit, font=normalFont)
    submitButton.pack(pady=15)

    #Include external hyperlink for further reading based on question data from json file
    linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on this topic!", font=linkFont)
    linkLabel.pack()
    linkLabel.bind("<Button-1>", lambda event:openUrl(questionData["link"]))
    
    #Run the main loop and binds enter to submit
    window.bind("<Return>", lambda event: submit())
    window.mainloop()

    #Updated compliance value is returned
    return newCompliance

#Function to actually show the question the user got wrong ---WORK IN PROGRESS---
def showWrongQuestion(window, questionData, questionNumber, questionAmount):
    #Remove all the elements to prepare the next question and change window title
    clearElements(window)
    global goBackCondition
    goBackCondition = False
    window.title("Question " + str(questionNumber))
    
    #Set fonts
    questionFont = ctk.CTkFont(family="Helvetic", size=23, weight="bold")
    normalFont = ctk.CTkFont(family="Times New Roman", size=18)
    linkFont = ctk.CTkFont(family="Helvetic", slant="italic", underline=True, size=18)

    #Set question number
    questionNumberLabel = ctk.CTkLabel(window, text="Question " + str(questionNumber) + "/" + str(questionAmount), font=normalFont)
    questionNumberLabel.place(relx=0.95, rely=0.02, anchor=tk.E)

    #Set question text from json file
    questionLabel = ctk.CTkLabel(window, text=questionData["text"], font=questionFont)
    questionLabel.pack(pady=30)

    #Set explanation text from json file
    explanationLabel = ctk.CTkLabel(window, text=questionData["explanation"], font=normalFont)
    explanationLabel.pack(pady=10)

    #Include external hyperlink for further reading based on question data from json file
    linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on this topic!", font=linkFont)
    linkLabel.pack()
    linkLabel.bind("<Button-1>", lambda event:openUrl(questionData["link"]))
    
    def previous():
        global goBackCondition
        goBackCondition = True
        window.quit()

    def next():
        window.quit()

    #Only shows the go back button if question number is larger than 1, and only shows the go next button if question number is less than the question amount (current 28)
    if questionNumber < 28:
        goNextButton = ctk.CTkButton(window, text="Go to the next question", command=next, font=normalFont)
        goNextButton.pack(pady=10)
    if questionNumber > 1:
        goBackButton = ctk.CTkButton(window, text="Go to the previous question", command=previous, font=normalFont)
        goBackButton.pack(pady=10)

    window.mainloop()

    return goBackCondition