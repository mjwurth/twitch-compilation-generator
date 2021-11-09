# this code is an example of using the twitch-compilation-generator
from twitch import createCompilation, createCompilationAuto

# this produces a clip of Northernlion of the best videos from the last week numbered 1 that is 1 minute long
createCompilation("Northernlion", 'last_week', 1, 1)
# createCompilation('streamer', 'time period', video number, length of video in minutes)

# uncommenting the next line will produce videos for each streamer in streamers.txt of the past week that are 1 minute long
# createCompilationAuto('last_week', 1)