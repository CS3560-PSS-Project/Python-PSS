# import datetime
from turtle import clear
from user import *
from task import *

def main():
    user1 = User("Tom", 1)
    
    while True:
        print("----------Menu----------")
        print("1. Create a task")
        print("2. Delete a task")
        print("3. Print the schedule")
        print("4. Write schedule to a file. ")
        print("5. Exit")
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
            print("Program exit!")
            exit()

        else:
            print("Wrong Option. Please try again!")

    
   
    # user1.find_task("task2")
    # user1.edit_task(task2, name="newTask2")
    # user1.create_task(task1)
    # user1.edit_task()
    # user1.schedule.printSchedule()



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
