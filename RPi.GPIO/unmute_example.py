try:
    import RPi.GPIO as GPIO 
except RuntimeError:
    print( f'{__name__} error: RPi.GPIO import error - probably you not use the "sudo" statement to run the .py file')

import sys 

MUTE_GPIO = 17
FALT_GPIO = 27

if __name__ == '__main__':

  args = sys.argv 
  print( "Unmute file - to unmute the amp use '& python3 unmute.py 0'")
  print( "Args:", args )

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings( False )
  GPIO.setup( MUTE_GPIO, GPIO.OUT )
  GPIO.setup( FALT_GPIO, GPIO.IN )

  if len( args ) == 2:
    GPIO.output( MUTE_GPIO, GPIO.HIGH if bool(args[1]) else GPIO.LOW )
    print( 'Mutted' if args[1] == '1' else 'Unmutted')
  else:
    GPIO.output( MUTE_GPIO, GPIO.HIGH )
    print( 'No arguments are used, system mutted')

  print( f'System fault: [{GPIO.input(FALT_GPIO)}] {"NOT FAULT" if GPIO.input( FALT_GPIO ) else "FAULT"}' )
