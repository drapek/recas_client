import threading

from src import camera_handler, commands_handler


def main():
    thr1 = threading.Thread(target=commands_handler.run, args=(), kwargs={})
    thr2 = threading.Thread(target=camera_handler.run, args=(), kwargs={})

    thr1.start()
    thr2.start()

    thr1.join()
    thr2.join()


if __name__ == '__main__':
    main()
