WAVEFORM_SINE=0
DEFAULT=0
class Awaitable: # dummy
    pass
class button:
    def pressed(button: int) -> int:
        ...
    LEFT = 1
    RIGHT = 2
class light:
    def color(light: int, color: int) -> None:
        ...
    POWER=0
    CONNECT=1
class light_matrix:
    def clear() -> None:
        ...
    def get_orientation() -> int:
        ...
    def get_pixel(x: int, y: int) -> int:
        ...
    def set_orientation(top: int) -> int:
        ...
    def set_pixel(x: int, y: int, intensity: int) -> None:
        ...
    def show(pixels: list[int]) -> None:
        ...
    def show_image(image: int) -> None:
        ...
    def write(text: str, intensity: int = 100, time_per_character: int = 500) -> Awaitable:
        ...
    IMAGE_HEART = 1
    IMAGE_HEART_SMALL = 2
    IMAGE_HAPPY = 3
    IMAGE_SMILE = 4
    IMAGE_SAD = 5
    IMAGE_CONFUSED = 6
    IMAGE_ANGRY = 7
    IMAGE_ASLEEP = 8
    IMAGE_SURPRISED = 9
    IMAGE_SILLY = 10
    IMAGE_FABULOUS = 11
    IMAGE_MEH = 12
    IMAGE_YES = 13
    IMAGE_NO = 14
    IMAGE_CLOCK12 = 15
    IMAGE_CLOCK1 = 16
    IMAGE_CLOCK2 = 17
    IMAGE_CLOCK3 = 18
    IMAGE_CLOCK4 = 19
    IMAGE_CLOCK5 = 20
    IMAGE_CLOCK6 = 21
    IMAGE_CLOCK7 = 22
    IMAGE_CLOCK8 = 23
    IMAGE_CLOCK9 = 24
    IMAGE_CLOCK10 = 25
    IMAGE_CLOCK11 = 26
    IMAGE_ARROW_N = 27
    IMAGE_ARROW_NE = 28
    IMAGE_ARROW_E = 29
    IMAGE_ARROW_SE = 30
    IMAGE_ARROW_S = 31
    IMAGE_ARROW_SW = 32
    IMAGE_ARROW_W = 33
    IMAGE_ARROW_NW = 34
    IMAGE_GO_RIGHT = 35
    IMAGE_GO_LEFT = 36
    IMAGE_GO_UP = 37
    IMAGE_GO_DOWN = 38
    IMAGE_TRIANGLE = 39
    IMAGE_TRIANGLE_LEFT = 40
    IMAGE_CHESSBOARD = 41
    IMAGE_DIAMOND = 42
    IMAGE_DIAMOND_SMALL = 43
    IMAGE_SQUARE = 44
    IMAGE_SQUARE_SMALL = 45
    IMAGE_RABBIT = 46
    IMAGE_COW = 47
    IMAGE_MUSIC_CROTCHET = 48
    IMAGE_MUSIC_QUAVER = 49
    IMAGE_MUSIC_QUAVERS = 50
    IMAGE_PITCHFORK = 51
    IMAGE_XMAS = 52
    IMAGE_PACMAN = 53
    IMAGE_TARGET = 54
    IMAGE_TSHIRT = 55
    IMAGE_ROLLERSKATE = 56
    IMAGE_DUCK = 57
    IMAGE_HOUSE = 58
    IMAGE_TORTOISE = 59
    IMAGE_BUTTERFLY = 60
    IMAGE_STICKFIGURE = 61
    IMAGE_GHOST = 62
    IMAGE_SWORD = 63
    IMAGE_GIRAFFE = 64
    IMAGE_SKULL = 65
    IMAGE_UMBRELLA = 66
    IMAGE_SNAKE = 67
class motion_sensor:
    def acceleration(raw_unfiltered: bool) -> tuple[int, int, int]:
        ...
    def angular_velocity(raw_unfiltered: bool) -> tuple[int, int, int]:
        ...
    def gesture() -> int:
        ...
    def get_yaw_face() -> int:
        ...
    def quaternion() -> tuple[float, float, float, float]:
        ...
    def reset_tap_count() -> None:
        ...
    def reset_yaw(angle: int) -> None:
        ...
    def set_yaw_face(up: int) -> bool:
        ...
    def stable() -> bool:
        ...
    def tap_count() -> int:
        ...
    def tilt_angles() -> tuple[int, int, int]:
        ...
    def up_face() -> int:
        ...
    TAPPED = 0
    DOUBLE_TAPPED = 1
    SHAKEN = 2
    FALLING = 3
    UNKNOWN = -1
    TOP = 0
    FRONT = 1
    RIGHT = 2
    BOTTOM = 3
    BACK = 4
    LEFT = 5
class port:
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
class sound:
    def beep(freq: int = 440, duration: int = 500, volume: int = 100, *, attack: int = 0, decay: int = 0, sustain: int = 100, release: int = 0, transition: int = 10, waveform: int = WAVEFORM_SINE, channel: int = DEFAULT) -> Awaitable:
        ...
    def stop() -> None:
        ...
    def volume(volume: int) -> None:
        ...
    ANY = -2
    DEFAULT = -1
    WAVEFORM_SINE = 1
    WAVEFORM_SAWTOOTH = 3
    WAVEFORM_SQUARE = 2
    WAVEFORM_TRIANGLE = 1
def device_uuid() -> str:
    ...
def hardware_id() -> str:
    ...
def power_off() -> int:
    ...
def temperature() -> int:
    ...
