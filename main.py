import customtkinter as ctk
import tkinter as tk
import random
import questionhandler 

#Create the main window
window = ctk.CTk()
window.title("Cyber Law Compliance Toolkit")
window.geometry("1300x650")

#Initial compliance level as a percentage
complianceLevel = 100


#Function to clear previous question elements
def clearElements(window):
    for elements in window.winfo_children():
        elements.destroy() 

def showResults():
    #Remove all the elements to prepare the results and change window title
    clearElements(window)
    window.title("Your Results")

    #Display final compliance value as a percentage with text depending on the final value itself
    complianceTitleLabel = ctk.CTkLabel(window, text= "Final compliance level:", font=titleFont)        
    complianceTitleLabel.pack(pady=15)
    complianceLevelLabel = ctk.CTkLabel(window, text=str(complianceLevel) + "%", font=normalFont)
    complianceLevelLabel.pack(pady=15)

    resultDescriptionLabel = ctk.CTkLabel(window, text= "sample text", font=normalFont)

    #Different result descriptions based on the compliance value
    if complianceLevel > 80:
        resultDescriptionLabel.configure(text= "We believe that your business is very compliant with cyber laws. Great Job!")
        resultDescriptionLabel.pack(pady=15)
    elif complianceLevel > 50:
        resultDescriptionLabel.configure(text= "We believe that you may be in minor breach of the GDPR.\nYou may face fines up to £8.7 million or 2% of global annual turnover (whichever is higher)")
        resultDescriptionLabel.pack(pady=15)
    else:
        resultDescriptionLabel.configure(text= "We believe that you may be in serious breach of the GDPR.\nYou may face fines up to £17.5 million or 4% of global annual turnover (whichever is higher)")
        resultDescriptionLabel.pack(pady=15)
        
    endButton = ctk.CTkButton(window, text="End", command=close, font=normalFont)
    endButton.pack(pady=15)

#Start function for running the questions (starting the test)
def start():
    #Clear all elements from the window to prepare the test
    clearElements(window) 
    global complianceLevel
    questionNumber = 1
    
    #List of questions from json file gets shuffled to randomise the order
    questionList = questionhandler.loadQuestions('questions.json')
    random.shuffle(questionList)
    questionAmount = len(questionList)

    #Run each question dynamically
    while questionNumber <= len(questionList):
        question = questionList[questionNumber - 1]
        complianceLevel = questionhandler.showQuestion(window, question, complianceLevel, questionNumber, questionAmount)
        #Print compliance level in terminal (debugging purposes)
        print("Compliance Level after question", questionNumber, ":", complianceLevel)
        questionNumber = questionNumber + 1
    
    #After each of the questions have been answered, show the results
    showResults()

#Cancel function to not run the test and to close the program
def close():
    window.destroy()

#Set fonts
titleFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
normalFont = ctk.CTkFont(family="Times New Roman", size=18)

#Set the title
titleLabel= ctk.CTkLabel(window, text="Welcome to CyberComply: The Cyber Law Compliance Toolkit for Accountants", font=titleFont)
titleLabel.pack(pady=25)

#Set the description
descriptionLabel = ctk.CTkLabel(window, text="Find out how compliant your accountancy business is with cyber laws", font=normalFont)
descriptionLabel.pack(pady=15)

#Create start and close buttons
startButton = ctk.CTkButton(window, text="Start", command=start, font=normalFont)
startButton.pack(pady=15)
closeButton = ctk.CTkButton(window, text="Close", command=close, font=normalFont)
closeButton.pack(pady=15)

#Run the main loop
window.mainloop()

#Print final compliance score in the terminal (debugging purposes)
print("Final compliance level:", complianceLevel)
