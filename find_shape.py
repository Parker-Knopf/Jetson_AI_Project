from cv2 import threshold
import jetson.inference
import jetson.utils

import argparse
import sys, os

import random
import time

class FindShape():
	'''Distinguish Shape through visual imaging'''

	def __init__(self):
		# parse the command line
		parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

		parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
		parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
		parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
		parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
		parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

		try:
			self.opt = parser.parse_known_args()[0]
		except:
			print("")
			parser.print_help()
			sys.exit(0)

		# load the object detection network
		self.net = jetson.inference.detectNet(self.opt.network, sys.argv, self.opt.threshold)

		# create video sources & outputs
		self.input = jetson.utils.videoSource(self.opt.input_URI, argv=sys.argv)
		self.output = jetson.utils.videoOutput(self.opt.output_URI, argv=sys.argv)

	def determineClass(self):
		# capture the next image
		img = self.input.Capture()

		# detect objects in the image (with overlay)
		detections = self.net.Detect(img, overlay=self.opt.overlay)

		# print the detections
		# print("detected {:d} objects in image".format(len(detections)))

		# for detection in detections:
		# 	print(detection)

		# render the image
		self.output.Render(img)

		# update the title bar
		self.output.SetStatus("{:s} | Network {:.0f} FPS".format(self.opt.network, self.net.GetNetworkFPS()))

		# print out performance info
		# self.net.PrintProfilerTimes()

		# exit on input/output EOS
		if not self.input.IsStreaming() or not self.output.IsStreaming():
			return 'null'
		
		for detection in detections:
			return (detection.ClassID)

		return 'null'

class Password():

	def __init__(self):
		self.findShape = FindShape()

		self.num = 2
		self.parameters = ['circle', 'square']
		self.password = self.createPassword()
		self.getshape()


	def createPassword(self):
		password = []
		print("Password:")
		for i in range(0, self.num):
			print(i)
			password.append(random.choice(self.parameters))
			print(f"element {i}: {password[i]}")

		return password

	def checkPassword(self, attempt):
		if attempt == self.password:
			return True
		return False

	def getshape(self):
		classID = self.findShape.determineClass()
		if classID == int(1):
			return self.parameters[0]
		elif classID == int(2):
			return self.parameters[1]
		return 'null'

	def main(self):
		'''main running loop'''

		try:

			self.createPassword()
			print('\n########## OBJECT PASSWORD PROTOTYPE ##########\n')
			do = 1
			while do:
				print('Try to guess the password now by placing either a circle or square in the frame of the camera.')

				attempt= []
				threshold = 2
				for i in range(0, self.num):
					print(f"\nPlace object in camera frame now for password element: {i}")
					while self.getshape() == 'null':
						pass
					time_start = time.time()
					while self.getshape() != 'null' and ((time.time() - time_start) < threshold):
						attempt.append(self.getshape())
					time_stop = time.time()			
					duration = time_stop - time_start
					if duration < threshold:
						print("NOPE", i)
						i = i - 1
					else:
						print(f"Recorded element {i}: {attempt[i]}")

						print("\nRemove object from frame now:")

						while self.getshape() == attempt[i]:
							pass
				
				if self.checkPassword(attempt):
					print("Succefuly guessed the password!\n")
					do = 0
				else:
					print("Password incorrect, try again\n")

		except KeyboardInterrupt:
			pass


if __name__ == "__main__":
	password = Password()
	password.main()