from pymata4 import pymata4
import sys, time
board = pymata4.Pymata4()

def servo(my_board, i):
    my_board.servo_write(5, i)
    my_board.servo_write(6, 180-i)
    time.sleep(1)


try:
    board.set_pin_mode_servo(5)
    board.set_pin_mode_servo(6)
    board.servo_write(5, 75)
    board.servo_write(6, 75)
    while True:
        angle = int(input("각: "))
        servo(board, angle)

except KeyboardInterrupt:
         board.shutdown()
         sys.exit(0)        
