import sys
import os
import pandas as pd
import plotly.express as px

file_path = sys.argv[1]

# handles the command line arguments
if (not (len(file_path) > 1)) or (not (os.path.exists(file_path))):
    exit("Please provide a valid file path to the video")

# Cleans up pre-exisiting files
os.system("rm *.csv")

# Runs the program through PySceneDetect
os.system("scenedetect --input {} --stats output.stats.csv detect-content list-scenes".format(file_path))
os.system("sed -i 1d *.csv")

# Generates the graph
outputStats = pd.read_csv("output.stats.csv")
fig = px.line(outputStats, x=['Frame Number', y=['delta_hue', 'delta_lum', 'delta_sat'])
fig.show()