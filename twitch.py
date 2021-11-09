import os
import random

def output(string):
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print(current_time, "|", string)

def getLength(filename): #returns seconds
    import subprocess
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def createCompilationAuto(period = 'last_week', minDuration = 10):
    output("Program started.")

    #load streamers
    output("Loading streamers.")

    lines = ""
    with open('streamers.txt') as f:
        lines = f.readlines()

    i = 0
    while (i < (len(lines)-1)): # remove \n
        lines[i] = lines[i][:-1]
        i += 1
    i = 0
    while (i < len(lines)): # split and make int
        lines[i] = lines[i].split(",")
        lines[i][1] = int(lines[i][1])
        i += 1

    output("Streamers loaded.")

    output("Beginning compilation generation.")
    for line in lines:
        createCompilation(line[0], period, line[1], minDuration)

    #update gamecount file
    output("Updating streamers.txt.")
    f = open("streamers.txt", "w+")
    i = 0
    while i < len(lines):
        f.write(lines[i][0] + ", " + str(lines[i][1] + 1))
        if i != len(lines) - 1:
            f.write("\n")
        i+=1
    f.close()

    return 0

def createCompilation(streamer, period = 'last_week', videoNum = 0, minDuration = 10):
    output("Creating compilation for " + streamer + ".")

    # make output directory if it does not exist
    os.system('mkdir output > NUL')

    output("Retrieving clips.")

    # get list of clips from twitch-dl
    os.system('twitch-dl clips ' + streamer + ' --period ' + period + ' --limit 100 > temp.txt')
    with open('temp.txt') as f:
        clipLines = f.readlines()
    os.remove('temp.txt')

    # reformat into style retrieved from twitch
    channelClips = []
    i = 0
    while (i < len(clipLines)):
        if ('Clip' in clipLines[i]):
            try:
                tempClip = {}
                tempClip['id'] = clipLines[i][9:-5]
                tempClip['title'] = clipLines[i+1][5:-5]
                tempClip['url'] = clipLines[i+4][4:-5]
                tempClip['game'] = clipLines[i+2].split('playing')[1][6:-5]
                channelClips.append(tempClip)
                i = i + 5
            except:
                i = i + 1
        else:
            i = i + 1
    
    output("Beginning clip download.")

    duration = 0
    i = 0
    downloads = []
    games = []
    titles = []
    invalid = []
    # downloads required clips
    while((duration < minDuration*60) and i < len(channelClips)):
        try:
            title = channelClips[i]['title']
        except:
            i += 1
            continue
        if('\\' in title):
            i += 1
            continue

        oldFiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]

        os.system("twitch-dl download -q source " + channelClips[i]['url'] + " > NUL")
        
        newFiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
        download = ""
        for file in newFiles:
            if file not in oldFiles:
                download = file
        if (len(newFiles) == len(oldFiles)) or (download == ""):
            i += 1
            continue

        duration += getLength(download)
        while True:
            try:
                titles.append(title)
                break
            except:
                title = title[:-1]
        if(channelClips[i]['game'] not in games):
            games.append(channelClips[i]['game'])
        downloads.append('output/' + download)
        os.rename(download, 'output/' + download)
        
        i += 1

    # join clips
    output("Joining clips.")
    random.shuffle(downloads)
    tsClipLocations = []
    f= open("temp.txt","w+")
    for clip in downloads:
        #convert to .ts
        clipname = clip[:-4]
        os.system("ffmpeg -loglevel error -i " + clipname + ".mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts " + clipname + ".ts")
        tsClipLocations.append(clipname + ".ts")
        #concoctenate .ts to mp4
        f.write("file '" + clipname + ".ts" + "'\n")
    f.close() 
    os.system("ffmpeg -loglevel error -f concat -safe 0 -i temp.txt -c copy " + "output" + ".mp4")
    os.remove("temp.txt")
    os.system('ffmpeg -loglevel error -err_detect ignore_err -i output.mp4 -c copy output/' + streamer + "_" + str(videoNum) + ".mp4")
    os.remove('output.mp4')

    # create textfile
    output("Creating text file.")
    f= open('output/' + streamer + "_" + str(videoNum) + ".txt","w+")
    # title
    random.shuffle(titles)
    count = 0
    while(True): # tries titles til it finds a valid one
        try:
            title = titles[count] + " | " + streamer + " Twitch Highlights #" + str(videoNum)
            break
        except:
            count += 1
        
    f.write(title + "\n")
    # description
    desc = streamer + "'s Twitch Channel: https://www.twitch.tv/" + streamer
    f.write(desc + "\n")
    # playlists
    f.write(streamer + " Twitch Highlights\n")
    # tags
    tags = "twitch, clips, compilation, highlights, streamer, streamers, broadcaster, " + streamer 
    for game in games:
        tags+= game + ', '
    f.write(tags + "\n")
    f.close()

    # clean up
    output("Deleting extra files.")
    for file in downloads:
        try:
            os.remove(file)
        except:
            output("Unable to delete " + file)
    for file in tsClipLocations:
        try:
            os.remove(file)
        except:
            output("Unable to delete " + file)
    for file in invalid:
        try:
            os.remove(file)
        except:
            output("Unable to delete " + file)

    return 
