#Ryan Mastin 101229946
#Assignment 3 Question1
import psycopg2

#sets up the connection reqs, our database is on local host with the following info
connReqs = "host='localhost' dbname='A3' user='postgres' password='postgres'"

#create a connection
connection = psycopg2.connect(connReqs)

#creates a cursor to execute actions on the database
cursor = connection.cursor()

#main menu loop
exitFlag = True
while exitFlag == True:
    #prints main menu
    print("\nFunctions:\ngetAllStudents(): Retrieves and displays all records from the students table. ")
    print("addStudent(first_name, last_name, email, enrollment_date): Inserts a new student record into the students table. ")
    print("updateStudentEmail(student_id, new_email): Updates the email address for a student with the specified student_id. ")
    print("deleteStudent(student_id): Deletes the record of the student with the specified student_id. \n")
    print("*Type quit to leave*")
    
    #if user types quit the program will quit
    userInput = input("Please Enter Input: ")
    if(userInput.lower() == "quit"):
        exitFlag = False
        #not Needed but just incase
        connection.commit()
    
    #selects all records from the student table and prints each returned student
    elif(userInput == "getAllStudents()"):
        cursor.execute("SELECT * FROM Students")
        records = cursor.fetchall()
        for record in records:
            print(record)
    
    #addStudent() function, strips unessesary stuff off (brackets and splits on commas) creating a list of pure values
    elif("addStudent(" in userInput and userInput[-1] == ")"):
        tobeAdded = (userInput.split("("))
        details = tobeAdded[1].strip(")")
        stuffs = details.split(",")

        #Replaces all spaces with nothing so we can have consistant data in the database
        for i in range(0, len(stuffs)):
            stuffs[i] = stuffs[i].replace(" ", "")
        
        if(len(stuffs) != 4):
            print("Incorrect number of Args, please enter it again")
            continue
        #insert statement for our database, .format inserts our variables into the string then executes and commits 
        try:
            insertStatement = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('{}', '{}', '{}', '{}');".format(stuffs[0], stuffs[1], stuffs[2], stuffs[3])
            cursor.execute(insertStatement)
            print("*Added Student*")
        except psycopg2.Error as error:
            print("Error")

    #updateStudentEmail() function, strips unessesary stuff off (brackets and splits on commas) creating a list of pure values
    elif("updateStudentEmail(" in userInput and userInput[-1] == ")"):
        tobeUpdated = (userInput.split("("))
        emails = tobeUpdated[1].strip(")")
        inputList = emails.split(",")
    
        if(len(inputList) != 2):
            print("Incorrect number of Args, please enter it again")
            continue

        #if spaces exist (likely) then replace them with nothing
        if(" " in inputList[1] or " " in inputList[0]):
            inputList[1] = inputList[1].replace(" ", "")
            inputList[0] = inputList[0].replace(" ", "")
        studentNumber = inputList[0]
        new_email = inputList[1]
        
        #attempts to find the student, if its found then updates the found student
        findStudent = "SELECT * FROM students WHERE student_id = {};".format(studentNumber)
        cursor.execute(findStudent)
        potential = cursor.fetchone()
        if potential:
            try:
                #update the student with the new values using string format
                update_query = ("""UPDATE students SET email = '{}' WHERE student_id = {};""").format(new_email, studentNumber)
                cursor.execute(update_query)
                print("*Updated Student*")
            except psycopg2.Error as err:
                print("Error")
        else:
            print("No Student Found")

    #deleteStudent() function, strips unessecary stuff off (brackets and splits on commas) creating a list of pure values
    elif("deleteStudent(" in userInput and userInput[-1] == ")"):
        tobeDeleted = userInput.split("(")
        studentNumber = tobeDeleted[1].replace(")", "")

        if(len(studentNumber) == 0) :
            print("Please correct inputs and retry")
            continue
        #First attempts to find the student in the database, if its found go ahead and delete. otherwise print and continue
        findStudent = "SELECT * FROM students WHERE student_id = {};".format(studentNumber)
        cursor.execute(findStudent)
        potential = cursor.fetchone()
        if potential:
            try:
                 #creates the delete query for our database, .format inserts the student number into the query.
                delete_query = "DELETE FROM students WHERE student_id = {};".format(studentNumber)
                cursor.execute(delete_query)
                print("*Deleted Student*")
            except psycopg2.Error as err:
                print("Error")
        else:
            print("Could not find student")

    else:
        print("Unknown Command")
    
    connection.commit()
#closes the cursor and connection on exit (not needed but good practice)
cursor.close()
connection.close()
