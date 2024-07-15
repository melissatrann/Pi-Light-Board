# Pi Light Board

This repository implements models of physical data given by a set of Neopixel LEDs, providing several utility functions to easily separate and program Neopixel rings. 
In particular, each ring is given its own object, which can then be manipulated more easily as an isolated unit. In addition, a FixedLengthBuffer with built in iterator
is implemented to facilitate the use of a moving average to make sensor data more reliable.

## Code Quality Guidelines
- Please ensure your indentation is four spaces.
- Comment every function, no matter how small. Good documentation will help for anyone else that wants to use this in the future!
- Use multi-line strings for top-level function and class comments, like so:
```python
def foo(self, arg1, arg2):
    """
    Describe what this function does.

    :param arg1: description of the first parameter
    :param arg2: description of the second parameter
    :return: description of the return value
    """
    return arg1 + arg2
```
- Manual type hints are OK, but not necessary.
- Avoid magic numbers/strings. Constants should be `NAMED = "named"`.
- Write "Pythonic" code. Prefer
```python
# list comprehensions
[x + 1 for x in num_list if x % 2 == 0]
```
over
```python
# manual iteration
for i in range(len(num_list)):
    if num_list[i] % 2 == 0:
        num_list[i] += 1
```

Thank you!

## (Current) Order and Size of Neopixel Rings
Diversity x24 -- Challenge x16 -- Motivate x12 -- Discovery x16 -- Imagine x16 -- Inspire x24 -- Love x12 -- Joy x24
