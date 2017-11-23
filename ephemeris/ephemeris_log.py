import logging


class ProgressConsoleHandler(logging.StreamHandler):
    """
    A handler class which allows the cursor to stay on
    one line for selected messages
    """
    on_same_line = False

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            same_line = hasattr(record, 'same_line')
            if self.on_same_line and not same_line:
                stream.write('\r\n')
            stream.write(msg)
            if same_line:
                stream.write('.')
                self.on_same_line = True
            else:
                stream.write('\r\n')
                self.on_same_line = False
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


def disable_external_library_logging():
    # Omit (most of the) logging by external libraries
    logging.getLogger('bioblend').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.ERROR)
    try:
        logging.captureWarnings(True)  # Capture HTTPS warngings from urllib3
    except AttributeError:
        pass


def ensure_log_configured():
    # For library-style usage - just ensure a log exists and use ephemeris name.
    if 'log' not in globals():
        global log
        log = setup_global_logger()


def setup_global_logger(include_file=False):
    formatter = logging.Formatter('%(asctime)s %(levelname)-5s - %(message)s')
    progress = ProgressConsoleHandler()
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(progress)

    if include_file:
        file_handler = logging.FileHandler('/tmp/galaxy_tool_install.log')
        logger.addHandler(file_handler)
    return logger
