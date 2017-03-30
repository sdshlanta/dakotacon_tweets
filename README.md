# dakotacon_tweets
Kool tweets display for DakotaCon.

# Requirements
## Python
  Python 3+

## Packages
  (Python - see requirements.txt for ez pip installation)
    Tweepy
  (Util)
    jp2a

# Usage
python dakotacon_tweets.py

# Config
## Keys
  CONSUMER\*, ACCESS_TOKEN\* in dakotacon_tweets.py are Twitter API credentials
## Globals
  IMAGE_WIDTH - Width of image for image column. Everything is scaled off of this value (e.g. image height because aspect ratio is maintained, tweets being centered, etc)
  
  LINE_DELAY - Time to sleep between characters being printed in a line. Should pretty small.
  
  ROW_DELAY - Time to sleep between each "row" (e.g. each tweet). 
