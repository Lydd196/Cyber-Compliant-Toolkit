import customtkinter as ctk
import random
import questionhandler 
import datetime
import webbrowser
import sys
import json
import os 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Create the main window
window = ctk.CTk()
window.title("Cyber Law Compliance Toolkit")
window.geometry("1920x1080")
window._state_before_windows_set_titlebar_color = "zoomed"
ctk.set_appearance_mode("Dark")

#Initial compliance level as a percentage
complianceLevel = 100
firstAccess = True
graphViewed = False

#Function to open url in new tab
def openUrl(link):
   webbrowser.open_new_tab(link)

#Function to load the last quiz's compliance value -----SUBJECT TO CHANGE------
def loadOldCompliance(oldFile):
    with open(oldFile, 'r') as file:
        oldFile = json.load(file)
    return oldFile

#Function for getting the closest json file to the current date
def getClosestJsonFile(directory):
    #Get current datetime and storing all json files in current diretory in the files list
    now = datetime.datetime.now()
    files = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            files.append(file)

    #Parse dates from filenames and store them with their corresponding file
    fileDates = []
    for file in files:
        try:
            dateString = file.replace(".json", "")  # Remove '.json'
            fileDate = datetime.datetime.strptime(dateString, "%Y-%m-%d-%H-%M-%S")
            fileDates.append((fileDate, file))
        except ValueError:
            pass  #Skip files that dont match my datetime format

    #If no .json files are found, then it returns nothing
    if len(fileDates) == 0:
        return None  
    
    closestFile = None
    smallestDifference = 9999999999999999.999999

    #Find the file with the closest date to now
    for fileDate, filename in fileDates:
        timeDifference = abs((now - fileDate).total_seconds())
        if timeDifference < smallestDifference:
            smallestDifference = timeDifference
            closestFile = filename
    return closestFile  

#Function for exporting the question data as a json format, with the name as the current datetime, currently just storing the compliance value
def download():
    time = datetime.datetime.now()
    datetimeString = time.strftime("%Y-%m-%d-%H-%M-%S")
    datetimeStringJson = datetimeString + ".json"
    with open(datetimeStringJson, 'w') as f:
        json.dump(complianceLevel, f)

#Function to clear previous question elements
def clearElements(window):
    for elements in window.winfo_children():
        elements.destroy() 

