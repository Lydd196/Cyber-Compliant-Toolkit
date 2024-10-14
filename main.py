import customtkinter as ctk
import tkinter as tk
import random
import questionhandler 

#Create the main window
root = ctk.CTk()
root.title("Cyber Law Compliance Toolkit")
root.geometry("1300x650")

#Initial compliance level as a percentage
complianceLevel = 100

def showResults():
    #Remove all the elements to prepare the results and change window title
    for elements in root.winfo_children():
        elements.destroy()  
    root.title("Your Results")

    #Display final compliance value as a percentage with text depending on the final value itself
    complianceTitleLabel = ctk.CTkLabel(root, text= "Final compliance level:", font=titleFont)        
    complianceTitleLabel.pack(pady=15)
    
    complianceLevelLabel = ctk.CTkLabel(root, text=str(complianceLevel) + "%", font=normalFont)
    complianceLevelLabel.pack(pady=15)

    resultDescriptionLabel = ctk.CTkLabel(root, text= "sample text", font=normalFont)
    if complianceLevel > 80:
        resultDescriptionLabel.configure(text= "We believe that your business is very compliant with cyber laws. Great Job!")
        resultDescriptionLabel.pack(pady=15)
    elif complianceLevel > 50:
        resultDescriptionLabel.configure(text= "We believe that you may be in minor breach of the GDPR.\nYou may face fines up to £8.7 million or 2% of global annual turnover (whichever is higher)")
        resultDescriptionLabel.pack(pady=15)
    else:
        resultDescriptionLabel.configure(text= "We believe that you may be in serious breach of the GDPR.\nYou may face fines up to £17.5 million or 4% of global annual turnover (whichever is higher)")
        resultDescriptionLabel.pack(pady=15)
        
    endButton = ctk.CTkButton(root, text="End", command=close, font=normalFont)
    endButton.pack(pady=15)

#Start function for running the questions (starting the test)
def start():
    #Remove all the elements to prepare the test
    for elements in root.winfo_children():
        elements.destroy()  
    global complianceLevel
    questionNumber = 1
    
    #List of questions from json file gets shuffled to randomise the order
    questionList = questionhandler.loadQuestions('questions.json')
    random.shuffle(questionList)
    questionAmount = len(questionList)

    #Run each question dynamically
    while questionNumber <= len(questionList):
        question = questionList[questionNumber - 1]
        complianceLevel = questionhandler.showQuestion(root, question, complianceLevel, questionNumber, questionAmount)
        #Print compliance level in terminal (debugging purposes)
        print("Compliance Level after question", questionNumber, ":", complianceLevel)
        questionNumber = questionNumber + 1

    #After each of the questions have been answered, show the results
    showResults()

    
#Cancel function to not run the test and to close the program
def close():
    root.destroy()

titleFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
normalFont = ctk.CTkFont(family="Times New Roman", size=18)

titleLabel= ctk.CTkLabel(root, text="Welcome to CyberComply: The Cyber Law Compliance Toolkit for Accountants", font=titleFont)
titleLabel.pack(pady=25)

descriptionLabel = ctk.CTkLabel(root, text="Find out how compliant your accountancy business is with cyber laws", font=normalFont)
descriptionLabel.pack(pady=15)

#Create start and close buttons
startButton = ctk.CTkButton(root, text="Start", command=start, font=normalFont)
startButton.pack(pady=15)

closeButton = ctk.CTkButton(root, text="Close", command=close, font=normalFont)
closeButton.pack(pady=15)

#Run the main loop
root.mainloop()

#Print final compliance score in the terminal (debugging purposes)
print("Final compliance level:", complianceLevel)
