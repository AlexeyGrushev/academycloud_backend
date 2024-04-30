from subprocess import Popen


def run_flower():
    command = "celery -A app.config.worker flower --basic_auth=admin:admin"
    process = Popen(command.split(), shell=False)
    process.communicate()


if __name__ == "__main__":
    run_flower()
