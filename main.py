import customtkinter as ctk
import tkinter as tk
import random
import questionhandler 
import webbrowser

#Create the main window
window = ctk.CTk()
window.title("Cyber Law Compliance Toolkit")
window.geometry("1500x750")

#Initial compliance level as a percentage
complianceLevel = 100

#Function to open url in new tab
def openUrl(link):
   webbrowser.open_new_tab(link)

#Function to clear previous question elements
def clearElements(window):
    for elements in window.winfo_children():
        elements.destroy() 

#Function to show the results
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

    #Different result descriptions based on the compliance value and worst law average
    averageLoss = questionhandler.returnAverageLoss()
    for index in range(0, len(averageLoss)):
        averageLoss[index] = round(averageLoss[index], 2)
   
    if complianceLevel > 80:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is very compliant with cyber laws. Great Job!")
        resultDescriptionLabel.pack(pady=15)
    elif complianceLevel > 50:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is not very compliant with cyber laws")
        resultDescriptionLabel.pack(pady=15)
    else:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is not compliant at all with cyber laws")
        resultDescriptionLabel.pack(pady=15)  

    #Average loss thresholds are calculated by ((x/y)* 100-z/x) where x is the amount of that question type, y is the total number of questions and z is dependant on the condition (50 for serious breach and 80 for minor breach (MAY CHANGE))
    #THIS AVERAGE SYSTEM MUST BE CHANGED IF NEW QUESTIONS ARE ADDED
    if averageLoss[0] > 0.71 or averageLoss[1] > 0.71 or averageLoss[2] > 0.71:
        breachesTitleLabel = ctk.CTkLabel(window, text= "Potential Breaches", font=subheadingFont)
        breachesTitleLabel.pack(pady=10)
    
    #If the average loss per question for the UK GDPR is higher than 1.78, it will have a message for serious breach, if it is higher than 0.71, it will have a message for minor breach, else no message
    if averageLoss[0] > 1.78:
        gdprDetailsLabel = ctk.CTkLabel(window, text= "We believe that your firm may be in serious breach of the GDPR.\nYou may face fines up to £17.5 million or 4% of global annual turnover (whichever is higher).\nThis is enforced under the Data Protection Act 2018.", font=normalFont)
        gdprDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the UK GDPR/Data Protection Act!", font=linkFont)
        linkLabel.pack(pady=(0, 25))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.gov.uk/data-protection"))
    elif averageLoss[0] > 0.71:
        gdprDetailsLabel = ctk.CTkLabel(window, text= "We believe that your firm may be in minor breach of the GDPR.\nYou may face fines up to £8.7 million or 2% of global annual turnover (whichever is higher).\nThis is enforced under the Data Protection Act 2018.", font=normalFont)
        gdprDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the UK GDPR/Data Protection Act!", font=linkFont)
        linkLabel.pack(pady=(0, 25))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.gov.uk/data-protection"))

    #If the average loss per question for the UK GDPR is higher than 1.78, it will have a message for serious breach, if it is higher than 0.71, it will have a message for minor breach, else no message
    if averageLoss[1] > 1.78:
        cmaDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in serious breach of the Computer Misuse Act 1990.\nThey may face up to 2 years imprisonment", font=normalFont)
        cmaDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Computer Misuse Act!", font=linkFont)
        linkLabel.pack(pady=(0, 25))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/computer-misuse-act"))
    elif averageLoss[1] > 0.71:
        cmaDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in minor breach of the Computer Misuse Act 1990.\nThey may face small fines if escalated", font=normalFont)
        cmaDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Computer Misuse Act!", font=linkFont)
        linkLabel.pack(pady=(0, 25))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/computer-misuse-act"))

    #If the average loss per question for the UK GDPR is higher than 1.78, it will have a message for serious breach, if it is higher than 0.71, it will have a message for minor breach, else no message
    if averageLoss[2] > 1.78:
        fraudDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in serious breach of The Fraud Act 2006.\nThey may face up to 10 years imprisonment if escalated", font=normalFont)
        fraudDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on The Fraud Act!", font=linkFont)
        linkLabel.pack(pady=(0, 25))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/fraud-act-2006"))
    elif averageLoss[2] > 0.71:
        fraudDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in minor breach of The Fraud Act 2006.\nThey may face small fines or a short imprisonment period if escalated", font=normalFont)
        fraudDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on The Fraud Act!", font=linkFont)
        linkLabel.pack(pady=(0, 25))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/fraud-act-2006"))
        
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
subheadingFont = ctk.CTkFont(family="Times New Roman", weight="bold", underline=True, size=18)
linkFont = ctk.CTkFont(family="Helvetic", slant="italic", underline=True, size=18)

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
