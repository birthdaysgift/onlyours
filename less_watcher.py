from os import path
from subprocess import run
from threading import Thread
from time import asctime, sleep


def watch(app, watch, compile):
    app_path = path.join(
        path.dirname(path.abspath(__file__)),
        app,
        "static",
        app
    )
    watch = path.normpath(watch)
    watch_path = path.join(app_path, 'less', watch + '.less')
    less_path = path.join(app_path, "less", compile + ".less")
    css_path = path.join(app_path, "css", compile + ".css")

    print(f"Started on /{app}/less/{watch}.less -> /{app}/css/{compile}.css")

    time_tmp = path.getmtime(watch_path)
    time = time_tmp
    while True:
        try:
            time = path.getmtime(watch_path)
        except FileNotFoundError:
            sleep(0.5)
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
            print(f"LESS path: {less_path}")
            print(f"CSS path: {css_path}")
            print("")
        sleep(0.5)


Thread(target=watch, args=('auth_custom', 'login', 'login')).start()
Thread(target=watch, args=('auth_custom', 'register', 'register')).start()

Thread(target=watch, args=('pages', 'page', 'page')).start()
Thread(target=watch, args=('pages', 'edit', 'edit')).start()

Thread(target=watch, args=('pages', 'ajax/delete_post', 'delete_post')).start()
Thread(target=watch, args=('pages', 'ajax/all_photos', 'ajax/all_photos')).start()
Thread(target=watch, args=('pages', 'ajax/detail_photo', 'ajax/detail_photo')).start()
Thread(target=watch, args=('pages', 'ajax/all_friends', 'ajax/all_friends')).start()
Thread(target=watch, args=('pages', 'ajax/all_videos', 'ajax/all_videos')).start()
Thread(target=watch, args=('pages', 'ajax/detail_video', 'ajax/detail_video')).start()


Thread(target=watch, args=('pages', 'elephant', 'elephant')).start()
Thread(target=watch, args=('pages', 'mixins', 'page')).start()
Thread(target=watch, args=('pages', 'navigation', 'page')).start()

Thread(target=watch, args=('pages', 'left/avatar', 'page')).start()
Thread(target=watch, args=('pages', 'left/buttons', 'page')).start()
Thread(target=watch, args=('pages', 'left/friends', 'page')).start()

Thread(target=watch, args=('pages', 'middle/about', 'page')).start()
Thread(target=watch, args=('pages', 'middle/posts', 'page')).start()

Thread(target=watch, args=('pages', 'right/audio', 'page')).start()
Thread(target=watch, args=('pages', 'right/photo', 'page')).start()
Thread(target=watch, args=('pages', 'right/video', 'page')).start()

Thread(target=watch, args=('talks', 'talks', 'talks')).start()
Thread(target=watch, args=('talks', 'contacts', 'talks')).start()
Thread(target=watch, args=('talks', 'messages', 'talks')).start()
Thread(target=watch, args=('talks', 'mixins', 'talks')).start()
Thread(target=watch, args=('talks', 'navigation', 'talks')).start()
