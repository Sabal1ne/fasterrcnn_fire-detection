# 🔥 Faster RCNN Fire Detection

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 1.10+](https://img.shields.io/badge/pytorch-1.10+-orange.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Система обнаружения пожара и дыма на базе **PyTorch Faster RCNN ResNet50 FPN V2** с удобным веб-интерфейсом.

## ✨ Возможности

- 🌐 **Веб-интерфейс** на базе Gradio — детекция через браузер без кода
- 📷 **Детекция на изображениях** — одиночное фото или папка
- 🎥 **Обработка видео** — с прогресс-баром и статистикой
- 🧠 **Две архитектуры**: Faster RCNN ResNet50 FPN и FPN V2
- 📊 **Метрики COCO** (mAP) и логирование в WandB / TensorBoard
- 🔧 **Гибкие аугментации**: Mosaic, Albumentations
- 💾 **Автосохранение** лучшей модели по mAP

## ⚡ Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Sabal1ne/fasterrcnn_fire-detection.git
cd fasterrcnn_fire-detection

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить веб-интерфейс
python launch_ui.py
```

Откройте браузер: **http://localhost:7860**

## 📊 Результаты моделей

| Модель | mAP@0.5 | FPS (GPU) | FPS (CPU) |
|--------|---------|-----------|-----------|
| Faster RCNN ResNet50 FPN V2 | **46.7%** | ~15 | ~2 |
| Faster RCNN ResNet50 FPN | 37.0% | ~18 | ~3 |

## 🖥️ Обучение на своих данных

```bash
python train.py \
  --model fasterrcnn_resnet50_fpn_v2 \
  --config data_configs/fire.yaml \
  --epochs 50 \
  --batch-size 4 \
  --project-name fire_detection
```

## 🔍 Инференс

**На изображении:**
```bash
python inference.py \
  --input path/to/image.jpg \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.5
```

**На видео:**
```bash
python inference_video.py \
  --input path/to/video.mp4 \
  --weights outputs/training/fire_detection/best_model.pth \
  --threshold 0.7
```

## 📚 Документация

| Файл | Описание |
|------|----------|
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Установка, требования, проверка |
| [docs/USAGE.md](docs/USAGE.md) | Веб-интерфейс, CLI, Python API |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Архитектура, структура, расширение |
| [docs/FAQ.md](docs/FAQ.md) | Частые вопросы и решение проблем |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Руководство по вкладу в проект |

## ��️ Структура проекта

```
fasterrcnn_fire-detection/
├── app.py                 # Веб-интерфейс (Gradio)
├── train.py               # Скрипт обучения
├── inference.py           # Инференс на изображениях
├── inference_video.py     # Инференс на видео
├── datasets.py            # Dataset и DataLoader
├── models/                # Архитектуры моделей
├── utils/                 # Вспомогательные утилиты
├── torch_utils/           # PyTorch утилиты (из pytorch/vision)
├── data_configs/          # Конфигурационные файлы
└── docs/                  # Документация
```

## 🤝 Контрибуция

Мы рады любым вкладам! Смотрите [CONTRIBUTING.md](CONTRIBUTING.md) для деталей.

Приоритетные задачи:
- [ ] Тесты (pytest)
- [ ] REST API (FastAPI)
- [ ] Поддержка COCO формата
- [ ] CI/CD GitHub Actions

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 🙏 Благодарности

- [PyTorch Vision](https://github.com/pytorch/vision) за код в `torch_utils/`
- Авторам Faster RCNN за архитектуру
- Сообществу PyTorch

---

⭐ Если проект полезен — поставьте звезду!  
🐛 Нашли баг? [Создайте Issue](https://github.com/Sabal1ne/fasterrcnn_fire-detection/issues)
