import customtkinter as ctk
import tkinter as tk
import random
import questionhandler 

# Create the main window
root = ctk.CTk()
root.title("Cyber Law Compliance Toolkit")
root.geometry("1100x550")

# Initial compliance level as a percentage
complianceLevel = 100

# Start function for running the questions (starting the test)
def start():
    descriptionLabel.destroy()
    startButton.destroy()
    closeButton.destroy()
    global complianceLevel
    questionNumber = 1

    # List of questions
    questionList = [questionhandler.q1, questionhandler.q2, questionhandler.q3]

    # Shuffle the questions to randomize the order
    random.shuffle(questionList)

    # Iterate over the shuffled questions and update compliance level
    for question in questionList:
        complianceLevel = question(complianceLevel, questionNumber)
        questionNumber = questionNumber + 1

    titleLabel.configure(text="Your Results")
    
    # Display final compliance value as a percentage
    complianceTitleLabel = ctk.CTkLabel(root, text= "Final compliance level:", font=titleFont)
    complianceTitleLabel.pack(pady=15)

    complianceLevelLabel = ctk.CTkLabel(root, text=str(complianceLevel) + "%", font=normalFont)
    complianceLevelLabel.pack(pady=15)

    resultDescriptionLabel = ctk.CTkLabel(root, text= "sample text", font=normalFont)
    if complianceLevel > 95:
        resultDescriptionLabel.configure(text= "We believe that your business is very compliant with cyber laws. Great Job!")
        resultDescriptionLabel.pack(pady=15)
    elif complianceLevel > 90:
        resultDescriptionLabel.configure(text= "We believe that your business is not very compliant with the Data Protection Act, read more here:")
        resultDescriptionLabel.pack(pady=15)
    else:
        resultDescriptionLabel.configure(text= "Very bad!")
        resultDescriptionLabel.pack(pady=15)
        
    endButton = ctk.CTkButton(root, text="End", command=close, font=normalFont)
    endButton.pack(pady=15)

# Cancel function to not run the test and to close the program
def close():
    root.destroy()

titleFont = ctk.CTkFont(family="Helvetic", size=25, weight="bold") 
normalFont = ctk.CTkFont(family="Times New Roman", size=18)
titleLabel= ctk.CTkLabel(root, text="Welcome to CyberComply: The Cyber Law Compliance Toolkit for Accountants", font=titleFont)
titleLabel.pack(pady=25)


descriptionLabel = ctk.CTkLabel(root, text="Find out how compliant your accountancy business is with cyber laws", font=normalFont)
descriptionLabel.pack(pady=15)

# Create start and close buttons
startButton = ctk.CTkButton(root, text="Start", command=start, font=normalFont)
startButton.pack(pady=15)

closeButton = ctk.CTkButton(root, text="Close", command=close, font=normalFont)
closeButton.pack(pady=15)

# Run the main loop
root.mainloop()

# Print final compliance score in the terminal (debugging purposes)
print("Final compliance level:", complianceLevel)
