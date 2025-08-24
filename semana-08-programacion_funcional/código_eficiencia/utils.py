from functools import wraps
from threading import Thread
from os import path
import timeit
import tracemalloc



def timeout(seconds=10, error_message=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if error_message is None:
                final_message = (
                    f"El código no finaliza dentro del tiempo máximo asignado ({seconds} seg)."
                )
            else:
                final_message = error_message

            result = [Exception(final_message)]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e

            thread = Thread(target=target, daemon=True)
            thread.start()
            thread.join(seconds)
            if isinstance(result[0], Exception):
                raise result[0]

            return result[0]
        return wrapper
    return decorator


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        end = timeit.default_timer()
        print(f"\nTiempo ejecución {func.__name__:<25} {end - start:.5f} segundos", end="")
        return result
    return wrapper


def memory_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        _, memory_peak = tracemalloc.get_traced_memory()
        memory_peak /= 2**20
        print(f"\nUso memoria {func.__name__:<25}      {memory_peak:.2f} MB ", end="")
        tracemalloc.stop()
        return result
    return wrapper


ruta_transacciones = path.join("data", "credit_card_transactions.csv")
ruta_estados = path.join("data", "states.csv")
