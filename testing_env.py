from serial_monitor import SerialController, Direction


serial_controller = SerialController()
#serial_controller.get_room_data(Direction.CLOCKWISE)
serial_controller.get_room_data(Direction.COUNTER_CLOCKWISE)
#serial_controller.get_room_data(Direction.CLOCKWISE)
