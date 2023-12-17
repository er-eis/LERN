import logging


def setup_logging():
    log_format = "%(asctime)s - %(levelname)s - [%(pathname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
    )

    uvicorn_logger = logging.getLogger("uvicorn")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    uvicorn_logger.handlers = [handler]
    uvicorn_logger.setLevel(logging.INFO)
