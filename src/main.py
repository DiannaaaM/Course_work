from src.logger import setup_logging
from src.reports import reports_main
from src.services import servies_main
from src.views import views_main

logger = setup_logging()


def main() -> None:
    """
    Отвечает за основную логику проекта с пользователем и связывает функциональности между собой.
    """
    logger.info("Start application")
    logger.info("Starting run views module")
    views_main()
    logger.info("Starting run servies module")
    servies_main()
    logger.info("Starting run reports module")
    reports_main()


if __name__ == "__main__":
    main()
