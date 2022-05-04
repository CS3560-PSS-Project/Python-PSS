from datetime import datetime
from datetime import timedelta
import re

class Task:
 def __init__(self,name, type, start_date, start_time, duration):
   self.name = name
   self.type = type
   if(re.match("^[0-9]{8}$", start_date)):
       try:
        print(x)
       except:
        print("An exception occurred")

   self.start_date = start_date
   # Round user’s given task start time to the nearest 15min (0.25) and make sure that the start time is in between 0 to 23.75
   # if(start_time < 0):
   #    self.start_time = 0
   # elif start_time > 23.75:
   #    self.start_time = 23.75
   self.start_time = start_time
   self.duration = duration
   # Make sure duration of the task is a positive number from 0.25 to 23.75
   self.date_time_obj = datetime.strptime(start_date + start_time, '%Y%m%d%H:%M') 
   #DateTime object might be useful if we needed to sort or insert a task into the schedule
   self.duration_obj = timedelta(minutes=duration)
 def setDate(self, start_date):
     self.date_time_obj = datetime.strptime(start_date + self.start_time, '%Y%m%d%H:%M') 
 def setTime(self, start_time):
     self.date_time_obj = datetime.strptime(self.start_date + start_time, '%Y%m%d%H:%M') 
 def setDuration(self, duration):
     self.duration_obj = timedelta(minutes=duration) 
 def display(self):
     print("name: ", self.name, "\ntype: ", self.type, "\nstart date: ", self.start_date,\
          "\nstart time", self.start_time, "\nduration: ", self.duration)

 
class TransientTask(Task):
    def __init__(self, name, type, start_date, start_time, duration):
        super().__init__(name, type, start_date, start_time, duration)    

class RecurringTask(Task):
    def __init__(self, name, type, start_date, start_time, duration, end_date, frequency):
        super().__init__( name, type, start_date, start_time, duration)
        self.end_date = end_date
        self.frequency = frequency
        self.date_time_end_obj = datetime.strptime(end_date, '%Y%m%d') 
    def setDueDate(self, end_date):
     self.date_time_end_obj = datetime.strptime(end_date, '%Y%m%d') 
    def display(self):
        super().display()
        print("end date: ", self.end_date, "\nfrequency: ", self.frequency)
        

class AntiTask(Task):
    def __init__(self, name, type, start_date, start_time, duration):
        super().__init__( name, type, start_date, start_time, duration)
