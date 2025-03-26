import customtkinter as ctk
import random
import questionhandler 
import datetime
import webbrowser
import sys
import json
import os 
import stat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Create the main window with specific properties
window = ctk.CTk()
window.title("Cyber Law Compliance Toolkit")
window.geometry("1920x1080")
window._state_before_windows_set_titlebar_color = "zoomed"
window.resizable(False, False)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

#Initial values such as averages, compliance value, etc
complianceLevel = 100
firstAccess = True
wrongList = []
gdprAverage = 0
misuseAverage = 0
fraudAverage = 0
swapGraphButton = None
canvas = None  

#Defining the folder for JSON files 
jsonFolder = "TestResults"

#Start function for running the questions (starting the test)
def start():
    #Clear all elements from the window to prepare the test
    clearElements(window) 
    global complianceLevel, questionNumber
    questionNumber = 1
    
    #List of questions from json file gets ordered from randomised gdpr first, randomised cma next, then randomised fraud last
    questions = questionhandler.loadQuestions()
    gdprQuestions = []
    cmaQuestions = []
    fraudQuestions = []
    for question in questions:
        if question["law"] == "UK GDPR":
            gdprQuestions.append(question)
        elif question["law"] == "Computer Misuse Act":
            cmaQuestions.append(question)
        elif question["law"] == "The Fraud Act":
            fraudQuestions.append(question)
    random.shuffle(gdprQuestions)
    random.shuffle(cmaQuestions)
    random.shuffle(fraudQuestions)
    questionDataList = gdprQuestions + cmaQuestions + fraudQuestions
    questionAmount = len(questionDataList)
    selectedAnswers = []

    #Callback function to go to previous question
    def goPreviousQuestion():
        global questionNumber   
        questionNumber = questionNumber - 1
        selectedAnswers.pop()  
        window.quit()  

    #Run each question dynamically, adding the selection option to a list after each question
    while questionNumber <= len(questionDataList):
        question = questionDataList[questionNumber - 1]
        selectedOption = questionhandler.showQuestion(window, question, questionNumber, questionAmount, goPreviousQuestion)
        if selectedOption != 0:
            selectedAnswers.append(selectedOption)
            questionNumber = questionNumber + 1
    
    #After each of the questions have been answered, calculate the compliance and the average losses for laws
    questionIndex = 0
    while questionIndex < len(selectedAnswers):
        answer = selectedAnswers[questionIndex]
        if answer != None:
            currentQuestionData = questionDataList[questionIndex]
            newComplianceLevel = complianceLevel + currentQuestionData["deduction"][answer - 1]
            averageLossUpdate(newComplianceLevel, complianceLevel, currentQuestionData["law"])
            if newComplianceLevel != complianceLevel:
                wrongList.append(currentQuestionData["id"])
            complianceLevel = newComplianceLevel
            questionIndex = questionIndex + 1
    
    #If compliance is less than zero, it is set to zero
    if complianceLevel < 0:
        complianceLevel = 0

    #After compliance and average losses for laws have been calculated, show the results 
    showResults()

#Cancel function to not run the test and to close the program, by usage of terminating main.py
def close():
    sys.exit(0)
window.protocol("WM_DELETE_WINDOW", close)

