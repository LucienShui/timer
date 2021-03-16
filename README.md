# Timer

Python code timer, support block wise and function wise

## Installation

```shell
pip install timer
```

## Usage

1. import
    ```py
    from timer import timer
    ```

2. decorate without brackets
    ```py
    @timer
    def func(): ...
    ```

3. decorate with brackets
    ```py
    @timer()
    def func(): ...
    ```

4. decorate with name and time unit
    ```py
    @timer('function name', 's')
    def func(): ...
    ```

5. decorate with key word arguments
    ```py
    @timer(name='function name', unit='s')
    def func(): ...
    ```
   
6. block wise without object

    ```py
    with timer():
        ...
    ```
   
7. block wise with object
   
    ```py
    with timer() as t:
        ...
        print(t.elapse)
    ```

## Sample Code

```python
import logging
import time

from timer import timer

# timer would print nothing without this line or logging level is info or higher
logging.basicConfig(level=logging.DEBUG)


# explicit the timer's name and it's time unit
@timer('function:add', unit='s')
def add(a, b):
    time.sleep(.1)
    return a + b


# function name is timer's name for default
@timer
def sub(a, b):
    time.sleep(.1)
    return a - b


if __name__ == '__main__':
    # 'timer' would be timer's name by default
    with timer('time.sleep(2)') as t:
        print(3)
        time.sleep(1)
        print(f'after time.sleep(1) once, t.elapse = {t.elapse}')
        time.sleep(1)
        print(f'after time.sleep(1) twice, t.elapse = {t.elapse}')
    print(f'after with, t.elapse = {t.elapse}')

    print(add(1, 1))
    print(sub(2, 1))
```

### Outputs

```plain
3
after time.sleep(1) once, t.elapse = 1.003798776
after time.sleep(1) twice, t.elapse = 2.0052743459999998
DEBUG:timer.time.sleep(2): 2.006 s
after with, t.elapse = 2.005628447
DEBUG:timer.function:add: 0.105 s
2
DEBUG:timer.sub: 102 ms
1
```

## Special Thanks

[@Krzysztof S](https://github.com/papierukartka)
