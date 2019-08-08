#"""
								#dPexel  0.5
#A simple app with a UI that allows users to download bulk images from #Pexel (image wesbsite)

#"""

############### Imports ###############

from appJar import gui
import constant
from tempfile import TemporaryFile
import os
from apiRequests import execute_search
from apiRequests import search_urls
from apiRequests import download_images

############### FX ###############

current_porcentage = 0

def set_():
	# function that executes the searching, gets variables from inputs
	app.thread(execute_search, app.getEntry('User key:'), app.getEntry('Searching word:'), constant.search_pages, app.getOptionBox('img_format'))
	max_photos = len(search_urls)
	app.setScaleRange("Number of photos: ", minimum_photos, max_photos, curr=max_photos)
	write_cached_data()

def download():
	# function that downloads desired amount of images from the requested array of urls
	num_of_photos = app.getScale("Number of photos: ")
	app.thread(download_images, search_urls, app.getEntry('Path'), num_of_photos)

def quit_app():
	# function that executes when the exit button is pressed
	app.stop()

def write_cached_data():
	# function to write temporal data from current usage of the app
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

def porcentage(current_porcentaje):
	# This function is executed every time a image is downloaded and it updates to match the download progress
	print('function executed')
	app.setStatusbar('Downloading...', current_porcentaje)
	if (current_porcentaje <= 50):
		app.setStatusbarBg('red')
	elif (current_porcentaje <= 70):
		app.setStatusbarBg('yellow')
	elif (current_porcentaje == 100):
		app.setStatusbarBg('green')
		app.setStatusbar('Success!', current_porcentaje)
		


############### Define GUI components ##################

app = gui('dPexels', '640x480')

app.setPadding([10, 0])
app.setInPadding([0, 0])

app.setStretch('sides')
app.addLabel('title', 'Download all the images from PEXELS! :)', 0, 0, colspan=3).config(font="Roman 20")
app.addHorizontalSeparator(1, 0, 3, colour="red")
app.addLabelEntry('User key:', 2, 0, colspan=3)
app.addLabel('description', 'You can find your key in this link:', 3, 0, colspan=1).config(font="Helvetica 11")
app.addWebLink('https://www.pexels.com/api/new/', 'https://www.pexels.com/api/new/', 3, 1, colspan=2)
app.addLabelEntry('Searching word:', 5, 0, colspan=3)
app.addOptionBox('img_format', ['original', 'large', 'medium', 'small', 'portrait', 'landscape', 'tiny'], 6, 1, colspan=2)
app.addLabel('Image format: ', 'Image format: ', 6, 0, colspan=1)
app.addLabelEntry('Path', 7, 0,colspan=3)
app.addLabelScale("Number of photos: ", 8, 0,colspan=3)
app.addButton('Set', set_, 9, 0, colspan=0)
app.addButton('Download',download, 9, 1, colspan=0)
app.addButton('Exit',quit_app, 9, 2, colspan=0)
app.setStatusbar('Download progress', 0)


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


############### Sets in its own thread the function download_images so the app wont frezee when downloading ################

app.thread(porcentage, current_porcentage)

################ read if exists previous defined variables ##########################

read_cached_data()

############## Run app #################################


app.go()





