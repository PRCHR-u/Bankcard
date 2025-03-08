import logging
import os

# Путь к папке logs
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

# Создание папки logs, если её нет
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def setup_logger(module_name: str) -> logging.Logger:
    """
    Настройка логгера для указанного модуля.

    :param module_name: Имя модуля.
    :return: Настроенный объект Logger.
    """
    # Создаем логгер для модуля
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG) # Уровень логирования

    # Создаем обработчик для записи логов в файл
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(project_root, "logs", f"{module_name}.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, mode='w')  # mode='w' для перезаписи файла
    file_handler.setLevel(logging.DEBUG)

    # Создаем форматтер для логов
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger
