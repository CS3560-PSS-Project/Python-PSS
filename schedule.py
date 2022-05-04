
from task import *
from datetime import datetime
from datetime import timedelta

class Schedule:
    def __init__(self):
        self.transient_tasks = []
        self.recurring_tasks = []
        self.anti_tasks = []

    def __isNameUnique(self, task):
        for any in self.transient_tasks:
            if any.name == task.name:
                return False
        for any in self.recurring_tasks:
            if any.name == task.name:
                return False
        for any in self.anti_tasks:
            if any.name == task.name:
                return False
        return True

    def __antiTaskExist(self, canceled_day, any):
        if canceled_day.date_time_obj.date() >= any.date_time_obj.date() and \
            canceled_day.date_time_obj.date() <= any.date_time_end_obj.date() and\
                canceled_day.start_time == any.start_time and\
                    canceled_day.duration == any.duration:
                        return True
        return False


    def getOverlap(self, task):
        match self.__check_type(task):
            case "transient":
                for any in self.transient_tasks:
                    if any.date_time_obj.date() == task.date_time_obj.date():
                        if self.__overlap(task, any):
                            return False 
                for any in self.recurring_tasks: 
                    if any.frequency=="daily":
                        booked_step = 1   
                    else:
                        booked_step = 7
                    booked = [any.date_time_obj + timedelta(days=x) for x in\
                         range(0, (any.date_time_end_obj-any.date_time_obj).days + 2, booked_step)]
                    for canceled_day in self.anti_tasks:
                        if self.__antiTaskExist(canceled_day, any): # if anti task exists, we can book another task overlapping the time of the recurrent task
                            booked.remove(canceled_day.date_time_obj)                
                    for day in booked:
                        if day.date() == task.date_time_obj.date():
                            if self.__overlap(task, any):
                                return False 
            case "recurring":
                if task.frequency == 'daily':
                    booking_step = 1
                else:
                    booking_step = 7
                booking = [(task.date_time_obj + timedelta(days=x)).date() for x in \
                    range(0, (task.date_time_end_obj-task.date_time_obj).days + 2, booking_step)]
                for any in self.transient_tasks:
                    if any.date_time_obj.date() in booking:
                        if self.__overlap(task, any):
                            return False 
                for any in self.recurring_tasks:
                    if any.frequency=="daily":
                        booked_step = 1   
                    else:
                        booked_step = 7
                    booked = [any.date_time_obj + timedelta(days=x) for x in \
                        range(0, (any.date_time_end_obj-any.date_time_obj).days + 2, booked_step)]
                    for day in booked:
                        if day.date() in booking:
                            if self.__overlap(task, any):
                                return False   
            case "anti_task":
                for any in self.anti_tasks:
                    if any.date_time_obj.date() == task.date_time_obj.date():
                        if self.__overlap(task, any):
                            return False 
        return True     
                    
    def __overlap(self, task, any):
        if (task.date_time_obj+task.duration_obj).time() <= any.date_time_obj.time() or \
            task.date_time_obj.time() >= (any.date_time_obj+any.duration_obj).time():
            return False
        return True

    def create_task(self, task):
        if self.__isNameUnique(task):# make sure name is unique
            if self.getOverlap(task):# Check if tasks overlap
                if self.__getCrossOverDay(task):# make sure tasks don't cross over days
                    match self.__check_type(task):
                        case "recurring":
                            self.recurring_tasks.append(task)
                            self.recurring_tasks.sort(key=lambda task: task.date_time_obj)
                        case "transient":                                       
                            self.transient_tasks.append(task)
                            self.transient_tasks.sort(key=lambda task: task.date_time_obj)
                        case "anti_task":
                            if self.recurringTaskExist(task):
                                self.anti_tasks.append(task)
                                self.anti_tasks.sort(key=lambda task: task.date_time_obj)
                            else:
                                print("unable to create the task; recurring task does not exist") 
                        case default:
                            print("unable to create the task") 
                else:
                    print("it crosses over day")
            else:
                print("an overlap found")
        else:
            print("the name is not unique")
                
    # Make sure that there is a recurring task when creating a anti-task
    # making sure the start time of the recurring matches the start time and date of this anti-task  
    def recurringTaskExist(self, task):
        for any in self.recurring_tasks:
            if any.frequency == "daily":           
                booked_step = 1
            else:
                booked_step = 7
            booked = [(any.date_time_obj + timedelta(days=x)).date() for x in \
                range(0, (any.date_time_end_obj-any.date_time_obj).days + 2, booked_step)]
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
        print("deleting the following task:")
        task = self.find_task(name)
        print()
        if task != None:
            match self.__check_type(task[0]):
                case "recurring":
                    if self.__deleteAssociatedTasks(task[0]):
                    # If a recurring task is deleted, then anti-tasks associated with all occurrences of this task are also deleted
                        self.recurring_tasks.remove(task[0])
                    else:
                        print("the recurring task cannot be deleted")
                case "transient":
                    self.transient_tasks.remove(task[0])
                case "anti_task":
                    # make sure anti task doesn't overlap any transient task; otherwise 
                    # a message will give the name of the two tasks that would conflict
                    if self.__getConflict(task[0]):
                        self.anti_tasks.remove(task[0]) 
                    else:
                        print("the anti task overlaps a transient task")  
                case default:
                    print("task doesn't exist")
        else:
            print("task does not exist")
      

    def __deleteAssociatedTasks(self, task):
        if task.frequency == 'daily':
            booked_step = 1
        else:
            booked_step = 7
        booked = [task.date_time_obj + timedelta(days=x) for x in \
            range(0, (task.date_time_end_obj-task.date_time_obj).days + 2, booked_step)]
        results = []
        for any in self.anti_tasks:
            if any.date_time_obj in booked and any.duration == task.duration:
                results.append(any)
        for any in results:
            if not self.__getConflict(any):
                print("anti-tasks associated with all occurrences of this task cannot be deleted")
                return False
        for any in results:
            self.anti_tasks.remove(any) 
        return True

    def __getConflict(self, task): #returns true if two tasks would conflict
        for any in self.transient_tasks:
            if any.start_date == task.start_date and self.__overlap(task, any):
                return False
        return True

    def edit_task(self, taskName, **kwargs):
        task = self.find_task(taskName) #tuple(task, index)
        if(task != None):
            match self.__check_type(task):
                case "recurring":
                    for key, value in kwargs.items():
                        if key == "name":
                            self.recurring_tasks[task[1]].name = value
                        if key == "start_date":
                            self.recurring_tasks[task[1]].start_date = value
                            self.recurring_tasks[task[1]].setDate(value)
                        if key == "start_time":
                            self.recurring_tasks[task[1]].start_time = value
                            self.recurring_tasks[task[1]].setTime(value)
                        if key == "duration":
                            self.recurring_tasks[task[1]].duration = value
                            self.recurring_tasks[task[1]].setDuration(value)
                        if key == "end_date":
                            self.recurring_tasks[task[1]].end_date = value
                            self.recurring_tasks[task[1]].setDueDate(value)
                        if key == "frequency":
                            self.recurring_tasks[task[1]].frequency = value                            
                    if self.__isNameUnique(self.recurring_tasks[task[1]]):# make sure name is unique
                        if self.getOverlap(self.recurring_tasks[task[1]]):# Check if tasks overlap
                            if self.__getCrossOverDay(self.recurring_tasks[task[1]]):# make sure tasks don't cross over days
                                self.recurring_tasks.sort(key=lambda task: self.recurring_tasks[task[1]].date_time_obj)
                                print("task successfully edited")
                            else:
                                print("cannot be edited; it crosses over days")
                                self.recurring_tasks[task[1]] = task[0] #back to inital value
                        else:
                            print("cannot be edited; tasks overlap")
                            self.recurring_tasks[task[1]] = task[0] #back to inital value
                    else:
                        print("cannot be edited; name is not unique")
                        self.recurring_tasks[task[1]] = task[0]  #back to inital value      
                case "transient":
                    for key, value in kwargs.items():
                        if key == "name":
                            self.transient_tasks[task[1]].name = value
                        if key == "start_date":
                            self.transient_tasks[task[1]].start_date = value
                            self.transient_tasks[task[1]].setDate(value)
                        if key == "start_time":
                            self.transient_tasks[task[1]].start_time = value
                            self.transient_tasks[task[1]].setTime(value)
                        if key == "duration":
                            self.transient_tasks[task[1]].duration = value
                            self.transient_tasks[task[1]].setDuration(value)
                    if self.__isNameUnique(self.transient_tasks[task[1]]):# make sure name is unique
                        if self.getOverlap(self.transient_tasks[task[1]]):# Check if tasks overlap
                            if self.__getCrossOverDay(self.transient_tasks[task[1]]):# make sure tasks don't cross over days
                                self.transient_tasks.sort(key=lambda task: self.transient_tasks[task[1]].date_time_obj)
                                print("task successfully edited")
                            else:
                                print("cannot be edited; it crosses over days")
                                self.transient_tasks[task[1]] = task[0] #back to inital value
                        else:
                            print("cannot be edited; tasks overlap")
                            self.transient_tasks[task[1]] = task[0] #back to inital value
                    else:
                        print("cannot be edited; name is not unique")
                        self.transient_tasks[task[1]] = task[0]  #back to inital value        
                case "anti_task":
                    for key, value in kwargs.items():
                        if key == "name":
                            self.anti_tasks[task[1]].name = value
                        if key == "start_date":
                            self.anti_tasks[task[1]].start_date = value
                            self.anti_tasks[task[1]].setDate(value)
                        if key == "start_time":
                            self.anti_tasks[task[1]].start_time = value
                            self.anti_tasks[task[1]].setTime(value)
                        if key == "duration":
                            self.anti_tasks[task[1]].duration = value
                            self.anti_tasks[task[1]].setDuration(value)                      
                    if self.__isNameUnique(self.anti_tasks[task[1]]):# make sure name is unique
                        if self.getOverlap(self.anti_tasks[task[1]]):# Check if tasks overlap
                            if self.__getCrossOverDay(self.anti_tasks[task[1]]):# make sure tasks don't cross over days
                                if self.recurringTaskExist(self.anti_tasks[task[1]]):
                                    self.anti_tasks.sort(key=lambda task: self.anti_tasks[task[1]].date_time_obj)
                                    print("task successfully edited")
                                else:
                                    print("cannot be edited; it crosses over days")
                                    self.anti_tasks[task[1]] = task[0] #back to inital value
                            else:
                                print("cannot be edited; it crosses over days")
                                self.anti_tasks[task[1]] = task[0] #back to inital value
                        else:
                            print("cannot be edited; tasks overlap")
                            self.anti_tasks[task[1]] = task[0] #back to inital value
                    else:
                        print("cannot be edited; name is not unique")
                        self.anti_tasks[task[1]] = task[0]  #back to inital value      
                case default:
                    print("task cannot be edited")
        else:
            print("task doesn't exist")

    def printSchedule(self):
        print("\nRecurring:\n")
        for any in self.recurring_tasks:
            any.display()
            print()
        print("\nTransient:\n")
        for any in self.transient_tasks:
            any.display()
            print()
        print("\nAnti task:\n")
        for any in self.anti_tasks:
            any.display()
            print()
          

