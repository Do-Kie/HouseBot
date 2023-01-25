import datetime

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


# confirms in print that bot is connected
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Stops the bot from replying to itself
@client.event
async def on_message(message):
    if message.author == client.user:
        return
# Shows a list of all houses
    if message.content.startswith('!houselist'):
        for x in Houselist:
            Message = "House: " + x.HouseName + ", Founder: " + x.PersonName + ", Points: " + str(x.Points) + ", Tokens: " + str(x.Tokens)
            await message.channel.send(Message)

# Shows the current house info of the user that sent the message !myhouse
    if message.content.startswith('!myhouse'):
        for x in Houselist:
            if int(x.UserID) == int(message.author.id):
                Message = "House: " + x.HouseName + ", Founder: " + x.PersonName + ", Points: " + str(x.Points) + ", Tokens: " + str(x.Tokens)
                await message.channel.send(Message)

#Function which adds or removes points from a specified user, spends tokens of the user that sends the message
#Takes a point from jeremy when relevant
    if message.content.startswith("!points"):
        roww = message.content.split()
        for x in Houselist:
            if int(x.UserID) == int(message.author.id):
                x.Pointtime = message.created_at
                x.Tokens -=1
                if roww[1] == x.PersonName:
                    await message.channel.send("You cannot change your own points! You have lost a point as a penalty.")
                    x.Points -=1
                    if roww[1] == "Jeremy":
                        x.Points -=1
                        await message.channel.send("Jeremy lost another point because he didn't make this bot")
                    return
        for x in Houselist:
            if roww[1] == x.PersonName:
                if roww[2] == "add":
                    x.Points +=1
                    await message.channel.send(x.HouseName + " has gained a point!")
                if roww[2] == "remove":
                    x.Points -=1
                    await message.channel.send(x.HouseName + " has lost a point!")
                    if roww[1] == "Jeremy":
                        x.Points -=1
                        await message.channel.send("Jeremy lost another point because he didn't make this bot")

# Changes the housename of the user that sent the message and replies with updated house info
    if message.content.startswith('!changehousename'):
        rowww = message.content.split()
        for x in Houselist:
            if int(x.UserID) == int(message.author.id):
                x.HouseName = rowww[1]
                Message = "Your current house: " + x.HouseName + ", " + x.PersonName + ", " + str(x.Points)
                await message.channel.send(Message)

# Shows the current winner of the upcoming house cup
    if message.content.startswith('!winner'):
        winner = "nobody"
        winnerpoints: int = -5000
        for x in Houselist:
            if int(x.Points) > winnerpoints:
                winner =x.HouseName
                winnerpoints = x.Points
        await message.channel.send(winner)

# Shows the current loser of the upcoming house cup
    if message.content.startswith('!loser'):
        loser = "nobody"
        loserpoints: int = 5000
        for x in Houselist:
            if int(x.Points) < loserpoints:
                loser =x.HouseName
                loserpoints = x.Points
        await message.channel.send(loser)

# Replies to user with timestamp of the !timestamp message in UTC
    if message.content.startswith("!timestamp"):
        mtime = message.created_at
        await message.channel.send(mtime)

# Bot token
client.run('MTA2NjU2Njc1MTcyODQ0NzYxOQ.GW_QQy.sHcgflOq8Rq9Un2-Cwu0P04EwlFOtwA5w285O4')

# File voodoo, saves all house variables in a CSV text file
FileSave = open("File1.txt", "w")
for x in Houselist:
    FileSave.write(x.HouseName + "," + x.PersonName + "," + str(x.Points) + "," + str(x.UserID) + "," + str(x.Pointtime) + "," + str(x.Tokens) + "," + "\n")
