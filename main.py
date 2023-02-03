import datetime

import random

import discord
# Instantiate house list
Houselist = []

#Instantiates the class House, which contains all variables of each users houses
class House():
    def __init__(self, HouseName, PersonName, Points, UserID, Pointtime, Tokens):
        self.HouseName = HouseName
        self.PersonName = PersonName
        self.Points = int(Points)
        self.UserID = UserID
        self.Pointtime = str(Pointtime)
        self.Tokens = int(Tokens)

#File voodoo, Reads the save file and splits each line by commas, then passes the variables to separate houses in Houselist
FileLoad = open("File1.txt", 'r')
for line in FileLoad:
    row = line.split(",")
    Houselist.append(House(row[0], row[1], row[2], row[3], row[4], row[5]))

# Discord voodoo, redirects certain commands to the discord class functions
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

#checks if characters are ascii or not
def Asciireplacer(s):
    return "".join([x if ord(x) < 128 else '?' for x in s])

# confirms in print that bot is connected
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Stops the bot from replying to itself
@client.event
async def on_message(message):
    if message.author == client.user:
        return
# help
    if "!help" in message.content:
        await message.channel.send("no")

# Shows a list of all houses
    if "!houselist" in message.content:
        for x in Houselist:
            Message = "House: " + x.HouseName + ", Founder: " + x.PersonName + ", Points: " + str(x.Points) + ", Tokens: " + str(x.Tokens)
            await message.channel.send(Message)

# Shows the current house info of the user that sent the message !myhouse
    if "!myhouse" in message.content:
        for x in Houselist:
            if int(x.UserID) == int(message.author.id):
                Message = "House: " + x.HouseName + ", Founder: " + x.PersonName + ", Points: " + str(x.Points) + ", Tokens: " + str(x.Tokens)
                await message.channel.send(Message)

#Function which adds or removes points from a specified user, spends tokens of the user that sends the message
#Takes a point from jeremy when relevant
    if "!points" in message.content:
        words = message.content.split("!points")
        command = words[1].split()
        if len(command) < 3:
            for i in range(3):
                command.append("?")
        for a in Houselist:
            if int(a.UserID) == int(message.author.id):
                a.Pointtime = message.created_at
        for b in Houselist:
            if b.PersonName.lower() == command[0].lower() and int(message.author.id) != int(b.UserID):
               try:
                   command[2] = int(command[2])
               except ValueError:
                   await message.channel.send("You must specify a number between 1 and 10 to add or remove")
               if command[1].lower() == "add":
                   if int(command[2]) < 11:
                       for x in Houselist:
                            if int(x.UserID) == int(message.author.id) and x.Tokens >= int(command[2]):
                               x.Tokens -= int(command[2])
                               b.Points += int(command[2])
                               await message.channel.send(command[0] + " has recieved " + str(command[2]) + " points!")
               elif command[1].lower() == "remove":
                   if int(command[2]) < 11:
                       for x in Houselist:
                           if int(x.UserID) == int(message.author.id) and x.Tokens >= int(command[2]):
                               x.Tokens -= int(command[2])
                               b.Points -= int(command[2])
                               await message.channel.send(command[0] + " has lost " + str(command[2]) + " points!")
                               if b.PersonName == "Jeremy":
                                   b.Points -=1
                                   await message.channel.send("Jeremy has lost another point because he did not make this bot.")
               elif command[1].lower() == "?" or command[1].lower() == str:
                   await message.channel.send("You must specify if you would like to add or remove points.")
            elif int(message.author.id) == int(b.UserID) and command[0].lower() == b.PersonName.lower():
                await message.channel.send("You cannot alter your own points.")

        if command[0] == "?":
            await message.channel.send("You must specify the name of the person you wish to add or remove points from.")


# Changes the housename of the user that sent the message and replies with updated house info
    if message.content.startswith('!changehousename'):
        rowww = message.content.split()
        tempname = Asciireplacer(rowww[1])
        for x in Houselist:
            if int(x.UserID) == int(message.author.id):
                x.HouseName = tempname
                Message = "Your current house: " + x.HouseName + ", " + x.PersonName + ", " + str(x.Points)
                await message.channel.send(Message)

# Shows the current winner of the upcoming house cup
    if "!winner" in message.content:
        winner = "nobody"
        winnerpoints: int = -50000000
        for x in Houselist:
            if int(x.Points) > winnerpoints:
                winner =x.HouseName
                winnerpoints = x.Points
        await message.channel.send("The current winner is: " + winner)

# Shows the current loser of the upcoming house cup
    if "!loser" in message.content:
        loser = "nobody"
        loserpoints: int = 500000000
        for x in Houselist:
            if int(x.Points) < loserpoints:
                loser =x.HouseName
                loserpoints = x.Points
        await message.channel.send("The current loser is: " + loser)

#gamble function
    if message.content.startswith("!gamble"):
        column = message.content.split()
        if len(column) == 1:
            await message.channel.send("You have gambled incorrectly. You must place a wager in points after the !gamble command")
            return
        for x in Houselist:
            if int(x.UserID) == int(message.author.id):
                if int(column[1]) > int(x.Points) or int(column[1]) < 0:
                    await message.channel.send("You are too broke to gamble. Get a job.")
                else:
                    roll = random.randint(1,100)
                    if roll < 31:
                        x.Points = x.Points -int(column[1])
                        await message.channel.send("You rolled " + str(roll) + " and lost all the points you bet. You have " + str(x.Points) + " remaining.")
                    elif 61 > roll > 30:
                        loss = int(column[1]) // 2
                        x.Points = x.Points - loss
                        await message.channel.send("You rolled " + str(roll) + " and lost " + str(loss) + " points.")
                    elif 91 > roll > 60:
                        await message.channel.send("You rolled " + str(roll) + " and your points were returned to you in full. You have " + str(x.Points) + "remaining.")
                    elif 100 > roll > 90:
                        gain = int(column[1]) * 2
                        x.Points = x.Points + gain
                        await message.channel.send("You rolled " + str(roll) + " and have doubled your bet. You have " + str(x.Points) + "remaining.")
                    elif roll == 100:
                        gain = int(column[1]) * 3
                        x.points = x.Points + gain
                        await message.channel.send("You rolled " + str(roll) + " and have TRIPLED your bet! You have " + (x.Points) + "remaining.")
                    else:
                        await message.channel.send("You have gambled incorrectly.")


# Replies to user with timestamp of the !timestamp message in UTC
    if "!timestamp" in message.content:
        mtime = message.created_at
        await message.channel.send(mtime)

# create new house command
    if "!test" in message.content:
        await message.channel.send("Test!")
# leave house command


# Bot token


# File voodoo, saves all house variables in a CSV text file
FileSave = open("File1.txt", "w")
for x in Houselist:
    FileSave.write(x.HouseName + "," + x.PersonName + "," + str(x.Points) + "," + str(x.UserID) + "," + str(x.Pointtime) + "," + str(x.Tokens) + "," + "\n")
