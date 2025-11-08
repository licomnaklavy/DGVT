import argparse


class DependencyGraphVisualizer:
    def __init__(self):
        self.config = {}
        self.parser = self._setup_argparse()

    def _setup_argparse(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Инструмент визуализации графа зависимостей пакетов",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # Обязательные параметры
        parser.add_argument(
            "--package",
            dest="package_name",
            required=True,
            help="Имя анализируемого пакета"
        )

        # Параметры репозитория
        repo_group = parser.add_mutually_exclusive_group(required=True)
        repo_group.add_argument(
            "--repo-url",
            dest="repository_url",
            help="URL-адрес репозитория пакетов"
        )
        repo_group.add_argument(
            "--test-repo",
            dest="test_repo_mode",
            action="store_true",
            help="Режим работы с тестовым репозиторием"
        )

        # Дополнительные параметры
        parser.add_argument(
            "--version",
            dest="package_version",
            default="latest",
            help="Версия пакета (по умолчанию: latest)"
        )

        parser.add_argument(
            "--ascii-tree",
            dest="ascii_tree_mode",
            action="store_true",
            help="Режим вывода зависимостей в формате ASCII-дерева"
        )

        parser.add_argument(
            "--max-depth",
            dest="max_depth",
            type=int,
            default=10,
            help="Максимальная глубина анализа зависимостей (по умолчанию: 10)"
        )

        parser.add_argument(
            "--filter",
            dest="filter_substring",
            default="",
            help="Подстрока для фильтрации пакетов"
        )

        return parser

    def _validate_arguments(self, args) -> None:
        if not args.package_name or not args.package_name.strip():
            raise ValueError("Имя пакета не может быть пустым")

        if args.repository_url and not args.test_repo_mode:
            if not (args.repository_url.startswith('http://') or
                    args.repository_url.startswith('https://')):
                raise ValueError("URL репозитория должен начинаться с http:// или https://")

        if args.max_depth < 1:
            raise ValueError("Максимальная глубина должна быть положительным числом")

        if args.package_version and args.package_version != "latest":
            version_parts = args.package_version.split('.')
            if not all(part.isdigit() for part in version_parts if part):
                raise ValueError("Неверный формат версии пакета. Используйте формат X.Y.Z или 'latest'")

    def _parse_arguments(self) -> None:
        try:
            args = self.parser.parse_args()

            self._validate_arguments(args)

            self.config = {
                "package_name": args.package_name,
                "repository_url": args.repository_url,
                "test_repo_mode": args.test_repo_mode,
                "package_version": args.package_version,
                "ascii_tree_mode": args.ascii_tree_mode,
                "max_depth": args.max_depth,
                "filter_substring": args.filter_substring
            }

        except argparse.ArgumentError as e:
            raise ValueError(f"Ошибка в аргументах командной строки: {e}")

    def display_config(self) -> None:
        print("Конфигурация параметров:")
        for key, value in self.config.items():
            print(f"{key}: {value}")

    def run(self) -> int:
        try:
            self._parse_arguments()

            self.display_config()

            return 0

        except ValueError as e:
            print(f"ОШИБКА: {e}")
            self.parser.print_help()
            return 1
        except Exception as e:
            print(f"НЕОЖИДАННАЯ ОШИБКА: {e}")
            return 1


def main():
    visualizer = DependencyGraphVisualizer()
    return visualizer.run()

if __name__ == "__main__":
    main()