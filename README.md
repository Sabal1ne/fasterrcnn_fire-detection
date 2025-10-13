# Faster RCNN Fire Detection

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 1.10+](https://img.shields.io/badge/pytorch-1.10+-orange.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Обнаружение объектов с помощью PyTorch Faster RCNN ResNet50 FPN V2**

Проект для обнаружения пожара и других объектов с использованием современных архитектур Faster RCNN.

## 🔥 Основные возможности

- ✅ **Веб-интерфейс**: Удобный Gradio интерфейс для работы с моделью через браузер
- ✅ Две архитектуры модели: Faster RCNN ResNet50 FPN и FPN V2
- ✅ Поддержка предобученных весов
- ✅ Гибкая система аугментаций (Mosaic, Albumentations)
- ✅ Инференс на изображениях и видео
- ✅ Логирование в WandB и TensorBoard
- ✅ Автоматическое сохранение лучшей модели
- ✅ Поддержка Pascal VOC формата аннотаций (XML)
- ✅ **Развертывание на хостинге**: Готовые конфигурации для публичного доступа

## 📋 Содержание

- [Установка](#-установка)
- [Быстрый старт](#-быстрый-старт)
  - [🌐 Веб-интерфейс](#-веб-интерфейс-рекомендуется) (Рекомендуется!)
  - [CLI интерфейс](#инференс-на-изображении-cli)
- [🚀 Развертывание на хостинге](#-развертывание-на-хостинге) (Новое!)
- [Структура проекта](#-структура-проекта)
- [Использование](#-использование)
- [Конфигурация](#-конфигурация)
- [Документация](#-документация)
- [Контрибуция](#-контрибуция)
- [Лицензия](#-лицензия)

## 🚀 Установка

### Требования

- Python 3.7+
- PyTorch 1.10+
- CUDA (опционально, для GPU)

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/Sabal1ne/fasterrcnn_fire-detection.git
cd fasterrcnn_fire-detection
```

### Шаг 2: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 3: Подготовка данных

Создайте структуру каталогов:

```bash
mkdir -p data/train data/test
```

Поместите ваши изображения и XML аннотации в папки `data/train` и `data/test`.

## ⚡ Быстрый старт

> 💡 **Новичок?** Смотрите [QUICKSTART.md](QUICKSTART.md) для пошагового руководства!

### 🌐 Веб-интерфейс (Рекомендуется)

**Самый простой способ использования нейросети!**

```bash
python launch_ui.py
```

Или напрямую:

```bash
python app.py
```

Откройте браузер по адресу: `http://localhost:7860`

Веб-интерфейс предоставляет:
- 📷 Детекция на изображениях с загрузкой через браузер
- 🎥 Обработка видео с прогресс-баром
- ⚙️ Удобная настройка порога детекции
- 📊 Подробная статистика обнаружений
- 🎨 Современный и интуитивный дизайн

📖 Подробнее: [WEB_INTERFACE.md](WEB_INTERFACE.md)

## 🚀 Развертывание на хостинге

Теперь вы можете развернуть нейросеть на хостинге для доступа с любого устройства!

### Быстрый старт - Публичная ссылка

Запустите с публичной ссылкой (действует 72 часа):

**Linux/Mac:**
```bash
./launch_public.sh
```

**Windows:**
```cmd
launch_public.bat
```

**Или через Python:**
```bash
export GRADIO_SHARE=True  # Linux/Mac
set GRADIO_SHARE=True     # Windows
python launch_ui.py
```

После запуска вы получите публичную ссылку вида `https://xxxxx.gradio.live` для доступа с любого устройства!

### Постоянное развертывание

Для постоянного хостинга доступны несколько вариантов:

1. **🤗 Hugging Face Spaces** (рекомендуется, бесплатно)
   - Простое развертывание через git push
   - Бесплатный постоянный хостинг
   - Автоматический HTTPS

2. **🐳 Docker** (универсальное решение)
   ```bash
   docker-compose up -d
   ```

3. **☁️ Railway / Render / Cloud Run**
   - Готовые конфигурационные файлы включены
   - Автоматическое развертывание из GitHub

📖 **Полное руководство по развертыванию**: [DEPLOYMENT.md](DEPLOYMENT.md)

### Обучение модели

```bash
python train.py \
  --model fasterrcnn_resnet50_fpn_v2 \
  --config data_configs/fire.yaml \
  --epochs 50 \
  --batch-size 4 \
  --project-name fire_detection
```

### Инференс на изображении (CLI)

```bash
python inference.py \
  --input path/to/image.jpg \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.5 \
  --show-image
```

### Инференс на видео (CLI)

```bash
python inference_video.py \
  --input path/to/video.mp4 \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.7 \
  --show-image
```

## 📁 Структура проекта

```
fasterrcnn_fire-detection/
├── data_configs/          # Конфигурационные файлы
│   ├── fire.yaml         # Конфигурация для fire detection
│   └── ppe.yaml          # Конфигурация для PPE detection
├── models/                # Определения моделей
├── utils/                 # Вспомогательные утилиты
├── torch_utils/           # PyTorch утилиты
├── app.py                 # 🌐 Веб-интерфейс (Gradio)
├── launch_ui.py           # Запуск веб-интерфейса
├── train.py              # Скрипт обучения
├── inference.py          # Инференс на изображениях
├── inference_video.py    # Инференс на видео
└── datasets.py           # Dataset и DataLoader

Подробнее: см. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
```

## 📚 Использование

### 🌐 Веб-интерфейс

Самый простой способ работы с моделью:

```bash
python launch_ui.py
```

Интерфейс предоставляет:

1. **Загрузка модели**: Загрузите обученные веса и конфигурацию
2. **Детекция на изображениях**: Перетащите изображение и получите результат
3. **Обработка видео**: Загрузите видео для обработки всех кадров
4. **Настройка параметров**: Изменяйте порог детекции в реальном времени
5. **Статистика**: Получайте подробную информацию об обнаружениях

### Параметры обучения

```bash
python train.py --help
```

Основные параметры:
- `--model`: Выбор модели (`fasterrcnn_resnet50_fpn` или `fasterrcnn_resnet50_fpn_v2`)
- `--config`: Путь к конфигурационному файлу
- `--epochs`: Количество эпох обучения
- `--batch-size`: Размер батча
- `--project-name`: Имя проекта для сохранения результатов
- `--use-train-aug`: Использование дополнительных аугментаций
- `--no-mosaic`: Отключение mosaic аугментации

### Параметры инференса

```bash
python inference.py --help
```

Основные параметры:
- `--input`: Путь к изображению или папке
- `--weights`: Путь к файлу весов модели
- `--threshold`: Порог уверенности для детекции (0-1)
- `--show-image`: Показать результаты на экране
- `--config`: Путь к конфигурационному файлу (опционально)

## ⚙️ Конфигурация

Конфигурационные файлы находятся в `data_configs/`. Пример конфигурации:

```yaml
TRAIN_DIR_IMAGES: 'data/train'
TRAIN_DIR_LABELS: 'data/train'
VALID_DIR_IMAGES: 'data/test'
VALID_DIR_LABELS: 'data/test'

CLASSES: [
    '__background__',
    'fire',
    'smoke'
]

NC: 3
SAVE_VALID_PREDICTION_IMAGES: True
```

## 📖 Документация

- [QUICKSTART.md](QUICKSTART.md) - 🚀 Пошаговое руководство для начинающих
- [WEB_INTERFACE.md](WEB_INTERFACE.md) - 🌐 Руководство по веб-интерфейсу
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Подробная структура проекта
- [DATA_FORMAT.md](DATA_FORMAT.md) - Формат данных и аннотаций
- [TODO.md](TODO.md) - План развития и задачи
- [CONTRIBUTING.md](CONTRIBUTING.md) - Руководство по контрибуции

## 🏗️ Архитектура модели

### Предварительная подготовка Backbone ResNet50

Предварительная подготовка Backbone ResNet50 является важной задачей для повышения производительности всей модели обнаружения объектов. Модель ResNet50 (как и многие другие модели классификации) была обучена с использованием нового рецепта обучения. К ним относятся, но не ограничиваются ими:

* Оптимизация скорости обучения.
* Более длительное обучение.
* Дополнения, такие как TrivialAugment, случайное стирание, MixUp и CutMix.
* Повторное увеличение
* EMA
* Настройка уменьшения веса

Благодаря этим новым технологиям точность ResNet50 @ 1 возрастает до 80,858% с прежних 76,130%.

### Обучение Faster RCNN ResNet50 FPN V2

Как упоминалось ранее, большинство улучшений для обучения всей модели обнаружения объектов были взяты из вышеупомянутой статьи.

Авторы этих улучшений называют их улучшениями в соответствии с оптимизацией после публикации статьи. К ним относятся:

* FPN с пакетной нормализацией.
* Использование двух сверточных уровней в сети Region Proposal * (RPN) вместо одного. Другими словами, использование более мощного модуля FPN.
* Используя более массивную головку регрессии. Если быть точным, используя четыре сверточных слоя с пакетной нормализацией, за которыми следует линейный слой. Ранее использовалась двухслойная MLP-головка без пакетной нормализации.
* Нормализации замороженных пакетов не использовались.

**Результаты**: Использование приведенного выше рецепта улучшает mAP с предыдущих 37,0% до 46,7%, что дает увеличение mAP на 9,7%.

## 💡 Примеры и руководства

### Пример 1: Обучение на custom датасете

## 💡 Примеры и руководства

### Пример 1: Обучение на custom датасете

1. Подготовьте ваш датасет в формате Pascal VOC (изображения + XML аннотации)
2. Создайте конфигурационный файл в `data_configs/`
3. Запустите обучение:

```bash
python train.py \
  --model fasterrcnn_resnet50_fpn_v2 \
  --config data_configs/your_config.yaml \
  --epochs 50 \
  --batch-size 4 \
  --project-name your_project
```

### Пример 2: Fine-tuning на предобученной модели

```bash
python train.py \
  --model fasterrcnn_resnet50_fpn_v2 \
  --config data_configs/fire.yaml \
  --epochs 25 \
  --resume-training \
  --weights outputs/training/previous_model/best_model.pth
```

### Пример 3: Batch inference на папке изображений

```bash
python inference.py \
  --input data/test_images/ \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.6
```

## 🎯 Метрики производительности

### Faster RCNN ResNet50 FPN V2
- **mAP@0.5**: 46.7% (улучшение на 9.7% по сравнению с FPN)
- **Inference Speed**: ~15 FPS (GPU), ~2 FPS (CPU)
- **Model Size**: ~160 MB

### Faster RCNN ResNet50 FPN
- **mAP@0.5**: 37.0%
- **Inference Speed**: ~18 FPS (GPU), ~3 FPS (CPU)
- **Model Size**: ~160 MB

## ❓ FAQ

<details>
<summary><b>Как изменить количество классов?</b></summary>

Отредактируйте конфигурационный файл в `data_configs/`:
```yaml
CLASSES: ['__background__', 'class1', 'class2', ...]
NC: количество_классов_включая_background
```
</details>

<details>
<summary><b>Как использовать несколько GPU?</b></summary>

Используйте `torch.nn.DataParallel` или `torch.nn.parallel.DistributedDataParallel`. 
Поддержка будет добавлена в будущих версиях.
</details>

<details>
<summary><b>Какой формат аннотаций поддерживается?</b></summary>

Сейчас поддерживается только Pascal VOC XML формат. Поддержка COCO JSON планируется.
</details>

<details>
<summary><b>Можно ли использовать другие backbone архитектуры?</b></summary>

Да, вы можете добавить свою модель в `models/` следуя существующим примерам.
</details>

## 🤝 Контрибуция

Мы приветствуем любые вклады! Пожалуйста, ознакомьтесь с [CONTRIBUTING.md](CONTRIBUTING.md) для получения подробной информации.

### Приоритетные задачи
- [x] ~~Веб-интерфейс для удобного использования~~ ✅
- [ ] Адаптация для fire detection
- [ ] Добавление тестов
- [ ] Поддержка COCO формата
- [ ] REST API для инференса

См. полный список задач в [TODO.md](TODO.md)

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 🙏 Благодарности

- PyTorch Vision для кода в `torch_utils/`
- Faster RCNN авторы за отличную архитектуру
- Сообщество PyTorch за поддержку

## 📧 Контакты

- GitHub Issues: [Создать issue](https://github.com/Sabal1ne/fasterrcnn_fire-detection/issues)
- Автор: [@Sabal1ne](https://github.com/Sabal1ne)

---

⭐ Если проект был полезен, поставьте звезду!
