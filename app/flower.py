from subprocess import Popen

from app.config.app_settings import settings


def run_flower():
    command = "celery -A app.config.worker flower" \
        f" --basic_auth={settings.FLOWER_LOGIN}:{settings.FLOWER_PASSWORD}"
    process = Popen(command.split(), shell=False)
    process.communicate()


if __name__ == "__main__":
    run_flower()
