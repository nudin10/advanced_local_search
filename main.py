from app import cli, __app_name__
from random import seed

def main():
    # seed(10000)
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
