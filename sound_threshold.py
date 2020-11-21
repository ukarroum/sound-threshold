import pyaudio
import argparse
import wave
import audioop

import numpy as np

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second

def tune(seconds=10, multiplier=1.2):
	print("Just speak as you would like to in game :) ")

	p = pyaudio.PyAudio()

	stream = p.open(format=sample_format,
					channels=channels,
					rate=fs,
					frames_per_buffer=chunk,
					input=True)

	all_rms = []
	
	for i in range(0, int(fs / chunk * seconds)):
		data = stream.read(chunk)
		all_rms.append(audioop.rms(data, 2))
	
	print(f"You can use a threshold of : {int(np.mean(all_rms)*multiplier)}")

def run(threshold):
	p = pyaudio.PyAudio()

	stream = p.open(format=sample_format,
					channels=channels,
					rate=fs,
					frames_per_buffer=chunk,
					input=True)
	while(True):
		data = stream.read(chunk)
		if audioop.rms(data, 2) > threshold:
			print("\a")

if __name__ == "__main__":
	COMMANDS = {"tune": tune, "run": run}
	parser = argparse.ArgumentParser()

	parser.add_argument("command", choices=COMMANDS.keys())

	parser.add_argument("--threshold", help="A given threshold above which you start getting beeps, the value is expressed in RMS")

	args = parser.parse_args()

	if args.command == "tune":
		tune()
	elif args.command == "run":
		if args.threshold is not None:
			run(int(args.threshold))
		else:
			print("Error : The threshold parameter is mandatory in the run mode")
	
