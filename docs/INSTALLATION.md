# 📦 Установка

## Содержание

- [Требования](#требования)
- [Установка](#установка)
- [Проверка установки](#проверка-установки)
- [Решение проблем](#решение-проблем)

---

## Требования

| Компонент | Версия | Обязательно |
|-----------|--------|-------------|
| Python | 3.7+ | ✅ Да |
| PyTorch | 1.10+ | ✅ Да |
| TorchVision | 0.11+ | ✅ Да |
| CUDA | 11.0+ | ❌ Нет (нужен для GPU) |

> 💡 Без CUDA проект работает на CPU — медленнее, но функционально полностью.

---

## Установка

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/Sabal1ne/fasterrcnn_fire-detection.git
cd fasterrcnn_fire-detection
```

### Шаг 2: (Опционально) Создание виртуального окружения

```bash
# Создание
python -m venv venv

# Активация — Linux/Mac
source venv/bin/activate

# Активация — Windows
venv\Scripts\activate
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

**Ключевые пакеты:**

| Пакет | Назначение |
|-------|------------|
| `torch`, `torchvision` | Deep learning фреймворк |
| `opencv-python` | Обработка изображений и видео |
| `albumentations` | Аугментации данных |
| `gradio` | Веб-интерфейс |
| `pycocotools` | Метрики COCO (mAP) |
| `wandb` | Логирование экспериментов (опционально) |

### Автоматическая установка (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
```

Скрипт создаст виртуальное окружение, установит зависимости и подготовит структуру каталогов.

---

## Проверка установки

### Проверка зависимостей

```bash
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import torchvision; print('TorchVision:', torchvision.__version__)"
python -c "import gradio; print('Gradio:', gradio.__version__)"
```

### Проверка GPU (если используется)

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

### Тестовый запуск интерфейса

```bash
python launch_ui.py
```

Перейдите в браузере на `http://localhost:7860`. Если страница открылась — установка прошла успешно.

---

## Решение проблем

### `ModuleNotFoundError: No module named 'torch'`

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

Или для CPU:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### `ModuleNotFoundError: No module named 'pycocotools'`

**Linux/Mac:**
```bash
pip install pycocotools
```

**Windows:**
```bash
pip install pycocotools-windows
```

### `ModuleNotFoundError: No module named 'cv2'`

```bash
pip install opencv-python
# или headless вариант (без GUI)
pip install opencv-python-headless
```

### Ошибка при установке `albumentations`

```bash
pip install albumentations --upgrade
```

### Медленная работа без GPU

Убедитесь, что установлена версия PyTorch с поддержкой CUDA:

```bash
python -c "import torch; print(torch.version.cuda)"
```

Если вывод `None` — переустановите PyTorch с CUDA поддержкой.

---

> 🔗 Подробнее об использовании: [USAGE.md](USAGE.md)
