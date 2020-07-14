try:
    from PIL import ImageGrab
except ImportError:
    import Image
import time as TIME
import cv2
import numpy as np
import winsound
import OCR
from plyer import notification
import rsn


def get_data(s,e,path):
	found = False
	for i in np.arange(25, 150, 25).tolist():
		print(f'using scale: {i}% original size...')
		res = retrieve(path,scale=i)
		if res:
			print('quitting loop')
			break

	return res

def count_players(screen_np):
	res_ = cv2.matchTemplate(screen_np,player,cv2.TM_CCOEFF_NORMED)
	res2_ = cv2.matchTemplate(screen_np,leech,cv2.TM_CCOEFF_NORMED)

	threshold_ = 0.7 #originally at 0.9
	players = 0 
	leeches = 0

	loc = np.where( res_ >= threshold_)
	loc2 = np.where( res2_ >= threshold_)


	for pt in zip(*loc[::-1]):
		players += 1

	for i in zip(*loc2[::-1]):
		leeches += 1
	

	return (players,leeches)

	    



def retrieve(path,scale=1):
	large_flag =  False
	


	screen_np = cv2.imread(path,0)
	width = int(screen_np.shape[1] * scale / 100)
	height = int(screen_np.shape[0] * scale / 100)
	dim = (width, height)
	# resize image
	screen_np = cv2.resize(screen_np, dim, interpolation = cv2.INTER_LINEAR)
		
				
	print('processing...')
	res = None
	res2 = None
	try:
		res = cv2.matchTemplate(screen_np,tmpl,cv2.TM_CCORR_NORMED) 
		res2 = cv2.matchTemplate(screen_np,large,cv2.TM_CCORR_NORMED)
	

		loc = np.where(res >= threshold)

		#run the image detection on screenshot
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) 
		min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res2) #get the location and accuracy val
		
		print(f"detection rate: {max_val}")
		if max_val < 0.8:
			return None

		if   max_val > 0.8 :
			print('detected winterface!  \n')
			#print('with threshold of: ',max_val)
			#cv2.imwrite('resources/scrnshotforcompare.png',screen_np)


			if max_val1 >= 0.99:
				large_flag = True
				#print('large floor')

			#optional in testing:	
			#now we need to crop the parts we need and run text detection

			floor_num = screen_np[max_loc[1]+56:max_loc[1]+78,max_loc[0]+41:max_loc[0]+94]
			bon_num = screen_np[max_loc[1]+136:max_loc[1]+164,max_loc[0]+297:max_loc[0]+332]
			time_num = screen_np[max_loc[1]+300:max_loc[1]+321,max_loc[0]+34:max_loc[0]+82]
			mod_num = screen_np[max_loc[1]+157:max_loc[1]+182,max_loc[0]+297:max_loc[0]+331]
			name = screen_np[max_loc[1]+40:max_loc[1]+55,max_loc[0]+364:max_loc[0]+486]


			'''debug'''
			#cv2.imshow('name',name)
			#cv2.waitKey(0)
			'''end of debug'''
			image_np = np.array(floor_num)
			image_np2 = np.array(bon_num)
			image_np3 = np.array(time_num)
			image_np4 = np.array(mod_num)
			image_np5 = np.array(name)

			name_ = rsn.get_rsn(image_np5)
			floor = OCR.apply_ocr(bitmaps,image_np)
			print(floor)
			bon =  OCR.apply_ocr(bitmaps,image_np2)
			time = OCR.apply_ocr(bitmaps,image_np3)
			mod = OCR.apply_ocr(bitmaps,image_np4)
			
			winterface = [name_ ,floor,bon,time,mod]
		
			if bon :
				line =  winterface[0] + ' ' + winterface[1] + ' '  +  winterface[2] + ' ' + winterface[3] + ' '  + winterface[4]+ ' '
			blank_line = True

			if "Floor" in floor:
				blank_line = False
				print('successfully captured a floor winterface!')
				print(winterface)
			
			try:
				players_and_leechers = (0,0)
				players_and_leechers = count_players(screen_np)
				print(players_and_leechers)
			except Exception as e:
				print('problem with count_players func',e)


			if blank_line == False:
				winsound.Beep(2500,1500)
				log = open("log.txt",'a+')

				if large_flag:
					line += '\t LARGE ' + '\n'
				else :
					line += '\t MED/SMALL ' + '\n'	

				log.write(line)

				cat = {1: '1s',2:'2s',3:'3s',4:'4s',5:'5s'}
				cat_ = cat[players_and_leechers[0] - players_and_leechers[1]]

				if players_and_leechers == (1,0):
					cat_ =  '1:1'

				if large_flag:
					line = name_ + ',' + floor[8:] + "," +  bon + "," + time+ "," + mod + ", LARGE" + ',' + cat_
				else :
					line = name_ + ',' + floor[8:] + ","  + bon + "," + time+ "," + mod + ", MED/SMALL" + ',' + cat_

				log.close()
				blank_line = True

				time_ = time.split(':')
				return line
	except Exception as e:
		print(e)
		print('failed...')

			
			

