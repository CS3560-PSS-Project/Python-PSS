from datetime import datetime
from datetime import timedelta
import re
from tkinter import EXCEPTION

class Task:
 def __init__(self,name, type, start_date, start_time, duration):
   self.name = name
   self.type = type
   try:
    self.start_date = self.getValidDate(start_date)
    # Round user’s given task start time to the nearest 15 min (0.25)
    # make sure that the start time is in between 0 to 23.75
    self.start_time = self.getValidTime(start_time)
    # DateTime object is used to sort or insert a task into the schedule
    self.date_time_obj = datetime.strptime(str(self.start_date) + self.timeToStr(self.start_time), '%Y%m%d%H.%M') 
    # Make sure duration of the task is a positive number from 0.25 to 23.75
    self.duration = self.getValidDuration(duration)
    # Duration object is used to compare tasks inside schedule
    self.duration_obj = timedelta(minutes=self.duration*60)
   except:
       print("Error: Invalid date, time or duration")

 def getValidDate(self, start_date):
    if(re.match("^[0-9]{8}$", str(start_date))): 
        year = str(start_date)[0:4]
        month = str(start_date)[4:6]
        day = str(start_date)[6:8]
        if (int(day) < 1 or int(day) > 31) or\
            (int(month) < 1 or int(month) > 12) or\
                (int(month) == 2 and int(day) > 28) or\
                    (int(month) in [4,6,9,11] and int(day) > 30):
            print("Error: Invalid date!")
            raise Exception("Invalid date")
        else:
            return int(year+month+day)
    else:
        raise Exception("Invalid date")

 def getValidTime(self, start_time):
    tempTime = self.__getNearestTime(start_time)
    if tempTime == 24.0:
        tempTime=0.0     
    elif tempTime > 24.0 or tempTime < 0.0:
        print("Error: Invalid time!")
        raise Exception("Invalid time")
    return tempTime
 

 def getValidDuration(self, duration):
    tempDuration = self.__getNearestTime(duration)
    if duration > 23.75 or duration == 0.0:
        print("Error: Invalid duration!")
        raise Exception("Invalid duration")
    return tempDuration


 def __getNearestTime(self, time):
    if time >= 0:
        min = round(time - int(time), 2) 
        hour = int(time)
        if min >= 0.0 and min <= .12:
            min = 0.0                 
        elif min > .12 and min <= .37:
            min = .25
        elif min > .37 and min <= .62:
            min = .50
        elif min > .62 and min <= .87:
            min = .75
        elif min > .87:
            min = 0.0 
            hour+=1
        return hour+min
    else:
        print("Error: time cannot be a negative number.")
        raise Exception("Invalid time")
        
 def timeToStr(self, time):
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

 def setDate(self, start_date):
     self.start_date = self.getValidDate(start_date)
     self.date_time_obj = datetime.strptime(str(self.start_date) + self.timeToStr(self.start_time), '%Y%m%d%H.%M') 
 def setTime(self, start_time):
     self.start_time = self.getValidTime(start_time)
     self.date_time_obj = datetime.strptime(str(self.start_date) + self.timeToStr(self.start_time), '%Y%m%d%H.%M') 
 def setDuration(self, duration):
     self.duration = self.getValidDuration(duration)
     self.duration_obj = timedelta(minutes=self.duration*60)
 def display(self):
     print("-----------------------------\n| name: ", self.name, "\n-----------------------------", "\ntype: ",\
          self.type, "\nstart date: ", self.start_date,"\nstart time:", self.start_time, "\nduration: ", self.duration)
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
        self.date_time_end_obj = datetime.strptime(str(self.end_date), '%Y%m%d')
        if  self.date_time_end_obj.date() < self.date_time_obj.date():
            print("Error: due date cannot be before the start date!")
            raise Exception("Invalid time")
    def setDueDate(self, end_date):
        self.end_date = self.getValidDate(end_date)
        self.date_time_end_obj = datetime.strptime(str(self.end_date), '%Y%m%d') 
    def setFrequency(self, freq):
        if freq == 1:
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
