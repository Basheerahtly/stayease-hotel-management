#constants declaration
BOOKING_FILE="guest_bookings.csv"
PAYMENT_FILE="payments.csv"
GUEST_FILE = "guest_bookings.csv"
ROOMS_FILE = "rooms.csv"
PAYMENTS_FILE = "payments.csv"


# --------------- HOUSEKEEPING ----------------
# username --> housekeeper
# password --> housekeeping
def housekeeping_login(): #login menu for manager role - asking for username and password
    housekeeping_username="housekeeper"
    housekeeping_password="housekeeping"
    max_attempts=3
    attempts=0
    while attempts < max_attempts:
        username=input("Please enter your username: ").strip()
        password=input("Please enter your password: ").strip()
        if username == housekeeping_username and password == housekeeping_password:
            print("Login Successful.\n")
            return True
        else:
            attempts += 1
            print(f"Wrong username or password. Attempts left:{max_attempts-attempts}")

    print("Too many failed login attempts. Access denied")
    return False

def update_status():
    while True:
        print(
            "Please enter room number(type exit to return to housekeeping menu): ")  #choosing the room number to update its cleaning status
        room_number = input()
        if room_number.lower() == "exit":  # to return to housekeeping menu
            break
        if not validate_room_id(room_number):  # validation check for room id
            continue  # restarting the loop if room id is invalid

        try:
            with open("rooms.csv", 'r') as lines:
                lines = lines.readlines()
                header = lines[0]
                rooms = lines[1:]

                #validate room function
                if room_in_file(room_number, rooms):  #checks if room is in file
                    for i in range(len(rooms)):  #loop that runs for every row
                        rooms_data = rooms[i].strip().split(',')  #splits the line into words
                        current_room = rooms_data[0].strip()  #as room_id has index [0], it will look in the room_id to match the entered room number
                        if current_room == room_number:  #if the current room in the row matches the room input, it will enter the loop
                            print(f"Select new status \n1. Clean \n2. Dirty \n3. In progress")  #displays status menu
                            while True:
                                try:  #in case a wrong data type is entered
                                    choice = int(input("Enter your choice: "))
                                    if choice in range(1, 4):
                                        if choice == 1:
                                            rooms_data[4] = "Clean"
                                            break
                                        elif choice == 2:
                                            rooms_data[4] = "Dirty"
                                            break
                                        elif choice == 3:
                                            rooms_data[4] = "In progress"
                                            break
                                    else:
                                        print("Please enter a valid choice(1-3): ")


                                except ValueError:
                                    print("Invalid choice.Please enter a valid choice: ")  #exception handling if wrong data type is entered
                            rooms[i] = ",".join(rooms_data) + "\n"  #rebuilds the row in a csv format so that it can br written to the file

                    with open("rooms.csv", 'w') as file:  # updates the file
                        file.writelines([header] + rooms)
                        print("Room cleaning status updated!")

                else:
                    print("Room is not in the file")
                    break

        except FileNotFoundError:
            print("File not found")
            break  #exception handling if the file is not found

def report_maintenance():
    while True:
        print("*" * 10, "Report Maintenance Menu", "*" * 10)
        new = input("New Issue (yes/no) (type exit to return to housekeeping menu): ").lower().strip()
        if new == "exit":  # to return to housekeeping menu
            break
        if new == "yes":
            print("Please enter room number: ")
            while True:
                room_number = input().strip()

                if validate_room_id(room_number):  # validation check for room id
                    break
                else:
                    print("Please enter a valid room ID: ")


            try: #file handling
                with open("rooms.csv", 'r') as rooms:
                    rooms = rooms.readlines()[1:]
                    if room_in_file(room_number, rooms):  # checks if room is in file
                        for i in range(len(rooms)):  # loop that runs for every row
                            rooms_data = rooms[i].strip().split(',')  # splits the line into words
                            current_room = rooms_data[0].strip()  # as room_id has index [0], it will look in the room_id to match the entered room number
                            if current_room == room_number: #if the room in the line matches the room number input
                                print("*" * 10, "Please Choose Maintenance Type", "*" * 10)
                                print(f"1.Plumbing \n2.Electrical \n3.Furniture \n4.Cleaning \n5.Air Conditioning \n6.Other")
                                while True:
                                  try:
                                    choice_type = int(input("Enter your choice: "))
                                    if choice_type in range(1, 7): #inout validation
                                        match choice_type:
                                            case 1: maintenance_type = "Plumbing"
                                            case 2: maintenance_type = "Electrical"
                                            case 3: maintenance_type = "Furniture"
                                            case 4: maintenance_type = "Cleaning"
                                            case 5: maintenance_type = "Air Conditioning"
                                            case 6: maintenance_type = input("Enter Maintenance Type: ")
                                        break
                                    else:
                                        print("Please enter a valid choice(1-6): ")

                                  except ValueError:
                                      print("Invalid choice.Please enter a valid choice: ")

                                while True:
                                            description = input("Enter description: ")
                                            if validate_description(description): #calls function that validates description
                                                break
                                            print(f"Please enter a correct description(20 Characters): ")

                                while True:
                                            date = input("Enter date (YYYY-MM-DD): ")
                                            if validate_date(date): #calls function that validates the date
                                                break
                                            print("Please enter a valid date (YYYY-MM-DD): ")

                                while True:
                                            reporting_person = input("Enter reporting_person: ")
                                            if validate_name(reporting_person): #calls the function that validates name
                                                break
                                            print("Please enter a valid name: ")

                                while True:
                                            reporting_to = input("Reporting to: ")
                                            if validate_name(reporting_to): #calls the function that validates name
                                                break
                                            print("Please enter a valid name: ")
                                while True:
                                        try:
                                            print(f"Choose Status:    \n1.Not Solved \n2.In Progress \n3.Solved")
                                            status = int(input("Enter status: "))
                                            if status in range(1, 4): #input validation
                                                match status:
                                                    case 1: status = "Not Solved"
                                                    case 2: status = "In Progress"
                                                    case 3: status = "Solved"
                                                break
                                            else:
                                                print("Please enter a valid status(1-3): ")

                                        except ValueError:
                                            print("Invalid choice.Please enter a valid choice(1-3): ")

                                try:
                                    with open("maintenance.csv", 'a') as maintenance: #opens maintenance file in append mode to add the new line
                                        maintenance.write(f"{current_room}, {maintenance_type}, {description}, {date}, {reporting_person}, {reporting_to}, {status}\n") #adds the line to the file
                                    print("Maintenance updated!")

                                except FileNotFoundError:
                                    print("File not found")

            except FileNotFoundError:
                print("File not found")

        else:
            print("*" * 10, "Additional Report Menu", "*" * 10)
            print(f"1.View Maintenance Issues \n2.Update Maintenance Data \n3.Exit")
            choice = input("Enter your choice: ").lower()
            match choice:
                case "1": to_find_issue()
                case "2": update_maintenance_data()
                case "3": break

def to_find_issue():
    while True:
        print(f"Choose the status \n1.Not Solved \n2.Solved \n3.In Progress \n4.Exit") #displays menu
        choice = input("Enter your choice: ").strip()
        if choice not in ["1", "2", "3", "4"]: #validation of input
            print("Please enter a valid choice(1-4): ")
            continue

        header = ["Room Number", "Maintenance Type", "Description", "Date", "Reported by", "Reported to", "Status"] #header that is displayed along with the data
        head = False #used to display the header only once
        data_not_solved =  False
        data_solved =  False
        data_in_progress =  False
        if choice == "4":
            break #exits the loop
        try: #file handling
            with open("maintenance.csv", 'r') as maintenance_file: #opens the maintenance file in read mode
                for line in maintenance_file: #loops though the maintenance file
                    maintenance_data = line.strip().split(',') #separates the data in the line with a comma
                    if len(maintenance_data) < 7: #to ensure the file has 6 columns
                        continue
                    status = maintenance_data[6].strip() #index 6 in the maintenance file stores the status
                    if choice == "1" and status == "Not Solved":
                        if not head: #to display the header only once
                            print(",".join(header))
                            print(line)
                            data_not_solved = True
                            head = True
                        else:
                            print(line)
                    elif choice == "2" and status == "Solved":
                        if not head:
                            print(",".join(header))
                            print(line)
                            data_solved = True
                            head = True
                        else:
                            print(line)
                    elif choice == "3" and status == "In Progress":
                        if not head:
                            print(",".join(header))
                            print(line)
                            data_in_progress = True
                            head = True
                        else:
                            print(line)

                if not data_not_solved and choice == "1":
                    print("No maintenance with status 'Not Solved'")
                if not data_solved and choice == "2":
                    print("No maintenance with status 'Solved'")
                if not data_in_progress and choice == "3":
                    print("No maintenance with status 'In Progress'")


        except FileNotFoundError:
            print("File not found")
            break

