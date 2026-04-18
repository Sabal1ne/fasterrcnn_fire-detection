# 🏗️ Разработка

## Содержание

- [Архитектура проекта](#архитектура-проекта)
- [Структура директорий](#структура-директорий)
- [Основные компоненты](#основные-компоненты)
- [Формат данных](#формат-данных)
- [Как расширить проект](#как-расширить-проект)
- [Тестирование](#тестирование)
- [Стиль кода](#стиль-кода)
- [Дорожная карта](#дорожная-карта)

---

## Архитектура проекта

```
┌─────────────────────────────────────────────┐
│          Gradio Web Interface (app.py)       │
│         User-Friendly Frontend               │
├─────────────────────────────────────────────┤
│         FireDetectionApp Class               │
│    (Model Management & Inference Logic)      │
├─────────────────────────────────────────────┤
│      Inference Scripts                       │
│  inference.py  |  inference_video.py         │
├─────────────────────────────────────────────┤
│      Core ML Components                     │
│  models/  |  utils/  |  torch_utils/        │
├─────────────────────────────────────────────┤
│         PyTorch Faster RCNN Model            │
│  ResNet50 FPN  |  ResNet50 FPN V2            │
└─────────────────────────────────────────────┘
```

---

## Структура директорий

```
fasterrcnn_fire-detection/
├── data_configs/              # Конфигурационные файлы датасетов
│   ├── fire.yaml             # Fire detection (fire, smoke)
│   └── ppe.yaml              # PPE detection (helmet, vest)
├── models/                    # Определения моделей
│   ├── __init__.py
│   ├── create_fasterrcnn_model.py   # Фабрика моделей
│   ├── fasterrcnn_resnet50_fpn.py   # Faster RCNN FPN
│   └── fasterrcnn_resnet50_fpn_v2.py # Faster RCNN FPN V2
├── torch_utils/               # Утилиты PyTorch (из pytorch/vision)
│   ├── engine.py             # Циклы обучения/валидации
│   ├── coco_eval.py          # Оценка COCO метрик
│   └── utils.py              # Вспомогательные функции
├── utils/                     # Кастомные утилиты
│   ├── annotations.py        # Рисование bounding boxes
│   ├── general.py            # Сохранение модели, графики
│   ├── logging.py            # WandB, TensorBoard
│   └── transforms.py         # Аугментации изображений
├── docs/                      # Документация
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   ├── DEVELOPMENT.md
│   └── FAQ.md
├── app.py                     # 🌐 Веб-интерфейс Gradio
├── launch_ui.py               # Запуск веб-интерфейса
├── launch_ui.sh               # Запуск на Linux/Mac
├── launch_ui.bat              # Запуск на Windows
├── train.py                   # Скрипт обучения
├── inference.py               # Инференс на изображениях
├── inference_video.py         # Инференс на видео
├── datasets.py                # Dataset и DataLoader
├── example_train.py           # Пример обучения
├── example_usage.py           # Примеры программного использования
├── setup.sh                   # Автоматическая установка
├── requirements.txt           # Зависимости
├── requirements-dev.txt       # Зависимости для разработки
├── CONTRIBUTING.md            # Руководство по вкладу
└── README.md                  # Главная документация
```

**Не включены в репозиторий (создаются пользователем/обучением):**

```
├── data/                      # Данные для обучения
│   ├── train/                # Изображения + XML аннотации
│   └── test/                 # Тестовые данные
└── outputs/                   # Результаты
    ├── training/             # Чекпоинты и графики
    └── inference/            # Результаты инференса
```

---

## Основные компоненты

### Модели (`models/`)

| Файл | Описание |
|------|----------|
| `create_fasterrcnn_model.py` | Фабрика: создаёт нужную модель по имени |
| `fasterrcnn_resnet50_fpn.py` | Базовая модель (mAP@0.5: 37.0%) |
| `fasterrcnn_resnet50_fpn_v2.py` | Улучшенная V2 (mAP@0.5: 46.7%) |

**Добавление новой модели:**

```python
# models/my_model.py
import torchvision
from torchvision.models.detection import FasterRCNN

def create_my_model(num_classes: int, pretrained: bool = True):
    model = ...  # ваша реализация
    return model
```

Затем зарегистрируйте в `create_fasterrcnn_model.py`.

### Работа с данными (`datasets.py`)

Класс `CustomDataset` загружает изображения с Pascal VOC XML аннотациями.

**Ключевые функции:**

| Функция | Описание |
|---------|----------|
| `create_train_dataset()` | Тренировочный датасет |
| `create_valid_dataset()` | Валидационный датасет |
| `create_train_loader()` | DataLoader для обучения |
| `create_valid_loader()` | DataLoader для валидации |

### Утилиты (`utils/`)

| Файл | Ключевые классы/функции |
|------|------------------------|
| `general.py` | `Averager`, `SaveBestModel`, `save_model()`, `save_loss_plot()` |
| `transforms.py` | Аугментации через albumentations |
| `annotations.py` | Рисование bounding boxes на изображениях |
| `logging.py` | Настройка WandB и TensorBoard |

---

## Формат данных

### Структура датасета

```
data/
├── train/
│   ├── image001.jpg
│   ├── image001.xml    # Аннотации для image001.jpg
│   ├── image002.jpg
│   └── image002.xml
└── test/
    ├── image101.jpg
    └── image101.xml
```

### Формат Pascal VOC XML

```xml
<annotation>
    <filename>image001.jpg</filename>
    <size>
        <width>640</width>
        <height>480</height>
        <depth>3</depth>
    </size>
    <object>
        <name>fire</name>
        <bndbox>
            <xmin>100</xmin>
            <ymin>150</ymin>
            <xmax>300</xmax>
            <ymax>400</ymax>
        </bndbox>
    </object>
</annotation>
```

**Правила:**
- XML файл должен иметь то же имя, что и изображение
- `<name>` должен совпадать с классами в конфигурации
- Координаты должны быть в пределах размеров изображения
- Изображения без аннотаций автоматически исключаются

### Инструменты разметки

| Инструмент | Тип | Ссылка |
|-----------|-----|--------|
| **LabelImg** | Десктоп | [github.com/tzutalin/labelImg](https://github.com/tzutalin/labelImg) |
| **CVAT** | Веб | [cvat.org](https://cvat.org/) |
| **Roboflow** | Онлайн | [roboflow.com](https://roboflow.com/) |

---

## Как расширить проект

### Добавить новый класс объектов

1. Добавьте метку в файл конфигурации:
```yaml
CLASSES: ['__background__', 'fire', 'smoke', 'my_new_class']
NC: 4
```

2. Подготовьте данные с новыми аннотациями (XML с `<name>my_new_class</name>`)

3. Запустите обучение:
```bash
python train.py --config data_configs/my_config.yaml --epochs 50
```

### Добавить новую модель

1. Создайте файл `models/my_model.py`
2. Реализуйте функцию `create_my_model(num_classes, pretrained)`
3. Зарегистрируйте в `models/create_fasterrcnn_model.py`:
```python
from models.my_model import create_my_model

MODELS = {
    "fasterrcnn_resnet50_fpn": create_model_fpn,
    "fasterrcnn_resnet50_fpn_v2": create_model_fpn_v2,
    "my_model": create_my_model,  # добавить
}
```

### Fine-tuning на своём датасете

```bash
python train.py \
  --model fasterrcnn_resnet50_fpn_v2 \
  --config data_configs/your_config.yaml \
  --epochs 25 \
  --resume-training \
  --weights outputs/training/previous_run/best_model.pth
```

---

## Тестирование

Тестовая инфраструктура запланирована. Зависимости для тестирования:

```bash
pip install -r requirements-dev.txt
```

Для запуска тестов (после их создания):

```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

---

## Стиль кода

Проект следует [PEP 8](https://pep8.org/).

```bash
# Проверка стиля
flake8 .

# Автоформатирование
black .
isort .
```

**Основные правила:**

- Отступы: 4 пробела
- Длина строки: максимум 100 символов
- Именование: `CamelCase` для классов, `snake_case` для функций
- Docstrings для всех публичных функций и классов

---

## Дорожная карта

### Version 0.1.0 ✅ (Текущая)
- Базовое обучение Faster RCNN
- Инференс на изображениях и видео
- Веб-интерфейс Gradio

### Version 0.2.0 (В работе)
- [ ] Полное тестирование (pytest)
- [ ] CI/CD GitHub Actions
- [ ] REST API (FastAPI/Flask)
- [ ] Поддержка COCO формата аннотаций

### Version 0.3.0
- [ ] Дополнительные модели (MobileNet, RetinaNet)
- [ ] Экспорт в ONNX/TensorRT
- [ ] Webcam real-time детекция

### Version 1.0.0
- [ ] Production deployment (Docker)
- [ ] Покрытие тестами > 80%
- [ ] Полная документация API

---

> 🔗 Хотите внести вклад? → [CONTRIBUTING.md](../CONTRIBUTING.md)  
> 🔗 Часто задаваемые вопросы → [FAQ.md](FAQ.md)
