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

def retrieve(path,multiscale=False):
	large_flag =  False
	leeches = 0
	'''
	screen = ImageGrab.grab() #screenshot
	screen_np = np.array(screen) #translate it to a format cv2 understands

	screen_np = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)'''

	screen_np = cv2.imread(path,0)
	#screen_np = cv2.cvtColor(screen_np,cv2.COLOR_RGB2BGR)
	#screen_np = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
	print('red imagae file...')

	res = cv2.matchTemplate(screen_np,tmpl,cv2.TM_CCORR_NORMED) 
	res2 = cv2.matchTemplate(screen_np,large,cv2.TM_CCORR_NORMED)
	
	loc = np.where(res >= threshold)

	#run the image detection on screenshot
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) 
	min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res2) #get the location and accuracy val
	
	print(f"detection rate: {max_val}")
	if   max_val > 0.8 :
		print('detected winterface!  \n')
		#print('with threshold of: ',max_val)
		#cv2.imwrite('resources/scrnshotforcompare.png',screen_np)

		for pt in zip(*loc[::-1]):
			leeches = leeches + 1

		if max_val1 >= 0.99:
			large_flag = True
			#print('large floor')

		#optional in testing:	
		#now we need to crop the parts we need and run text detection

		floor_num = screen_np[max_loc[1]+56:max_loc[1]+78,max_loc[0]+41:max_loc[0]+94]
		bon_num = screen_np[max_loc[1]+136:max_loc[1]+164,max_loc[0]+297:max_loc[0]+332]
		time_num = screen_np[max_loc[1]+300:max_loc[1]+321,max_loc[0]+34:max_loc[0]+82]
		mod_num = screen_np[max_loc[1]+157:max_loc[1]+182,max_loc[0]+297:max_loc[0]+331]

		image_np = np.array(floor_num)
		image_np2 = np.array(bon_num)
		image_np3 = np.array(time_num)
		image_np4 = np.array(mod_num)


		floor = OCR.apply_ocr(bitmaps,image_np)
		bon =  OCR.apply_ocr(bitmaps,image_np2)
		time = OCR.apply_ocr(bitmaps,image_np3)
		mod = OCR.apply_ocr(bitmaps,image_np4)
		
		winterface = [floor,bon,time,mod]
	
		if bon :
			line =  '[' + winterface[0] + '] ' + '[ bon : ' +  winterface[1]+ '] ' + '[ time : ' + winterface[2] + '] ' +'[ mod : ' + winterface[3]+ ']'
		blank_line = True

		if "Floor" in floor:
			blank_line = False
			print('successfully captured a floor winterface!')
			print(winterface)

		if blank_line == False:
			winsound.Beep(2500,1500)
			log = open("log.txt",'a+')

			if large_flag:
				line += '\t LARGE ' + category[leeches] + '\n'
			else :
				line += '\t MED/SMALL ' + category[leeches] + '\n'	

			log.write(line)
			if large_flag:
				line = floor[8:] + " " + " " + bon + " " + time+ " " + mod + " LARGE"
			else :
				line = floor[8:] + " " + " " + bon + " " + time+ " " + mod + " MED/SMALL"

			log.close()
			blank_line = True
			notification.notify(
			title='Winterface found!',
			message='logged floor...',
			app_name='Winterface',
			)

			time_ = time.split(':')
			return line

			
			

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


category = {1:'4s',2:'trio',3:'duo',4:'solo',0:'1:1'}




