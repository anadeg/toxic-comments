import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.FileHandler("debug.log"),
                        logging.StreamHandler(sys.stdout)]
                    )
modes = {"info": logging.INFO,
         "error": logging.ERROR}


def log_to_file_and_console(info):
    # mylogs = logging.getLogger(__name__)
    logging.info(info)
