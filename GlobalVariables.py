import pyaudio

OCM_API = '' #maybe speaker recognistion API
LOCALE = 'en-us'
speech_key, service_region = "", "westus" #maybe speech service api
profile_info={}

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
