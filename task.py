from datetime import datetime
from datetime import timedelta
import re
from tempfile import TemporaryDirectory

class Task:
 def __init__(self,name, type, start_date, start_time, duration):
   self.name = name
   self.type = type
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

 def getValidDate(self, start_date):
    if(re.match("^[0-9]{8}$", str(start_date))): 
        year = str(start_date)[0:4]
        month = str(start_date)[4:6]
        day = str(start_date)[6:8]
        if int(year) < 2022:
            year = "2022"
        if int(day) < 1:
            day = "01"
        if int(month) < 1:
            month = "01"
        elif int(month) > 12:
            month = "12"
        if int(month) == 2 and int(day) > 28:
            day = "28"
        elif int(month) in [4,6,9,11] and int(day) > 30:
            day = "30"
        elif int(month) in [1,3,5,7,8,10,12] and int(day) > 31:
            day = "31"
        return int(year+month+day)
    else:
        return  20230101

 def getValidTime(self, start_time):
    tempTime = self.__getNearestTime(start_time)
    if tempTime >= 24.0 and tempTime < 25:
        tempTime-=24.0  # "%.2d:%.2d" % (hour, min)    
    elif tempTime >= 25.0:
        tempTime = 23.75
    return tempTime

 def getValidDuration(self, duration):
    tempDuration = self.__getNearestTime(duration)
    if duration > 23.75:
        tempDuration = 23.75
    return tempDuration

 def __getNearestTime(self, time):
    if time > 0:
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
        return 0.0
        
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
        self.date_time_end_obj = datetime.strptime(str(self.end_date), '%Y%m%d') 
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
