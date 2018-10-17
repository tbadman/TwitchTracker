"""
Game Data class for population tracker.

Toby Badman
October, 2018
"""
import numpy as np
import matplotlib.pyplot as plt

class GameData:
    """Container for game data recieved from Twitch request."""

    def __init__(self, colors):
        """Setup initial values"""
        self.line, = plt.plot([], [], color=next(colors))
        self.name = ''
        self.viewers = 0
        self.text = ''
        self.text_xpos = 0
        self.text_ypos = 0
        self.text_color = None
        self.streamer = ''
        self.stream_viewers = 0

    def set_name(self, name):
        """Store game name"""
        self.name = name

    def update_text(self, xpos, ypos, streamer_info):
        """Create/update tooltip text"""
        if streamer_info:
            self.text = ("Game: " + self.name + "\n" +
                         "Viewers: " + str(self.viewers) + "\n" +
                         "Top Streamer: " + self.streamer + "\n" +
                         "Stream Viewers: " + str(self.stream_viewers))
        else:
            self.text = ("Game: " + self.name + "\n" +
                         "Viewers: " + str(self.viewers))

        self.text_xpos = xpos
        self.text_ypos = ypos - 0.01*ypos
        self.text_color = self.line.get_color()

    def update_data(self, xpos, ypos, reset):
        """Update plot position data"""
        self.viewers = ypos
        self.line.set_xdata(np.append(self.line.get_xdata(), xpos))

        if not reset:
            self.line.set_ydata(np.append(self.line.get_ydata(), ypos))
        else:
            self.line.set_ydata(
                np.append([0 for _ in range(len(self.line.get_ydata()))], ypos)
            )

    def set_streamer_data(self, streamer, viewers):
        """Store streamer name and viewer count"""
        self.streamer = streamer
        self.stream_viewers = viewers
