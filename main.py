from assistant import Assistant
from utils import setup_logging
from config import *

def main():
    setup_logging()
    assistant = Assistant()
    assistant.start()

if __name__ == "__main__":
    main()