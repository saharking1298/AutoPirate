from datetime import datetime


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Logger:
    # Modes: console, file, web
    ENABLED = True
    MODE = "console"

    @staticmethod
    def _log(level, *text, sep=" "):
        if Logger.ENABLED:
            text = f"{now()} {level} {sep.join([*text])}"
            if Logger.MODE == "console":
                print(text)

    @staticmethod
    def log(*text, sep=" "):
        # Logger._log("LOG", *text, sep=sep)
        text = sep.join([*text]) + "\n"
        print(text)

    @staticmethod
    def error(*text, sep=" "):
        Logger._log("ERROR", *text, sep=sep)
