"""
Copyright Square Root, Inc. Used with permission.
"""

import datetime as dt
import logging as lg
import logging.handlers as lgh


INFO = lg.INFO
DEBUG = lg.DEBUG
CRITICAL = lg.CRITICAL
WARN = lg.WARN
ERROR = lg.ERROR


def get_default_root_logger(console_verbosity=INFO, filename=None, logfile_verbosity=DEBUG):
    """Return a logger with default settings
    This function should be invoked in the main part of your module.
    Log file maintenance is handled automatically with the TimedRotatingFileHandler. This handler will automatically
    delete log files older than 7 days, and handles the naming of the files, as well. All time stamps are in UTC.
    :param console_verbosity: Logging level to console (INFO, DEBUG, CRITICAL, WARN, ERROR)
    :type console_verbosity: n/a
    :param filename: log file name. File logging is disabled if set to None
    :type filename: str
    :param logfile_verbosity: log file verbosity. Ignored if filename is none. Set to INFO, DEBUG, CRITICAL or WARN
    :type logfile_verbosity: n/a
    :returns: A pre-formatted logger
    :rtype: lg.Logger
    """

    logger = lg.getLogger()
    logger.setLevel(DEBUG)
    logger.handlers = []  # Get rid of default handlers

    # Format
    fmt = lg.Formatter('%(asctime)s - %(name)s - %(lineno)d -  %(levelname)s - %(message)s')

    # Stream handler
    strm_hndlr = lg.StreamHandler()
    strm_hndlr.setFormatter(fmt)
    strm_hndlr.setLevel(console_verbosity)

    logger.addHandler(strm_hndlr)

    # File handler
    if filename:
        file_hndlr = lgh.TimedRotatingFileHandler(filename, when='D', interval=1, backupCount=7, utc=True)
        file_hndlr.setFormatter(fmt)
        file_hndlr.setLevel(logfile_verbosity)
        logger.addHandler(file_hndlr)

    return logger


def get_logger(name):
    lg.basicConfig()  # A bit of a hack--does nothing except prevent error
    logger = lg.getLogger(name)
    return logger


def get_canned_header(logger, name):
    """Get a standard header for log files
    The header looks like this:
2014-03-24 16:50:16,716 - root - INFO -
************************************************************************************************************************
2014-03-24 16:50:16,716 - root - INFO - name
2014-03-24 16:50:16,716 - root - INFO - Today is: Mon Mar 24 16:50:16 2014
2014-03-24 16:50:16,716 - root - INFO -
************************************************************************************************************************
    :param logger: Logger
    :type logger: lg.Logger
    :param name: Heading of log file
    :type name: str
    """

    logger.info('\n{0}'.format('*'*120))
    logger.info(name)
    logger.info('Today is: {0}'.format(dt.datetime.today().strftime('%c')))
    logger.info('\n{0}\n'.format('*'*120))


def get_bulleted_list(l, indent=3, bullet='*'):
    """ Render a list into a string with bullet points
    :param  l: List to bulletify
    :type   l: list[str]
    :param  indent: Number of tabs to indent (default: 3)
    :type   indent: int
    :returns: bulleted list
    :rtype  : str
    """
    sep = ''.join(['\t' * indent, bullet, ' {0}'])
    return '\n'.join(sep.format(x) for x in l)