#Function to create the compliance graph on the main page, with a button to go to the average loss graph
def complianceGraph():
    global canvas, swapGraphButton
    jsonFolderCheck()
    if canvas != None:
        canvas.get_tk_widget().destroy()
    if swapGraphButton != None:
        swapGraphButton.destroy()
  
    #Get current datetime and storing all json files in current directory in the files list
    files = []
    for file in os.listdir(jsonFolder):
        if file.endswith(".json"):
            files.append(file)

    #Parse dates from filenames and store them with their corresponding file, if it doesnt meet the required format or is higher than current date, it is ignored
    fileData = []
    for file in files:
        try:
            dateString = file.replace(".json", "") 
            fileDate = datetime.datetime.strptime(dateString, "%Y-%m-%d-%H-%M-%S")
            complianceValue = loadOldCompliance(os.path.join(jsonFolder, file))
            if fileDate <= datetime.datetime.now() and isinstance(complianceValue, int) and complianceValue <= 100 and complianceValue >= 0:  
                fileData.append((fileDate, complianceValue))
        except ValueError:
            pass

    #If no .json files are found, then it returns nothing
    if len(fileData) == 0:
        return None  

    #Sort the data by date
    fileData.sort()
    dates = []
    complianceLevels = []

    #Iterate through fileData and append elements to date and compliance lists
    for data in fileData:
        dates.append(data[0])
        complianceLevels.append(data[1])

    #Plot the compliance value for each json file using matplotlib and pyplot libraries, showing progression over time
    figure, axes = plt.subplots(figsize=(15, 6))
    figure.patch.set_facecolor("#2c2c2c") 
    axes.set_facecolor("#2c2c2c")   
    axes.plot(dates, complianceLevels, marker="o", markersize=10, linestyle="-", linewidth = 2.5, color="blue", label="Compliance Level")
    axes.set_xlabel("Date", fontsize=18, fontname="Times New Roman", color="white")
    axes.set_ylabel("Compliance Level (%)", fontsize=18, fontname="Times New Roman", color="white")
    axes.set_title("Compliance Levels Over Time", fontsize=18, fontname="Times New Roman", color="white")

    #Horizontal lines showing what is good compliance or bad compliance
    axes.hlines(y=80, xmin=dates[0], xmax=dates[len(dates) - 1], colors="green", linewidth=5, label="Good Compliance")
    axes.hlines(y=50, xmin=dates[0], xmax=dates[len(dates) - 1], colors="red", linewidth=5, label="Bad Compliance")
    
    #Format the date on the x axis as d/m/y
    axes.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))  
    axes.tick_params(axis="x", rotation=25, colors="white", labelsize=14)  
    axes.tick_params(axis="y", colors="white", labelsize=14)
    axes.legend(loc="upper left", fontsize=10, facecolor="#2c2c2c", edgecolor="white", labelcolor="w")
    axes.grid(color="gray", linestyle="--", linewidth=0.7)
    plt.tight_layout()
        
    #Draw graph and create button to go to the average graph
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", pady=5)  
    graphButton.configure(text="Hide Graph")
    swapGraphButton = ctk.CTkButton(window, text=">", command=averagesGraph, font=normalFont)
    swapGraphButton.pack(pady=5)
    graphButton.configure(text="Hide Graph", command=deleteGraph)

#Function to create the compliance graph on the main page, with a button to go to the compliance graph
def averagesGraph():
    global canvas, swapGraphButton
    jsonFolderCheck()
    if canvas != None:
        canvas.get_tk_widget().destroy()
    if swapGraphButton != None:
        swapGraphButton.destroy()
    
    #Get current datetime and storing all json files in current directory in the files list
    files = []
    for file in os.listdir(jsonFolder):
        if file.endswith(".json"):
           files.append(file)

    #Parse dates from filenames and store them with their corresponding file, if it doesnt meet the required format or is higher than current date, it is ignored
    fileData = []
    for file in files:
        try:
            dateString = file.replace(".json", "") 
            fileDate = datetime.datetime.strptime(dateString, "%Y-%m-%d-%H-%M-%S")
            gdpr, cma, fraud = loadOldAverages(os.path.join(jsonFolder, file))
            if fileDate <= datetime.datetime.now() and isinstance(gdpr, float) == True and gdpr < 5.0 and gdpr >= 0.0 and isinstance(cma, float) == True and cma < 5.0 and cma >= 0.0 and isinstance(fraud, float) == True and fraud < 5.0 and fraud >= 0.0:  
                fileData.append((fileDate, gdpr, cma, fraud))
        except ValueError:
            pass

    #If no .json files are found, then it returns nothing
    if len(fileData) == 0:
        return None  

    #Sort the data by date
    fileData.sort()
    dates = []
    gdprAverages = []
    cmaAverages = []
    fraudAverages = []

    #Iterate through fileData and append elements to date and averages lists
    for data in fileData:
        dates.append(data[0])
        gdprAverages.append(data[1])
        cmaAverages.append(data[2])
        fraudAverages.append(data[3])

    #Plot the compliance value for each json file using matplotlib and pyplot libraries, showing progression over time
    figure, axes = plt.subplots(figsize=(15, 6))
    figure.patch.set_facecolor("#2c2c2c") 
    axes.set_facecolor("#2c2c2c")   
    axes.plot(dates, gdprAverages, marker="o", markersize=10, linestyle="-", linewidth = 2.5, color="blue", label="GDPR")
    axes.plot(dates, cmaAverages, marker="o", markersize=10, linestyle="-", linewidth = 2.5, color="orange", label="Computer Misuse Act")
    axes.plot(dates, fraudAverages, marker="o", markersize=10, linestyle="-", linewidth = 2.5, color="purple", label="Fraud Act")
    axes.invert_yaxis()
    axes.set_xlabel("Date", fontsize=18, fontname="Times New Roman", color="white")
    axes.set_ylabel("Average Compliance Loss Per Question", fontsize=18, fontname="Times New Roman", color="white")
    axes.set_title("Average Compliance Loss Per Law Per Question Over Time", fontsize=18, fontname="Times New Roman", color="white")

    #Horizontal lines showing what is good compliance or bad compliance
    axes.hlines(y=0.66, xmin=dates[0], xmax=dates[len(dates) - 1], colors="green", linewidth=5, label="Good Compliance")
    axes.hlines(y=1.66, xmin=dates[0], xmax=dates[len(dates) - 1], colors="red", linewidth=5, label="Bad Compliance")

    #Format the date on the x axis as d/m/y
    axes.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))  
    axes.tick_params(axis="x", rotation=25, colors="white", labelsize=14)  
    axes.tick_params(axis="y", colors="white", labelsize=14)
    axes.legend(loc="upper left", fontsize=10, facecolor="#2c2c2c", edgecolor="black", labelcolor="w")
    axes.grid(color="gray", linestyle="--", linewidth=0.7)
    plt.tight_layout()
        
    #Draw graph and create button to go to the compliance graph
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", pady=5)  
    graphButton.configure(text="Hide Graph")
    swapGraphButton = ctk.CTkButton(window, text="<", command=complianceGraph, font=normalFont)
    swapGraphButton.pack(pady=5)
    graphButton.configure(text="Hide Graph", command=deleteGraph)

