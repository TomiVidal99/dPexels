#"""
								#dPexel  0.5
#A simple app with a UI that allows users to download bulk images from #Pexel (image wesbsite)

#"""

############### Imports ###############

from appJar import gui
import constant
from tempfile import TemporaryFile
import os
from apiRequests import search_urls
from apiRequests import download_images
from apiRequests import execute_search


############### FX ###############

def set_():
	# function that executes the searching, gets variables from inputs
	app.threadCallback(execute_search, set_finished, app.getEntry('User key:'), app.getEntry('Searching word:'), constant.search_pages, app.getOptionBox('img_format'), fetch_progress)
	

def set_finished(response):
	# Callback function executed when set has been executed
	max_photos = len(search_urls)
	app.setScaleRange("Number of photos: ", minimum_photos, max_photos, curr=max_photos)
	write_cached_data()

def download():
	# function that downloads desired amount of images from the requested array of urls
	global can_download
	can_download = True
	
	if (len(search_urls) > 0):
		num_of_photos = app.getScale("Number of photos: ")
		app.threadCallback(download_images, download_finished, search_urls, app.getEntry('Path'), num_of_photos, download_progress)
	else:
		print('None urls available, modify search parameters')

def download_finished(response):
	# Callback function executed when download has been completed
	print('download has been completed!!! ', response)

def quit_app():
	# function that executes when the exit button is pressed
	app.stop()

def write_cached_data():
	# function to write temporal data from current instance of the app
	data = open('temp.txt', 'w') 
	if (app.getEntry('User key:') != ''):
		data.writelines(app.getEntry('User key:') + '\n')
	else:
		data.writelines('key\n') 		
	if (app.getEntry('Path') != ''):
		data.writelines(app.getEntry('Path') + '\n')
	else:
		data.writelines('path\n')
	data.close()
	
def read_cached_data():
	# function to read temporal data from previous usages of the app 
	print('reading old data')
	if (os.path.exists('./temp.txt')):
		data = open('temp.txt', 'r') 
		data_ = data.readlines()
		print(data_)
		if (data_[0] != 'key\n'):
			user_key = data_[0].split('\n')[0]
			app.setEntry('User key:', user_key)
			print(user_key)
		if (data_[1] != 'path\n'):	
			path = data_[1].split('\n')[0]
			app.setEntry('Path', path)
			print(path)
	else:
		file = open('temp.txt', 'w')
		file.write('key\n')
		file.write('path\n')


def download_progress(current_porcentaje, current, total):
	# This function is executed every time a image is downloaded and it updates to match the download progress
	def fn(c, n, t):
		app.queueFunction(app.setStatusbar, 'Downloading...   ' + str(c) + '%         ' + str(n) + ' de ' + str(t), 0)
		if (current_porcentaje <= 50):
			app.queueFunction(app.setStatusbarBg, 'red')
		elif (current_porcentaje <= 70):
			app.queueFunction(app.setStatusbarBg, 'yellow')
		elif (current_porcentaje == 100):
			app.queueFunction(app.setStatusbarBg, 'green')
			app.queueFunction(app.setStatusbar, 'Success! ' + str(c) + '%         ' + str(n) + ' de ' + str(t), 0)
	app.thread(fn, current_porcentaje, current, total)


def fetch_progress(current_porcentaje):
	# This function is executed when requesting the images and so it displays the current progress on the progress bar
	def fn(c):
		print(c)
		if (c == 'finished'):
			app.queueFunction(app.setStatusbar, 'Data feched')
			app.queueFunction(app.setStatusbarBg, 'green')
		else:
			app.queueFunction(app.setStatusbar, 'Fetching data...')
			app.queueFunction(app.setStatusbarBg, 'grey')	

	app.thread(fn, current_porcentaje)


def stop_download():
	# Function that executes when stop download button is pressed; and it will do so
	# TODO yet
	print('stopping...')


def KeyPress(key):
	if (key == 	'<Up>'):
		set_()
	elif (key == '<Return>'):
		download()
	else:
		print('Not binding for that key')

############### Define GUI components ##################

app = gui('dPexels', '640x480')

app.setPadding([10, 0])
app.setInPadding([0, 0])

app.setStretch('sides')
app.addLabel('title', 'Download all the images from PEXELS! :)', 0, 0, colspan=4).config(font="Roman 20")

app.addHorizontalSeparator(1, 0, colspan=4, colour="red")

app.addLabelEntry('User key:', 2, 0, colspan=4)

app.addLabel('description', 'You can find your key in this link:', 3, 0, colspan=1).config(font="Helvetica 11")

app.addWebLink('https://www.pexels.com/api/new/', 'https://www.pexels.com/api/new/', 3, 1, colspan=3)

app.addLabelEntry('Searching word:', 5, 0, colspan=4)

app.addOptionBox('img_format', ['original', 'large', 'medium', 'small', 'portrait', 'landscape', 'tiny'], 6, 1, colspan=3)

app.addLabel('Image format: ', 'Image format: ', 6, 0, colspan=1)

app.addLabelEntry('Path', 7, 0,colspan=4)

app.addLabelScale("Number of photos: ", 8, 0,colspan=4)

app.addButton('Set', set_, 9, 0, colspan=1)
app.addButton('Download', download, 9, 1, colspan=1)
app.addButton('Stop download', stop_download, 9, 2, colspan=1)
app.addButton('Exit', quit_app, 9, 3, colspan=1)

app.addStatusbar(fields=1)


############### Config ################################

minimum_photos = 0
max_photos = 0

app.configure(bg='lightgray', fg='black', font={'size':12, 'family': 'Helvica'}, resizable='True')
app.buttonFont = 10
app.setTransparency(100) # 100 means that it is not transparent
app.setLocation('CENTER')
app.setScaleRange("Number of photos: ", minimum_photos, max_photos, curr=0)
app.showScaleValue("Number of photos: ", show=True)

app.setEntryTooltip('User key:', 'You need to make an account on the pexels website and copy your own key')
app.setEntryTooltip('Searching word:', 'A descriptive key word for the images that you are looking for')
app.setLabelTooltip('Number of photos: ', 'Select the amount of photos that you want to download')

app.setStatusbar('Download progress', 0)
app.setStatusbarWidth(100, 0)

#####################################################################################

# set hotkeys

app.bindKey('<Up>', KeyPress)
app.bindKey('<Return>', KeyPress)

################ read if exists previous defined variables ##########################

read_cached_data()

############## Run app #################################

app.go()





