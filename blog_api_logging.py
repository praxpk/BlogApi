import logging


class BlogApiLog:
    def __init__(self, module_name: str, log_file: str) -> None:
        self.module_name = module_name
        self.log_file = log_file
        self.logging_level = logging.INFO

    def get_logger(self) -> logging:
        log_format = '%(asctime)s  %(name)5s  %(levelname)5s  %(message)s'
        logging.basicConfig(level=self.logging_level, format=log_format, filename=self.log_file, filemode='a')
        console = logging.StreamHandler(stream=None)
        console.setLevel(self.logging_level)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger(self.module_name).addHandler(console)
        return logging.getLogger(self.module_name)
