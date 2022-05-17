from user import *
from task import *
import enum

def main():
    class TaskEnum(enum.Enum):
        Class = 1
        Study = 2
        Sleep = 3
        Exercise = 4
        Work = 5
        Meal = 6
        Visit = 7 
        Shopping = 8
        Appointment = 9
        Cancellation = 10

    user1 = User("Tom", 1)
    user1.read_schedule("Schedule.json")

    while True:
        print("----------Menu----------")
        print("1. Create a task")
        print("2. Delete a task")
        print("3. Edit a task")
        print("4. Find a task")
        print("5. Write schedule to a file.")
        print("6. Read schedule from a file.")
        print("7. View schedule for a Day, a Week, or a Month")
        print("8. Write schedule for a Day, a Week, or a Month")
        print("9. Print Schedule")
        print("10. Exit")
        option = input("Enter your option: ")
        if option == '1':
            print("please select a task.\n")
            print("1)Class \t7)Visit \t10)Cancellation")
            print("2)Study \t8)Shopping")
            print("3)Sleep \t9)Appointment")
            print("4)Excercise\n5)Work\n6)Meal")
            taskOption = int(input("Enter your option: "))
            try:
                if taskOption in [1, 2, 3, 4, 5, 6]:
                    taskNameCreate = input("Enter task name you want to create: ")
                    taskStartDate = int(input("Enter task start date with the format YYYYMMDD: "))
                    taskStartTime = float(input("Enter task start time with the format HH.MM: "))
                    taskDuration = float(input("Enter task duration with the format HH.MM: "))
                    taskEndDate = int(input("Enter task end date with the format YYYYMMDD: "))
                    taskFrequency = int(input("Enter task frequency, 1 for daily task and 7 for weekly task: "))
                    user1.create_task(RecurringTask(taskNameCreate, TaskEnum(taskOption).name, taskStartDate, taskStartTime,\
                        taskDuration, taskEndDate, taskFrequency))

                elif taskOption == 10:
                    taskNameCreate = input("Enter task name you want to create: ")
                    taskStartDate = int(input("Enter task start date with the format YYYYMMDD: "))
                    taskStartTime = float(input("Enter task start time with the format HH.MM: "))
                    taskDuration = float(input("Enter task duration with the format HH.MM: "))
                    user1.create_task(AntiTask(taskNameCreate, TaskEnum(taskOption).name, taskStartDate, taskStartTime, taskDuration))   
                            
                else:
                    taskNameCreate = input("Enter task name you want to create: ")
                    taskStartDate = int(input("Enter task start date with the format YYYYMMDD: "))
                    taskStartTime = float(input("Enter task start time with the format HH.MM: "))
                    taskDuration = float(input("Enter task duration with the format HH.MM: "))  
                    user1.create_task(TransientTask(taskNameCreate, TaskEnum(taskOption).name, taskStartDate, taskStartTime, taskDuration)) 
            except:
                print("Something went wrong, try again!\n")
          
        elif option == '2':
            taskNameDelete = input("Enter task name you want to delete: ")
            user1.delete_task(taskNameDelete)

        elif option == '3':
            try:
                taskNameedited = input("Enter task name you want to edit: ")
                newName= input("Enter a new task name.(enter to skip): ")
                newStartDate= input("Enter a new start date with the format YYYYMMDD.(enter to skip): ")
                newStartDate= "" if newStartDate=="" else int(newStartDate)
                newStartTime= input("Enter a new Start Time with the format HH.MM.(enter to skip): ")
                newStartTime="" if newStartTime=="" else float(newStartTime)
                newDuration= input("Enter a new duration with the format HH.MM.(enter to skip): ")
                newDuration="" if newDuration=="" else float(newDuration)
                newDueDate= input("Enter a new due date with the format YYYYMMDD.(enter to skip): ")
                newDueDate= "" if newDueDate=="" else int(newDueDate)
                newFreq= input("Enter a new frequency, 1 for daily task and 7 for weekly task.(enter to skip): ")
                newFreq= "" if newFreq=="" else int(newFreq)

                user1.schedule.edit_task(taskNameedited, name=newName, start_date=newStartDate,start_time=newStartTime,\
                    duration=newDuration,end_date=newDueDate,frequency=newFreq)
            except:
                print("Something went wrong, try again!\n")

        elif option == '4':
            fileNameRead = input("Enter a task name you want to find: \n")
            user1.find_task(fileNameRead)
            print()

        elif option == '5':
            user1.write_schedule("../Python-PSS/Schedule.json")
            print("Write a schedule complete\n")

        elif option == '6':
            try:
                fileNameRead = input("Enter a file name you want to read: ")
                user1.read_schedule(fileNameRead)
            except:
                print("Something went wrong, try again!\n") 

        elif option == '7':
            try:
                startDate = input("Enter a start date with the format YYYYMMDD: ")
                numOfDays = input("Enter 1 for a day, 7 for a week and 28 to 31 for a month: ")
                user1.schedule.viewSchedule(startDate, numOfDays)
            except:
                print("Something went wrong, try again!\n")       

        elif option == '8':  
            try:
                startDate = input("Enter a start date with the format YYYYMMDD: ")
                numOfDays = input("Enter 1 for a day, 7 for a week and 28 to 31 for a month: ")
                fileName = input("Enter a file name: ")           
                user1.schedule.writeSchedule(startDate, numOfDays, fileName)       
            except:
                print("Something went wrong, try again!\n") 

        elif option == '9':
            user1.schedule.printSchedule()
            
        elif option == '10':
            print("Program exit!")
            exit()
        else:
            print("Wrong Option. Please try again!")
   
