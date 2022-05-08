# import datetime
from turtle import clear
from user import *
from task import *

def main():
    user1 = User("Tom", 1)
    # task1 = RecurringTask("task1", "study", "20220528", 12.10, 1.25, "20220801", "daily")
    # task2 = TransientTask("task2", "visit", "20220603", 11, 0.32)
    # task3 = AntiTask("task3", "cancellation", "20220701", 12.10, 1.25)     
    # task4 = TransientTask("task4", "visit", "20220701", 11.50, 1)
    # task5 = RecurringTask("task5", "study", "20220301", 12, 1, "20220430", "daily")
    # task6 = AntiTask("task6", "cancellation", "20220421", 12, 1.25)
    # task7 = TransientTask("task7", "visit", "20220701", 12.10, 1.25)
    # task8 = AntiTask("task8", "cancellation", "20220801", 12, 1.25)
    # task9 = AntiTask("task9", "cancellation", "20220725", 12, 1.25)
    # task10 = AntiTask("task33", "cancellation", "20220603", 12.10, 1.25) 
    # user1.create_task(task1)
    # user1.create_task(task2)
    # user1.create_task(task3)
    # user1.create_task(task4)
    # user1.create_task(task5)
    # user1.create_task(task6)
    # user1.create_task(task7)
    # user1.create_task(task8)
    # user1.create_task(task9)
    # user1.create_task(task10)
    #user1.schedule.edit_task("task1", name='task111', frequency='weekly') #start_time=9.75, duration=0.35, end_date="20220710"
    # user1.schedule.edit_task("new task 3", start_date='20220809')

    # user1.schedule.printSchedule()
    # test = task2.clone()
    #name='task5',start_date='20220801'start_time=12.0  
    # user1.write_schedule("../Python-PSS/Schedule.json")

    while True:
        print("----------Menu----------")
        print("1. Create a task")
        print("2. Delete a task")
        print("3. Print the schedule")
        print("4. Write schedule to a file.")
        print("5. Read schedule to a file.")
        print("6. Exit")
        option = int(input("Enter your option: "))
        if option == 1:
            taskOption = input("Enter 'R' for Recurring Task, 'T' for Transient Task, 'A' for Anti Task: ")            
            if taskOption == 'R' or taskOption == 'r':
                taskNameCreate = input("Enter task name you want to create: ")
                taskType = input("Enter task type: ")
                taskStartDate = input("Enter task start date: ")
                taskStartTime = float(input("Enter task start time: "))
                taskDuration = float(input("Enter task duration: "))
                taskEndDate = input("Enter task end date: ")
                taskFrequency = input("Enter task frequency: ")
                user1.create_task(RecurringTask(taskNameCreate, taskType, taskStartDate, taskStartTime, taskDuration, taskEndDate, taskFrequency))        
            elif taskOption == 'T' or taskOption == 't':
                taskNameCreate = input("Enter task name you want to create: ")
                taskType = input("Enter task type: ")
                taskStartDate = input("Enter task start date: ")
                taskStartTime = float(input("Enter task start time: "))
                taskDuration = float(input("Enter task duration: "))
                user1.create_task(TransientTask(taskNameCreate, taskType, taskStartDate, taskStartTime, taskDuration))        
            elif taskOption == 'A' or taskOption =='a':
                taskNameCreate = input("Enter task name you want to create: ")
                taskType = input("Enter task type: ")
                taskStartDate = input("Enter task start date: ")
                taskStartTime = float(input("Enter task start time: "))
                taskDuration = float(input("Enter task duration: "))
                user1.create_task(AntiTask(taskNameCreate, taskType, taskStartDate, taskStartTime, taskDuration))        
                
        elif option == 2:
            taskNameDelete = input("Enter task name you want to delete: ")
            user1.delete_task(taskNameDelete)

        elif option == 3:
            user1.schedule.printSchedule()

        elif option == 4:
            user1.write_schedule("../Python-PSS/Schedule.json")
            print("Write a schedule complete")
            exit()

        elif option == 5:
            fileNameRead = input("Enter a file name you want to read: ")
            user1.read_schedule(fileNameRead)
            exit()
        elif option == 6:
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
