from datetime import datetime
from datetime import timedelta
import re

class Task:
 def __init__(self,name, type, start_date, start_time, duration):
   self.name = name
   self.type = type
   self.start_date = self.getValidDate(start_date)
   # Round user’s given task start time to the nearest 15 min (0.25)
   # make sure that the start time is in between 0 to 23.75
   self.start_time = self.getValidTime(start_time)
   # DateTime object is used to sort or insert a task into the schedule
   self.date_time_obj = datetime.strptime(self.start_date + self.toStrTime(self.start_time), '%Y%m%d%H.%M') 
   # Make sure duration of the task is a positive number from 0.25 to 23.75
   self.duration = self.getValidDuration(duration)
   # Duration object is used to compare tasks inside schedule
   self.duration_obj = timedelta(minutes=int(self.duration*60))

 def getValidDate(self, start_date):
    if(re.match("^[0-9]{8}$", start_date)): 
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
        return year+month+day
    else:
        return  "20230101"
 def getValidTime(self, start_time):
    if start_time > 0: 
        min = round(start_time - int(start_time), 2) 
        hour = int(start_time)
        if min == 0:
            min == 0.0                       
        elif min > 0 and min <= .25:
            min = .25
        elif min > .25 and min <=.50:
            min = .50
        elif min > .50 and min <= .75:
            min = .75
        elif min > .75:
            min = 0.0 
            hour +=1
        if hour < 0 or hour > 23:
            hour = 0.0
        return min + hour  # "%.2d:%.2d" % (hour, min)
    else:
        return 10.0
 def toStrTime(self, time):
    min = round(time - int(time), 2) 
    hour = int(time) 
    if min == .25:
        min = .15
    elif min == .50:
        min = .3
        return str(hour + min) + "0"
    elif min == .75:
        min = .45
    else:
        min = 0.0
    return str(hour + min)
 def getValidDuration(self, duration):
    if duration > 0  and duration <= 23.75:
        min = round(duration - int(duration), 2)
        hour = int(duration)
        if min == 0:
            min = 0.0
        elif min > 0 and min <= .25:
            min = .25
        elif min > 0.25 and min <= 0.5:
            min = 0.5
        elif min > 0.5 and min <= 0.75:
            min = 0.75
        elif min > 0.75:
            min = 0.0
            hour+=1
        return min + hour # int((min + hour)* 60)
    elif duration <= 0:
        return .25
    else:
        return 24

 def setDate(self, start_date):
     self.start_date = self.getValidDate(start_date)
     self.date_time_obj = datetime.strptime(self.start_date + self.toStrTime(self.start_time), '%Y%m%d%H.%M') 
 def setTime(self, start_time):
     self.start_time = self.getValidTime(start_time)
     self.date_time_obj = datetime.strptime(self.start_date + self.toStrTime(self.start_time), '%Y%m%d%H.%M') 
 def setDuration(self, duration):
     self.duration = self.getValidDuration(duration)
     self.duration_obj = timedelta(minutes=int(self.duration*60))
 def display(self):
     print("name: ", self.name, "\ntype: ", self.type, "\nstart date: ", self.start_date,\
          "\nstart time:", self.start_time, "\nduration: ", self.duration)
 def clone(self):
     tempTask = Task(self.name,self.type,self.start_date,self.start_time,self.duration)
     return tempTask
 
class TransientTask(Task):
    def __init__(self, name, type, start_date, start_time, duration):
        super().__init__(name, type, start_date, start_time, duration) 
    def clone(self):
        tempTask = TransientTask(self.name,self.type,self.start_date,self.start_time,self.duration)
        return tempTask   

class RecurringTask(Task):
    def __init__(self, name, type, start_date, start_time, duration, end_date, frequency):
        super().__init__( name, type, start_date, start_time, duration)
        self.end_date = self.getValidDate(end_date)
        self.frequency = frequency
        self.date_time_end_obj = datetime.strptime(self.end_date, '%Y%m%d') 
    def setDueDate(self, end_date):
        self.end_date = self.getValidDate(end_date)
        self.date_time_end_obj = datetime.strptime(self.end_date, '%Y%m%d') 
    def setFrequency(self, freq):
        if freq.lower() == "daily":
            self.frequency = "daily"
        else:
            self.frequency = "weekly"
    def display(self):
        super().display()
        print("end date: ", self.end_date, "\nfrequency: ", self.frequency)
    def clone(self):
        tempTask = RecurringTask(self.name,self.type,self.start_date,self.start_time,self.duration,self.end_date,self.frequency)
        return tempTask 
        
class AntiTask(Task):
    def __init__(self, name, type, start_date, start_time, duration):
        super().__init__( name, type, start_date, start_time, duration)
    def clone(self):
        tempTask = AntiTask(self.name,self.type,self.start_date,self.start_time,self.duration)
        return tempTask 
