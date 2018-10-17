from matplotlib import pyplot as plt
from matplotlib import animation
from my_class import GameData
import datetime as dt
import os
import matplotlib.cm as cm
import numpy as np
import requests
import requests_cache
import json


clientID = {"Client-ID": "hw4byyky0odf9lb3ew7jfcgjcnf1jv"}


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
        game.set_name(game_name)

        if streamer_info:
            streamers = request_stream_data(game_name)
            top_streamer = streamers['streams'][0]['channel']['display_name']
            top_streamer_viewers = streamers['streams'][0]['viewers']
            game.set_streamer_data(top_streamer,top_streamer_viewers)

    return games

def draw_tooltip(game):

    tooltip.set_text(game.text)
    tooltip.set_position(ax.transLimits.transform((game.text_xpos, game.text_ypos)))
    tooltip.set_backgroundcolor(game.text_color)

def draw_permtip(text):
    perm_tooltip.set_text(text)
    perm_tooltip.set_x(0.02)
    perm_tooltip.set_y(0.64)
    perm_tooltip.set_backgroundcolor('white')

def on_plot_hover(event, games):

    if event.xdata is not None and event.ydata is not None:
        for j,game in enumerate(games):
            for i in range(len(game.line.get_xdata())):
                if (abs(event.xdata - game.line.get_xdata()[i]) < 10 and
                    abs(event.ydata - game.line.get_ydata()[i]) < 0.01*game.line.get_ydata()[i]):
                    game.update_text(event.xdata,event.ydata, streamer_info)
                    draw_tooltip(game)
                else:
                    game.update_text(0,0, streamer_info)


def animate(i):

    game_data = request_game_data()
    curr_time = float(i)*float(refresh_rate)/1000.
    #curr_time = dt.datetime.now()

    old_order = [game.name for game in games]
    new_order = [new_game['game']['name'] for new_game in game_data['top']]

    perm_text = 'Top Games'

    for i,game in enumerate(games):

        try:
            game.update_data(curr_time,game_data['top'][new_order.index(game.name)]['viewers'],0)
        except:
            for new_game in game_data['top']:
                if new_game['game']['name'] not in old_order:
                    print('NEW GAME: {}'.format(new_game['game']['name']))
                    game.set_name(new_game['game']['name'])
                    game.update_data(curr_time,new_game['viewers'],1)

        if streamer_info:
            streamers = request_stream_data(game.name)
            top_streamer = streamers['streams'][0]['channel']['display_name']
            top_streamer_viewers = streamers['streams'][0]['viewers']
            game.set_streamer_data(top_streamer,top_streamer_viewers)

        perm_text = perm_text + "\n" + str(i+1) + ": " + game.name

    #if curr_time>300:
    #    ax.set_xlim(curr_time+0.0001-300,curr_time)
    #else:
    ax.set_xlim(0,curr_time+0.0001)
    ax.set_ylim(game_data['top'][len(game_data['top'])-1]['viewers']-10000,game_data['top'][0]['viewers']+10000)

    draw_permtip(perm_text)

    return games

"""Parameters"""
streamer_info = True # add top streamer information to mouse-over (significantly reduces performance)
refresh_rate = 400    # animation update rate (ms)
game_limit = 10       # number of games to monitor
                      # output becomes difficult to interpret (though possible) if this is > ~15

try:
    os.remove('twitch_cache.sqlite')
except OSError:
    pass

#request URL
games_url = "https://api.twitch.tv/kraken/games/top?limit=" + str(game_limit)
requests_cache.install_cache('twitch_cache', backend='sqlite', expire_after=10)

#Initialize plot
colors = iter(cm.rainbow(np.linspace(0, 1, game_limit)))
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 120000))
plt.xlabel("Seconds")
plt.ylabel("Number of Viewers")
plt.title("Most Popular Twitch Streams")

#Initialize mouse-over tooltip and permanent tooltip
tooltip = ax.text(0,0, '', fontsize=8,bbox={'facecolor':'white', 'alpha':0.5}, transform = ax.transAxes)
perm_tooltip = ax.text(0,1, '', fontsize=7,bbox={'facecolor':'white', 'alpha':1}, transform = ax.transAxes)

games = [GameData(colors) for _ in range(game_limit)]

#Animate and mouse-over effect
anim = animation.FuncAnimation(fig, animate, init_func=init, interval=refresh_rate, blit=False)
fig.canvas.mpl_connect('motion_notify_event', lambda event: on_plot_hover(event, games))

plt.show()
