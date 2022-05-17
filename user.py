from schedule import *
from task import *
import json

class User:
    def __init__(self, user_name, id):
        self.name = user_name
        self.name = id
        self.schedule = Schedule()

    def create_task(self, task):
        self.schedule.create_task(task)
 
    def edit_task(self, taskName, **kwargs):
        self.schedule.edit_task(taskName, **kwargs)

    def delete_task(self, name):
        self.schedule.delete_task(name)
 
    def find_task(self, name):
        if self.schedule.find_task(name) == None:
            print("Task does not exist.")
    
    def read_schedule(self, filename):
        self.schedule.read_schedule(filename)

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

    #def write_schedule(self, filename):
        # with open(filename, 'w') as f:
        #     f.write("{")
        #     f.write("\n\"Recurring\":\n\t[")
        #     i=0
        #     for any in self.schedule.recurring_tasks:
        #         f.write("\n\t\t{")
        #         f.write("\n")
        #         f.write("\t\t\t\"Name\":\""+any.name+"\",\n")
        #         f.write("\t\t\t\"Type\":\""+any.type+"\",\n")
        #         f.write("\t\t\t\"Start Date\":\""+any.start_date+"\",\n")
        #         f.write("\t\t\t\"Start Time\":\""+any.start_time+"\",\n")
        #         f.write("\t\t\t\"Duration\":"+any.duration+",\n")
        #         f.write("\t\t\t\"End Date\":"+any.end_date+",\n")
        #         f.write("\t\t\t\"Frequency\":\""+any.frequency+"\"\n")                            
        #         if i is (len(self.schedule.recurring_tasks) -1):
        #             f.write("\t\t}")
        #         else:
        #             f.write("\t\t},")
        #         i+=1
        #     i = 0
        #     f.write("\n\t],")

        #     f.write("\n\"Transient\":\n\t[")
        #     i=0
        #     for any in self.schedule.transient_tasks:
        #         f.write("\n\t\t{")
        #         f.write("\n")
        #         f.write("\t\t\t\"Name\":\""+any.name+"\",\n")
        #         f.write("\t\t\t\"Type\":\""+any.type+"\",\n")
        #         f.write("\t\t\t\"Start Date\":\""+any.start_date+"\",\n")
        #         f.write("\t\t\t\"Start Time\":\""+any.start_time+"\",\n")
        #         f.write("\t\t\t\"Duration\":"+any.duration+"\n")                          
        #         if i is (len(self.schedule.transient_tasks) -1):
        #             f.write("\t\t}")
        #         else:
        #             f.write("\t\t},")
        #         i+=1
        #     i = 0
        #     f.write("\n\t],")
            
        #     f.write("\n\"Anti\":\n\t[")
        #     i=0
        #     for any in self.schedule.anti_tasks:
        #         f.write("\n\t\t{")
        #         f.write("\n")
        #         f.write("\t\t\t\"Name\":\""+any.name+"\",\n")
        #         f.write("\t\t\t\"Type\":\""+any.type+"\",\n")
        #         f.write("\t\t\t\"Start Date\":\""+any.start_date+"\",\n")
        #         f.write("\t\t\t\"Start Time\":\""+any.start_time+"\",\n")
        #         f.write("\t\t\t\"Duration\":"+any.duration+"\n")                        
        #         if i is (len(self.schedule.anti_tasks) -1):
        #             f.write("\t\t}")
        #         else:
        #             f.write("\t\t},")
        #         i+=1
        #     i = 0
        #     f.write("\n\t]")

        #     f.write("\n}")

    # def read_schedule(self, filename):
        # print("\nRecurrint Task: ")
        # for r in data['Recurring']:
        #     tempTask = RecurringTask(r['Name'], r['Type'], r['Start Date'], int(r['Start Time']),\
        #          int(r['Duration']), r['End Date'], r['Frequency'])
        #     tempTask.display()

        # print("\nTransient Task: ")
        # for t in data['Transient']:
        #     print(t)

        # print("\nAnti Task: ")
        # for a in data['Anti']:
        #     print(a)
        # # Closing file
        # f.close()

        
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

