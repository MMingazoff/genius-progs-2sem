from threading import Thread, BoundedSemaphore
import time
import random


get_data_bound = BoundedSemaphore(value=10)
write_to_file_bound = BoundedSemaphore(value=5)
write_to_console_bound = BoundedSemaphore(value=1)


def limiter(func):
    def wrapper(*args, **kwargs):
        if func.__name__ == 'get_data':
            bounder = get_data_bound
        elif func.__name__ == 'write_to_file':
            bounder = write_to_file_bound
        else:
            bounder = write_to_console_bound
        with bounder:
            func(*args, **kwargs)
    return wrapper


@limiter
def get_data(task_id):
    print(f"processing get_data({task_id})")
    time.sleep(random.randint(1, 3))
    print(f"completed get_data({task_id})")


@limiter
def write_to_file(task_id):
    print(f"processing write_to_file({task_id})")
    time.sleep(random.randint(1, 5))
    print(f"completed write_to_file({task_id})")


@limiter
def write_to_console(task_id):
    print(f"processing write_to_console({task_id})")
    time.sleep(random.randint(1, 5))
    print(f"completed write_to_console({task_id})")


def main():
    for task_id in range(20):
        get_data_thread = Thread(target=get_data, args=(task_id,))
        get_data_thread.start()
        get_data_thread.join()
        write_to_file_thread = Thread(target=write_to_file, args=(task_id,))
        write_to_console_thread = Thread(target=write_to_console, args=(task_id,))
        write_to_file_thread.start()
        write_to_console_thread.start()


if __name__ == '__main__':
    main()
