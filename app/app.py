"""
Main application
"""

import time
import sys

import logs
import structlog
import notification

from conf import Configuration
from exchange import ExchangeInterface

from behaviour import Behaviour


def main():
    """Initializes the application
    """
    # Load settings and create the config object
    config = Configuration()
    settings = config.settings

    # Set up logger
    logs.configure_logging(settings['log_level'], settings['log_mode'])
    logger = structlog.get_logger()

    exchange_interface = ExchangeInterface(config.tickers)
    notifier = notification.Notifier(config.notifiers)

    behaviour = Behaviour(
        config,
        exchange_interface,
        notifier
    )

    behaviour.run(settings['output_mode'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