def update_maintenance_data():
    while True:
        print(f"Select to update \n1.Type \n2.Description \n3.Date \n4.Reported by \n5.Reported to \n6.Status \n7.exit") #displays menu to choose from
        try: #error handling in case wrong data type is input
            selection = int(input("Enter your choice: "))
            if selection == 7:
                break #if selection is 7, break is used to exit the while True

            if selection > 6 or selection < 1: #input validation
                print("Please enter a valid choice(1-6): ")
                continue

            try: #to handle file
                with open("maintenance.csv", 'r') as maintenance: #opening maintenance file in read mode
                    maintenance = maintenance.readlines() #reading the file and putting all the contents in the list maintenance
                    header = maintenance[0] #reads the first line of the list and stores. The first line is the header. It keeps it in variable header so that it does not get overwritten.
                    data = maintenance[1:] #reads after the first line

                while True:
                    room_number = input("Please enter room number to update: ")
                    if not validate_room_id(room_number):  # validation check for room id
                        continue  # restarting the loop if room id is invalid
                    if room_in_file(room_number, data): #checks if room is in the rooms file
                        break #if yes, it exits the loop and continues with the program
                    print("Room not in maintenance")

                for i in range(len(data)): #iteration between columns
                    maintenance_data = data[i].strip().split(",") #seperates each word with a comma
                    current_room = maintenance_data[0].strip() #the index 0 in the maintenance_data is the room number
                    if current_room == room_number: #finds the line where the room input is equal as the room in the file
                        if selection == 1:
                            try: #error handling in case a wrong data type is entered
                                print(f"Choose new maintenance type \n1.Plumbing \n2.Electrical \n3.Furniture \n4.Cleaning \n5Air conditioning \n6.Other") #displays menu
                                select = int(input("Enter your choice: "))
                                if select in range(1, 7): #input validation
                                    match select:
                                        case 1: maintenance_data[1] = "Plumbing" #maintenance_data[1] stores the maintenance type
                                        case 2: maintenance_data[1] = "Electrical"
                                        case 3: maintenance_data[1] = "Furniture"
                                        case 4: maintenance_data[1] = "Cleaning"
                                        case 5: maintenance_data[1] = "Air conditioning"
                                        case 6: maintenance_data[1] = input("Enter type: ")
                                else:
                                    print("Please enter valid choice(1-6): ")

                            except ValueError:
                                print("Please enter valid choice(1-6): ")

                        elif selection == 2:
                            while True: #while true is used in all inputs for validation
                                new_description = input("Enter new description: ")
                                if validate_description(new_description): #calls function that validates description
                                    maintenance_data[2] = new_description #maintenance_data[2] stores the description
                                    break
                                print("Please enter valid description(max 20 characters): ")

                        elif selection == 3:
                            while True:
                                new_date = input("Enter new date(YYYY-MM-DD): ")
                                if validate_date(new_date): #calls function that validates the date
                                    maintenance_data[3] = new_date #maintenance_data[3] stores the date
                                    break
                                print("Please enter valid date(YYYY-MM-DD): ")

                        elif selection == 4:
                            while True:
                                new_reported_by = input("Enter new reported by: ")
                                if validate_name(new_reported_by): #calls the function that validates name
                                    maintenance_data[4] = new_reported_by #maintenance_data[4] stores the name of the person reporting
                                    break
                                print("Please enter a valid name: ")

                        elif selection == 5:
                            while True:
                                new_reported_to = input("Enter new reported to: ")
                                if validate_name(new_reported_to): #calls the function that validates the name
                                    maintenance_data[5] = new_reported_to #maintenance_data[5] stores the name of the person reporting to
                                    break
                                print("Please enter a valid name: ")

                        elif selection == 6:
                            try:
                                print(f"Select new maintenance status:  \n1.Not Solved \n2.Solved \n3.In Progress")
                                choice = int(input("Enter your choice: "))
                                if choice in range(1, 4): #validates input
                                    match choice:
                                        case 1: maintenance_data[6] = "Not Solved"
                                        case 2: maintenance_data[6] = "Solved"
                                        case 3: maintenance_data[6] = "In Progress"


                            except ValueError:
                                print("Please enter valid choice")

                        data[i] = ",".join(maintenance_data) + "\n" #rebuilds the line in a csv format
                        break

                with open("maintenance.csv", 'w') as file:  # updates the file
                    file.writelines([header] + data)
                    print("Maintenance status updated!")
                break

            except FileNotFoundError:
                print("File not found")

        except ValueError:
            print("Incorrect input. Please enter valid input")

def daily_schedule():
 while True:
        try:
            while True:
                today = input("Enter today's date (YYYY-MM-DD)(type exit to go back to main menu): ").strip().lower()  #exit added in case wrong choice is entered
                if today == "exit":
                    return #to exit all loops


                if validate_date(today): #calls function that validates the date
                    try: #file handling
                        with open("rooms.csv", "r") as file: #opens rooms file in read mode
                            rooms = file.readlines()[1:] #reads the file and stores the data in the list rooms
                        with open("guest_bookings.csv", "r") as file: #opens the bookings file in read mode
                            bookings = file.readlines()[1:] #reads the file and stores the data in the list booking

                    except FileNotFoundError:
                        print("File not found")

                    schedule_data = [] #new empty list
                    head = ["Room_ID","Cleaning_Type","Check-in/out Date","Cleaning_Time","Priority\n"]
                    header = ",".join(head)
                    for line in bookings: #goes through bookings fle
                                data = line.strip().split(',') #separates the data by a comma
                                room_number = data[13] #index 2 in guest bookings file stores the room number
                                checkin = data[5] #index 3 in guest bookings file stores the checkin date
                                checkout = data[6] #index 4 in guest bookings file stores the checkout date

                                if checkin == today: #checks if the date input matches the checkin date of the line
                                    print("Check-in found for today:")
                                    print(f"Room Number : {room_number}")
                                    print(f"Check-in   : {checkin}")
                                    while True:
                                        time = input("Enter cleaning time(HH:MM): ").strip().lower() #cleaning time is input
                                        if validate_time(time): #calls the function that validates time
                                            schedule_data.append(f"{room_number},Pre-arrival room check,{checkin},{time},-\n") #adds the line to the list schedule_data
                                            break
                                        else:
                                            print("Please enter valid time(HH:MM): ")

                                #same procedure for checkout as checkin
                                elif checkout == today:
                                    print("Checkout found for today:")
                                    print(f"Room Number : {room_number}")
                                    print(f"Check-out   : {checkout}")
                                    while True:
                                        time = input("Enter cleaning time(HH:MM): ").strip().lower()
                                        if validate_time(time):
                                            schedule_data.append(f"{room_number},Check-out in-depth cleaning,{checkout},{time},-\n")
                                            break
                                        else:
                                            print("Please enter valid time(HH:MM): ")

                    for lines in rooms: #goes through the rooms file
                                    room_data = lines.strip().split(',') #separates the data with a comma
                                    room_number = room_data[0] #index 0 in the rooms file stores the room number
                                    status = room_data[4] #index 4 in the rooms file stores the cleaning status of the room

                                    if status == "Dirty": #if the status is dirty, it needs to be cleaned
                                        print(f"Room Number {room_number} needs to be cleaned")
                                        while True:
                                            timestamp = input("Please enter cleaning time(HH:MM): ").strip().lower() #to input cleaning time
                                            if validate_time(timestamp): #calls the function that validates the cleaning time
                                                schedule_data.append(f"{room_number},Pending cleaning,{today},{timestamp},High\n") #adds the line to the list schedule_data
                                                break
                                            else:
                                                print("Please enter valid time(HH:MM): ")

                                    elif status == "In progress": #if the room cleaning status is in progress, it has a lower priority but is still displayed
                                        schedule_data.append(f"{room_number},Cleaning in progress,{today},-,Medium\n") #adds the line to the list schedule_data

                    print("*" * 10, "Today's Schedule", "*" * 10) #displays the schedule
                    print(header)
                    for line in schedule_data: #goes through the list and displays each line

                        print(line, end="")

                    with open("cleaning_schedule.csv", "w") as schedule_file: #opens the cleaning_schedule file in write mode as ,every day, the whole file is changed to store only the daily schedule
                                schedule_file.writelines(schedule_data)  #overwrites the schedule_data and adds the list

                    with open("schedule_log.csv", "a") as schedule_log: #opens the schedule_log file in append mode, it stores all the cleaning schedule
                                schedule_log.writelines(schedule_data) #adds the list to the file

                else:
                    print("Incorrect Date")
                    print("Please try again.")
                    break

        except ValueError:
            print("Invalid input.Please enter a valid input. ")

