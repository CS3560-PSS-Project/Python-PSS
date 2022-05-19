from schedule import *
from task import *
import json

class User:
    def __init__(self, user_name, id):
        self.name = user_name
        self.name = id
        self.schedule = Schedule()

    def create_task(self, task):
        if self.schedule.create_task(task):
            print("Task successfully created!")
        
 
    def edit_task(self, taskName, **kwargs):
        self.schedule.edit_task(taskName, **kwargs)

    def delete_task(self, name):
        if self.schedule.delete_task(name):
            print("Task successfully deleted!")


    def find_task(self, name):
        if self.schedule.find_task(name) == None:
            print("Task does not exist.")
    
    def read_schedule(self, filename):
        if self.schedule.read_schedule(filename):
            print("Read schedule succesfully done!")

    def write_schedule(self, filename):
        data = []
        for any in self.schedule.recurring_tasks:
            entry = {'Name': any.name, 'Type': any.type, 'Start Date': any.start_date,\
                'Start Time': any.start_time, 'Duration':any.duration, 'End Date':any.end_date,\
                    'Frequency': any.frequency}
            data.append(entry)
        for any in self.schedule.anti_tasks:
            entry = {'Name': any.name, 'Type': any.type, 'Start Date': any.start_date,\
                'Start Time': any.start_time, 'Duration':any.duration}
            data.append(entry)
        for any in self.schedule.transient_tasks:
            entry = {'Name': any.name, 'Type': any.type, 'Start Date': any.start_date,\
                'Start Time': any.start_time, 'Duration':any.duration}
            data.append(entry)

        jsonFile = json.dumps(data, indent=2)
        file = open(filename, 'w')
        file.write(jsonFile)
        file.close()
        print("Write schedule succesfully done!")
