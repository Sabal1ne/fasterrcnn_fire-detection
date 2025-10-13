# Руководство по контрибуции / Contributing Guide

Спасибо за ваш интерес к проекту Faster RCNN Fire Detection! Мы приветствуем любые вклады в развитие проекта.

## Содержание

- [Как внести вклад](#как-внести-вклад)
- [Настройка окружения разработки](#настройка-окружения-разработки)
- [Стандарты кода](#стандарты-кода)
- [Процесс Pull Request](#процесс-pull-request)
- [Сообщения об ошибках](#сообщения-об-ошибках)
- [Предложения по улучшению](#предложения-по-улучшению)

## Как внести вклад

Существует несколько способов внести вклад в проект:

1. **Сообщить об ошибке** - создайте issue с описанием проблемы
2. **Предложить улучшение** - создайте issue с описанием предложения
3. **Исправить ошибку** - создайте pull request с исправлением
4. **Добавить функциональность** - создайте pull request с новой функциональностью
5. **Улучшить документацию** - создайте pull request с улучшениями документации

## Настройка окружения разработки

### 1. Клонирование репозитория

```bash
git clone https://github.com/Sabal1ne/fasterrcnn_fire-detection.git
cd fasterrcnn_fire-detection
```

### 2. Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Linux/Mac)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
# Установка основных зависимостей
pip install -r requirements.txt

# Установка зависимостей для разработки (после создания requirements-dev.txt)
pip install -r requirements-dev.txt
```

### 4. Подготовка данных

Создайте структуру каталогов для данных:

```bash
mkdir -p data/train
mkdir -p data/test
```

Поместите ваши изображения и XML аннотации в соответствующие папки.

## Стандарты кода

### Python Code Style

Мы следуем [PEP 8](https://www.python.org/dev/peps/pep-0008/) стандарту для Python кода.

**Основные правила**:

1. **Отступы**: Используйте 4 пробела (не tabs)
2. **Длина строки**: Максимум 100 символов
3. **Импорты**: Группируйте импорты (стандартная библиотека, сторонние библиотеки, локальные модули)
4. **Именование**:
   - Классы: `CamelCase`
   - Функции и переменные: `snake_case`
   - Константы: `UPPER_CASE`

### Примеры

#### ✅ Хороший стиль

```python
def load_model(model_path: str, num_classes: int = 2) -> torch.nn.Module:
    """
    Load a pre-trained model from the specified path.
    
    Args:
        model_path: Path to the model checkpoint
        num_classes: Number of classes in the dataset
        
    Returns:
        Loaded model
    """
    model = create_model(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path))
    return model
```

#### ❌ Плохой стиль

```python
def loadModel(modelPath,numClasses=2):
    model=createModel(num_classes=numClasses)
    model.load_state_dict(torch.load(modelPath))
    return model
```

### Документация

Все функции и классы должны иметь docstrings:

```python
def calculate_map(predictions: list, targets: list, iou_threshold: float = 0.5) -> float:
    """
    Calculate mean Average Precision for object detection.
    
    Args:
        predictions: List of predicted bounding boxes and scores
        targets: List of ground truth bounding boxes
        iou_threshold: IoU threshold for considering a detection as correct
        
    Returns:
        mAP value
        
    Raises:
        ValueError: If predictions and targets have different lengths
    """
    pass
```

### Type Hints

Используйте type hints для всех функций:

```python
from typing import List, Dict, Tuple, Optional

def process_image(
    image_path: str, 
    model: torch.nn.Module,
    threshold: float = 0.5
) -> Tuple[np.ndarray, List[Dict[str, float]]]:
    """Process a single image and return predictions."""
    pass
```

## Процесс Pull Request

### 1. Создание ветки

Создайте новую ветку для вашей работы:

```bash
# Для новой функциональности
git checkout -b feature/your-feature-name

# Для исправления ошибки
git checkout -b fix/bug-description

# Для улучшения документации
git checkout -b docs/description
```

### 2. Внесение изменений

- Делайте небольшие, логически связанные коммиты
- Пишите понятные commit messages
- Следуйте стандартам кода

### 3. Тестирование

Перед отправкой pull request убедитесь что:

```bash
# Код соответствует стандартам (после настройки линтеров)
flake8 .
black --check .

# Все тесты проходят (после создания тестов)
pytest tests/
```

### 4. Commit Messages

Используйте понятные commit messages:

```
✅ Хорошо:
- Add support for COCO format annotations
- Fix bounding box validation in datasets.py
- Update README with installation instructions

❌ Плохо:
- update
- fix bug
- changes
```

### 5. Отправка Pull Request

1. Push вашей ветки:
```bash
git push origin your-branch-name
```

2. Создайте Pull Request на GitHub
3. Заполните описание PR:
   - Что изменено
   - Почему это необходимо
   - Как это протестировано

### 6. Code Review

- Будьте открыты к обсуждению и предложениям
- Отвечайте на комментарии
- Вносите необходимые изменения

## Сообщения об ошибках

При создании issue с сообщением об ошибке, пожалуйста, включите:

1. **Описание проблемы**: Что пошло не так?
2. **Шаги для воспроизведения**: Как воспроизвести ошибку?
3. **Ожидаемое поведение**: Что должно было произойти?
4. **Фактическое поведение**: Что произошло на самом деле?
5. **Окружение**:
   - Python версия
   - PyTorch версия
   - OS
   - GPU (если применимо)
6. **Лог ошибки**: Полный текст ошибки
7. **Скриншоты**: Если применимо

### Шаблон Issue для ошибки

```markdown
## Описание проблемы
Краткое описание проблемы

## Шаги для воспроизведения
1. Шаг 1
2. Шаг 2
3. ...

## Ожидаемое поведение
Что должно было произойти

## Фактическое поведение
Что произошло на самом деле

## Окружение
- Python: 3.9.7
- PyTorch: 1.12.0
- OS: Ubuntu 20.04
- GPU: NVIDIA RTX 3080

## Лог ошибки
```
Вставьте полный лог ошибки здесь
```

## Дополнительная информация
Любая дополнительная информация, которая может помочь
```

## Предложения по улучшению

При создании issue с предложением по улучшению, пожалуйста, включите:

1. **Описание**: Что вы хотите добавить или улучшить?
2. **Обоснование**: Почему это улучшение необходимо?
3. **Предложенное решение**: Как вы предлагаете это реализовать?
4. **Альтернативы**: Рассматривали ли вы альтернативные подходы?
5. **Дополнительная информация**: Примеры, ссылки и т.д.

## Приоритеты для контрибуции

Если вы ищете, с чего начать, вот приоритетные задачи:

### High Priority
- Создание тестов для существующего кода
- Улучшение документации
- Адаптация для fire detection
- Исправление закомментированного кода

### Medium Priority
- Добавление новых моделей
- Улучшение производительности
- Добавление новых аугментаций

### Low Priority
- Создание веб-интерфейса
- Дополнительные utility скрипты

## Лицензия

Отправляя pull request, вы соглашаетесь с тем, что ваш вклад будет распространяться под той же лицензией, что и проект.

## Вопросы?

Если у вас есть вопросы, создайте issue с меткой "question" или свяжитесь с мейнтейнерами проекта.

## Благодарности

Спасибо всем контрибьюторам, которые помогают улучшить этот проект! 🙏
