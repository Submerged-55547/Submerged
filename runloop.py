def run(*functions: Awaitable) -> None:
    ...
def sleep_ms(duration: int) -> Awaitable:
    ...
def until(function: Callable[[], bool], timeout: int = 0) -> Awaitable:
    ...
