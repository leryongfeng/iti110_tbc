import os
from pathlib import Path

def gen_requirements():

    os.system('pip3 install pipreqs')
    os.system('pip3 install pip-tools')

    os.system('python -m  pipreqs.pipreqs .')
    Path("requirements.txt").rename("requirements.txt")


def run_requirements():
    os.system('pip install -r requirements.txt')

if __name__ == "__main__":
    # gen_requirements()
    run_requirements()