#Function to show the results and automatically downloads a JSON file (currently just storing the compliance value)
def showResults():
    global firstAccess
    global closestFile
    if firstAccess == True:
        directory = '.'  # Directory where JSON files are stored
        closestFile = getClosestJsonFile(directory)
        download()
        firstAccess = False
    
    #Clears the current elements such that the window is ready to display the results
    clearElements(window)
    window.title("Your Results")

    #Display final compliance value as a percentage with text depending on the final value itself
    complianceTitleLabel = ctk.CTkLabel(window, text= "Final compliance level:", font=titleFont)        
    complianceTitleLabel.pack(pady=15)
    complianceLevelLabel = ctk.CTkLabel(window, text=str(complianceLevel) + "%", font=normalFont)
    complianceLevelLabel.pack(pady=15)

    #Additionally displays the compliance value as a pie chart using the pyplot and canvas libraries
    pieValues = [complianceLevel, 100 - complianceLevel]
    labels = ['Compliant', 'Non-Compliant']
    colors = ["#0ac700", "#bf0000"]
    figure, axes = plt.subplots(figsize=(3, 3))
    figure.patch.set_facecolor("#2c2c2c") 
    axes.set_facecolor("#2c2c2c")   
    axes.pie(pieValues, labels=labels, autopct="%1.0f%%", colors=colors, startangle=90, textprops={"color": "white", 'fontsize': 18})
    axes.axis('equal')  
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    resultDescriptionLabel = ctk.CTkLabel(window, text= "sample text", font=normalFont)

    #Different result descriptions based on the compliance value 
    externalInfo = questionhandler.returnExternalInfo()
    for index in range(0, len(externalInfo) - 1):
        externalInfo[index] = round(externalInfo[index], 2)
    wrongList = externalInfo[3]
    if complianceLevel > 80:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is very compliant with cyber laws. Great Job!")
        resultDescriptionLabel.pack(pady=15)
    elif complianceLevel > 50:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is not very compliant with cyber laws")
        resultDescriptionLabel.pack(pady=15)
    else:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is not compliant at all with cyber laws")
        resultDescriptionLabel.pack(pady=15)  

    #Average loss thresholds are calculated by (x/y* (100-z))/x where x is the amount of that question type, y is the total number of questions and z is dependant on the condition (50 for serious breach and 80 for minor breach (MAY CHANGE))
    #THIS AVERAGE SYSTEM MUST BE CHANGED IF NEW QUESTIONS ARE ADDED
    if externalInfo[0] > 0.66 or externalInfo[1] > 0.66 or externalInfo[2] > 0.66:
        breachesTitleLabel = ctk.CTkLabel(window, text= "Potential Breaches", font=subheadingFont)
        breachesTitleLabel.pack(pady=10)
    
    #If the average loss per question for the UK GDPR is higher than 1.66, it will have a message for serious breach, if it is higher than 0.66, it will have a message for minor breach, else no message
    if externalInfo[0] > 1.66:
        gdprDetailsLabel = ctk.CTkLabel(window, text= "We believe that your firm may be in serious breach of the GDPR.\nYou may face fines up to £17.5 million or 4% of global annual turnover (whichever is higher).\nThis is enforced under the Data Protection Act 2018.", font=normalFont)
        gdprDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the UK GDPR/Data Protection Act!", font=linkFont)
        linkLabel.pack(pady=(0, 20))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.gov.uk/data-protection"))
    elif externalInfo[0] > 0.66:
        gdprDetailsLabel = ctk.CTkLabel(window, text= "We believe that your firm may be in minor breach of the GDPR.\nYou may face fines up to £8.7 million or 2% of global annual turnover (whichever is higher).\nThis is enforced under the Data Protection Act 2018.", font=normalFont)
        gdprDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the UK GDPR/Data Protection Act!", font=linkFont)
        linkLabel.pack(pady=(0, 20))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.gov.uk/data-protection"))

    #If the average loss per question for the Computer Misuse Act is higher than 1.66, it will have a message for serious breach, if it is higher than 0.66, it will have a message for minor breach, else no message
    if externalInfo[1] > 1.66:
        cmaDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in serious breach of the Computer Misuse Act 1990.\nThey may face up to 2 years imprisonment.", font=normalFont)
        cmaDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Computer Misuse Act!", font=linkFont)
        linkLabel.pack(pady=(0, 20))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/computer-misuse-act"))
    elif externalInfo[1] > 0.66:
        cmaDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in minor breach of the Computer Misuse Act 1990.\nThey may face small fines if escalated.", font=normalFont)
        cmaDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Computer Misuse Act!", font=linkFont)
        linkLabel.pack(pady=(0, 20))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/computer-misuse-act"))

    #If the average loss per question for the Fraud Act is higher than 1.66, it will have a message for serious breach, if it is higher than 0.66, it will have a message for minor breach, else no message
    if externalInfo[2] > 1.66:
        fraudDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in serious breach of the Fraud Act 2006.\nThey may face up to 10 years imprisonment if escalated.", font=normalFont)
        fraudDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Fraud Act!", font=linkFont)
        linkLabel.pack(pady=(0, 20))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/fraud-act-2006"))
    elif externalInfo[2] > 0.66:
        fraudDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in minor breach of The Fraud Act 2006.\nThey may face small fines or a short imprisonment period if escalated.", font=normalFont)
        fraudDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Fraud Act!", font=linkFont)
        linkLabel.pack(pady=(0, 20))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/fraud-act-2006"))
    
    #If there is a closest file, loads it and shows a message depending on whether the firm has improved their compliance or not
    if closestFile != None:
        lastCompliance = loadOldCompliance(closestFile)
        #Remove .json and show the date as d/m/y
        dateString = closestFile.replace(".json", "")  
        fileDate = datetime.datetime.strptime(dateString, "%Y-%m-%d-%H-%M-%S")
        formattedDate = fileDate.strftime("%d/%m/%Y")
        if lastCompliance > complianceLevel:
            difference = lastCompliance - complianceLevel
            differenceLabel = ctk.CTkLabel(window, text= "Your compliance score decreased by " + str(difference) + "% from last time on " + formattedDate, font=normalFont)
            differenceLabel.pack()
        elif complianceLevel > lastCompliance:
            difference = complianceLevel - lastCompliance
            differenceLabel = ctk.CTkLabel(window, text= "Your compliance score increased by " + str(difference) + "% from last time on " + formattedDate, font=normalFont)
            differenceLabel.pack()

    #Buttons for reviewing incorrect questions as well as a button to close the program
    if complianceLevel != 100:
        reviewQuestionsButton = ctk.CTkButton(window, text="Review Incorrect Answers", command=lambda: reviewWrongQuestions(wrongList) ,font=normalFont)
        reviewQuestionsButton.pack(padx=10, pady=5, anchor="center")
    endButton = ctk.CTkButton(window, text="End", command=close, font=normalFont)
    endButton.pack(padx=10, pady=5, anchor="center")

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

