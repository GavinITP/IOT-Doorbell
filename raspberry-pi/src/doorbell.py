#!/usr/bin/env python

from multiprocessing import Process
import websocket
import RPi.GPIO as GPIO
import time
import signal
import keyboard
import cv2
import base64
import asyncio

GREEN = 5
RED = 7
YELLOW = 11
TRIG = 16
ECHO = 18
BUZZ = 22

L = GPIO.LOW
H = GPIO.HIGH

camConnectionString = 'rtsp://admin:admin@192.168.61.63:8554/live'
# camConnectionString = 'rtsp://admin:admin@192.168.1.181:8554/live'
# webSocketConnectionString = 'ws://192.168.70.193:8080/?type=raspberry_pi'
webSocketConnectionString = 'ws://175.41.178.14:8080?type=raspberry_pi'

imagePath = "/home/pi/snapshot.jpg"

class GracefullKiller:
	kill_signal = False
	def __init__(self):
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)

	def exit_gracefully(self, signum, frame):
		self.kill_signal = True

state = 0
player = cv2.VideoCapture(camConnectionString)
ws = websocket.WebSocket()
usCount = 0

def resetRGB():
	GPIO.output(RED, H)
	GPIO.output(YELLOW, H)
	GPIO.output(GREEN, H)

def sendSnapshot(filePath):
	try:
		with open(filePath, 'rb') as f:
			im = f.read()
			ws.send(im, websocket.ABNF.OPCODE_BINARY)
	except Exception as error:
		print("Error while sending via web socket.", error)

def readSingleFrame():
	repeat = 3
	while repeat:
		good, frame = player.read()
		while player.isOpened() and not good:
			good, frame = player.read()
		repeat=repeat-1
	return good, frame

def readingDataStream():
	try:
		ws.connect(webSocketConnectionString, timeout=15)
	except:
		print("Web socket connection Error")
	global player
	try:
		player.release()
		player = cv2.VideoCapture(camConnectionString)
	except:
		print("Cam Initialize Error")
	try:
		good, frame = readSingleFrame()
		if not good:
			raise ValueError
		cv2.imwrite(imagePath, frame)
		sendSnapshot(imagePath)
	except ValueError:
		print("Connection Error")
		player = cv2.VideoCapture(camConnectionString)
	time.sleep(5)

if __name__ == '__main__':
	killer = GracefullKiller()

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

	# RGB is active low
	GPIO.setup(GREEN, GPIO.OUT)
	GPIO.setup(YELLOW, GPIO.OUT)
	GPIO.setup(RED, GPIO.OUT)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)
	GPIO.setup(BUZZ, GPIO.OUT)

	GPIO.output(BUZZ, L)
	GPIO.output(TRIG, L)
	resetRGB()

	try:
		ws.connect(webSocketConnectionString, timeout=15)
		print("Is connected to web socket:", True)
		ws.sock.settimeout(5)
	except Exception as error:
		print("Error while trying to connect via web socket.", error)

	print("Is connected to IP Cam:", player.isOpened())
	print("Calibrating......")
	time.sleep(2)

	while not killer.kill_signal:
		if state == 0:
			# waiting for person to stand in front of ultrasonic sensor
			GPIO.output(TRIG, H)
			time.sleep(0.00001)
			GPIO.output(TRIG, L)

			while GPIO.input(ECHO) == L:
				start_time = time.time()

			while GPIO.input(ECHO) == H:
				end_time = time.time()

			duration = end_time - start_time
			distance = duration * 17150
			print(distance)
			time.sleep(0.5)

			if distance <= 100 and distance >= 30:
				usCount = usCount+1
			else:
				usCount = 0
			if usCount >= 3:
				state = 1

		elif state == 1:
			usCount = 0
			GPIO.output(YELLOW, L)
			time.sleep(5)

			# readingData Process
			readingDataStream()

			resetRGB()
			state = 2
		elif state == 2:
			# Showing approval result
			print("Waiting for server result")
			try:
				res = ws.recv()
				print(res)
				res = res.split(': ')[1]
				print(res)
			except Exception as error:
				print("Error from  backend response", error)
				ws.connect(webSocketConnectionString, timeout=15)
				ws.sock.settimeout(5)
				res = 0

			if res == "Accept":
				# approved
				GPIO.output(GREEN, L)
			else:
				# rejected
				GPIO.output(RED, L)

			time.sleep(10)
			resetRGB()
			state = 0

	print("Gracefully exited")
	resetRGB()
	GPIO.cleanup()
	player.release()
