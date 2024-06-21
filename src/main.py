from src.reports import main_reports
from src.services import main_servies
from src.views import main_views


def main() -> None:
    """
    Отвечает за основную логику проекта с пользователем и связывает функциональности между собой.
    """
    main_views()
    main_reports()
    main_servies()


if __name__ == "__main__":
    main()
