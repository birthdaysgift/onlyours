from os.path import abspath, dirname, getmtime, join
from subprocess import run
from threading import Thread
from time import asctime, sleep


def watch(app_name, file_name):
    app_path = join(dirname(abspath(__file__)), app_name, "static", app_name)
    less_path = join(app_path, "less", file_name + ".less")
    css_path = join(app_path, "css", file_name + ".css")

    print(f"Less watcher has been started on {app_name}:{file_name}.")

    time_tmp = getmtime(less_path)
    time = time_tmp
    while True:
        try:
            time = getmtime(less_path)
        except FileNotFoundError:
            continue
        if time_tmp != time:
            time_tmp = time
            result = run("lessc " + less_path + " " + css_path, shell=True)
            if result.returncode == 0:
                print("\^_^/")
                print("Compiled successfully!")
            else:
                print("|>_<|")
                print("Something went wrong...")
            print(asctime())
            print(f"App name: {app_name}")
            print(f"File name: {file_name}")
            print(f"LESS path: {less_path}")
            print(f"CSS path: {css_path}")
            print("")
        sleep(1)


Thread(target=watch, args=("pages", "page")).start()
Thread(target=watch, args=("pages", "photo")).start()
Thread(target=watch, args=("talks", "talks")).start()
