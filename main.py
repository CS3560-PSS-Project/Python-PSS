# import datetime
from turtle import clear
from user import *
from task import *

def main():
    user1 = User("Tom", 1)

    task1 = RecurringTask("task1", "study", "20220528", 12.0, 1.25, "20220801", "daily")
    # task1.display()
    task2 = TransientTask("task2", "visit", "20220801", 11.25, 0.45)
    # task2.display()
    task3 = AntiTask("task3", "cancellation", "20220701", 12.0, 1.25)
    # task3.display()
    task4 = TransientTask("task4", "visit", "20220511", 13.25, 1)
    task5 = RecurringTask("task5", "study", "20220301", 12, 1.25, "20220430", "daily")
    task6 = AntiTask("task6", "cancellation", "20220421", 12, 1.25)
    task7 = TransientTask("task7", "visit", "20220421", 11.33, 1)
    task8 = AntiTask("task8", "cancellation", "20220801", 12, 1.25)
    task9 = AntiTask("task9", "cancellation", "20220725", 12, 1.25)

    user1.create_task(task1)
    user1.create_task(task2)
    user1.create_task(task3)
    user1.create_task(task4)
    user1.create_task(task5)
    user1.create_task(task6)
    user1.create_task(task7)
    user1.create_task(task8)
    user1.create_task(task9)

    user1.delete_task("task5")
    user1.schedule.printSchedule()
   
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

