

from src.reports import reports_main
from src.services import servies_main
from src.views import views_main


def main() -> None:
    """
    Отвечает за основную логику проекта с пользователем и связывает функциональности между собой.
    """
    views_main()
    servies_main()
    reports_main()


if __name__ == "__main__":
    main()
