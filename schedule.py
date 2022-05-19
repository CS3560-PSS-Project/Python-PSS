
import json
from task import *
from datetime import datetime
from datetime import timedelta
import os

class Schedule:
    def __init__(self):
        self.transient_tasks = []
        self.recurring_tasks = []
        self.anti_tasks = []

    def __isNameUnique(self, name):
        for any in self.transient_tasks:
            if any.name == name:
                return False
        for any in self.recurring_tasks:
            if any.name == name:
                return False
        for any in self.anti_tasks:
            if any.name == name:
                return False
        return True

    def __antiTaskExist(self, canceled_day, any):
        if canceled_day.date_time_obj.date() >= any.date_time_obj.date() and \
            canceled_day.date_time_obj.date() <= any.date_time_end_obj.date() and\
                canceled_day.start_time == any.start_time and\
                    canceled_day.duration == any.duration:
                        return True
        return False


    def getOverlap(self, task, *args):
        match self.__check_type(task):
            case "transient":
                for any in self.transient_tasks:
                    if any.name not in args and any.date_time_obj.date() == task.date_time_obj.date():
                        if self.__overlap(task, any):
                            return False 
                for any in self.recurring_tasks: 
                    if any.name not in args:
                        booked = [any.date_time_obj + timedelta(days=x) for x in\
                            range(0, (any.date_time_end_obj-any.date_time_obj).days + 2, any.frequency)]
                        for canceled_day in self.anti_tasks:
                            if self.__antiTaskExist(canceled_day, any): # if anti task exists, we can create another task overlapping with the recurrent task
                                booked.remove(canceled_day.date_time_obj)                
                        for day in booked:
                            if day.date() == task.date_time_obj.date():
                                if self.__overlap(task, any):
                                    return False 
            case "recurring":
                booking = [(task.date_time_obj + timedelta(days=x)).date() for x in \
                    range(0, (task.date_time_end_obj-task.date_time_obj).days + 2, task.frequency)]
                for any in self.transient_tasks :
                    if any.name not in args and any.date_time_obj.date() in booking:
                        if self.__overlap(task, any):
                            return False 
                for any in self.recurring_tasks:
                    if any.name not in args:
                        booked = [any.date_time_obj + timedelta(days=x) for x in \
                            range(0, (any.date_time_end_obj-any.date_time_obj).days + 2, any.frequency)]
                        for day in booked:
                            if day.date() in booking:
                                if self.__overlap(task, any):
                                    return False   
            case "anti_task":
                for any in self.anti_tasks:
                    if any.name not in args and any.date_time_obj.date() == task.date_time_obj.date():
                        if self.__overlap(task, any):
                            return False 
        return True     
                    
    def __overlap(self, task, any):
        if (task.date_time_obj+task.duration_obj).time() <= any.date_time_obj.time() or \
            task.date_time_obj.time() >= (any.date_time_obj+any.duration_obj).time():
            return False
        print("Error: "  + task.name + " has overlap with " + any.name)
        return True

    def create_task(self, task):
        if self.__isNameUnique(task.name):# make sure name is unique
            if self.getOverlap(task):# Check if tasks overlap
                if self.__getCrossOverDay(task):# make sure tasks don't cross over days
                    match self.__check_type(task):
                        case "recurring":
                            self.recurring_tasks.append(task)
                            self.recurring_tasks.sort(key=lambda task: task.date_time_obj)
                            return True
                        case "transient":                                       
                            self.transient_tasks.append(task)
                            self.transient_tasks.sort(key=lambda task: task.date_time_obj)
                            return True
                        case "anti_task":
                            if self.recurringTaskExist(task):
                                self.anti_tasks.append(task)
                                self.anti_tasks.sort(key=lambda task: task.date_time_obj)
                                return True
                            else:
                                print("Error: unable to create " + task.name + "; recurring task does not exist.") 
                                return False
                else:
                    print("Error: the task, " + task.name + " crosses over day.")
                    return False
            else:
                # an overlap found
                return False
        else:
            print("Error: the name " + task.name + " is not unique.")
            return False
                
    # Make sure that there is a recurring task when creating a anti-task
    # making sure the start time of the recurring matches the start time and date of this anti-task  
    def recurringTaskExist(self, task):
        for any in self.recurring_tasks:
            booked = [(any.date_time_obj + timedelta(days=x)).date() for x in \
                range(0, (any.date_time_end_obj-any.date_time_obj).days + 2, any.frequency)]
            if task.date_time_obj.date() in booked:
                if task.start_time == any.start_time and\
                    task.duration == any.duration:
                    return True
        return False
   
    def __getCrossOverDay(self, task):
        if task.date_time_obj.date() != (task.date_time_obj + task.duration_obj).date():
            return False
        return True

    def __check_type(self, task):
        if(task.type.lower() in ["class", "study", "sleep", "exercise", "work", "meal"]):
            return "recurring"
        if(task.type.lower() in ["visit", "shopping", "appointment"]):
            return "transient"
        if(task.type.lower() in ["cancellation"]):
            return "anti_task"

    def find_task(self, name):
        for task in self.transient_tasks:
            if task.name == name:   
                task.display() # polymorphism: it calles the display method for each task object
                return (task, self.transient_tasks.index(task))
        for task in self.recurring_tasks:
            if task.name == name:   
                task.display() # polymorphism: it calles the display method for each task object
                return (task, self.recurring_tasks.index(task))
        for task in self.anti_tasks:
            if task.name == name:   
                task.display() # polymorphism: it calles the display method for each task object
                return (task, self.anti_tasks.index(task))
        return None

    def delete_task(self, name):
        print("Deleting the following task:")
        task = self.find_task(name)
        if task != None:
            match self.__check_type(task[0]):
                case "recurring":
                    if self.__deleteAssociatedTasks(task[0])[0]:
                    # If a recurring task is deleted, then anti-tasks associated with all occurrences of this task are also deleted
                        self.recurring_tasks.remove(task[0])
                        return True
                    else:
                        print("Error: the recurring task, " + name + " cannot be deleted.")
                case "transient":
                    self.transient_tasks.remove(task[0])
                    return True
                case "anti_task":
                    # make sure anti task doesn't overlap any transient task; otherwise 
                    # a message will give the name of the two tasks that would conflict
                    if self.__getConflict(task[0]):
                        self.anti_tasks.remove(task[0]) 
                        return True
                    else:
                        print("Error: " + name + "overlaps a transient task.")  
                        return False
        else:
            print("Error: task does not exist.")
            return False
      
    def __findAssociatedTasks(self, task):
        booked = [task.date_time_obj + timedelta(days=x) for x in \
            range(0, (task.date_time_end_obj-task.date_time_obj).days + 2, task.frequency)]
        results = []
        cloneResults = []
        for any in self.anti_tasks:
            if any.date_time_obj in booked and any.duration == task.duration:
                results.append(any)
                cloneResults.append(any.clone())
        return(results, cloneResults)

    def __deleteAssociatedTasks(self, task):
        booked = [task.date_time_obj + timedelta(days=x) for x in \
            range(0, (task.date_time_end_obj-task.date_time_obj).days + 2, task.frequency)]
        results = []
        cloneResult = []
        for any in self.anti_tasks:
            if any.date_time_obj in booked and any.duration == task.duration:
                results.append(any)
                cloneResult.append(any.clone())
        for any in results:
            if not self.__getConflict(any):
                print("Error: anti-tasks associated with all occurrences of " + task.name + " cannot be deleted.")
                return (False, [])
        for any in results:
            self.anti_tasks.remove(any) 
        return (True, cloneResult)

    def __getConflict(self, task): #returns true if two tasks would conflict
        for any in self.transient_tasks:
            if any.start_date == task.start_date and self.__overlap(task, any):
                return False
        return True

    def __edit(self, task, kwargs):
        for key, value in kwargs.items():
            if key == "name" and value != "":               
                task.name = value
            elif key == "start_date" and value != "":
                task.setDate(value)
            elif key == "start_time" and value != "": 
                task.setTime(value)
            elif key == "duration" and value != "":
                task.setDuration(value)
            elif key == "end_date" and value != "" and task.type.lower in [["visit", "shopping", "appointment"]]:
                task.setDueDate(value)
            elif key == "frequency" and value != "" and task.type.lower in [["visit", "shopping", "appointment"]]:
                task.setFrequency(value)

    def edit_task(self, taskName, **kwargs):
        print("Editing the following task:")
        tuple = self.find_task(taskName) #tuple(task, index)
        if(tuple != None):
            task = tuple[0].clone()
            temp = tuple[0].clone()
            self.__edit(temp, kwargs)
            index = tuple[1]
            match self.__check_type(task):    
                case "transient":
                    self.transient_tasks.remove(tuple[0])
                    if(self.create_task(temp)):
                        print("task successfully edited.")
                        return True
                    else:
                        print("Error: unable to edit the task.")
                        self.transient_tasks.insert(index, task) 
                        return False             
                case "recurring":
                    assoc = self.__deleteAssociatedTasks(task) # deletes all associated anti tasks and returns a tuple, a boolean 
                    if assoc[0]:                               # and a list of deleted tasks' clone.
                        self.recurring_tasks.remove(tuple[0])  # if it succesfully deletes all associated tasks
                        if(self.create_task(temp)):            # we create a new task instead of existing one
                            for any in assoc[1]:               # we need to recreate all anti tasks with the updated time and duration
                                if any.date_time_obj.date() >= temp.date_time_obj.date() and \
                                    any.date_time_obj.date() <= temp.date_time_end_obj.date():
                                    any.setTime(temp.start_time)
                                    any.setDuration(temp.duration)
                                    self.create_task(any)

                            print("task successfully edited.")
                            return True
                        else:
                            print("Error: unable to edit the task.")
                            self.recurring_tasks.insert(index, task)  # if we are unable to recreate the task
                            for any in assoc[1]:                      # we need to recreate the tasks we deleted in the beginning
                                self.create_task(any)
                            return False 
                    else:
                        print("Error: unable to edit the task.")
                        for any in assoc[1]:
                            self.create_task(any)

                case "anti_task":
                    self.anti_tasks.remove(tuple[0])
                    if(self.create_task(temp)):
                        print("task successfully edited")
                        return True
                    else:
                        print("Error: unable to edit the task.")
                        self.anti_tasks.insert(index, task)
                        return False 
        else:
            print("Error: task doesn't exist.")
    
    def __dayView(self, date, show=True):
        result = []
        date_obj = datetime.strptime(date, '%Y%m%d')
        for any in self.recurring_tasks:
            bookedDates = [(any.date_time_obj + timedelta(days=x)).date() for x in \
                range(0, (any.date_time_end_obj-any.date_time_obj).days + 2, any.frequency)]
            listOfAntiTasks = self.__findAssociatedTasks(any)[0]
            flag = False
            if date_obj.date() in bookedDates:
                flag = True
                for antiTask in listOfAntiTasks:
                    if antiTask.date_time_obj.date() == date_obj.date():
                        flag = False
                        break
            if flag:
                result.append(any)
        for any in self.transient_tasks:
            if any.date_time_obj.date() == date_obj.date():
                result.append(any)    
        result.sort(key=lambda task: task.date_time_obj.time())
        if show:
            print("----> ", date_obj.date(), " <----")
            counter = 1
            for any in result:
                print("[", counter, "]")
                print("task Name: ", any.name)
                print("task Type: ", any.type)
                print("Start time: {:d}:{:02d}".format(any.date_time_obj.hour, any.date_time_obj.minute))
                print("Duration: ", any.duration_obj)
                counter+=1
        return result
       
    def viewSchedule(self, date, numOfDays):
        if(re.match("^[0-9]{8}$", date)): 
            date_obj = datetime.strptime(date, '%Y%m%d')
            if numOfDays.isnumeric():
                if int(numOfDays) < 0:
                    numOfDays = 0
                dates = [(date_obj + timedelta(days=x)).strftime("%Y%m%d") for x in range(0, int(numOfDays))]
                for date in dates:
                    self.__dayView(date)
        else:
            print("Error: date should be in the following format: 'YYYYMMDD'")

    def writeSchedule(self, date, numOfDays, fileName):
        data = []
        if(re.match("^[0-9]{8}$", date)): 
            date_obj = datetime.strptime(date, '%Y%m%d')
            if numOfDays.isnumeric():
                if int(numOfDays) < 0:
                    numOfDays = 0
                dates = [(date_obj + timedelta(days=x)).strftime("%Y%m%d") for x in range(0, int(numOfDays))]
                for date in dates:
                    tasks = self.__dayView(date, False)
                    for any in tasks:
                        entry = {'Name': any.name, 'Type': any.type, 'Date': date,\
                            'Start Time': any.start_time, 'Duration':any.duration}
                        data.append(entry)
        
            jsonFile = json.dumps(data, indent=2)        
            file = open(fileName, 'w')
            file.write(jsonFile)
            file.close()
        else:
            print("Error: date should be in the following format: YYYYMMDD")

    def printSchedule(self):
        print("\t-------------\n\t| Recurring |\n\t-------------")
        for any in self.recurring_tasks:
            any.display()
        print("\t-------------\n\t| Transient |\n\t-------------")
        for any in self.transient_tasks:
            any.display()
        print("\t-------------\n\t| Anti task |\n\t-------------")
        for any in self.anti_tasks:
            any.display()

  
    def read_schedule(self, filename):
        if os.path.exists(filename):
            f = open(filename)
            data = json.load(f)
            flag = True
            task = 0
            for any in data:
                if any['Type'] in ["class", "study", "sleep", "exercise", "work", "meal"]:
                    tempTask = RecurringTask(any['Name'], any['Type'], any['Start Date'], any['Start Time'], any['Duration'],\
                        any['End Date'], any['Frequency'])
                    flag = self.create_task(tempTask)
                    if not flag:
                        task = any # save the name of the task that cause error
                        break
                if any['Type'] in ["cancellation"]:
                    tempTask = AntiTask(any['Name'], any['Type'], any['Start Date'], any['Start Time'], any['Duration'])
                    flag = self.create_task(tempTask)
                    if not flag:
                        task = any
                        break
                if any['Type'] in ["visit", "shopping", "appointment"]:
                    tempTask = TransientTask(any['Name'], any['Type'], any['Start Date'], any['Start Time'], any['Duration'])
                    flag = self.create_task(tempTask)
                    if not flag:
                        task = any
                        break
            if not flag:
                for any in data:
                    if any == task:
                        break
                    self.__delete(any['Name'])
            f.close()
            return True
        else:
            print("File does not exist.")
            return False

    def __delete(self, name):
        task = self.find_task(name)[0]
        match self.__check_type(task):
            case "recurring":
                # If a recurring task is deleted, then anti-tasks associated with all occurrences of this task are also deleted
                self.recurring_tasks.remove(task)
            case "transient":
                self.transient_tasks.remove(task)
            case "anti_task":
                # make sure anti task doesn't overlap any transient task; otherwise 
                # a message will give the name of the two tasks that would conflict
                self.anti_tasks.remove(task) 
            case default:
                print("task doesn't exist")
