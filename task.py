from datetime import datetime
from datetime import timedelta
import re

class Task:
 def __init__(self,name, type, start_date, start_time, duration):
   self.name = name
   self.type = type
   if(re.match("^[0-9]{8}$", start_date)): # we can hide error handeling process inside a function
       year = start_date[0:4]
       month = start_date[4:6]
       day = start_date[6:8]
       if int(month) < 1:
           month = "01"
       if int(month) > 12:
           month = "12"
       if int(day) < 1:
           day = "01"
       if int(month) ==2 and  int(day) > 28:
           day = "28"
       if int(month) in [4,6,9,11] and int(day) > 30:
           day = "30"
       if int(month) in [1,3,5,7,8,10,12] and int(day) > 31:
           day = "31"
       self.start_date = year+month+day
   else:
       self.start_date = "20220101"
   # Round user’s given task start time to the nearest 15 min (0.25)
   # make sure that the start time is in between 0 to 23.75
   if start_time > 0: # we can hide error handeling process inside a function
        min = round(start_time - int(start_time), 2) 
        hour = int(start_time)                       
        if min > .0 and min <= .25:
            min = 15
        elif min > .25 and min <=.50:
            min = 30
        elif min > .50 and min <= .75:
            min = 45
        else:
            if min != 0:
                    min = 0 
                    hour +=1
        if hour < 0:
            hour = 0
        if hour > 23:
            hour = 23
        self.start_time = "%d:%d" % (hour, min)
   else:
       start_time = "10:00"
   # DateTime object is used to sort or insert a task into the schedule
   self.date_time_obj = datetime.strptime(self.start_date + self.start_time, '%Y%m%d%H:%M') 
   # Make sure duration of the task is a positive number from 0.25 to 23.75
   if duration > 0  and duration <= 23.75:
        self.duration = duration * 60
   elif duration <= 0:
        self.duration = 15
   else:
        self.duration = 23.75 * 60
   # Duration object is used to compare tasks inside schedule
   self.duration_obj = timedelta(minutes=self.duration)
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