#Function to review the questions the user lost compliance score on 
def reviewWrongQuestions(wrongList):
    #Clears all current elements and loads the wrong questions using json and result data 
    clearElements(window) 
    questionNumber = 1
    questionList = questionhandler.loadWrongQuestions("questions.json", wrongList)
    questionAmount = len(questionList)
    #A flag to go back to the results page
    global goToResults 
    goToResults = False

    while questionNumber <= len(questionList):
        if questionNumber < 1:
            questionNumber = 1
        question = questionList[questionNumber - 1]

        #Callback to go to results
        def goToResultsCallback() :
            global goToResults
            goToResults = True
            showResults()

        #Returned value is a condition
        goBackCondition = questionhandler.showWrongQuestion(window, question, questionNumber, questionAmount, goToResultsCallback)

        #Showing the question returns a condition to check if the user wanted to go back or not, if so, deducts the question number by 1 and shows the previous result, or if the user wanted to go to results, activates the flag
        if goToResults == True:
            break
        if goBackCondition == False:
            questionNumber = questionNumber + 1
        else:
            questionNumber = questionNumber - 1
            goBackCondition = False

def graph():
    global graphViewed
    global canvas
    if graphViewed == False:
        #Get current datetime and storing all json files in current diretory in the files list
        files = []
        for file in os.listdir("."):
            if file.endswith(".json"):
                files.append(file)

        #Parse dates from filenames and store them with their corresponding file
        fileData = []
        for file in files:
            try:
                dateString = file.replace(".json", "") 
                fileDate = datetime.datetime.strptime(dateString, "%Y-%m-%d-%H-%M-%S")
                complianceValue = loadOldCompliance(file)
                fileData.append((fileDate, complianceValue))
            except ValueError:
                pass  #Skip files that dont match my datetime format

        #If no .json files are found, then it returns nothing
        if len(fileData) == 0:
            return None  

        #Sort the data by date
        fileData.sort()

        #Extract dates and compliance levels for plotting
        dates = []
        complianceLevels = []

        #Iterate through fileData and append elements to respective lists
        for data in fileData:
            dates.append(data[0])
            complianceLevels.append(data[1])

        #Plot the compliance value for each json file using matplotlib and pyplot libraries, showing progression over time
        figure, axes = plt.subplots(figsize=(15, 8))
        figure.patch.set_facecolor("#2c2c2c") 
        axes.set_facecolor("#2c2c2c")   
        axes.plot(dates, complianceLevels, marker='o', linestyle='-', color='red', label='Compliance Level')
        axes.set_xlabel("Date", fontsize=18, fontname="Times New Roman", color="white")
        axes.set_ylabel("Compliance Level (%)", fontsize=18, fontname="Times New Roman", color="white")
        axes.set_title("Compliance Levels Over Time", fontsize=18, fontname="Times New Roman", color="white")
        #Format the date on the x axis as d/m/y
        axes.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))  
        axes.tick_params(axis='x', rotation=25, colors="white")  
        axes.tick_params(axis='y', colors="white")
        axes.legend(loc="upper left", fontsize=10, facecolor="#2c2c2c", edgecolor="white", labelcolor="w")
        axes.grid(color="gray", linestyle="--", linewidth=0.7)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", pady=5)  
        graphButton.configure(text="Hide Graph")
        graphViewed = True
    else:
        canvas.get_tk_widget().destroy()
        graphButton.configure(text="Show Graph")
        graphViewed = False
    
#Cancel function to not run the test and to close the program, by usage of terminating main.py
def close():
    sys.exit(0)

#Set it so when the window is deleted, it makes sure the window is destroyed and closed properly
window.protocol("WM_DELETE_WINDOW", close)

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
startButton.pack(pady=8)
graphButton = ctk.CTkButton(window, text="Show Graph", command=graph, font=normalFont)
graphButton.pack(pady=8)
closeButton = ctk.CTkButton(window, text="Close", command=close, font=normalFont)
closeButton.pack(pady=8)

#Run the main loop
window.mainloop()

#Print final compliance score in the terminal (debugging purposes)
print("Final compliance level:", complianceLevel)
