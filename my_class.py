import numpy as np
import matplotlib.pyplot as plt

class GameData:
    """Container for game data recieved from Twitch request."""
    
    def __init__(self,colors):
        """Setup initial values"""
        self.line, = plt.plot([],[],color=next(colors))
        self.name = ''
        self.viewers = 0
        self.text = ''
        self.text_xpos = 0
        self.text_ypos = 0
        self.text_color = None
        self.streamer = ''
        self.stream_viewers = 0

    def set_name(self,name):
        self.name = name

    def update_text(self, x,y, streamer_info):
        if streamer_info:
            self.text = ("Game: " + self.name + "\n" +
                         "Viewers: " + str(self.viewers) + "\n" +
                         "Top Streamer: " + self.streamer + "\n" +
                         "Stream Viewers: " + str(self.stream_viewers))
        else:
            self.text = ("Game: " + self.name + "\n" +
                         "Viewers: " + str(self.viewers))
            
        self.text_xpos = x
        self.text_ypos = y - 0.01*y
        self.text_color = self.line.get_color()

    def update_data(self,x,y,reset):
        """Update plot data"""
        self.viewers = y
        self.line.set_xdata(np.append(self.line.get_xdata(),x))
        
        if not reset:
            self.line.set_ydata(np.append(self.line.get_ydata(),y))
        else:
            self.line.set_ydata(
                np.append([0 for m in range(len(self.line.get_ydata()))],y)
            )

    def set_streamer_data(self, streamer, viewers):
        self.streamer = streamer
        self.stream_viewers = viewers
