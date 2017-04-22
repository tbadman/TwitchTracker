from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.cm as cm
import numpy as np
import requests
import json

url = "https://api.twitch.tv/kraken/games/top"
clientID = {"Client-ID": "XXXXX"}

colors = iter(cm.rainbow(np.linspace(0, 1, 10)))
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 120000))
lines = [plt.plot([], [], color = next(colors), label = 'line {}'.format(i))[0] for i in range(10)]
dummy_array = np.array([])
plt.xlabel("Seconds")
plt.ylabel("Number of Viewers")
plt.title("Most Popular Twitch Streams")

def init():    
    for line in lines:
        line.set_data([], [])
    return lines
    
    
def animate(i):
    r = requests.get(url,headers=clientID)
    data = r.json()
    
    if i==0:
        global order
        order = [data['top'][n]['game']['name'] for n in range(10)]
        ax.legend(labels=[data['top'][j]['game']['name'] for j in range(10)], loc="upper left", fontsize='x-small')
        
    for j,line in enumerate(lines):
        line.set_xdata(np.append(line.get_xdata(),i))
        game_found = False
        for top_game in data['top']:
            if top_game['game']['name'] == order[j]:
                line.set_ydata(np.append(line.get_ydata(), top_game['viewers']))
                game_found = True
        if not game_found:
            for top_game in data['top']:
                if top_game['game']['name'] not in order:
                    print(len(dummy_array),len(line.get_xdata()))
                    print('NEW GAME: ',top_game['game']['name'])
                    order[j] = top_game['game']['name']
                    line.set_ydata(np.append(dummy_array),top_game['viewers'])
                    line.set_label(top_game['game']['name'])
                    
    np.append(dummy_array,[0])

    if i>300:
        ax.set_xlim(i-300,i)
    else:
        ax.set_xlim(0,i)
    ax.set_ylim(data['top'][9]['viewers']-10000,data['top'][0]['viewers']+10000)
        
    return lines

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=2000, blit=False)
plt.show()