def room_in_file(room_number, rooms):
    for line in rooms: #goes through the rooms file
        data = line.split(',') #seperates the data in the line
        if data[0] == str(room_number): #data[0] has the room number
            return True
    return False

def validate_time(time):
    if len(time) != 5:  # Check length
        return False

    if time[2] != ':':  # Check separator
        return False

    hour = time[0:2] #hour starts with index 0 to 1
    minute = time[3:5] #minutes start with index 3 to 4

    if not (hour.isdigit() and minute.isdigit()):  # Check numeric values
        return False

    hour = int(hour)
    minute = int(minute)

    if hour < 0 or hour > 23:  # Validate ranges
        return False
    if minute < 0 or minute > 59:
        return False

    return True

def validate_name(name):
    if 5 < len(name) < 20: #the name needs to be more than 5 characters but less than 20
        return True
    return False

def validate_description(description):
    if 5 < len(description) < 20: #the description needs to be more than 5 characters but less than 20
        return True
    return False

def housekeeping(): #displays the housekeeping main menu
  if housekeeping_login():
    while True:
        print("*"*10 , "Welcome to The Housekeeping Menu", "*"*10)
        print(f"1.Update room cleaning status \n2.Report Maintenance issues \n3.View daily cleaning schedule \n4.Back to main menu \n5.Exit Program") #displays menu
        choice = int(input("Enter your choice: "))  # input choice
        if choice in range (1,6): #input validation
            match choice:
                case 1: update_status()  #calling function update_status() for updating room cleaning status
                case 2: report_maintenance()  #calling function report_maintenance()  to report any maintenance issues
                case 3: daily_schedule()  #calling function daily_schedule() to view and display the daily cleaning schedule
                case 4: main()  #exit back to main menu
                case 5: exit()
        else:
            print("Please enter a valid choice (1-4).")

  else:
        return




# --------------- RECEPTIONIST ----------------
# username --> receptionist
# password --> recep123
def receptionist_login():
    correct_username = "receptionist"
    correct_password = "recep123"
    attempts = 0

    # Allow only 3 login attempts
    while attempts < 3:
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Check if credentials match
        if username == correct_username and password == correct_password:
            print("Login successful.\n")
            return True

        attempts += 1
        print("Wrong username or password. Attempts left:", 3 - attempts)

    # If login fails 3 times
    print("Too many failed attempts. Access denied.\n")
    return False

def receptionist_logout():
    # Simple logout message
    print("Logged out successfully.\n")

def receptionist():
    if not receptionist_login():
        return

    while True:
        print("*" * 10, "Welcome to The Receptionist Menu", "*" * 10)
        print("1. Register Guest")
        print("2. Update Guest Information")
        print("3. Manage bookings")
        print("4. View Room Availability")
        print("5. Logout")
        print("6. Main Menu")
        print("7. Exit Program")

        choice = input("Enter choice: ")

        if choice == "1":
            register_guest()
        elif choice == "2":
            update_guest()
        elif choice == "3":
            manage_bookings()
        elif choice == "4":
            view_room_availability()
        elif choice == "5":
            receptionist_logout()
            break
        elif choice == "6":
            main()
        elif choice == "7":
            exit()
        else:
            print("Invalid choice.\n")

def register_guest():
    field_names, records = load_file(GUEST_FILE)

    booking_id = input("Enter Booking ID (B***): ")
    if not valid_booking_id(booking_id):
        return

    for booking in records:
        if booking["booking_ID"] == booking_id and booking["status"] == "confirmed":

            print("Reservation found. Proceeding with guest registration.\n")

            # Guest details
            while True:
                name = input("Enter Guest Name: ")
                if valid_name(name):
                    booking["name"] = name
                    break

            while True:
                phone = input("Enter Phone Number: ")
                if valid_phone(phone):
                    booking["phone"] = phone
                    break

            while True:
                id_number = input("Enter ID / Passport Number: ")
                if valid_id(id_number):
                    booking["ID_number"] = id_number
                    break

            while True:
                email = input("Enter Email: ")
                if valid_email(email):
                    booking["email"] = email
                    break

            save_file(GUEST_FILE, field_names, records)
            print("Guest registered successfully.\n")
            return

    print("Booking not found, awaiting payment, cancelled, or already checked-in.\n")

def update_guest():
    field_names, guests = load_file(GUEST_FILE)

    # Get valid Guest ID to update
    while True:
        booking_id = input("Enter Booking ID to update: ")
        if valid_booking_id(booking_id):
            break
        else:
            print("Please enter a valid Booking ID(B***).")

    found = False
    # Search for the guest
    for guest in guests:
        if guest["booking_ID"] == booking_id:
            found = True
            # Update name if entered
            while True:
                name = input("Enter new name (leave blank to keep): ")
                if name != "":
                    if valid_name(name):
                        guest["name"] = name
                        break
                    else:
                        print("Name must be less than 20 characters.")
                else:
                    break

            # Update phone if entered
            while True:
                phone = input("Enter new phone (leave blank to keep): ")
                if phone != "":
                    if valid_phone(phone):
                        guest["phone"] = phone
                        break
                    else:
                        print("Phone must be 10 digits.")
                else:
                    break

            while True:
                id_number = input("Enter guest ID number or passport number (leave blank to keep): ")
                if id_number != "":
                    if valid_id(id_number):
                        guest["ID_number"] = id_number
                        break
                    else:
                        print("ID number must be a maximum of 12 digits only.")
                else:
                    break

                while True:
                    email = input("Enter guest email (leave blank to keep): ")
                    if email != "":
                        if valid_email(email):
                            guest["email"] = email
                            break
                        else:
                            print("Invalid email format.")
                    else:
                        break
            break

    if not found:
        print("Booking ID not found.\n")
        return

    save_file(GUEST_FILE, field_names, guests)
    print("Guest updated successfully.\n")

def valid_name(name):
    # Name must not be empty, must be less than 20 characters, letters and spaces only
    if len(name) == 0:
        print("Name cannot be empty.")
        return False

    if len(name) > 20:
        print("Name must be less than 20 characters.")
        return False

    # Check every character is either a letter or a space
    for ch in name:
        if not (ch.isalpha() or ch == " "):
            print("Name must contain only letters and spaces.")
            return False

    return True

def valid_phone(phone):
    # Phone number must be 10 digits
    if len(phone) != 10:
        print("Phone number must be exactly 10 digits.")
        return False
    for ch in phone:
        if ch < '0' or ch > '9':
            print("Phone number must contain only digits.")
            return False
    return True

def valid_id(id_number):
    # id number or passport must be a maximum of 12 digits
    if len(id_number) > 12:
        print("ID number can be a maximum of 12 digits only.")
        return False
    return True

def valid_email(email):
    if '@' not in email and '.' not in email:
        print("Incorrect email format.")
        return False
    return True

def valid_booking_id(booking_id):
    # Booking ID must be 4 characters and start with 'B'
    if len(booking_id) != 4:
        print("Booking ID must be 4 characters (Example: B123).")
        return False
    if booking_id[0] != "B":
        print("Booking ID must start with 'B'.")
        return False
    for i in range(1, 4):
        if booking_id[i] < '0' or booking_id[i] > '9':
            print("Last three characters must be digits.")
            return False
    return True

def valid_check_out_time(check_out_time):
    try:
        parts = check_out_time.split(":")  # split hours and minutes
        if len(parts) != 2:
            return False

        hour = int(parts[0])
        minute = int(parts[1])

        # validate hour and minute range
        if hour < 0 or hour > 23:
            return False
        if minute < 0 or minute > 59:
            return False

        return True
    except ValueError:
        return False

def calculate_time_difference(end_time):
    end_hour, end_minute = end_time.split(":")

    start_total_minutes = int("12") * 60
    end_total_minutes = int(end_hour) * 60 + int(end_minute)

    if end_total_minutes <= start_total_minutes:
        return None  # check out fee is not applicable

    difference = end_total_minutes - start_total_minutes
    hours = difference // 60
    minutes = difference % 60

    return hours, minutes

