from constants import *
import math
from customtkinter import *
from PIL import Image

def getConfigPage(app):
    body = CTkFrame(app.win, fg_color="transparent", corner_radius=0)
    body.pack(fill="both", expand=True)

    return body
