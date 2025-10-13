# Структура проекта Faster RCNN Fire Detection

## Обзор проекта

Этот проект реализует обнаружение объектов с использованием PyTorch Faster RCNN ResNet50 FPN и FPN V2.
Проект изначально был разработан для обнаружения средств индивидуальной защиты (PPE), но может быть адаптирован для обнаружения пожара и других объектов.

## Дерево каталогов

```
fasterrcnn_fire-detection/
├── data_configs/           # Конфигурационные файлы для наборов данных
│   └── ppe.yaml           # Конфигурация для PPE датасета
├── models/                 # Определения моделей
│   ├── __init__.py
│   ├── create_fasterrcnn_model.py  # Фабрика создания моделей
│   ├── fasterrcnn_resnet50_fpn.py  # Faster RCNN ResNet50 FPN
│   └── fasterrcnn_resnet50_fpn_v2.py  # Faster RCNN ResNet50 FPN V2
├── torch_utils/            # Утилиты PyTorch (из pytorch/vision)
│   ├── __init__.py
│   ├── coco_eval.py       # Оценка COCO метрик
│   ├── coco_utils.py      # Утилиты для COCO датасета
│   ├── engine.py          # Циклы обучения и валидации
│   ├── utils.py           # Общие утилиты
│   └── README.md          # Информация об источнике кода
├── utils/                  # Пользовательские утилиты проекта
│   ├── __init__.py
│   ├── annotations.py     # Утилиты для аннотаций
│   ├── general.py         # Общие вспомогательные функции
│   ├── logging.py         # Функции логирования
│   └── transforms.py      # Трансформации изображений
├── datasets.py             # Класс Dataset и DataLoader
├── train.py               # Основной скрипт обучения
├── inference.py           # Скрипт инференса для изображений
├── inference_video.py     # Скрипт инференса для видео
├── requirements.txt       # Зависимости Python
├── README.md              # Основная документация
└── .gitignore            # Игнорируемые файлы Git

Отсутствующие каталоги (создаются автоматически или добавляются пользователем):
├── data/                  # Каталог данных (не в репозитории)
│   ├── train/            # Обучающие изображения и XML аннотации
│   └── test/             # Тестовые изображения и XML аннотации
└── outputs/              # Результаты обучения и инференса
    ├── training/         # Результаты обучения
    └── inference/        # Результаты инференса
```

## Описание основных компонентов

### 1. Модели (models/)

#### create_fasterrcnn_model.py
- **Назначение**: Фабрика для создания различных вариантов Faster RCNN моделей
- **Доступные модели**:
  - `fasterrcnn_resnet50_fpn`: Классическая модель Faster RCNN с ResNet50 backbone
  - `fasterrcnn_resnet50_fpn_v2`: Улучшенная версия V2 с лучшими результатами

#### fasterrcnn_resnet50_fpn.py
- Реализация Faster RCNN ResNet50 FPN
- Поддержка предобученных весов
- Настраиваемое количество классов

#### fasterrcnn_resnet50_fpn_v2.py
- Улучшенная версия с новыми техниками обучения
- FPN с batch normalization
- Более мощная головка регрессии
- Увеличение mAP с 37.0% до 46.7%

### 2. Скрипты обучения и инференса

#### train.py (13424 байт)
- **Основной скрипт для обучения модели**
- **Поддерживаемые аргументы**:
  - `--model`: Выбор модели (fasterrcnn_resnet50_fpn или fasterrcnn_resnet50_fpn_v2)
  - `--config`: Путь к конфигурационному файлу
  - `--epochs`: Количество эпох обучения
  - `--batch-size`: Размер батча
  - `--workers`: Количество воркеров для загрузки данных
  - `--project-name`: Имя проекта для сохранения результатов
  - `--use-train-aug`: Использование дополнительных аугментаций
  - `--no-mosaic`: Отключение mosaic аугментации
  - `--resume-training`: Продолжение обучения с чекпоинта

**Функциональность**:
- Загрузка конфигурации датасета
- Создание DataLoader для обучения и валидации
- Настройка модели и оптимизатора
- Цикл обучения с валидацией
- Сохранение лучшей модели и графиков потерь
- Логирование в WandB и TensorBoard

#### inference.py (6442 байт)
- **Инференс на отдельных изображениях**
- **Основные функции**:
  - Загрузка обученной модели
  - Обработка одного изображения или папки изображений
  - Визуализация результатов
  - Подсчет FPS

#### inference_video.py (7178 байт)
- **Инференс на видео**
- Поддержка различных видео форматов
- Опция показа результатов в реальном времени
- Сохранение обработанного видео

### 3. Работа с данными