if __name__ == "__main__":
    main()



# class Task:
#  def __init__(self, name, due_date, priority):
#    self.name = name
#    self.due_date = due_date
#    self.priority = priority

# class Schedule:
#  def __init__(self):
#    self.tasks = []
 

 
# schedule = Schedule()
# schedule.create_task('Homework', datetime.datetime(2019, 11, 5), 1)
# schedule.create_task('Shopping', datetime.datetime(2019, 11, 5), 2)
# schedule.create_task('Laundry', datetime.datetime(2019, 11, 6), 3)
# schedule.view_task('Homework')
# schedule.delete_task('Shopping')
# schedule.edit_task('Laundry', 'Dishes', datetime.datetime(2019, 11, 7), 1)
# schedule.write_schedule('schedule.txt')
# schedule.read_schedule('schedule.txt')
# schedule.view_schedule_day(5)
# schedule.view_schedule_week(45)
# schedule.view_schedule_month(11)


    # task1 = RecurringTask("task1", "study", 20220501, 11.10, .45, 20220801, 1)
    # task2 = TransientTask("task2", "visit", 20220603, 9.00, 1.39)
    # task3 = AntiTask("task3", "cancellation", 20220603, 12, 1)     
    # task4 = TransientTask("task4", "visit", 20220701, 11.50, 1)
    # task5 = RecurringTask("task5", "study", 20220301, 18, 1, 20220630, 1) #1 for daily
    # task6 = AntiTask("task6", "cancellation", 20220701, 12, 1)
    # task7 = TransientTask("task7", "visit", 20220603, 9.10, 1.25)
    # task8 = TransientTask("task8", "visit", 20230603, 19.10, 0.25)
    # user1.create_task(task2)
    # user1.create_task(task1)
    # user1.create_task(task6)
    # user1.create_task(task3)
    # user1.create_task(task4)
    # user1.create_task(task5)
    # user1.create_task(task7)
    # user1.create_task(task8)
    # user1.schedule.printSchedule()
    # user1.write_schedule("Schedule.json")
    # user1.read_schedule("Schedule.json")
    #user1.schedule.edit_task("task6", name='task666', duration=2.35) #start_time=9.75, duration=0.35, end_date="20220710" , name='task111'start_time=9.75
    #user1.schedule.edit_task("new task 3", start_date='20220809')
    #user1.schedule.printSchedule()
    # user1.schedule.viewSchedule("20220303", "7") #1 for the same day, 7 for a week ....
    # user1.schedule.writeSchedule("20220503", "30", "oneMonth.json")