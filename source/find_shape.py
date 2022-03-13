import jetson.inference
import jetson.utils

import argparse
import sys

class FindShape():
	'''Distinguish Shape through visual imaging'''

	def __init__():
		# parse the command line
		self.parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

		self.parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
		self.parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
		self.parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
		self.parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
		self.parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 
		
		try:
			self.opt = self.parser.parse_known_args()[0]
		except:
			print("")
			self.parser.print_help()
			sys.exit(0)

		# load the object detection network
		self.net = jetson.inference.detectNet(self.opt.network, sys.argv, self.opt.threshold)

		# create video sources & outputs
		self.input = jetson.utils.videoSource(self.opt.input_URI, argv=sys.argv)
		self.output = jetson.utils.videoOutput(self.opt.output_URI, argv=sys.argv)

	def main(self):
		'''Main Loop'''
		try:
			while True:
				# capture the next image
				self.img = input.Capture()

				# detect objects in the image (with overlay)
				self.class_indx, self.confidence = net.Detect(self.img, overlay=opt.overlay)

				# print the detections
				print("detected {:d} shapes in image".format(len(class_index)))

				print(class_index)

				# render the image
				output.Render(self.img)

				# update the title bar
				output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

				# print out performance info
				net.PrintProfilerTimes()

				# exit on input/output EOS
				if not input.IsStreaming() or not output.IsStreaming():
					break

		except KeyboardInterrupt:
			pass

if __name__ == "__main__":
	findshape = FindShape()
	findshape.main()