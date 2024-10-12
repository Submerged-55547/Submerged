def absolute_position(port: int) -> int:
    ...
def get_duty_cycle(port: int) -> int:
    ...
def relative_position(port: int) -> int:
    ...
def reset_relative_position(port: int, position: int) -> None:
    ...
def run(port: int, velocity: int, *, acceleration: int = 1000) -> None:
    ...
def run_for_degrees(port: int, degrees: int, velocity: int, *, stop: int = BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable:
    ...
def run_for_time(port: int, duration: int, velocity: int, *, stop: int = BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable:
    ...
def run_to_absolute_position(port: int, position: int, velocity: int, *, direction: int = motor.SHORTEST_PATH, stop: int = BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable:
    ...
def run_to_relative_position(port: int, position: int, velocity: int, *, stop: int = BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable:
    ...
def set_duty_cycle(port: int, pwm: int) -> None:
    ...
def stop(port: int, *, stop: int = BRAKE) -> None:
    ...
def velocity(port: int) -> int:
    ...
READY = 0
RUNNING = 1
STALLED = 2
CANCELLED = 3
ERROR = 4
DISCONNECTED = 5
COAST = 0
BRAKE = 1
HOLD = 2
CONTINUE = 3
SMART_COAST = 4
SMART_BRAKE = 5
CLOCKWISE = 0
COUNTERCLOCKWISE = 1
SHORTEST_PATH = 2
LONGEST_PATH = 3
