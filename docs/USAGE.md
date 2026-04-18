# 🚀 Использование

## Содержание

- [Веб-интерфейс](#веб-интерфейс)
- [CLI (командная строка)](#cli-командная-строка)
- [Python API](#python-api)
- [Параметры конфигурации](#параметры-конфигурации)

---

## Веб-интерфейс

Самый простой способ работы с моделью — через браузер.

### Запуск

**Linux/Mac:**
```bash
python launch_ui.py
# или
./launch_ui.sh
```

**Windows:**
```bat
launch_ui.bat
# или
python launch_ui.py
```

После запуска откройте браузер: `http://localhost:7860`

### Использование интерфейса

#### 1. Загрузка модели

1. Нажмите **"Model Configuration"**
2. Загрузите файл весов `.pth`
3. (Опционально) Загрузите файл конфигурации `.yaml`
4. Выберите архитектуру модели
5. Нажмите **"Load Model"**

> Без своей модели интерфейс запустится с COCO pretrained моделью.

#### 2. Детекция на изображениях

1. Перейдите на вкладку **"📷 Image Detection"**
2. Загрузите изображение (drag & drop или кнопка)
3. Настройте порог детекции (рекомендуется `0.5`)
4. Нажмите **"🔍 Detect Objects"**

#### 3. Обработка видео

1. Перейдите на вкладку **"🎥 Video Detection"**
2. Загрузите видеофайл
3. Настройте порог детекции
4. Нажмите **"🔍 Process Video"**

### Поддерживаемые форматы

| Тип | Форматы |
|-----|---------|
| Изображения | `.jpg`, `.jpeg`, `.png` |
| Видео | `.mp4`, `.avi`, `.mov` |
| Веса модели | `.pth` |
| Конфигурация | `.yaml` |

### Настройка порога детекции

| Порог | Эффект |
|-------|--------|
| `0.3` | Больше детекций, возможны ложные срабатывания |
| `0.5` | Сбалансированный вариант ✅ рекомендуется |
| `0.7` | Только уверенные детекции, меньше ложных |

### Публичный доступ

Для доступа к интерфейсу из интернета добавьте `share=True` в `app.py`:

```python
demo.launch(share=True)
```

Gradio сгенерирует временную публичную ссылку (действует 72 часа).

---

## CLI (командная строка)

### Обучение модели

```bash
python train.py \
  --model fasterrcnn_resnet50_fpn_v2 \
  --config data_configs/fire.yaml \
  --epochs 50 \
  --batch-size 4 \
  --project-name fire_detection
```

#### Параметры обучения

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--model` | Архитектура модели | `fasterrcnn_resnet50_fpn_v2` |
| `--config` | Путь к конфигурационному файлу | обязательный |
| `--epochs` | Количество эпох | `50` |
| `--batch-size` | Размер батча | `4` |
| `--workers` | Число воркеров для загрузки данных | `4` |
| `--project-name` | Имя проекта для сохранения результатов | `default` |
| `--use-train-aug` | Дополнительные аугментации | `False` |
| `--no-mosaic` | Отключить mosaic аугментацию | `False` |
| `--resume-training` | Продолжить обучение с чекпоинта | `False` |
| `--weights` | Путь к весам для fine-tuning | — |
| `--use-wandb` | Логирование в WandB | `False` |

### Инференс на изображении

```bash
python inference.py \
  --input path/to/image.jpg \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.5 \
  --show-image
```

Обработка папки изображений:

```bash
python inference.py \
  --input path/to/images/ \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.5
```

#### Параметры инференса

| Параметр | Описание |
|----------|----------|
| `--input` | Путь к изображению или папке |
| `--weights` | Путь к файлу весов `.pth` |
| `--threshold` | Порог уверенности (0–1) |
| `--show-image` | Показать результаты в окне |
| `--config` | Конфигурационный файл (опционально) |

### Инференс на видео

```bash
python inference_video.py \
  --input path/to/video.mp4 \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.7 \
  --show-image
```

---

## Python API

Вы можете использовать компоненты проекта напрямую в коде Python.

### Загрузка модели и детекция

```python
from app import FireDetectionApp

# Инициализация
app = FireDetectionApp()

# Загрузка весов
app.load_model("outputs/training/fire_detection/best_model.pth")

# Детекция на изображении (PIL Image или numpy array)
result_image, stats = app.detect_image(image, threshold=0.5)

# result_image — изображение с нанесёнными bounding boxes
# stats — строка с текстовой статистикой
```

### Прямое использование модели

```python
import torch
from models.create_fasterrcnn_model import create_model

# Создание модели
model = create_model(num_classes=3, pretrained=True)
model.load_state_dict(torch.load("best_model.pth")["model_state_dict"])
model.eval()

# Инференс
import torchvision.transforms as T

transform = T.Compose([T.ToTensor()])
image_tensor = transform(image).unsqueeze(0)

with torch.no_grad():
    predictions = model(image_tensor)

boxes = predictions[0]["boxes"]
labels = predictions[0]["labels"]
scores = predictions[0]["scores"]
```

### Пакетная обработка изображений

```python
import os
from pathlib import Path
from PIL import Image
from app import FireDetectionApp

app = FireDetectionApp()
app.load_model("best_model.pth")

images_dir = Path("data/test_images")
output_dir = Path("outputs/results")
output_dir.mkdir(exist_ok=True)

for img_path in images_dir.glob("*.jpg"):
    image = Image.open(img_path)
    result, stats = app.detect_image(image, threshold=0.5)
    result.save(output_dir / img_path.name)
    print(f"{img_path.name}: {stats}")
```

---

## Параметры конфигурации

Конфигурационные файлы находятся в `data_configs/`. Пример:

```yaml
# data_configs/fire.yaml
TRAIN_DIR_IMAGES: 'data/train'
TRAIN_DIR_LABELS: 'data/train'
VALID_DIR_IMAGES: 'data/test'
VALID_DIR_LABELS: 'data/test'

CLASSES: [
    '__background__',
    'fire',
    'smoke'
]

NC: 3                          # Число классов включая background
SAVE_VALID_PREDICTION_IMAGES: True
```

### Параметры конфигурации

| Ключ | Описание |
|------|----------|
| `TRAIN_DIR_IMAGES` | Папка с обучающими изображениями |
| `TRAIN_DIR_LABELS` | Папка с обучающими XML аннотациями |
| `VALID_DIR_IMAGES` | Папка с валидационными изображениями |
| `VALID_DIR_LABELS` | Папка с валидационными XML аннотациями |
| `CLASSES` | Список классов (первый — всегда `__background__`) |
| `NC` | Количество классов включая `__background__` |
| `SAVE_VALID_PREDICTION_IMAGES` | Сохранять изображения с предсказаниями |

---

> 🔗 Проблемы? → [FAQ.md](FAQ.md)  
> 🔗 Структура проекта → [DEVELOPMENT.md](DEVELOPMENT.md)
