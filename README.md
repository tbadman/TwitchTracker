# Twitch View Tracker

Real-time Twitch viewer count for the top 10 most popular streaming games. More features planned for the future!

![Alt text](http://i.imgur.com/gnBYj37.png)

IMPORTANT: Requires a Client-ID code to run. Instructions to get your own:
- Go to https://www.twitch.tv/ and log in.
- Click on Settings in the top right corner.
- On the Connections tab, scroll to the bottom.
- Click 'Register Your Application' under 'Other Connections'.
- Follow the on-screen instructions to register and receive your personalized Client-ID code.
- Replace 'XXXXX' with your Client-ID code under clientID in population_tracking.py.

### Notes:

Mouse-over a line to bring up information about the corresponding game.
Current mouse-over information (will add more soon): 
- game name
- viewer count
- top streamer
- stream views

### Required Libraries:

- json - Twitch response data format
- matplotlib - Plotting and animating
- numpy - Used in animation for graph updating

### Updates:
- 04/25/17: Added class functionality

### Known Issues:
- Performance issues
- When a new game enters top 10 list, mouse-over tooltip reports operand type errors (can be ignored).
- Lack of comments, will fix shortly!
