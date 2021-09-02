import discord
import os
import requests
import json
import random
import calendar
import schedule
import numpy
import datetime
from datetime import date, timedelta
import pytz
from replit import db

client = discord.Client()

c = calendar.TextCalendar(calendar.SUNDAY)

today = datetime.datetime.now(tz=pytz.timezone('Canada/Pacific'))

d = today.strftime("%A, %B %d, %Y")

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")
  json_data = json.loads(response.text)
  joke = json_data['setup'] + "\n" + json_data['punchline']
  return(joke)

def update_schedule(task_info, user):
  if user == 'cait':
    if "c_schedule" in db.keys():
      c_schedule = db["c_schedule"]
      c_schedule.append(task_info)
      db["c_schedule"] = c_schedule
    else:
      db["c_schedule"] = [task_info]
  else:
    if "d_schedule" in db.keys():
      d_schedule = db["d_schedule"]
      d_schedule.append(task_info)
      db["d_schedule"] = d_schedule
    else:
      db["d_schedule"] = [task_info]
    
def task_today(user):
  if user == 'cait':
    if "c_schedule" in db.keys():
      c_schedule = db["c_schedule"]
      day = today.strftime("%A")
      status = bool(False)
      for x in c_schedule:
        if day in x:
          status = True
      return(status)
  else:
    if "d_schedule" in db.keys():
      d_schedule = db["d_schedule"]
      day = today.strftime("%A")
      status = bool(False)
      for x in d_schedule:
        if day in x:
          status = True
      return(status)

def get_status(user):
  if user == 'cait':
    if "c_schedule" in db.keys():
      c_schedule = db["c_schedule"]
      day = today.strftime("%A")
      curr_time = today.strftime("%l")
      temp_list = list()
      for x in c_schedule:
        if day in x:
          temp_list.append(x)
      if not temp_list:
        return("There are no tasks right now.1")
      else:
        for y in temp_list:
          task = y[0]
          str_time = y[2]
          end_time = y[3]
          if int(str_time) <= int(curr_time) <= int(end_time):
            return("currently in " + task + " until " + end_time)
        return("There are no tasks right now.2")
  else:
    if "d_schedule" in db.keys():
      d_schedule = db["d_schedule"]
      day = today.strftime("%A")
      curr_time = today.strftime("%l")
      temp_list = list()
      for x in schedule:
        if day in x:
          temp_list.append(x)
      if not temp_list:
        return("There are no tasks right now.1")
      else:
        for y in temp_list:
          task = y[0]
          str_time = y[2]
          end_time = y[3]
          if int(str_time) <= int(curr_time) <= int(end_time):
            return("currently in " + task + " until " + end_time)
        return("There are no tasks right now.2")

def return_daily_task(user):
  if user == 'cait':
    if "c_schedule" in db.keys():
      c_schedule = db["c_schedule"]
      day = today.strftime("%A")
      temp_list = list()
      for x in c_schedule:
        if day in x:
          temp_list.append(x)
      return(temp_list)
  else:
    if "d_schedule" in db.keys():
      d_schedule = db["d_schedule"]
      day = today.strftime("%A")
      temp_list = list()
      for x in d_schedule:
        if day in x:
          temp_list.append(x)
      return(temp_list)

# def delete_schedule(index, user):
#   if user == 'cait':
#     c_schedule = db["c_schedule"]
#     if len(c_schedule) > index:
#       del c_schedule[index]
#     db["c_schedule"] = c_schedule
#   else:
#     d_schedule = db["d_schedule"]
#     if len(d_schedule) > index:
#       del d_schedule[index]
#     db["d_schedule"] = d_schedule