#Function to delete the current graph and reset variables
def deleteGraph():
    global canvas, swapGraphButton, graphButton
    if canvas != None:
        canvas.get_tk_widget().destroy()
        canvas = None
    if swapGraphButton != None:
        swapGraphButton.destroy()
        swapGraphButton = None
    graphButton.configure(text="Show Graph", command=complianceGraph)

#Function to show the results and automatically downloads a JSON file
def showResults():
    global firstAccess, closestFile
    jsonFolderCheck()
    if firstAccess == True:
        closestFile = getClosestJsonFile(jsonFolder)
        download()
        firstAccess = False
    
    #Clears the current elements such that the window is ready to display the results
    clearElements(window)
    window.title("Your Results")

    #Display final compliance value as a percentage with text depending on the final value itself
    complianceTitleLabel = ctk.CTkLabel(window, text= "Final compliance level:", font=titleFont)        
    complianceTitleLabel.pack(pady=10)
    complianceLevelLabel = ctk.CTkLabel(window, text=str(complianceLevel) + "%", font=titleFont)
    complianceLevelLabel.pack(pady=10)

    #Additionally displays the compliance value as a pie chart using the pyplot and canvas libraries
    pieValues = [complianceLevel, 100 - complianceLevel]
    labels = ["Compliant", "Non-Compliant"]
    colors = ["#0ac700", "#bf0000"]
    figure, axes = plt.subplots(figsize=(8, 3))
    figure.patch.set_facecolor("#2c2c2c")
    axes.set_facecolor("#2c2c2c")
    axes.pie(pieValues, labels=labels, autopct="%1.0f%%", colors=colors, startangle=90, textprops={"color": "white", "fontsize": 18, "fontfamily": "Times New Roman"})
    axes.axis("equal") 
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(anchor="center")

    resultDescriptionLabel = ctk.CTkLabel(window, text= "sample text", font=normalFont)

    #Different result descriptions based on the compliance value 
    lawAverages = returnLawAverages()
    for index in range(0, len(lawAverages) - 1):
        lawAverages[index] = round(lawAverages[index], 2)
    if complianceLevel > 80:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is very compliant with cyber laws. Great Job!")
        resultDescriptionLabel.pack(pady=10)
    elif complianceLevel > 50:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is not very compliant with cyber laws")
        resultDescriptionLabel.pack(pady=10)
    else:
        resultDescriptionLabel.configure(text= "We believe that overall, your accountancy firm is not compliant at all with cyber laws")
        resultDescriptionLabel.pack(pady=10)  

    #Average loss thresholds are calculated by (100-y)/x where x is the total number of questions and y is dependant on the condition (50 for serious breach and 80 for minor breach (MAY CHANGE))
    #--------------------THIS AVERAGE SYSTEM MUST BE CHANGED IF NEW QUESTIONS ARE ADDED---------------------------
    if lawAverages[0] > 0.66 or lawAverages[1] > 0.66 or lawAverages[2] > 0.66:
        breachesTitleLabel = ctk.CTkLabel(window, text= "Potential Breaches", font=subheadingFont)
        breachesTitleLabel.pack(pady=10)
    
    #If the average loss per question for the UK GDPR is higher than 1.66, it will have a message for serious breach, if it is higher than 0.66, it will have a message for minor breach, else no message
    if lawAverages[0] > 1.66:
        gdprDetailsLabel = ctk.CTkLabel(window, text= "We believe that your firm may be in serious breach of the GDPR.\nYou may face fines up to £17.5 million or 4% of global annual turnover (whichever is higher).\nThis is enforced under the Data Protection Act 2018.", font=normalFont)
        gdprDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the UK GDPR/Data Protection Act!", font=linkFont)
        linkLabel.pack(pady=(0, 15))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.gov.uk/data-protection"))
    elif lawAverages[0] > 0.66:
        gdprDetailsLabel = ctk.CTkLabel(window, text= "We believe that your firm may be in minor breach of the GDPR.\nYou may face fines up to £8.7 million or 2% of global annual turnover (whichever is higher).\nThis is enforced under the Data Protection Act 2018.", font=normalFont)
        gdprDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the UK GDPR/Data Protection Act!", font=linkFont)
        linkLabel.pack(pady=(0, 15))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.gov.uk/data-protection"))

    #If the average loss per question for the Computer Misuse Act is higher than 1.66, it will have a message for serious breach, if it is higher than 0.66, it will have a message for minor breach, else no message
    if lawAverages[1] > 1.66:
        cmaDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in serious breach of the Computer Misuse Act 1990.\nThey may face up to 2 years imprisonment.", font=normalFont)
        cmaDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Computer Misuse Act!", font=linkFont)
        linkLabel.pack(pady=(0, 15))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/computer-misuse-act"))
    elif lawAverages[1] > 0.66:
        cmaDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in minor breach of the Computer Misuse Act 1990.\nThey may face small fines if escalated.", font=normalFont)
        cmaDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Computer Misuse Act!", font=linkFont)
        linkLabel.pack(pady=(0, 15))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/computer-misuse-act"))

    #If the average loss per question for the Fraud Act is higher than 1.66, it will have a message for serious breach, if it is higher than 0.66, it will have a message for minor breach, else no message
    if lawAverages[2] > 1.66:
        fraudDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in serious breach of the Fraud Act 2006.\nThey may face up to 10 years imprisonment if escalated.", font=normalFont)
        fraudDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Fraud Act!", font=linkFont)
        linkLabel.pack(pady=(0, 15))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/fraud-act-2006"))
    elif lawAverages[2] > 0.66:
        fraudDetailsLabel = ctk.CTkLabel(window, text= "We believe that some of your employees may be in minor breach of The Fraud Act 2006.\nThey may face small fines or a short imprisonment period if escalated.", font=normalFont)
        fraudDetailsLabel.pack()
        linkLabel = ctk.CTkLabel(window, text="Click here to learn more information on the Fraud Act!", font=linkFont)
        linkLabel.pack(pady=(0, 15))
        linkLabel.bind("<Button-1>", lambda event:openUrl("https://www.cps.gov.uk/legal-guidance/fraud-act-2006"))
    
    #If there is a closest file, loads it and shows a message depending on whether the firm has improved their compliance or not
    if closestFile != None:
        lastCompliance = loadOldCompliance(closestFile)
        
        #Remove the top-level part of the directory (removes "TestResults\")
        closest = os.path.splitext(os.path.basename(closestFile))[0]

        #Remove .json and show the date as d/m/y
        dateString = closest.replace(".json", "")  
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
    resultButtonsFrame = ctk.CTkFrame(window)
    resultButtonsFrame.pack(pady=5)
    if complianceLevel != 100:
        reviewQuestionsButton = ctk.CTkButton(resultButtonsFrame, text="Review Incorrect Answers", command=lambda: reviewWrongQuestions(wrongList) ,font=normalFont)
        reviewQuestionsButton.pack(padx=5, side="left")
    endButton = ctk.CTkButton(resultButtonsFrame, text="End", command=close, font=normalFont)
    endButton.pack(padx=5, side="left")

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
        def goToResults():
            global goToResults
            goToResults = True
            showResults()

        #Returned value is a condition
        goBackCondition = questionhandler.showWrongQuestion(window, question, questionNumber, questionAmount, goToResults)

        #Showing the question returns a condition to check if the user wanted to go back or not, if so, deducts the question number by 1 and shows the previous result, or if the user wanted to go to results, activates the flag
        if goToResults == True:
            break
        if goBackCondition == False:
            questionNumber = questionNumber + 1
        else:
            questionNumber = questionNumber - 1
            goBackCondition = False

