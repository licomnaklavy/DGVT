# Dependency Graph Visualizer - Этап 1

## Общее описание

Минимальный прототип инструмента визуализации графа зависимостей для менеджера пакетов. На данном этапе реализована только система конфигурации через командную строку. Готовые средства для получения зависимостей не используются.

## Функции и настройки

### Основные параметры конфигурации

#### Обязательные параметры:

- `--package` (обязательный) - Имя анализируемого пакета
  - Пример: `--package requests`
  - Ошибка: если параметр не указан или пустой

#### Параметры репозитория (обязательно один из двух):

- `--repo-url` - URL-адрес репозитория пакетов
  - Пример: `--repo-url https://pypi.org`
  - Ошибка: если URL не начинается с http:// или https://

- `--test-repo` - Режим работы с тестовым репозиторием
  - Флаг (не требует значения)
  - Пример: `--test-repo`

#### Дополнительные параметры:

- `--version` - Версия пакета (по умолчанию: "latest")
  - Пример: `--version 1.2.3`
  - Ошибка: неверный формат версии (должен быть X.Y.Z или "latest")

- `--ascii-tree` - Режим вывода зависимостей в формате ASCII-дерева
  - Флаг (не требует значения)
  - Пример: `--ascii-tree`

- `--max-depth` - Максимальная глубина анализа зависимостей (по умолчанию: 10)
  - Пример: `--max-depth 5`
  - Ошибка: значение меньше 1

- `--filter` - Подстрока для фильтрации пакетов
  - Пример: `--filter "test"`

### Валидация параметров

Приложение выполняет проверку всех входных параметров:

1. **Имя пакета** - не может быть пустым
2. **URL репозитория** - должен начинаться с http:// или https://
3. **Максимальная глубина** - должна быть положительным числом
4. **Версия пакета** - должна быть в формате X.Y.Z или "latest"

## Сборка и запуск

### Требования

- Python 3.6 или выше
- Стандартная библиотека Python (внешние зависимости не требуются)

### Запуск приложения

```bash
# Базовая конфигурация с внешним репозиторием
py main.py --package requests --repo-url https://pypi.org

# С тестовым репозиторием
py main.py --package numpy --test-repo

# Полная конфигурация
py main.py --package django --repo-url https://pypi.org --version 4.2 --max-depth 3 --filter "auth" --ascii-tree
```

### Получение справки
```bash
py main.py --help
```

## Примеры использования
### Пример 1: Базовый анализ пакета
```bash
py main.py --package requests --repo-url https://pypi.org
```

#### Вывод:
```bash
Конфигурация параметров:
package_name: requests
repository_url: https://pypi.org
test_repo_mode: False
package_version: latest
ascii_tree_mode: False
max_depth: 10
filter_substring: 
```
### Пример 2: Анализ с тестовым репозиторием и ограничением глубины
```bash
py main.py --package numpy --test-repo --max-depth 3 --version 1.24.0
```
#### Вывод:
```bash
Конфигурация параметров:
package_name: numpy
repository_url: None
test_repo_mode: True
package_version: 1.24.0
ascii_tree_mode: False
max_depth: 3
filter_substring: 
```

### Пример 3: Анализ с фильтрацией и ASCII-деревом
```bash
py main.py --package django --repo-url https://pypi.org --filter "test" --ascii-tree --max-depth 5
```

#### Вывод:
```bash
Конфигурация параметров:
package_name: django
repository_url: https://pypi.org
test_repo_mode: False
package_version: latest
ascii_tree_mode: True
max_depth: 5
filter_substring: test
```

### Пример 4: Ошибочные сценарии
```bash
# Ошибка: не указано имя пакета
py main.py --repo-url https://pypi.org

# Ошибка: не указан репозиторий
py main.py --package requests

# Ошибка: неверный URL
py main.py --package requests --repo-url ftp://example.com

# Ошибка: неверная версия
py main.py --package requests --repo-url https://pypi.org --version invalid
```