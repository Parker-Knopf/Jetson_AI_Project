from cv2 import threshold
import jetson.inference
import jetson.utils

import argparse
import sys

import random
import time

class FindShape():
	'''Distinguish Shape through visual imaging'''

	def __init__(self):
		# parse the command line
		self.parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

		self.parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
		self.parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
		self.parser.add_argument("--network", type=str, default="googlenet", help="pre-trained model to load (see below for options)")
		self.parser.add_argument("--camera", type=str, default="0", help="index of the MIPI CSI camera to use (e.g. CSI camera 0)\nor for VL42 cameras, the /dev/video device to use.\nby default, MIPI CSI camera 0 will be used.")
		self.parser.add_argument("--width", type=int, default=1280, help="desired width of camera stream (default is 1280 pixels)")
		self.parser.add_argument("--height", type=int, default=720, help="desired height of camera stream (default is 720 pixels)")
		self.parser.add_argument('--headless', action='store_true', default=(), help="run without display")

		try:
			self.opt = self.parser.parse_known_args()[0]
		except:
			print("")
			self.parser.print_help()
			sys.exit(0)

		# load the object detection network
		self.net = jetson.inference.imageNet(self.opt.network, sys.argv)

		# create video sources & outputs
		self.input = jetson.utils.videoSource(self.opt.input_URI, argv=sys.argv)
		self.output = jetson.utils.videoOutput(self.opt.output_URI, argv=sys.argv)
		self.font = jetson.utils.cudaFont()

	def determineClass(self):
		# capture the next image
		img = self.input.Capture()

		# classify the image
		class_id, confidence = self.net.Classify(img)

		# find the object description
		class_desc = self.net.GetClassDesc(class_id)

		# overlay the result on the image	
		self.font.OverlayText(img, img.width, img.height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, self.font.White, self.font.Gray40)
		
		# render the image
		self.output.Render(img)

		# update the title bar
		self.output.SetStatus("{:s} | Network {:.0f} FPS".format(self.net.GetNetworkName(), self.net.GetNetworkFPS()))

		# print out performance info
		#self.net.PrintProfilerTimes()

		# exit on input/output EOS
		if not self.input.IsStreaming() or not self.output.IsStreaming():
			return
		
		return class_id

class Password():

	def __init__(self):
		self.findShape = FindShape()

		self.num = 2
		self.parameters = ['circle', 'square']
		self.password = self.createPassword(self.num, self.parameters)


	def createPassword(self, num, parameters):
		password = [num]
		for i in range(0, num-1):
			print(i)
			password[i] = random.choice(parameters)
		return password

	def checkPassword(self, attempt):
		if attempt == self.password:
			return True

	def getshape(self):
		print("Class", self.findShape.determineClass())
		return self.findShape.determineClass()

	def main(self):
		'''main running loop'''

		try:

			print('\nA new password has been created!\n')
			self.createPassword(self.num, self.parameters)
			do = 1
			while do:
				print('Try to guess the password now by placing either a circle or square in the frame of the camera.')

				attempt= [self.num]
				for i in range(0, self.num-1):
					while self.getshape == 'null':
						pass
					time_start = time.time()
					while self.getshape != 'null':
						attempt[i] = self.getshape()
					time_stop = time.time()			
					threshold = time_stop - time_start
					if threshold < 1:
						i = i - 1
					else:
						print("Recorded:", attempt[i])
				
				if self.checkPassword(attempt):
					print("Succefuly guessed the password!")
					do = 0
				else:
					print("Password incorrect, try again")

		except KeyboardInterrupt:
			pass


if __name__ == "__main__":
	password = Password()
	password.main()