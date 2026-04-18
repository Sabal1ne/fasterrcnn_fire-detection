# ❓ FAQ — Часто задаваемые вопросы

## Содержание

- [Ошибки при установке](#ошибки-при-установке)
- [Ошибки при запуске](#ошибки-при-запуске)
- [Обучение модели](#обучение-модели)
- [Производительность](#производительность)
- [Кастомизация](#кастомизация)
- [Поддержка](#поддержка)

---

## Ошибки при установке

**Q: `ModuleNotFoundError: No module named 'torch'`**

A: Установите PyTorch согласно официальному сайту:
```bash
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
# CPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**Q: `ModuleNotFoundError: No module named 'pycocotools'`**

A:
```bash
# Linux/Mac
pip install pycocotools
# Windows
pip install pycocotools-windows
```

**Q: Ошибка при установке `albumentations`**

A:
```bash
pip install albumentations --upgrade
```

**Q: `error: Microsoft Visual C++ 14.0 or greater is required` (Windows)**

A: Установите [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

---

## Ошибки при запуске

**Q: `Port 7860 is already in use`**

A: Порт занят другим процессом. Измените порт в `app.py`:
```python
demo.launch(server_port=7861)
```

**Q: Интерфейс не открывается автоматически**

A: Откройте браузер вручную и перейдите на `http://localhost:7860`.

**Q: `CUDA out of memory`**

A: Уменьшите `--batch-size`:
```bash
python train.py --batch-size 2 ...
```
Или добавьте перед запуском:
```bash
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512  # Linux/Mac
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512     # Windows
```

**Q: Модель не загружается в веб-интерфейсе**

A: Проверьте:
1. Путь к файлу весов — он существует?
2. Соответствие архитектуры: файл `.pth` обучен для `fasterrcnn_resnet50_fpn_v2` — выберите именно эту архитектуру.
3. Файл не повреждён:
```python
import torch
checkpoint = torch.load("best_model.pth", map_location="cpu")
print(checkpoint.keys())
```

**Q: `FileNotFoundError` при запуске обучения**

A: Убедитесь, что структура данных соответствует конфигурации:
```bash
ls data/train/   # должны быть .jpg и .xml файлы
ls data/test/
```

---

## Обучение модели

**Q: Как изменить количество классов?**

A: Отредактируйте конфигурационный файл:
```yaml
CLASSES: ['__background__', 'class1', 'class2', 'class3']
NC: 4  # число классов + background
```

**Q: Какой формат аннотаций поддерживается?**

A: Pascal VOC XML формат. Подробнее — в [DEVELOPMENT.md](DEVELOPMENT.md#формат-данных).

**Q: Можно ли использовать изображения разных размеров?**

A: Да, датасет автоматически изменяет размер до нужного при загрузке.

**Q: Сколько данных нужно для обучения?**

A: Минимум 100–200 изображений на класс для приемлемых результатов. Для production рекомендуется 1000+ изображений на класс.

**Q: Как продолжить обучение с чекпоинта?**

A:
```bash
python train.py \
  --resume-training \
  --weights outputs/training/my_project/best_model.pth \
  --epochs 100
```

**Q: WandB просит авторизацию, я не хочу его использовать**

A: Запускайте без флага `--use-wandb` — по умолчанию WandB отключён.

---

## Производительность

**Q: Как ускорить обработку видео?**

A:
1. Убедитесь, что CUDA доступна: `python -c "import torch; print(torch.cuda.is_available())"`
2. Уменьшите разрешение входного видео
3. Закройте другие ресурсоёмкие приложения

**Q: Как ускорить инференс на изображениях?**

A:
- GPU ускоряет работу в 5–10 раз по сравнению с CPU
- Первая детекция медленнее (инициализация), последующие быстрее
- Модель `fasterrcnn_resnet50_fpn` немного быстрее, чем `v2`

**Q: Ожидаемая скорость работы**

A:

| Платформа | FPS (FPN) | FPS (FPN V2) |
|-----------|-----------|--------------|
| GPU (RTX 3080) | ~18 FPS | ~15 FPS |
| CPU | ~3 FPS | ~2 FPS |

---

## Кастомизация

**Q: Можно ли добавить новую backbone архитектуру?**

A: Да. Добавьте файл в `models/` и зарегистрируйте его в `create_fasterrcnn_model.py`. Подробнее: [DEVELOPMENT.md](DEVELOPMENT.md#добавить-новую-модель).

**Q: Как использовать несколько GPU?**

A: Поддержка multi-GPU запланирована. Пока используйте `torch.nn.DataParallel` вручную.

**Q: Как добавить поддержку COCO JSON формата?**

A: В текущей версии поддерживается только Pascal VOC XML. Поддержка COCO формата запланирована в версии 0.2.0.

**Q: Как настроить публичный доступ к интерфейсу?**

A: В `app.py` измените запуск:
```python
demo.launch(share=True)  # временная публичная ссылка (72 часа)
# или
demo.launch(server_name="0.0.0.0", server_port=7860)  # внутри сети
```

---

## Поддержка

Если вы не нашли ответ:

1. Проверьте раздел [Решение проблем](INSTALLATION.md#решение-проблем) в документации
2. Поищите среди [существующих Issues](https://github.com/Sabal1ne/fasterrcnn_fire-detection/issues)
3. Создайте [новый Issue](https://github.com/Sabal1ne/fasterrcnn_fire-detection/issues/new) с описанием проблемы, версиями Python/PyTorch и полным текстом ошибки

---

> 🔗 Установка: [INSTALLATION.md](INSTALLATION.md)  
> 🔗 Использование: [USAGE.md](USAGE.md)  
> 🔗 Разработка: [DEVELOPMENT.md](DEVELOPMENT.md)
