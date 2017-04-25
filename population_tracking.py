from matplotlib import pyplot as plt
from matplotlib import animation
from my_class import GameData
import os
import matplotlib.cm as cm
import numpy as np
import requests
import requests_cache
import json

games_url = "https://api.twitch.tv/kraken/games/top"
clientID = {"Client-ID": "XXXXX"}

try:
    os.remove('twitch_cache.sqlite')
except OSError:
    pass

requests_cache.install_cache('twitch_cache', backend='sqlite', expire_after=10)

def request_game_data():
    
    games = requests.get(games_url,headers=clientID)
    games = games.json()

    return games

def request_stream_data(game):

    stream_url = "https://api.twitch.tv/kraken/streams/?game=" + game
    stream = requests.get(stream_url,headers=clientID)
    stream = stream.json()

    return stream

def init():
    
    game_data = request_game_data()
    for i,game in enumerate(games):
        game_name = game_data['top'][i]['game']['name']
        streamers = request_stream_data(game_name)
        
        top_streamer = streamers['streams'][0]['channel']['display_name']
        top_streamer_viewers = streamers['streams'][0]['viewers']
        
        game.set_name(game_name)
        game.set_streamer_data(top_streamer,top_streamer_viewers)
        
    return games

def draw_tooltip(game):
    
    tooltip.set_text(game.text)
    tooltip.set_position(ax.transLimits.transform((game.text_xpos, game.text_ypos)))
    tooltip.set_backgroundcolor(game.text_color)

def on_plot_hover(event, games):
    
    if event.xdata is not None and event.ydata is not None:
        for j,game in enumerate(games):
            for i in range(len(game.line.get_xdata())):
                if (abs(event.xdata - game.line.get_xdata()[i]) < 10 and
                    abs(event.ydata - game.line.get_ydata()[i]) < 1000):
                    game.update_text(event.xdata,event.ydata)
                    draw_tooltip(game)
                else:
                    game.update_text(0,0)
                    
                
def animate(i):
    
    game_data = request_game_data()
    curr_time = float(i)*float(refresh_rate)/1000.

    old_order = [game.name for game in games]
    new_order = [new_game['game']['name'] for new_game in game_data['top']]
    
    for game in games:
        
        try:
            game.update_data(curr_time,game_data['top'][new_order.index(game.name)]['viewers'],0)
        except:
            for new_game in game_data['top']:
                if new_game['game']['name'] not in old_order:
                    print 'NEW GAME: ' + new_game['game']['name']
                    game.set_name(new_game['game']['name'])
                    game.update_data(curr_time,new_game['viewers'],1)

        streamers = request_stream_data(game.name)
        top_streamer = streamers['streams'][0]['channel']['display_name']
        top_streamer_viewers = streamers['streams'][0]['viewers']
        game.set_streamer_data(top_streamer,top_streamer_viewers)
                    
    if curr_time>300:
        ax.set_xlim(curr_time+0.0001-300,curr_time)
    else:
        ax.set_xlim(0,curr_time+0.0001)
    ax.set_ylim(game_data['top'][9]['viewers']-10000,game_data['top'][0]['viewers']+10000)
    
    return games

refresh_rate = 400 #ms
colors = iter(cm.rainbow(np.linspace(0, 1, 10)))
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 120000))
tooltip = ax.text(0, 0,  '', fontsize=8,bbox={'facecolor':'white', 'alpha':0.5}, transform = ax.transAxes)
plt.xlabel("Seconds")
plt.ylabel("Number of Viewers")
plt.title("Most Popular Twitch Streams")

games = [GameData(colors) for _ in range(10)]

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=refresh_rate, blit=False)
fig.canvas.mpl_connect('motion_notify_event', lambda event: on_plot_hover(event, games))
plt.show()
