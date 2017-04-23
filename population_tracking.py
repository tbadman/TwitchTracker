from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.cm as cm
import numpy as np
import requests
import requests_cache
import json

url = "https://api.twitch.tv/kraken/games/top"
clientID = {"Client-ID": "XXXXX"}

requests_cache.install_cache('twitch_cache', backend='sqlite', expire_after=10)

refresh_rate = 200 #ms
colors = iter(cm.rainbow(np.linspace(0, 1, 10)))
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 120000))
lines = [plt.plot([], [], color = next(colors), label = 'line {}'.format(i))[0] for i in range(10)]
plt.xlabel("Seconds")
plt.ylabel("Number of Viewers")
plt.title("Most Popular Twitch Streams")

def init():    
    for line in lines:
        line.set_data([], [])
    global texts
    texts = [ax.text(0, 0.95-i*0.05,  '', fontsize=8,
                     bbox={'facecolor':'white', 'alpha':0.5}) for i in range(len(lines))]
    return lines
    
def update_text(text,new_info,new_time,line):
    
    text.set_text(new_info['game']['name'])
    text.set_x(text.get_x+refresh_rate/1000)
    text.set_y(new_info['viewers'])
    text.set_backgroundcolor(line.get_color())
    
    return text

def on_plot_hover(event):
    for j,line in enumerate(lines):
        for i in range(len(line.get_xdata())):
            if (event.xdata is not None and event.ydata is not None and
                abs(float(event.xdata) - float(line.get_xdata()[i])) < 10 and abs(event.ydata - line.get_ydata()[i]) < 1000):

                for k in range(len(lines)):
                    texts[k].set_text('')
                    texts[k].set_x(0)
                    texts[k].set_y(0)
                    
                texts[j].set_text("Game: " + str(data['top'][j]['game']['name'])+"\n"+"Viewers: " + str(data['top'][j]['viewers']))
                texts[j].set_position((event.xdata,event.ydata-20000))
                texts[j].set_backgroundcolor(line.get_color())
                
def animate(i):
    r = requests.get(url,headers=clientID)
    global data
    data = r.json()
    time_seconds = float(i)*float(refresh_rate)/1000
    
    if i==0:
        global order
        order = [data['top'][n]['game']['name'] for n in range(10)]
        #ax.legend(labels=[data['top'][j]['game']['name'] for j in range(10)], loc="upper left", fontsize='x-small')
            
    for j,line in enumerate(lines):
        line.set_xdata(np.append(line.get_xdata(),time_seconds))
        
        game_found = False
        for top_game in data['top']:
            if top_game['game']['name'] == order[j]:
                line.set_ydata(np.append(line.get_ydata(), top_game['viewers']))
                game_found = True
        if not game_found:
            for top_game in data['top']:
                if top_game['game']['name'] not in order:
                    print('NEW GAME: ',top_game['game']['name'])
                    order[j] = top_game['game']['name']
                    line.set_ydata(np.append([None for m in range(len(line.get_ydata()))],top_game['viewers']))
                    #update_text(texts[j],top_game,time_seconds,line)
                    
    if time_seconds>300:
        ax.set_xlim(time_seconds+0.0001-300,time_seconds)
    else:
        ax.set_xlim(0,time_seconds+0.0001)
    ax.set_ylim(data['top'][9]['viewers']-10000,data['top'][0]['viewers']+10000)

    return lines

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=refresh_rate, blit=False)
fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)
plt.show()
