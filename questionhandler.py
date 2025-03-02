import customtkinter as ctk
import tkinter as tk
import json
import webbrowser
import sys
import os

#Initialise noSelect so it can be accessed by functions
noSelect = None
goBackCondition = None

#Function to show a question dynamically based on the loaded json file data
def showQuestion(window, questionData, questionNumber, questionAmount, goPreviousCallback):
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
    questionNumberLabel.place(relx=0.95, rely=0.01, anchor=tk.E)

    #Set question text from json file
    questionLabel = ctk.CTkLabel(window, text=questionData["text"], font=questionFont)
    questionLabel.pack(pady=20)

    #The selected option is stored as an int, first radiobutton is value 1, second radiobutton is value 2, etc.
    selectedOption = tk.IntVar()

    #Dynamically add answers as radio buttons
    optionNumber = 1
    while optionNumber <= len(questionData["options"]):
        answerRadioButton = ctk.CTkRadioButton(window, text=questionData["options"][optionNumber-1], font=normalFont, variable=selectedOption, value=optionNumber)
        answerRadioButton.pack(pady=10)
        optionNumber = optionNumber + 1

    #Define submit button functionality, if no option is selected it notifies the user. If an option is selected the selected option is returned and moves onto the next question
    def submit():
        global noSelect
        optionSelected = selectedOption.get()
        if optionSelected == 0 and noSelect == False:
            noSelectLabel = ctk.CTkLabel(window, text="Please select an option")
            noSelectLabel.pack(pady=7.5)
            noSelect = True
        elif optionSelected != 0:
            window.quit() 

    #Create submit button
    submitButton = ctk.CTkButton(window, text="Submit", command=submit, font=normalFont)
    submitButton.pack(pady=10)

    #Button for going to previous question, only appears after question 1
    if questionNumber > 1:
        goBackButton = ctk.CTkButton(window, text="<", font=normalFont, command=goPreviousCallback)
        goBackButton.place(relx=0.02, rely=0.03, anchor = tk.W)

    #Include external hyperlink for further reading based on question data from json file
    linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on this topic!", font=linkFont)
    linkLabel.pack()
    linkLabel.bind("<Button-1>", lambda event:openUrl(questionData["link"]))

    def enterSkip():
        if submitButton.winfo_exists() == True:
            submit()
    
    #Run the main loop and binds enter to submit
    window.bind("<Return>", lambda event: enterSkip())
    window.mainloop()

    #Selected option is returned
    return selectedOption.get()

#Function to actually show the question the user got wrong ---WORK IN PROGRESS---
def showWrongQuestion(window, questionData, questionNumber, questionAmount, showResultsCallback):
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
    questionLabel.pack(pady=20)

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

    #Only shows the go back button if question number is larger than 1, and only shows the go next button if question number is less than the question amount (current 30)
    navigateFrame = ctk.CTkFrame(window)
    navigateFrame.pack(pady=5)
    if questionNumber > 1:
        goBackButton = ctk.CTkButton(navigateFrame, text="<", command=previous, font=normalFont)
        goBackButton.pack(padx=5, side="left")
    resultsButton = ctk.CTkButton(navigateFrame, text="Results", command=showResultsCallback, font=normalFont)
    resultsButton.pack(padx=5, side="left")
    if questionNumber < questionAmount:
        goNextButton = ctk.CTkButton(navigateFrame, text=">", command=next, font=normalFont)
        goNextButton.pack(padx=5, side="left")
    
    window.mainloop()

    return goBackCondition

#Function to open url from json file in browser
def openUrl(link):
   webbrowser.open_new_tab(link)

#Function to clear previous question elements
def clearElements(window):
    for elements in window.winfo_children():
        elements.destroy() 

#Function to get the path for the question.json file, needed for exe
def getQuestionsPath(fileName):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, fileName)
    return os.path.join(os.path.abspath("."), fileName)

#Function to load questions from a json file
def loadQuestions():
    questionFile = getQuestionsPath("questions.json")
    with open(questionFile, 'r') as file:
        questionData = json.load(file)
    return questionData["questions"]

#Function to load only the questions answered incorrectly
def loadWrongQuestions(questionFile, wrongList):
    questionFile = getQuestionsPath("questions.json")
    with open(questionFile, 'r') as file:
        oldQuestionData = json.load(file)
    newQuestionData = []
    for question in oldQuestionData["questions"]:
        if question["id"] in wrongList:
            newQuestionData.append(question)
    return newQuestionData