def valid_date(date):
    # Date must be YYYY-MM-DD
    if len(date) != 10:
        print("Invalid date. Must be YYYY-MM-DD.")
        return False
    if date[4] != "-" or date[7] != "-":
        print("Invalid date. Format must be YYYY-MM-DD")
        return False

    y = date[0:4]
    m = date[5:7]
    d = date[8:10]

    if not y.isdigit() or not m.isdigit() or not d.isdigit():
        print("Invalid date. Year, month, and day must be numbers.")
        return False

    y = int(y)
    m = int(m)
    d = int(d)

    if y < 2024 or y > 2035:
        print("Invalid date. Year must be between 2024 and 2035.")
        return False
    if m < 1 or m > 12:
        print("Invalid date. Month must be 01-12.")
        return False
    if d < 1 or d > 31:
        print("Invalid date. Day must be 01-31.")
        return False

    return True

def manage_bookings():
    while True:
        print("1. Update Booking")
        print("2. Cancel Booking")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            update_booking()
        elif choice == "2":
            cancel_booking()
        elif choice == "3":
            print("Exiting system...")
            return
        else:
            print("Invalid choice.\n")

def update_booking():
    booking_fields, records = load_file(GUEST_FILE)
    room_fields, rooms = load_file(ROOMS_FILE)
    payment_fields, payments = load_file(PAYMENTS_FILE)

    booking_id = input("Enter Booking ID: ")
    if not valid_booking_id(booking_id):
        return

    for booking in records:
        if booking["booking_ID"] == booking_id:
            if booking["status"] in ("confirmed", "checked-in"):
                print(f"\n1. Check-in", f"\n2. Check-out")
                choice = input("Choose option: ")

                #  CHECK-IN
                if choice == "1":
                    if booking["status"]!="checked-in":
                        room_id = allocate_room(booking["room_type"])
                        if room_id is None:
                            print("No available room.")
                            return

                        booking["room_ID"] = room_id
                        booking["status"] = "checked-in"
                        print("Guest successfully checked in.")
                        print("Allocated room ID:", room_id)


                # CHECK-OUT
                elif choice == "2":
                        while True:
                            check_out_time = input("Enter check-out time (HH:MM): ")
                            if valid_check_out_time(check_out_time):
                                break
                        # CALCULATING CHECK-OUT FEE
                        booking["check_out_time"] = check_out_time

                        result = calculate_time_difference(check_out_time)
                        if result is not None:
                            extra_hours, extra_minutes = result
                            late_fee = (extra_hours * 30) + (extra_minutes * 0.5)
                        else:
                            late_fee = 0

                        booking["check_out_fee"] = late_fee
                        # VERIFYING PAYMENT OF CHECK-OUT FEE
                        fee_paid = False
                        for payment in payments:
                            if payment["booking_ID"] == booking_id and payment["description"].lower() == "check-out fee":
                                fee_paid = True
                                break

                        if late_fee > 0 and not fee_paid:
                            print("Booking not eligible for check-out. Check-out fee must be settled.")
                            print(f"Late Check-out fee: RM {late_fee}")
                            return

                        booking["status"] = "checked-out"

                        # Free the room
                        for room in rooms:
                            if room["room_ID"] == booking["room_ID"]:
                                room["room_availability"] = "available"
                                room["cleaning_status"] = "dirty"

                        save_file(ROOMS_FILE, room_fields, rooms)

                        print("Guest successfully checked out.")
                        print("Late check-out fee: RM", late_fee)

                else:
                    print("Invalid choice")
                    return

                save_file(GUEST_FILE, booking_fields, records)
                return

    print("Booking ID not found")
    return

def cancel_booking():
    booking_fields, bookings = load_file(GUEST_FILE)
    room_fields, rooms = load_file(ROOMS_FILE)

    booking_id = input("Enter Booking ID to cancel: ")
    if not valid_booking_id(booking_id):
        return

    for booking in bookings:
        if booking["booking_ID"] == booking_id:

            # Cannot cancel after check-in
            if booking["status"] in ("checked-in", "checked-out"):
                print("Booking cannot be cancelled at this stage.")
                return

            # Free room if already allocated
            if booking.get("room_ID", "") != "":
                for room in rooms:
                    if room["room_ID"] == booking["room_ID"]:
                        room["room_availability"] = "available"
                        room["cleaning_status"] = "dirty"

            booking["status"] = "cancelled"
            booking["room_ID"] = ""

            save_file(GUEST_FILE, booking_fields, bookings)
            save_file(ROOMS_FILE, room_fields, rooms)

            print("Booking successfully cancelled.")
            return

    print("Booking ID not found.")

def allocate_room(room_type):
    room_fields, rooms = load_file(ROOMS_FILE)

    # Find first available room of selected type
    for room in rooms:
        if room["room_type"].lower() == room_type.lower() and room["room_availability"].lower() == "available":
            room["room_availability"] = "occupied"
            save_file(ROOMS_FILE, room_fields, rooms)
            return room["room_ID"]
    return None

def view_room_availability():
    _, rooms = load_file(ROOMS_FILE)
    print("\nAvailable Rooms:")
    found = False
    for room in rooms:
        if room["room_availability"].lower() == "available":
            print("Room:", room["room_ID"], "| Type:", room["room_type"], "| Price:", room["room_price"])
            found = True
    if not found:
        print("No rooms available.\n")



# --------------- GUEST ----------------
def make_reservation():
    print("Please choose a room type: ")
    print(f"1.Single Room - RM100/Night \n2.Single King Room - RM150/Night \n3.Double Room - RM200/Night \n4.King Room - RM220/Night \n5.Queen Room - RM210/Night \n6.Deluxe King Room - RM300/Night \n7.Triple Room - RM280/Night \n8.Quadruple Room - RM350/Night \n9.Family Room - RM400/Night \n10.Family Suites - RM550/Night \n11.Exit")
    while True:
        try:
            room = int(input("Enter choice: "))
            if room not in range(1, 12):
                print("Invalid Choice.Please enter a number between 1 AND 11: ")
            else:
                break
        except ValueError:
            print("Invalid Choice.Please enter a number between 1 AND 11: ")

    room_type = ""
    if room == 11:
        return

    if room == 1: room_type = "single room"
    elif room == 2: room_type = "single king room"
    elif room == 3: room_type = "double room"
    elif room == 4: room_type = "king room"
    elif room == 5: room_type = "queen room"
    elif room == 6: room_type = "deluxe king room"
    elif room == 7: room_type = "triple room"
    elif room == 8: room_type = "quadruple room"
    elif room == 9: room_type = "family room"
    elif room == 10: room_type = "family suites"

    while True:
        checkin_date = input("Enter Check-in date (YYYY-MM-DD): ")
        if validate_date(checkin_date):  # calls function that validates the date
            break
        print("Please enter a valid Check-in date (YYYY-MM-DD): ")

    while True:
        checkout_date = input("Enter Check-out date (YYYY-MM-DD): ")
        if validate_date(checkout_date):  # calls function that validates the date
            break
        print("Please enter a valid Check-out date (YYYY-MM-DD): ")
    booking_id = generate_guest_id()
    status = "awaiting payment"

    price = ""
    checkin_day = int(checkin_date[-2:])
    checkout_day = int(checkout_date[-2:])

    if room == 1: price = 100
    elif room == 2: price = 150
    elif room == 3: price = 200
    elif room == 4: price = 220
    elif room == 5: price = 210
    elif room == 6: price = 300
    elif room == 7: price = 280
    elif room == 8: price = 350
    elif room == 9: price = 400
    elif room == 10: price = 550

    days = (checkout_day - checkin_day) * -1
    amount = abs(days * price)
    try:
        with open('guest_bookings.csv', 'a') as guest_bookings:
            guest_bookings.write(f"{booking_id},,,,,{checkin_date},{checkout_date},,{amount},,{status},{room_type},,,\n")
        print("Reservation Successful.")
        print(f"Booking ID: {booking_id}")
        print(f"Total in RM: {amount}")
    except FileNotFoundError:
        print("File not found")

def special_request():
    while True:
        booking_id = input("Booking ID: ")
        if valid_guest_id(booking_id):
            break
        print("Please enter a valid Booking ID(B***).")

    print("********* Please note that Special requests will be accommodated based on availability. *********")
    while True:
     choice = input("Do you wish to continue?(Y/N): ").lower().strip()
     if choice in ["y","n"]:
         break
     else:
         print("Please enter Y or N.")
    if choice == "n":
        return

    while True:
                print("Please enter your request: ")
                request = input().lower()
                if 0 < len(request) <= 50:
                    break
                else:
                    print("Please enter a valid request(1-50 characters): ")
    try:
                with open('guest_bookings.csv', 'r') as files:
                    my_file = files.readlines()
                    header = my_file[0]
                    text = my_file[1:]
    except FileNotFoundError:
                print("File not found")
                return

    found = False
    for i in range(len(text)):
                data = text[i].strip().split(',')
                if booking_id == data[0]:
                    found = True
                    data[14] = request
                    text[i] = ",".join(data) + "\n"
                    break

    if found:
                with open("guest_bookings.csv", 'w') as file:  # updates the file
                    file.writelines([header] + text)
                    print("Thank you for your request.")

    else:
                print("Booking ID not found.")

