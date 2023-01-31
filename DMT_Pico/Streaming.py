import time
from TC08_config import USBTC08_CONFIG, EXPERIMENT_CONFIG
from TC08_unit import LoggingUnit

if __name__ == "__main__":

    recording_period, polling_interval, sampling_interval_ms = EXPERIMENT_CONFIG[
        'recording_period'], EXPERIMENT_CONFIG['polling_interval'], EXPERIMENT_CONFIG['sampling_interval_ms']

    current_time = 0

    polling_period = []

    while current_time < recording_period:
        interval = min(polling_interval, recording_period - current_time)
        polling_period.append(interval)
        current_time += interval

    loggers = []

    for name, logger_info in USBTC08_CONFIG.items():
        loggers.append(LoggingUnit(logger_info, name,
                       sampling_interval_ms, recording_period))

    for logger in loggers:
        logger.setBuffers(polling_period)

    for logger in loggers:
        logger.runUnit()

    for index, poll in enumerate(polling_period):

        time.sleep(poll)

        for logger in loggers:
            logger.pollData(index)

    for logger in loggers:
        logger.stopUnit()
        logger.closeUnit()
        print(logger.grabData())
        print(logger.__repr__)
