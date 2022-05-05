from schedule import *
from task import *


class User:
 def __init__(self, user_name, id):
   self.name = user_name
   self.id = id
   self.schedule = Schedule()

 def create_task(self, task):
     self.schedule.create_task(task)
 
 def edit_task(self, taskName, **kwargs):
     self.schedule.edit_task(taskName, **kwargs)

 def delete_task(self, name):
     self.schedule.delete_task(name)
 
 def find_task(self, name):
     self.schedule.find_task(name)
   
   
 
#  def write_schedule(self, filename):
#    with open(filename, 'w') as f:
#      for task in self.tasks:
#        f.write(task.name + ',' + str(task.due_date) + ',' + str(task.priority) + '\n')
 
#  def read_schedule(self, filename):
#    with open(filename, 'r') as f:
#      for line in f:
#        name, due_date, priority = line.split(',')
#        task = Task(name, datetime.datetime.strptime(due_date, '%Y-%m-%d'), int(priority))
#        self.tasks.append(task)
 
#  def view_schedule_day(self, day):
#    for task in self.tasks:
#      if task.due_date.day == day:
#        print(task.name)
#        print(task.due_date)
#        print(task.priority)
 
#  def view_schedule_week(self, week):
#    for task in self.tasks:
#      if task.due_date.isocalendar()[1] == week:
#        print(task.name)
#        print(task.due_date)
#        print(task.priority)
 
#  def view_schedule_month(self, month):
#    for task in self.tasks:
#      if task.due_date.month == month:
#        print(task.name)
#        print(task.due_date)
#        print(task.priority)