def view_payment_history():
    while True:
        booking_id = input("Booking ID: ")
        if valid_guest_id(booking_id):
            break
        print("Please enter a valid Booking ID(B***).")

    try:
        with open('payments.csv', "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        print("File not found.")

    found = False
    for lines in data[1:]:
        line = lines.strip().split(',')
        if booking_id == line[1]:
            found = True
            print(f"*************** Payment history for Booking ID: {line[1]} ***************")
            print("Amount:",line[2])
            print("Date paid:",line[3])
            print("Payment Status:",line[4])
            print(f"Payment Description: {line[5]}")



    if not found:
        print("No payments found.")

def cancel_reservation():
    while True:
        booking_id = input("Booking ID: ")
        if valid_guest_id(booking_id):
            break
        print("Please enter a valid Booking ID(B***).")
    try:
        with open("guest_bookings.csv","r") as my_file:
            file = my_file.readlines()
            header = file[0]
            file_data = file[1:]
    except FileNotFoundError:
        print("File not found.")
        return

    found = False
    for i in range(len(file_data)):
        data = file_data[i].strip().split(',')
        if booking_id == data[0]:
            found = True
            data[10] = "cancelled"
            file_data[i] = ",".join(data) + "\n"
            break

    if found:
        with open("guest_bookings.csv", 'w') as file:  # updates the file
            file.writelines([header] + file_data)
            print("Reservation Cancelled.")
    else:
        print("Booking ID not found.")

def calculate_bill():
    try:
        with open("guest_bookings.csv", "r") as file:
            bookings = file.readlines()[1:]
    except FileNotFoundError:
        print("File not found")

    while True:
        booking_id = input("Please input Booking ID: ")
        if valid_guest_id(booking_id):
            break
        print("Please input a valid Booking ID(B***).")

    found = False
    for booking_line in bookings:
        data = booking_line.strip().split(",")
        if booking_id == data[0]:
            found = True
            print(f"*********** Bill Summary for Booking ID {booking_id} ***********")
            print(f"Booking ID: {booking_id}")
            print(f"Amount: {data[8]}")

    if not found:
        print("Booking ID not found.")

def valid_guest_id(booking_id):
    # Guest ID must be 4 characters and start with 'G'
    if len(booking_id) != 4:
        print("Booking ID must be 4 characters (Example: B123).")
        return False
    if booking_id[0] != "B":
        print("Booking ID must start with 'B'.")
        return False
    for i in range(1, 4):
        if booking_id[i] < '0' or booking_id[i] > '9':
            print("Last three characters must be digits.")
            return False
    return True

def generate_guest_id():
    try:
        with open('guest_bookings.csv', 'r') as guest_bookings:
            guest_bookings = guest_bookings.readlines()
            #Generating a new booking ID in the format G001, G002
            if len(guest_bookings) <= 1: #if bookings is empty, return the first allocated guest ID
                return "B001"

            for line in guest_bookings[1:]:
                if line.strip() == "":
                    continue

                data = line.strip().split(",")
                guest_id = data[0]

                max_id = 0
                if guest_id.startswith("B") and guest_id[1:].isdigit():
                    num = int(guest_id[1:])
                    if num > max_id:
                        max_id = num

            return f"B{max_id + 1:03d}"

    except FileNotFoundError:
        print("File not found")

    #else generates the next booking ID available
    last_id = guest_bookings[-1] #retrieving the last booking records from the list
    number = int(last_id[1:]) + 1 #incrementing the booking ID digits
    return f"G{number:03d}"

def show_available_rooms():
    _, _, rooms = load_rooms()
    print("\nAvailable Rooms:")
    print(f"1.Single Room - RM100/Night \n2.Single King Room - RM150/Night \n3.Double Room - RM200/Night \n4.King Room - RM220/Night \n5.Queen Room - RM210/Night \n6.Deluxe King Room - RM300/Night \n7.Triple Room - RM280/Night \n8.Quadruple Room - RM350/Night \n9.Family Room - RM400/Night \n10.Family Suites - RM550/Night \n11.Exit")
    while True:
        while True:
            try:
                choice = int(input("Enter choice: "))
                if choice not in range(1, 12):
                    print("Invalid Choice.Please enter a number between 1 AND 11: ")
                else:
                    break
            except ValueError:
                print("Invalid Choice.Please enter a number between 1 AND 11: ")

        if choice == 11:
            return

        found = False
        for r in rooms:
            if r["room_availability"].strip().lower() == "available":
                match choice:
                    case 1:
                        if r["room_type"].strip().lower() == "single room":
                            found = True
                    case 2:
                        if r["room_type"].strip().lower() == "single king room":
                            found = True
                    case 3:
                        if r["room_type"].strip().lower() == "double room":
                            found = True
                    case 4:
                        if r["room_type"].strip().lower() == "king room":
                            found = True
                    case 5:
                        if r["room_type"].strip().lower() == "queen room":
                            found = True
                    case 6:
                        if r["room_type"].strip().lower() == "deluxe king room":
                            found = True
                    case 7:
                        if r["room_type"].strip().lower() == "triple room":
                            found = True
                    case 8:
                        if r["room_type"].strip().lower() == "quadruple room":
                            found = True
                    case 9:
                        if r["room_type"].strip().lower() == "family room":
                            found = True
                    case 10:
                        if r["room_type"].strip().lower() == "family suites":
                            found = True

                if found:
                    print("Chosen room type is available.")
                    return

        else:
            print("We are deeply sorry, unfortunately your room type is not available.")
            print("Please choose another type: ")

def read_file(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
        return lines
    except FileNotFoundError:
        return []

def write_file(filename, lines):
    f = open(filename, "w", encoding="utf-8")
    f.writelines(lines)
    f.close()

def parse_csv_line(line):
    return [p.strip() for p in line.strip().split(",")]

def load_rooms():
    lines = read_file("rooms.csv") #this is for making a list of strings
    if len(lines) == 0:
        write_file("rooms.csv", ["room_ID,room_type,room_price,room_availability,cleaning_status\n"])
        lines = read_file("rooms.csv")

    header = parse_csv_line(lines[0])
    data_lines = lines[1:] #is used [1:] to slice the list

    idx_room_id = -1
    idx_type = -1
    idx_price = -1
    idx_avail = -1
    idx_clean = -1

    for i in range(len(header)):
        h = header[i].strip().lower()
        if h == "room_id":
            idx_room_id = i
        elif h == "room_type":
            idx_type = i
        elif h == "room_price":
            idx_price = i
        elif h == "room_availability":
            idx_avail = i
        elif h == "cleaning_status":
            idx_clean = i

    if idx_room_id == -1 or idx_type == -1 or idx_price == -1 or idx_avail == -1:
        return header, data_lines, []

    rooms = []
    for line in data_lines: # This is here to create iteration over the list
        if line.strip() == "":
            continue
        parts = parse_csv_line(line)
        while len(parts) < len(header):
            parts.append("")# The .append is used to modify the list
        rooms.append({ #Here specifically I used a list of dictionaries
            "raw_parts": parts,
            "room_ID": parts[idx_room_id],
            "room_type": parts[idx_type],
            "room_price": parts[idx_price],
            "room_availability": parts[idx_avail],
            "cleaning_status": parts[idx_clean] if idx_clean != -1 else ""
        })

    return header, data_lines, rooms

def guest_menu():
    while True:
        print("*"*10 , "Welcome to The Guest Menu", "*"*10)
        print("1. View Available Rooms")
        print("2. Make a Reservation")
        print("3. Cancel a Reservation")
        print("4. View Your Billing Summary")
        print("5. View Your Payment History")
        print("6. View Hotel Policy")
        print("7. Make Special Request")
        print("8. Main Menu")
        print("9. Exit Program")

        choice = input("\nSelect An Option By Number: ").strip()

        if choice == "1":
            show_available_rooms()
        elif choice == "2":
            make_reservation()
        elif choice == "3":
            cancel_reservation()
        elif choice == "4":
            calculate_bill()
        elif choice == "5":
            view_payment_history()
        elif choice == "6":
            hotel_policy()
        elif choice == "7":
            special_request()
        elif choice == "8":
            main()
        elif choice == "9":
            exit()
        else:
            print("Invalid choice. Please try again.")

def hotel_policy():
    try:
        with open("hotel_policy.txt", "r") as file:
            file = file.readlines()
            for line in file:
                print(line, end="")
    except FileNotFoundError:
        print("File not found")



# --------------- Accountant ----------------
# username --> accountant
# password --> acc123
def update_payment():
    payment_id = generate_payment_id()
    amount = ""
    while True:
        booking_id = input("Booking ID: ")

        if not valid_guest_id(booking_id):
            print("Invalid booking ID. Please try again.")
            continue

        try:
            with open("guest_bookings.csv", "r") as file:
                booking_lines = file.readlines()
        except FileNotFoundError:
            print("guest_bookings.csv not found.")
            return

        amount = 0
        found = False
        for line in booking_lines[1:]:
            row = line.strip().split(',')
            if row[0] == booking_id:
                amount = int(row[8])
                found = True
                break

        if found:
            break
        else:
            print("Booking ID not found. Please try again.")

    payment_data = [""] * 6
    payment_data[0] = payment_id
    payment_data[1] = booking_id

    while True:
        try:
            paid = int(input("Amount (RM): "))
            if paid <= 0:
                print("Amount must be greater than zero.")
            else:
                payment_data[2] = str(paid)
                break
        except ValueError:
            print("Please enter a number.")

    while True:
        date = input("Enter new date (YYYY-MM-DD): ")
        if validate_date(date):
            payment_data[3] = date
            break
        print("Please enter valid date (YYYY-MM-DD).")


    payment_status = "full paid"
    payment_data[5] = "hotel room"

    if paid * 2 == amount:
        payment_status = "half paid"

        try:
            with open("payments.csv", "r") as file:
                payment_lines = file.readlines()
        except FileNotFoundError:
            payment_lines = []

        for line in payment_lines:
            row = line.strip().split(',')
            if row[1] == booking_id and row[4] == "half paid":
                payment_status = "full paid"
                break

    elif paid != amount:
        payment_data[5] = "check-out fee"

    payment_data[4] = payment_status

    # ---------- Update booking status ----------
    for i in range(len(booking_lines)):
        row = booking_lines[i].strip().split(',')
        if row[0] == booking_id:
            if len(row) > 12:
                if payment_status == "half paid":
                    row[10] = "reserved"
                else:
                    row[10] = "confirmed"
                row[12] = payment_status
            booking_lines[i] = ",".join(row) + "\n"
            break

    with open("guest_bookings.csv", "w") as file:
        file.writelines(booking_lines)

    # ---------- Save payment ----------
    with open("payments.csv", "a") as file:
        file.write(",".join(payment_data) + "\n")

    print("Payment Registered.")

def search_payment():
    while True:
        booking_id = input("Booking ID: ").strip()
        if valid_guest_id(booking_id):
            break
        else:
            print("Please enter a valid Booking ID(B***).")

    try:
        with open("payments.csv", "r") as files:
            file = files.readlines()
    except FileNotFoundError:
        print("File not found.")

    header = ["Payment ID","Booking ID","Payment Amount","Payment Date","Payment Status","Payment Description\n"]

    found = False
    for search in file[1:]:
        data_lines = search.strip().split(",")
        if booking_id == data_lines[1]:
                print(",".join(header))
                print(",".join(data_lines))
                found = True


    if not found:
        print("Payment not found.")

def generate_payment_id():
    try:
        with open('payments.csv', 'r') as guest_bookings:
            guest_bookings = guest_bookings.readlines()
            #Generating a new payment ID in the format G001, G002
            if len(guest_bookings) <= 1: #if payment is empty, return the first allocated payment ID
                return "P001"

            for line in guest_bookings[1:]:
                if line.strip() == "":
                    continue

                data = line.strip().split(",")
                guest_id = data[0]

                max_id = 0
                if guest_id.startswith("P") and guest_id[1:].isdigit():
                    num = int(guest_id[1:])
                    if num > max_id:
                        max_id = num

            return f"P{max_id + 1:03d}"

    except FileNotFoundError:
        print("File not found")

    #else generates the next booking ID available
    last_id = guest_bookings[-1] #retrieving the last booking records from the list
    number = int(last_id[1:]) + 1 #incrementing the booking ID digits
    return f"G{number:03d}"

def accountant_login():
    username = "accountant"
    password = "acc123"
    attempts = 0

    while attempts < 3:
        u = input("Username: ").strip()
        p = input("Password: ").strip()

        if u == username and p == password:
            print("Login successful.")
            return True

        attempts += 1
        print("Invalid login. Attempts left:", 3 - attempts)

    print("Access denied.")
    return False

def accountant():
 if accountant_login():
    while True:
        print("*" * 10, "Welcome to The Accountant Menu", "*" * 10)
        print("\n1.Record Payments")
        print("2.Generate Income & Outstanding")
        print("3.Monthly Report")
        print("4.Main Menu")
        print("5.Exit Program")

        c = input("Choice: ").strip()

        if c == "1":
            manage_payments()
        elif c == "2":
            view_income_outstanding()
        elif c == "3":
            generate_monthly_reports()
        elif c == "4":
            main()
        elif c == "5":
            exit()
        else:
            print("Invalid choice.")

def manage_payments():
    while True:
        print("\n--- Record Payments ---")
        print("1. Add Payment")
        print("2. Search Payment")
        print("3. Back")

        c = input("Choice: ").strip()

        if c == "1":
            update_payment()
        elif c == "2":
            search_payment()
        elif c == "3":
            break
        else:
            print("Invalid option.")

def load_file(file_name):
    content=[] #creating a list of dictionaries to store the records of the file

    try:
        with open(file_name, "r", encoding="utf-8") as file:# opening the file in read mode
          lines = file.readlines()  # reading all the line from the file into the line list
          if not lines:  # if file is empty
            return [],[]  # return empty field_names and content
          field_names = lines[0].strip().split(",")  # extracting field_names from header row

          for line in lines[1:]: #looping through the data rows excluding the header
            data=line.strip().split(",")  #extracting data from the relevant row into individual values
            record={} # creating an empty dictionary to store each row of data

            for i in range(len(field_names)):  #looping through each column(fields)
               if i < len(data):
                  record[field_names[i]] = data[i]  # recording the first row data with its respective field name if it has a value
               else:
                  record[field_names[i]] = ""  #filling an empty column with an empty string
            content.append(record)  # appending the dictionary to the content list
          return field_names, content  # returns field_names and list of  record dictionaries

    except FileNotFoundError:
        print(f"{file_name} not found, creating new file")
        if file_name == "rooms.csv":
            field_names = ["room_ID", "room_type", "room_price","room_availability", "cleaning_status"]
        elif file_name == "guest_bookings.csv":
            field_names = ["guest_ID","booking_ID" "name", "phone","ID number","email","check_in_date","check_out_date","check_out_time","status"]
        elif file_name == "payments.csv":
            field_names=["payment_ID","booking_ID","amount","date","status","description"]
        else:
            field_names=[]
        with open(file_name, "w", encoding='utf-8') as file: #creation of files along with field names if they do not exist
            file.write(",".join(field_names)+"\n")
        return field_names, []

def save_file(file_name,field_names,content): #function to save the list back onto the file
    try:
        with open(file_name,"w", encoding='utf-8') as file: #opening the file in write mode, clearing existing contents
          file.write(",".join(field_names) +"\n") #writing the header row and moving to new line
          for row_record in content: #writing each row from the content list of dictionary onto file
              row_values=[] #to create each row values in the correct order based on field_names
              for field in field_names: #iterating through each field column
                  value = row_record.get(field,"")
                  row_values.append(str(value)) # extracting the record based on its field name and appending it to the row_values list and putting empty string it does not exist
              file.write(",".join(row_values) + "\n") #writing the string in the list separated by commas into the file and shifting to a new line after
        return True #successfull saving
    except Exception as e: #error handling
        print(f"{file_name} not found. Cannot save to the file.{e}")
        return False

def validate_date(date):#sub function to validate date
   try:
       parts = date.split("-") #splitting date into year,month,day
       if len(parts) != 3:
           return False
       year=int(parts[0])
       month=int(parts[1])
       day=int(parts[2])
       #validating year range
       if year<1900 or year >3000:
           return False
       #validating month range
       if month<1 or month>12:
           return False
       #validating day range
       if day < 1 or day > 31:
           return False
       return True
   except ValueError: #handles non-numeric data values
       return False

def view_income_outstanding():
    _, bookings=load_file(BOOKING_FILE)

    income = 0.0
    outstanding = 0.0

    for payment in bookings:
        try:
            amount = float(payment["amount"])
        except (ValueError, KeyError):
            continue  # skipping invalid records

        payment_status = payment.get("payment_status", "").lower()

        if payment_status == "full paid": # Full amount received
            income += amount
        elif payment_status == "half paid":# Half received, half outstanding
            income += amount / 2
            outstanding += amount / 2
        else:
            # No payment made yet → full outstanding
            outstanding += amount

    print("\n--- Income & Outstanding Report ---")
    print(f"Total Income Received : RM {income:.2f}")
    print(f"Total Outstanding     : RM {outstanding:.2f}\n")



    print("\n--- Financial Summary ---")
    print(f"Total Income       : RM {income:.2f}")
    print(f"Outstanding Amount : RM {outstanding:.2f}\n")

def generate_monthly_reports():#sub function to generate monthly report
    _, payments = load_file(PAYMENT_FILE)#loading payment contents list from payment file

    if not payments: #checking for records in booking and payment list
        print("No records available")
        return
    date = input("Enter the date(YYYY-MM-DD): ").strip()  # asking user for  the date for the report
    while not validate_date(date): #validating date input
        print("Invalid date format.")
        date = input("Enter the date(YYYY-MM-DD): ").strip()
    year=date[:4] #extacting year from the date input
    month=date[5:7]#extracting month from the date input
    income=0

    for payment in payments: #looping through payment list
        payment_date=payment.get("date","") #extracting the date of payment
        if len(payment_date)>=7 and payment_date[0:4]==year and payment_date[5:7]==month and (payment.get("status","").lower() in ("full paid","half paid")):
            income += float(payment.get("amount",0))
    #displaying monthly report
    print("\n---Monthly Report---")
    print("Income" + "" * 10 + ":"f"{income:.2f}")
    save_report("monthly_" + month + ".csv", [["Month", "Income"], [month, "%.2f" % income]]) #generate a monthly report file

def save_report(name, rows):
    file = open(name, "w", encoding="utf-8")
    for r in rows:
        file.write(",".join(r) + "\n")
    file.close()
    print("Saved:", name)





# --------------- MANAGER ----------------
# username --> manager
# password --> admin123
def manager_login(): #login menu for manager role - asking for username and password
    manager_username="manager"
    manager_password="admin123"
    max_attempts=3
    attempts=0
    while attempts < max_attempts:
        username=input("Please enter your username: ").strip()
        password=input("Please enter your password: ").strip()
        if username == manager_username and password == manager_password:
            print("Login Successful.\n")
            return True
        else:
            attempts += 1
            print(f"Wrong username or password. Attempts left:{max_attempts-attempts}")

    print("Too many failed login attempts. Access denied")
    return False

def manager_logout():
    print("Logged out successfully.\n")

def manager():
    if manager_login():
        while True: #loop will iterate as long as the user does not enter the choice displayed in menu
            print("*"*10 , "Welcome to The Manager Menu", "*"*10)
            print(f"1.Manage Rooms Records", f"\n2.View System Summary", f"\n3.Generate Reports",
                  f"\n4.Back to main menu", f"\n5.Exit")
            #asking user for choice of input
            choice = input("Enter your choice: ")
            match choice:
                case "1":
                    manage_rooms()
                case "2":
                    view_summary()
                case "3":
                    generate_reports()
                case "4":
                    manager_logout()
                    main()
                case "5":
                    exit()
                case _:
                    print("Invalid choice. Please choose between 1 and 5")
    # back to main menu if login fails
    else:
        return

def manage_rooms(): #sub-menu for managing rooms
    field_names,content=load_file(ROOMS_FILE) #loading field_names and contents lists
    while True:
       print("\n---Manage Rooms---")
       print(f"1.Add Room",f"\n2.Update Room",f"\n3.Remove Room",f"\n4.Back")
       choice = input("Enter your choice: ")
       match choice:
           case "1":
               add_room(field_names,content)
           case "2":
               update_room(field_names,content)
           case "3":
               remove_room(field_names,content)
           case "4":
               save_file(ROOMS_FILE, field_names, content)
               break
           case _:print("Invalid choice. Please choose between 1 and 4")

def add_room(field_names,content):# sub function for adding rooms
    while True: #continuously prompt user to enter valid room id until user choose to exit
      room_id = input("Enter Room ID: ").strip() #taking room_id as input and removing any blank spaces
      if not validate_room_id(room_id): #validation check for room id
          continue #restarting the loop if room id is invalid
      if room_id_exists(room_id,content): #checking if room_id already exists in records
          print("Room ID already exists.")
          answer=input(f"Do you want to add another Room ID? (Yes/No) :").strip().lower() #asking user if they want to try another room id
          if answer == "no":
              return #exit the function
          else:
              continue #restarting the loop to add room

      room_type=select_room_type() #allowing user to select room type from the predefined set
      room_price = get_room_price(room_type)#automatically set room price based on room type
      new_room={} #creating an empty dictionary to store new_room details
      for field in field_names: #looping through the field names in the rooms file
          new_room[field]="" #assigning empty spaces to all the fields first
     #creating new room record
      new_room["room_ID"]=room_id
      new_room["room_type"]=room_type
      new_room["room_price"]=room_price
      new_room["room_availability"]="available"
      new_room["clean"]="clean"
      content.append(new_room)#adding the new room record to the content list for
      print("Room successfully added")
      break #exiting the room after successful addition

def validate_room_id(room_id):# sub function for room_id validation
       if len(room_id)!= 4: #ensuring length of room id is 4 digits
           print("Room ID is invalid. Please enter a 4 digit Room ID- 2 digits for floor number and 2 digits for room number")
           return False
       for character in room_id: #looping through each character in room id
          if not character.isdigit(): #checking if each character is a digit
             print("Room ID  must contain only digits")
             return False
       return True #valid room id

def room_id_exists(room_id,content): #sub function for checking duplicate room_id when inputting
    for room in content:#looping through each room record in the content list
        if room["room_ID"] == room_id:
            return True # duplicate room ID
    return False

def select_room_type():#sub function for selecting room types from the given set
    room_type_list = ["Single Room", "Single King Room", "Double Room", "King Room", "Queen Room",
                      "Deluxe King Room", "Triple Room", "Quadruple Room", "Family Room", "Family Suites"]
    print("\nAvailable Room Types:")
    for room_type in room_type_list:
        print(f"{room_type}",end=", ") #printing each room type while looping through the list
    while True: #continuously prompt until valid room type is entered
        choice = input(f"\nSelect your room type: ").strip() #removing extra spaces from the input
        for room_type in room_type_list:
            if choice.lower() == room_type.lower(): #comparing user input against available room types
                return room_type
        print("Invalid room type. Please try again from the available room types")#prompting user to enter valid room type if invalid

def get_room_price(room_type):#sub function to retrieve room price based on selected room type
    #dictionary that maps room types to their fixed prices
    room_price_options={"single room":100,"single king room":150,"double room":200,"king room":220,"queen room":210,"deluxe king room":300,"triple room":280,"quadruple room":350,"family room":400,"family suites":550}
    return room_price_options.get(room_type.lower()) #returning corresponding price after converting room type to lower case

def update_room(field_names,content): #sub function for updating room
    if not content:#checking for empty room records list
        print("No room records available")
        return #back to menu
    while True: #looping until correct room id is entered or user no longer wants to update room
       room_id = input("Enter Room ID to update: ").strip()
       if not validate_room_id(room_id):  # validating format of room id
           continue

       for room in content:  # looping through room records to search for the room_id to be updated
           if room["room_ID"] == room_id:
               print("\nCurrent Room Details")  # displaying current details of the desired room id found
               for field in field_names:  # looping through each fields to displaying room information
                   print(f"{field}: {room.get(field, "")}")

               choice = input("Do you want to update this Room type? (Yes/No): ").lower().strip()
               if choice == "yes":
                   new_room_type = select_room_type()
                   room["room_type"] = new_room_type
                   new_room_price = get_room_price(new_room_type)
                   room["room_price"] = new_room_price
                   print("Room Details updated successfully") #confirming successful update
               answer=input(f"Do you want to update another Room? (Yes/No): ").strip().lower() #asking if the user will update another room
               if answer == "yes":
                   break #start update functon again
               return #exiting function after update is completed
       else: #executes if room id is not found
           print("Room ID not found")
           answer = input(f"Do you want to update another Room? (Yes/No): ").strip().lower()
           if answer == "no":
               return #exiting the update function if user chooses not to continue

def remove_room(field_names,content):#sub function for removing room
    while True: #looping until a valid room_id is entered to be removed or user chooses not to continue
        if not content:  # checking for empty content list
            print("No room records available")
            return #exit as room cannot be removed without records

        room_id = input("Enter Room ID to remove: ").strip()
        if not validate_room_id(room_id):  # room id validation check
            continue #start over again if invalid
        for i in range(len(content)):  # looping to search for the respective room_id to be removed using index value
            if content[i]["room_ID"] == room_id: #checking for matching room id
                print("\nRoom Details") #displaying the details of selected room
                for field in field_names: #llooping through each field to display the records of the selected room
                    print(f"{field}: {content[i].get(field, "")}")
                confirm = input("Confirm deletion? (Yes/No): ").lower().strip()  # confirming deletion prompt
                if confirm == "yes":
                    content.pop(i)  # removing the room record from the content list
                    print("Room removed successfully")
                else:
                    print("Room removal cancelled")
                return

        print("Room ID not found") #displayed if room id is not found
        answer = input(f"Do you want to remove another Room? (Yes/No): ").strip().lower() #asking user if they want to remove another room
        if answer == "no":
            return #exiting function if user chooses not to continue

def view_summary():# sub function for view_summary
    #loading the csv files to be used into their respective list
    _,rooms_content=load_file(ROOMS_FILE)
    _,booking_content=load_file(BOOKING_FILE)
    _,payment_content=load_file(PAYMENT_FILE)


    print("\n--- System Summary ---") #displaying relevant summary details
    print("Total Bookings:", calculate_total_booking(booking_content))
    print(f"Occupancy Rate: {calculate_occupancy_rate(rooms_content):.2f}%")
    print(f"Total Income: RM {calculate_total_income(payment_content):.2f}")

def calculate_total_booking(content):#sub function for calculating bookings
    total_bookings = 0 #initialising total bookings counter to 0
    for booking in content: #looping through each booking record
        if booking.get("booking_ID", "") != "":
            total_bookings += 1 #incrementing the counter if booking id exists
    return total_bookings

def calculate_occupancy_rate(content):#sub function for calculating occupancy rate
    total_rooms=len(content) #total number of rooms in system
    if total_rooms == 0: #if records is empty
        #prevent division by zero error later on
        return 0
    occupied_rooms = 0 #counter for occupied rooms
    for room in content: #looping through each room record to see which room is occupied
        if room.get("room_availability", "").lower() == "occupied":
            occupied_rooms += 1 #incrementing counter
    occupancy_rate = (occupied_rooms / total_rooms)*100 #calculation of occupancy rate as a percentage
    return occupancy_rate

def calculate_total_income(content):#sub function for calculating total income
    total_income=0 #initialising totalling variable to 0
    for payment in content: #looping through each payment record to extract payment amount
        amount = payment.get("amount","").strip()
        if amount!= "": #only increase total_income when amount is not empty
            total_income += float(amount)
    return total_income

def generate_reports(): #function for generate_reports()
    while True: #keeping the reports menu active until user chooses to go back
        print("\n--- Reports Menu ---")
        print(f"1. Daily Report", f"\n2. Monthly Report",f"\n3. Back")
        choice = input("Enter your choice: ")
        match choice:
         case "1":
            generate_daily_report()
         case "2":
            generate_monthly_report()
         case "3":
            break
         case _:
            print("Invalid option.")

def generate_daily_report():#sub function to generate daily reports
    #loading the csv files into the respective list
    _,bookings = load_file(BOOKING_FILE)
    _,payments = load_file(PAYMENT_FILE)
    if not bookings: #checkingg if bookings content list is not empty
        print("No booking records available")
        return

    date = input("Enter the date(YYYY-MM-DD): ").strip()  # prompting user for the date of the report to be generated
    while not validate_date(date): #validating date entered
        print("Invalid date format.")
        date = input("Enter the date(YYYY-MM-DD): ").strip()
    check_ins=0
    check_outs=0
    income=0
    for booking in bookings: #looping through booking list to count daily check-ins and check-outs
        if not booking.get("status", "")== "cancelled":
            if booking.get("check_in_date", "") == date:
                check_ins += 1
            if booking.get("check_out_date", "") == date:
                check_outs += 1


    for payment in payments: #looping through payment list to obtain income
        status = payment.get("status","").lower()
        if payment.get("date", "")== date and status in ("half paid","full paid"):
            income += float(payment.get("amount",0)) #adding up to income the value extracted
    #displaying daily report
    print("\n---Daily Report---")
    if check_ins ==0 and check_outs ==0 and income==0:
        print("No booking records available for this date.")
        return
    print("Date"+ ""*10 +":",date)
    print("Check-ins"+ ""*10 +":",check_ins)
    print("Check-outs"+ ""*10 +":",check_outs)
    print("Income"+ ""*10 +":"f"{income:.2f}")

    save_daily_report(date,check_ins,check_outs,income) #generating a daily report file

def save_daily_report(date,check_ins,check_outs,income):#sub function to generate daily report file
    daily_report = f"daily_report_{date}.txt" #creating the name of text file to be generated
    try:
        with open(daily_report,"w",encoding="utf-8") as file: #writing to the daily report file
            file.write("---Daily Report---")
            file.write(f"\nDate: {date}")
            file.write(f"\nCheckins: {check_ins}"+f"\nCheckouts: {check_outs}"+f"\nIncome:RM {income}")
        print(f"Daily report saved to {daily_report}")
    except Exception as e: #handling file writing errors
        print("Error saving daily report:",e)

def generate_monthly_report():#sub function to generate monthly report
    _, bookings = load_file(BOOKING_FILE) #loading booking contents list from booking file
    _, payments = load_file(PAYMENT_FILE)#loading payment contents list from payment file
    if not bookings:
        print("No booking records available for this month")
        return
    if not payments:
        print("No payment records available for this month")
        return
    date = input("Enter the date(YYYY-MM-DD): ").strip()  # asking user for  the date for the report
    while not validate_date(date): #validating date input
        print("Invalid date format.")
        date = input("Enter the date(YYYY-MM-DD): ").strip()
    year=date[:4] #extacting year from the date input
    month=date[5:7]#extracting month from the date input
    #initialising counters
    check_outs=0
    income=0
    for booking in bookings: #counting monthly check-outs from booking
        if not booking.get("status", "") == "cancelled":
            checkout_date = booking.get("check_out_date", "")
            if len(checkout_date) >= 7:  # checking length of date
                if checkout_date[0:4] == year and checkout_date[5:7] == month:  # checking the string character and splitting year and month
                    check_outs += 1


    for payment in payments: #looping through payment list
        payment_date=payment.get("date","") #extracting the date of payment
        if len(payment_date)>=7 and payment_date[0:4]==year and payment_date[5:7]==month and (payment.get("status","").lower() in ("full paid","half paid")):
            income += float(payment.get("amount",0))
    #displaying monthly report
    print("\n---Monthly Report---")
    print("Month/Year" + "" * 10 + ":", month,"/", year)
    print("Check-outs" + "" * 10 + ":", check_outs)
    print("Income" + "" * 10 + ":"f"{income:.2f}")
    save_monthly_report(year,month,check_outs,income) #generate a monthly report file

def save_monthly_report(year,month,check_outs,income):#sub function for generating monthly report file
    monthly_report = f"monthly_report_{year}-{month}.txt" #creating the name of the monthly report file
    try:
        with open(monthly_report,"w",encoding="utf-8") as file: #writing to the monthly report file
            file.write("---Monthly Report---")
            file.write(f"\nYear/Month: {year}"+"/"+f"{month}")
            file.write(f"\nCheck-outs:{check_outs}"+f"\nIncome:RM{income:.2f}")
        print(f"Monthly report saved to {monthly_report}")
    except Exception as e: #handling file writing errors
      print("Error saving monthly report:",e)



# --------------- MAIN ----------------
def main():
    print("*"*10 , "Welcome to StayEase Hotel Management System", "*"*10)
    print("Please Choose A Role: ")
    while True:
        try:
            choice = int(input(f"1.Guest \n2.Manager \n3.Receptionist \n4.Accountant \n5.Housekeeping \n6.Exit \nChoose: "))
            if choice in range(1,7):
                break
            else:
                print("Please enter a valid choice(1-6).")
        except ValueError:
            print("Please enter a valid choice(1-6).")

    match choice:
        case 1: guest_menu()
        case 2: manager()
        case 3: receptionist()
        case 4: accountant()
        case 5: housekeeping()
        case 6: exit()
main()




