from threading import Thread
import datetime
import cv2

class FPS:
	"""docstring for FPS"""
	def __init__(self):
		self._start = None
		self._end = None
		self._numFrames = 0

	def start(self):
		self._start = datetime.datetime.now()
		return self

	def stop(self):
		self._end = datetime.datetime.now()

	def update(self):
		self._numFrames += 1

	def elapsed(self):
		return (self._end - self._start).total_seconds()

	def fps(self):
		return self._numFrames / self.elapsed()		


class videoStream:
	def __init__(self, src=0, name="videoStream", fps=None):

		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		if fps:
			self.stream.set(cv2.CAP_PROP_FPS, fps)
		self.fokus = 0	
		self.name = name

		self.stopped = False

	def start(self):
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	
	def update(self):
		while True:
			if self.stopped:
				return
			
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		return self.grabbed, self.frame

	def stop(self):
		self.stopped = True

	def getWidth(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))

	def getHeight(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

	def getFPS(self):
		return int(self.stream.get(cv2.CAP_PROP_FPS))

	def isOpen(self):
		return self.stream.isOpened()

	def setFramePosition(self, framePos):
		self.stream.set(cv2.CAP_PROP_POS_FRAMES, framePos)

	def getFramePosition(self):
		return int(self.stream.get(cv2.CAP_PROP_POS_FRAMES))

	def getFrameCount(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))

	def setFocus(self):
		self.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
		self.stream.set(cv2.CAP_PROP_FOCUS, self.focus)

class multiCamera(videoStream):
	camAddrList = []
	def __init__(self,camAddrList, setFps=None):
		self.camAddr = camAddrList
		self._cams = []
		self._frames = []

		for cam_Addr in self.camAddr:
			cs = videoStream(src=cam_Addr, fps=setFps).start()
			self._cams.append(cs)


	def capture(self):
		self._frames = []
		for cm in self._cams:
			ret, frame = cm.read()
			if ret:
				self._frames.append(frame)
		return self._frames