zero = [cv2.imread("resources/bitmaps/0.bmp",0),'0',0]
nine = [cv2.imread("resources/bitmaps/9.bmp",0),'9',0]
seven = [cv2.imread("resources/bitmaps/7.bmp",0),'7',0]
plus = [cv2.imread("resources/bitmaps/+.bmp",0),'+',0]
six = [cv2.imread("resources/bitmaps/6.bmp",0),'6',0]
two = [cv2.imread("resources/bitmaps/2.bmp",0),'2',0]
eight = [cv2.imread("resources/bitmaps/8.bmp",0),'8',0]
three = [cv2.imread("resources/bitmaps/3.bmp",0),'3',0]
four = [cv2.imread("resources/bitmaps/4.bmp",0),'4',0]
minus = [cv2.imread("resources/bitmaps/-.bmp",0),'-',0]
precent = [cv2.imread("resources/bitmaps/%.bmp",0),'%',0]
one = [cv2.imread("resources/bitmaps/1.bmp",0),'1',0]
colon = [cv2.imread("resources/bitmaps/colon.bmp",0),':',0]
five = [cv2.imread("resources/bitmaps/5.bmp",0),'5',0]
floor = [cv2.imread("resources/bitmaps/floor.png",0),'Floor - ',0]
b0 = [cv2.imread("resources/bitmaps/0_.png",0),'0',0]
b1 = [cv2.imread("resources/bitmaps/1_.png",0),'1',0]
b2 = [cv2.imread("resources/bitmaps/2_.png",0),'2',0]
b3 = [cv2.imread("resources/bitmaps/3_.png",0),'3',0]
b4 = [cv2.imread("resources/bitmaps/4_.png",0),'4',0]
b5 = [cv2.imread("resources/bitmaps/5_.png",0),'5',0]
b6 = [cv2.imread("resources/bitmaps/6_.png",0),'6',0]
b7 = [cv2.imread("resources/bitmaps/7_.png",0),'7',0]
b8 = [cv2.imread("resources/bitmaps/8_.png",0),'8',0]
b9 = [cv2.imread("resources/bitmaps/9_.png",0),'9',0]

bitmaps = [zero,one,floor,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,colon,five,minus,precent,two,three,four,six,seven,eight,nine,plus]

max_detect_allowed = 1319208576.0
threshold = 0.9

tmpl = cv2.imread("resources/newtmp.png",0)  #get the template ready as cv2
large = cv2.imread("resources/large.png",0)
leech = cv2.imread("resources/leech.png",0)
player = cv2.imread("resources/player.png",0)


category = {1:'4s',2:'trio',3:'duo',4:'solo',0:'1:1'}