#Function to open url in new tab
def openUrl(link):
   webbrowser.open_new_tab(link)

#Function to load the a quizzes' compliance value, if the old file does not have a "compliance" variable, it returns nothing and is ignored
def loadOldCompliance(oldFile):
    with open(oldFile, "r") as file:
        oldFileData = json.load(file)
    oldCompliance = oldFileData.get("compliance")
    if oldCompliance == None:
        return
    else:
        return oldCompliance

#Function to load a quizzes' loss averages, if the old file does not have at least one of the old average variable, it returns and empty list and is ignored
def loadOldAverages(oldFile):
    with open(oldFile, "r") as file:
        oldFileData = json.load(file)
    oldGDPR = oldFileData.get("averagegdpr")
    oldCMA = oldFileData.get("averagecma")
    oldFraud = oldFileData.get("averagefraud")
    if oldGDPR == None or oldCMA == None or oldFraud == None:
        return []
    else:
        return [oldGDPR, oldCMA, oldFraud]

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
        #If .json file name doesnt meet expected datetime format or is later than the current datatime, it is ignored
        try:
            dateString = file.replace(".json", "")  
            fileDate = datetime.datetime.strptime(dateString, "%Y-%m-%d-%H-%M-%S")
            if fileDate <= now:  
                fileDates.append((fileDate, file))
        except ValueError:
            pass  

    #If no .json files are found, then it returns nothing
    if len(fileDates) == 0:
        return None  
    
    closestFile = None
    smallestDifference = 9999999999999999.999999

    #Find the file with the closest date to now, excluding later dates
    for fileDate, filename in fileDates:
        timeDifference = abs((now - fileDate).total_seconds())
        if timeDifference < smallestDifference:
            smallestDifference = timeDifference
            closestFile = filename
    return os.path.join(directory, closestFile)

