""" PI PINOUTS """
SHOCK_PIN = 4                           # OUTPUT
LED_PINS = [17, 27]                       # OUTPUT
SENSE_PINS = [16, 20, 12, 23, 24, 7, 8, 25]   # INPUT


""" OPERATION PARAMETERS """
saveimg_path = '/home/pi/imgs'

window_update_hz = 10
window_size_s = 5
led_strobe_hz = 10


""" CAMERA PARAMETERS """
video_resolution = (1920, 1080)


""" MOTION DETECT PARAMETERS """



""" OBJECT DETECT PARAMETERS """



""" CHOPPING PARAMETERS """
crust_thickness_mm = 8
fine_slice_mm = 1
coarse_slice_mm = 3
dice_spacing_mm = 5


""" AUDIO STUFF """
audio_path = 'media'
audio_catagories = {
    'tea': 'tea',
    'chop': 'chop',
    'thud': 'thud',
    'safen': 'safen',
    'safes': 'safes',
    'score': 'score',
    'oops': 'oops',
    'thank': 'thank'
}  # I know this dict is useless now but eh it's fine, 'futureproofing' ya?
freq = 44100
bitsize = -16
channels = 2
buffer = 2048
volume = 0.95


""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_FRAMES = True
