import pyaudio

#OCM_API = 'c65ff83b1f304484be136ec20c542b04'
OCM_API = '4e8668c25d584694bad2213865aa9155' #maybe speaker recognistion
LOCALE = 'en-us'
#speech_key, service_region = "cb6f8ab441c949458dd1c9ee295c2da3", "westus"
speech_key, service_region = "93c66e8e1d374597a1c9d9efd5bf2cd7", "westus" #maybe speech service
profile_info={}

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