#### datasets.py (13352 байт)
- **Класс CustomDataset**:
  - Загрузка изображений и XML аннотаций
  - Автоматическая очистка данных (удаление изображений без аннотаций)
  - Поддержка различных форматов изображений (jpg, jpeg, png, ppm)
  - Проверка корректности bounding boxes
  - Поддержка mosaic аугментации
  - Опциональные train-time аугментации

**Функции создания DataLoader**:
- `create_train_dataset()`: Создание тренировочного датасета
- `create_valid_dataset()`: Создание валидационного датасета
- `create_train_loader()`: Создание тренировочного DataLoader
- `create_valid_loader()`: Создание валидационного DataLoader

### 4. Утилиты (utils/)

#### general.py
- **Класс Averager**: Отслеживание средних значений потерь
- **Класс SaveBestModel**: Сохранение лучшей модели по mAP
- **Функции**:
  - `save_model()`: Сохранение модели
  - `save_loss_plot()`: Сохранение графиков потерь
  - `save_validation_results()`: Сохранение результатов валидации
  - `set_training_dir()`: Создание директории для обучения
  - `set_infer_dir()`: Создание директории для инференса

#### transforms.py
- Трансформации для обучения и валидации
- Аугментации через albumentations
- Поддержка advanced аугментаций

#### annotations.py
- Утилиты для рисования аннотаций
- Визуализация bounding boxes

#### logging.py
- Настройка логирования
- Интеграция с WandB и TensorBoard

### 5. Конфигурация

#### data_configs/ppe.yaml
```yaml
TRAIN_DIR_IMAGES: 'data/train'
TRAIN_DIR_LABELS: 'data/train'
VALID_DIR_IMAGES: 'data/test'
VALID_DIR_LABELS: 'data/test'
CLASSES: ['0', '1']
NC: 2
SAVE_VALID_PREDICTION_IMAGES: True
```

## Что уже реализовано

### ✅ Готовые компоненты

1. **Архитектура модели**:
   - Faster RCNN ResNet50 FPN
   - Faster RCNN ResNet50 FPN V2
   - Поддержка предобученных весов

2. **Пайплайн обучения**:
   - Полный цикл обучения с валидацией
   - Сохранение чекпоинтов
   - Логирование метрик
   - Визуализация результатов

3. **Обработка данных**:
   - Загрузка XML аннотаций
   - Data augmentation (mosaic, albumentations)
   - Автоматическая очистка данных

4. **Инференс**:
   - Инференс на изображениях
   - Инференс на видео
   - Визуализация результатов

5. **Утилиты**:
   - Оценка COCO метрик
   - Сохранение результатов
   - Логирование

## Статус проекта

### 🔄 Текущее состояние

**Сильные стороны**:
- Полная реализация пайплайна обучения и инференса
- Хорошая структура кода
- Документированные аргументы командной строки
- Поддержка современных техник обучения

**Слабые стороны**:
- Отсутствует каталог данных (data/)
- Нет примеров использования
- Минимальная документация API
- Отсутствуют тесты
- Закомментированный код в нескольких местах
- Нет CI/CD пайплайна
- Конфигурация только для PPE датасета

## Метрики и статистика

- **Общее количество Python файлов**: 19
- **Общее количество строк кода**: ~2580
- **Поддерживаемые модели**: 2
- **Размер requirements.txt**: 23 зависимости

## Технологический стек

- **Deep Learning Framework**: PyTorch (>= 1.10.0), TorchVision (>= 0.11.0)
- **Computer Vision**: OpenCV, Pillow, scikit-image
- **Data Augmentation**: Albumentations (>= 1.1.0)
- **Metrics**: pycocotools (>= 2.0.2)
- **Logging**: WandB, TensorBoard
- **Data Processing**: NumPy, pandas, scipy
- **Visualization**: matplotlib

## Примеры использования

### Обучение модели
```bash
python train.py \
  --model fasterrcnn_resnet50_fpn_v2 \
  --config data_configs/ppe.yaml \
  --epochs 50 \
  --project-name fasterrcnn_fire_detection \
  --use-train-aug \
  --no-mosaic
```

### Инференс на изображении
```bash
python inference.py \
  --input path/to/image.jpg \
  --weights outputs/training/best_model.pth \
  --threshold 0.5 \
  --show-image
```

### Инференс на видео
```bash
python inference_video.py \
  --weights outputs/training/best_model.pth \
  --input path/to/video.mp4 \
  --show-image \
  --threshold 0.9
```

## Заметки разработчика

1. **torch_utils** код взят из официального репозитория PyTorch Vision
2. Проект изначально настроен для PPE detection, требуется адаптация для fire detection
3. Все пути к данным относительны к корню проекта
4. Результаты сохраняются в `outputs/training/` и `outputs/inference/`
