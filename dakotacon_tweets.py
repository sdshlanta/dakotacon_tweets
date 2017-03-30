import tweepy
import sys, subprocess, shutil, string, time

class DakotaConStreamListener(tweepy.StreamListener):

    TERM_GREEN = "\033[1;32;40m"
    TERM_WHITE = "\033[0;37;40m"
	def __init__(self, logo = None, image_width = 50, line_delay = 0.0001, row_delay = 1):
		super().__init__()


		raw_term_size = shutil.get_terminal_size((50,50))

		self.term_height = int(raw_term_size.lines)
		self.term_width = int(raw_term_size.columns)

		self.count = 0
        self.logo = logo
        self.image_width = image_width
        self.line_delay = line_delay
        self.row_delay = row_delay
		
	def on_status(self, status):
		tweet = status

		tweet_text = self.clean_tweet(tweet.text)

		if "media" in tweet.entities \
			and tweet.entities["media"][0]["type"] == "photo" \
			and tweet.entities["media"][0]["media_url"][-3:] == "jpg":

			image_url = tweet.entities["media"][0]["media_url"]
			ascii_image = self.image_to_ascii(image_url)
		else:
			ascii_image = self.logo

			ascii_image = self.add_username_to_image(ascii_image, tweet.user.screen_name)


		self.print_row(tweet_text, ascii_image)

		return True

	def on_error(self, status_code):
		print("[!] Error: {}".format(status_code))

		return True

	def on_timeout(self):
		print("timeout...")

		return True

	def image_to_ascii(self, url):
		ascii_image = subprocess.check_output(["jp2a", "--width=" + str(self.image_width), url], universal_newlines=True).rstrip()

		return ascii_image

	def add_username_to_image(self, ascii_image, username):
		adjust = 0

		ascii_image_rows = ascii_image.split("\n")

		row_above = ascii_image_rows[-4]
		row_for_user = ascii_image_rows[-3]
		row_below = ascii_image_rows[-2]

		username = "@" + username

		midpoint = len(row_for_user) // 2
		user_midpoint = len(username) // 2

		start_edge = midpoint - user_midpoint
		end_edge = midpoint + user_midpoint + adjust

		if len(username) % 2:
			adjust = 1	

		row_above = row_above[:start_edge - 2] + " " * (len(username) + 2) + row_above[end_edge + adjust:]
		row_with_user = row_for_user[:start_edge - 2] + " " + username + " " + row_for_user[end_edge + adjust:]
		row_below = row_below[:start_edge - 2] + " " * (len(username) + 2) + row_below[end_edge + adjust:]

		ascii_image_rows[-4] = row_above
		ascii_image_rows[-3] = row_with_user
		ascii_image_rows[-2] = row_below

		return "\n".join(ascii_image_rows)

	def clean_tweet(self, text):

		text = "".join([c for c in text if c in string.ascii_letters or c in string.punctuation or c == " "])

		return text

	def print_row(self, text, ascii_image):
		tweet_chunk_len = 50

		ascii_image_rows = ascii_image.split("\n")
		image_height = len(ascii_image_rows)
		image_midpoint = image_height / 2

		chunked_tweet = [text[i:i+tweet_chunk_len] for i in range (0, len(text), tweet_chunk_len)]
		tweet_height = len(chunked_tweet)

		print(self.build_output_line(self.term_width, self.count, "", "", divider=True))
		self.count += 16
		for row in enumerate(ascii_image_rows):

			if abs(row[0] - image_midpoint) <= 1 and len(chunked_tweet) > 0:
				line = self.build_output_line(self.term_width, self.count, chunked_tweet.pop(0), row[1])
			else:
				line = self.build_output_line(self.term_width, self.count, "", row[1])

			self.print_output(line)

			self.count += 16

		time.sleep(ROW_DELAY)

		return

	def build_output_line(self, width, count, text, ascii_image_row, divider=False):
		filler = "="

		line = "|"
		line += " {0:#0{1}x} ".format(count, 8) # print hex in format: 0x00000000
		line += "|"

		if divider:

			line = line.ljust(width - self.image_width - 2, filler) # tweet column
			line += "|"
			line = line.ljust(width - 1, filler) # image column
			line += "|"

		else:
			width -= len(line)
			
			line += text.center(width - self.image_width - 2, ".") # tweet column
			line += "|"
			line += ascii_image_row # image column
			line += "|"
	
		return line

	def print_output(self, line):

		for c in line:
			print(c, end="")
			time.sleep(self.line_delay)
			
		print("\n", end="")

		return

def main():
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""

    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""

    IMAGE_WIDTH = 50
    LINE_DELAY = 0.0001
    ROW_DELAY = 1
    
    LOGO = subprocess.check_output(["jp2a", "--width=" + str(IMAGE_WIDTH), "logo.jpg"], universal_newlines=True).rstrip()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    dakotacon_listener = DakotaConStreamListener(LOGO, IMAGE_WIDTH, LINE_DELAY, ROW_DELAY)
    dakotacon_stream = tweepy.Stream(auth=api.auth, listener=dakotacon_listener)

    # Don't leave terminal bright green
    print(DakotaConStreamListener.TERM_GREEN)
    try:
        dakotacon_stream.filter(track=["dakotacon"])
    except:
        print(DakotaConStreamListener.TERM_WHITE)

if __name__ == '__main__':
    main()		
