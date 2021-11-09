# twitch-compilation-generator
Python code to automate the production of twitch compilations using twitch-dl and ffmpeg.

This is done by retrieving the top clips from a given period, shuffling them, and then joining them together.

## Requirements

- Python 3.5+ installed.
- [ffmpeg](https://ffmpeg.org/download.html) installed and on system path.
- twitch-dl installed from [here](https://github.com/ihabunek/twitch-dl).

## Usage

After downloading the repository, the code in twitch.py can be accessed using

`from twitch import createCompilation, createCompilationAuto`

An example of this is contained in example.py

### Creating compilations

A compilation is created using the function

`createCompilation('[streamer]', '[period]', [video number], [minimum length of video in minutes])`

where valid periods are: `last_day`, `last_week`, `last_month`, `all_time`.

This is also produces a text file of the same name which contains:
- a video title
- description
- playlist
- tags

An example of this is

`createCompilation("Northernlion", 'last_week', 1, 10)`

which creates a 10 minute compilation of the streamer Northernlion from their videos in the past week.

### Automatically creating compilations

For a given list of streamers it is convenient to produce compilations for each of these. This is done using the function

`createCompilationAuto('[period]', [minimum length of video in minutes])`

where valid periods are: `last_day`, `last_week`, `last_month`, `all_time`.

This will automatically run `createCompilation` for each streamer in a text file streamers.txt. After producing each compilation the video number is then incremented to keep track of the compilation number.

The format of streamers.txt is one line per streamer where each line is of the format 

`[streamer], [video number]`

In the git repository there is already a streamers.txt as an example.

## License

Licensed under the GPLv3: http://www.gnu.org/licenses/gpl-3.0.html