import logging


def setup_logger(log_file="app.log"):
    logger = logging.getLogger("maintenance_lab")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        # ✅ Добавлен timestamp
        fmt = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger