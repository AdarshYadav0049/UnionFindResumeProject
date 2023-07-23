from manim import *
import colorsys
import tomllib
from manim.utils.file_ops import open_file as open_media_file
from pprint import pprint
from Scene import MovingVertices
import cv2
import numpy as np
from play_vid import play_video

with open('config.toml', 'rb') as f:
    config_data = tomllib.load(f)
s = config_data['graph']['edges']
edges = []
for edge in s:
    tup=(edge[0], edge[1])
    edges.append(tup)

vid=MovingVertices(N=config_data['graph']['number_of_vertices'],EDGES=edges,LAY=config_data['graph']['layout'],
                   GRAD= config_data['color']['gradient'],
                   GS=config_data['color']['gradient_start'], GE =config_data['color']['gradient_end'])
vid.render()
play_video("media/videos/1080p60/MovingVertices.mp4")