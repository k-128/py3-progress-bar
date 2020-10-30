import shutil
import sys
import time
from functools import partial


def _with_progress_bar(func, symbol="■"):
    '''Decorator: Progress bar

    Params:
        [str] symbol > default: ■
            ex: ■, ░, □, ○, #
    '''
    def _func_with_progress_bar(*args, **kwargs):
        max_width, _ = shutil.get_terminal_size()
        gen = func(*args, **kwargs)
        while True:
            try:
                progress = next(gen)
            except StopIteration as e:
                sys.stdout.write("\n")
                return e.value
            else:
                space_to_pct = [3, 2, 1][len(str(progress)) - 1]
                message = f"[%s]{' ' * space_to_pct}{progress}%%"
                bar_width = max_width - len(message) + 2
                filled = int(round(bar_width / 100 * progress))
                space_left = bar_width - filled
                bar = f"{symbol * filled}{' ' * space_left}"
                sys.stdout.write(f"{message}\r" % bar)
                sys.stdout.flush()

    return _func_with_progress_bar


with_progress_bar = partial(_with_progress_bar, symbol="■")


@with_progress_bar
def test():
    yield 0
    time.sleep(2.5)
    yield 10
    time.sleep(1.5)
    yield 25
    for i in range(26, 101):
        time.sleep(0.1)
        yield i

    return "world"


if __name__ == "__main__":
    result = test()
    print(f"hello {result}")