#Function to clear previous question elements
def clearElements(window):
    for elements in window.winfo_children():
        elements.destroy() 

#Function for checking if TestResults exists and if it doesnt, it creates it
def jsonFolderCheck():
    if os.path.exists(jsonFolder) == False:
        os.makedirs(jsonFolder)

#Function to erase all read-only JSON files from the TestResults
def deleteJsonFiles():
    jsonFolderCheck()
    for file in os.listdir("TestResults"):
        if file.endswith(".json"):
            fileName = os.path.join("TestResults", file)
            os.chmod(fileName, stat.S_IWRITE)
            os.remove(fileName)

#Function for exporting the question data as a json format, with the name as the current datetime
def download():
    global gdprAverage, misuseAverage, fraudAverage
    time = datetime.datetime.now()
    datetimeString = time.strftime("%Y-%m-%d-%H-%M-%S")
    jsonFilename = datetimeString + ".json"
    jsonFilename = os.path.join(jsonFolder, jsonFilename)
    averagesData = returnLawAverages()
    downloadData = {"compliance": complianceLevel, "averagegdpr": averagesData[0], "averagecma": averagesData[1], "averagefraud": averagesData[2]}
    
    #Dumps all the download data in the json file and sets the file permission to read-only
    with open(jsonFilename, "w") as file:
        json.dump(downloadData, file)
    os.chmod(jsonFilename, stat.S_IREAD)

#Function to create/update a rolling average of the compliance loss for each of the laws
def averageLossUpdate(newCompliance, oldCompliance, questionType):
    global gdprAverage, misuseAverage, fraudAverage
    complianceDifference = oldCompliance - newCompliance
    if questionType == "UK GDPR":
        gdprAverage = gdprAverage + (complianceDifference/20)
    elif questionType == "Computer Misuse Act":
        misuseAverage = misuseAverage + (complianceDifference/6)
    elif questionType == "The Fraud Act":
        fraudAverage = fraudAverage + (complianceDifference/4)

#Function to return law averages to 2 decimal points
def returnLawAverages():
    return [round(gdprAverage, 2), round(misuseAverage, 2), round(fraudAverage, 2)]

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

#Create start, graph, delete and close buttons
startButton = ctk.CTkButton(window, text="Start", command=start, font=normalFont)
startButton.pack(pady=8)
graphButton = ctk.CTkButton(window, text="Show Graph", command=complianceGraph, font=normalFont)
graphButton.pack(pady=8)
deleteButton = ctk.CTkButton(window, text="Delete Previous Data", command=deleteJsonFiles, font=normalFont)
deleteButton.pack(pady=8)
closeButton = ctk.CTkButton(window, text="Close", command=close, font=normalFont)
closeButton.pack(pady=8)
jsonFolderCheck()

#Run the main loop
window.mainloop()