def delete_schedule(task, user):
  if user == 'cait':
    c_schedule = db["c_schedule"]
    count = 0
    for x in c_schedule:
      if task == x[0]:
        del c_schedule[count]
      count = count + 1
    db["c_schedule"] = c_schedule
  else:
    d_schedule = db["d_schedule"]
    count = 0
    for x in d_schedule:
      if task == x[0]:
        del d_schedule[count]
      count = count + 1
    db["d_schedule"] = d_schedule

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  msg = message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$day'):
    await message.channel.send(d)

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if message.content.startswith('$joke'):
    joke = get_joke()
    await message.channel.send(joke)

  if msg.startswith("$add"):
    m_list = msg.split(" ",5)
    m_list.pop(0)
    user = "daniel"
    if (message.author.id == 364601613165264896):
      user = "cait"
    update_schedule(m_list, user)
    await message.channel.send("New task added for " + user + ": " + m_list[0] + " on " + m_list[1] + " from " + m_list[2] + " to " + m_list[3])
  
  # if msg.startswith("$del"):
  #   user = msg.split(" ", 3)[1]
  #   index = int(msg.split(" ",3)[2])
  #   if user == 'cait':
  #     c_schedule = []
  #     if "c_schedule" in db.keys():
  #       delete_schedule(index, user)
  #       c_schedule = db["c_schedule"]
  #     await message.channel.send(c_schedule)
  #   else:
  #     d_schedule = []
  #     if "d_schedule" in db.keys():
  #       delete_schedule(index, user)
  #       d_schedule = db["d_schedule"]
  #     await message.channel.send(d_schedule)

  if msg.startswith("$del"):
    user = msg.split(" ", 3)[1]
    task = msg.split(" ",3)[2]
    if user == 'cait':
      c_schedule = []
      if "c_schedule" in db.keys():
        delete_schedule(task, user)
        c_schedule = db["c_schedule"]
      await message.channel.send(c_schedule)
    else:
      d_schedule = []
      if "d_schedule" in db.keys():
        delete_schedule(task, user)
        d_schedule = db["d_schedule"]
      await message.channel.send(d_schedule)
    
  # if msg.startswith("$schedule"):
  #   user = msg.split(" ", 2)[1]
  #   if user == 'cait':
  #     c_schedule = []
  #     if "c_schedule" in db.keys():
  #       c_schedule = db["c_schedule"]
  #     await message.channel.send(c_schedule)
  #   else:
  #     d_schedule = []
  #     if "d_schedule" in db.keys():
  #       d_schedule = db["d_schedule"]
  #     await message.channel.send(d_schedule)

  if msg.startswith("$schedule"):
    user = msg.split(" ", 2)[1]
    if user == 'cait':
      c_schedule = []
      if "c_schedule" in db.keys():
        c_schedule = db["c_schedule"]
        start_time = 25
        end_time = 0
        for x in c_schedule:
          if int(x[2]) < int(start_time):
            start_time = x[2]
          if int(x[3]) > int(end_time):
            end_time = x[3]
        total_time = int(end_time) - int(start_time) + 1
        DATASET = numpy.zeros(shape=(total_time ,7),dtype = object)
        count = 0
        add_time = start_time
        while int(add_time) <= int(end_time):
          DATASET[int(count), 0] = add_time
          count = int(count) + 1
          add_time = int(add_time) + 1
        for y in c_schedule:
          offset = int(y[2]) - int(start_time)
          task_duration = int(y[3]) - int(y[2])
          c = 0
          if y[1] == 'Monday':
            while c < task_duration:
              DATASET[offset, 1] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Tuesday':
            while c < task_duration:
              DATASET[offset, 2] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Wednesday':
            while c < task_duration:
              DATASET[offset, 3] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Thursday':
            while c < task_duration:
              DATASET[offset, 4] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Friday':
            while c < task_duration:
              DATASET[offset, 5] = str(y[0])
              offset = offset + 1
              c = c + 1
        s = ['Time    Mon    Tue    Wed    Thur    Fri    Sat']
        for data in DATASET:
          s.append('  '.join([str(item).center(5, ' ') for item in data]))
          d = '```'+'\n'.join(s) + '```'
          embed = discord.Embed(title = 'Caitlin\'s Schedule', description = d)
      await message.channel.send(embed = embed)
    else:
      d_schedule = []
      if "d_schedule" in db.keys():
        d_schedule = db["d_schedule"]
        start_time = 25
        end_time = 0
        for x in d_schedule:
          if int(x[2]) < int(start_time):
            start_time = x[2]
          if int(x[3]) > int(end_time):
            end_time = x[3]
        total_time = int(end_time) - int(start_time) + 1
        DATASET = numpy.zeros(shape=(total_time ,7),dtype = object)
        count = 0
        add_time = start_time
        while int(add_time) <= int(end_time):
          DATASET[int(count), 0] = add_time
          count = int(count) + 1
          add_time = int(add_time) + 1
        for y in d_schedule:
          offset = int(y[2]) - int(start_time)
          task_duration = int(y[3]) - int(y[2])
          c = 0
          if y[1] == 'Monday':
            while c < task_duration:
              DATASET[offset, 1] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Tuesday':
            while c < task_duration:
              DATASET[offset, 2] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Wednesday':
            while c < task_duration:
              DATASET[offset, 3] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Thursday':
            while c < task_duration:
              DATASET[offset, 4] = str(y[0])
              offset = offset + 1
              c = c + 1
          elif y[1] == 'Friday':
            while c < task_duration:
              DATASET[offset, 5] = str(y[0])
              offset = offset + 1
              c = c + 1
        s = ['Time    Mon    Tue    Wed    Thur    Fri    Sat']
        for data in DATASET:
          s.append('  '.join([str(item).center(5, ' ') for item in data]))
          d = '```'+'\n'.join(s) + '```'
          embed = discord.Embed(title = 'Daniel\'s Schedule', description = d)
      await message.channel.send(embed = embed)
  
  if msg.startswith("$today"):
    user = msg.split(" ", 2)[1]
    if not return_daily_task(user):
      await message.channel.send(user + " has no tasks today.")
    else:
      await message.channel.send(user + "'s tasks today include:")
      for x in return_daily_task(user):
        await message.channel.send(x[0] + " from " + x[2] + " to " + x[3])

  if msg.startswith("$curr"):
    user = msg.split(" ", 2)[1]
    await message.channel.send(get_status(user))
  
  if msg.startswith("$help"):
    await message.channel.send("To add a task: $add [task] [day of week] [start time] [end time] \nTo delete a task: $del [user (cait/daniel)] [task] \nTo view the schedule: $schedule \nTo view current status of all users: $curr \nTo get a randomized joke: $joke \nTo get today's task for a user: $today [user]")
    
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

client.run(os.getenv('TOKEN'))