#     def create_task(self, name, type, start_date, start_time, duration, end_date=None, frequency=None):
#         # Make sure names of tasks are unique 
#         # case_type = self.__check_type(type)
#         match self.__check_type(type):
#             case "recurring":
#                 # Check if tasks overlap
#                 # make sure tasks don't crosses over days
#                 task = RecurringTask(name, type, start_date, start_time, duration, end_date, frequency)
#                 self.recurring_tasks.append(task)
#             case "transient":
#                 # Check if tasks overlap
#                 # make sure tasks don't crosses over days
#                 task = RecurringTask(name, type, start_date, start_time, duration, end_date, frequency)
#                 self.recurring_tasks.append(task)
#             case "anti_task":
#                 # Ant-tasks cannot overlap
#                 # Make sure that there is a recurring task when creating a anti-task
#                 # making sure the start time of the recurring matches the start time and date of this anti-task
#                 task = AntiTask(name, type, start_date, start_time, duration)   
#                 self.anti_tasks.append(task)
#             case default:
#                 print("type doesn't exist")  

#     def find_task(self, name):
#         for task in self.transient_tasks:
#             if task.name == name:   
#                 #display_task(task)
#                 return (task, self.transient_tasks.task[1(task))
#         for task in self.recurring_tasks:
#             if task.name == name:   
#                 #display_task(task)
#                 return (task, self.recurring_tasks.task[1(task))
#         for task in self.anti_tasks:
#             if task.name == name:   
#                 #display_task(task)
#                 return (task, self.anti_tasks.task[1(task))
#         return None


#     def delete_task(self, name):
#         task = self.find_task(name)[0]
#         match self.__check_type(task.type):
#             case "recurring":
#                 # If a recurring task is deleted, then anti-tasks associated with all occurrences of this task are also deleted
#                 self.recurring_tasks.remove(task)
#             case "transient":
#                 self.transient_tasks.remove(task)
#             case "anti_task":
#                 # make sure anti task doesn't overlap any transient task; otherwise 
#                 # a message will give the name of the two tasks that would conflict
#                 self.anti_tasks.remove(task) 
#             case default:
#                 print("task doesn't exist")
 
#  #start_date=None, start_time=None, duration=None, end_date=None, frequency=None