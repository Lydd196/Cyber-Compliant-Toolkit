import customtkinter as ctk
import tkinter as tk
import random
import questionhandler 

#Create the main window
root = ctk.CTk()
root.title("Cyber Law Compliance Toolkit")
root.geometry("1100x550")

#Initial compliance level as a percentage
complianceLevel = 100

#Start function for running the questions (starting the test)
def start():
    descriptionLabel.destroy()
    startButton.destroy()
    closeButton.destroy()
    global complianceLevel
    questionNumber = 1

    #List of questions, gets shuffled to randomise the order
    questionList = [questionhandler.q1, questionhandler.q2, questionhandler.q3, questionhandler.q4, questionhandler.q5, questionhandler.q6, questionhandler.q7, questionhandler.q8 , questionhandler.q9]
    random.shuffle(questionList)

    #Iterate over the shuffled questions and update compliance level after each question
    for question in questionList:
        complianceLevel = question(complianceLevel, questionNumber)
        questionNumber = questionNumber + 1
        print(complianceLevel)

    titleLabel.configure(text="Your Results")
    root.title("Your Results")

    #Display final compliance value as a percentage with text depending on the level itself
    complianceTitleLabel = ctk.CTkLabel(root, text= "Final compliance level:", font=titleFont)
    complianceTitleLabel.pack(pady=15)

    complianceLevelLabel = ctk.CTkLabel(root, text=str(complianceLevel) + "%", font=normalFont)
    complianceLevelLabel.pack(pady=15)

    resultDescriptionLabel = ctk.CTkLabel(root, text= "sample text", font=normalFont)
    if complianceLevel > 95:
        resultDescriptionLabel.configure(text= "We believe that your business is very compliant with cyber laws. Great Job!")
        resultDescriptionLabel.pack(pady=15)
    elif complianceLevel > 90:
        resultDescriptionLabel.configure(text= "We believe that you may be in minor breach of the GDPR.\nYou may face fines up to £8.7 million or 2% of global annual turnover (whichever is higher)")
        resultDescriptionLabel.pack(pady=15)
    else:
        resultDescriptionLabel.configure(text= "We believe that you may be in serious breach of the GDPR.\nYou may face fines up to £17.5 million or 4% of global annual turnover (whichever is higher)")
        resultDescriptionLabel.pack(pady=15)
        
    endButton = ctk.CTkButton(root, text="End", command=close, font=normalFont)
    endButton.pack(pady=15)

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
