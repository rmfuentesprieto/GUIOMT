from omt.controller.source.beam_scanner.move_xy import MoveXY

move_xy = MoveXY('192.168.1.62',9988)
move_xy.start_connection()
print move_xy.ask_position()
print move_xy.set_origin()
print move_xy.ask_position()
move_xy.close_connection()