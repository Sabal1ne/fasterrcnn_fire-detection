# Структура данных и формат аннотаций

## Структура каталога данных

```
data/
├── train/                    # Обучающие данные
│   ├── image1.jpg
│   ├── image1.xml
│   ├── image2.jpg
│   ├── image2.xml
│   └── ...
└── test/                     # Тестовые данные
    ├── image1.jpg
    ├── image1.xml
    ├── image2.jpg
    ├── image2.xml
    └── ...
```

## Формат аннотаций Pascal VOC (XML)

Проект использует формат Pascal VOC для аннотаций. Каждое изображение должно иметь соответствующий XML файл с тем же именем.

### Пример XML файла

```xml
<annotation>
    <folder>train</folder>
    <filename>image1.jpg</filename>
    <path>/path/to/data/train/image1.jpg</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>640</width>
        <height>480</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>fire</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>100</xmin>
            <ymin>150</ymin>
            <xmax>300</xmax>
            <ymax>400</ymax>
        </bndbox>
    </object>
    <object>
        <name>smoke</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>350</xmin>
            <ymin>50</ymin>
            <xmax>600</xmax>
            <ymax>250</ymax>
        </bndbox>
    </object>
</annotation>
```

## Обязательные поля XML

### Корневой элемент `<annotation>`
Содержит все метаданные об изображении и объектах.

### Информация об изображении
- `<filename>`: Имя файла изображения (обязательно)
- `<size>`: Размеры изображения
  - `<width>`: Ширина изображения в пикселях
  - `<height>`: Высота изображения в пикселях
  - `<depth>`: Количество каналов (обычно 3 для RGB)

### Объекты `<object>` (может быть несколько)
- `<name>`: Класс объекта (должен соответствовать классам в конфигурации)
- `<bndbox>`: Координаты bounding box
  - `<xmin>`: X координата левого верхнего угла
  - `<ymin>`: Y координата левого верхнего угла
  - `<xmax>`: X координата правого нижнего угла
  - `<ymax>`: Y координата правого нижнего угла

## Важные замечания

1. **Имена файлов**: XML файл должен иметь то же имя, что и изображение (только расширение отличается)
   ```
   image1.jpg -> image1.xml
   photo_001.png -> photo_001.xml
   ```

2. **Координаты**: Все координаты должны быть в пределах размеров изображения
   - `0 <= xmin < xmax <= width`
   - `0 <= ymin < ymax <= height`

3. **Классы**: Имена классов в XML (`<name>`) должны точно совпадать с классами в конфигурационном файле

4. **Пустые изображения**: Изображения без объектов будут автоматически удалены из датасета

## Поддерживаемые форматы изображений

- JPEG (.jpg, .jpeg)
- PNG (.png)
- PPM (.ppm)

## Проверка данных

Датасет автоматически проверяется при загрузке:
- ✅ Удаляются изображения без соответствующих XML файлов
- ✅ Удаляются изображения без объектов в аннотациях
- ✅ Корректируются bounding boxes, выходящие за пределы изображения
- ✅ Логируются все проблемы с данными

## Инструменты для создания аннотаций

### Рекомендуемые инструменты:

1. **LabelImg** (рекомендуется)
   - Графический интерфейс для разметки
   - Нативная поддержка Pascal VOC формата
   - Скачать: https://github.com/tzutalin/labelImg
   
   ```bash
   pip install labelImg
   labelImg
   ```

2. **CVAT** (Computer Vision Annotation Tool)
   - Веб-интерфейс
   - Поддержка экспорта в Pascal VOC
   - Сайт: https://cvat.org/

3. **Roboflow**
   - Онлайн платформа
   - Автоматическая конвертация форматов
   - Сайт: https://roboflow.com/

## Пример скрипта проверки данных

```python
import os
import glob
from xml.etree import ElementTree as et

def validate_dataset(images_path, labels_path):
    """Validate dataset structure and annotations."""
    issues = []
    
    # Get all images and XML files
    image_files = glob.glob(os.path.join(images_path, '*.jpg'))
    xml_files = glob.glob(os.path.join(labels_path, '*.xml'))
    
    print(f"Found {len(image_files)} images")
    print(f"Found {len(xml_files)} XML annotations")
    
    # Check each image has corresponding XML
    for image_file in image_files:
        base_name = os.path.splitext(os.path.basename(image_file))[0]
        xml_file = os.path.join(labels_path, f"{base_name}.xml")
        
        if not os.path.exists(xml_file):
            issues.append(f"Missing XML for {image_file}")
            continue
            
        # Parse XML and check for objects
        tree = et.parse(xml_file)
        root = tree.getroot()
        objects = root.findall('object')
        
        if len(objects) == 0:
            issues.append(f"No objects in {xml_file}")
    
    if issues:
        print(f"\nFound {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✓ Dataset validation passed!")
    
    return len(issues) == 0

# Usage
if __name__ == "__main__":
    validate_dataset('data/train', 'data/train')
```

## Конвертация из других форматов

### Из COCO JSON в Pascal VOC XML

```python
# Скрипт будет добавлен в будущих версиях
# См. TODO.md для планируемых функций
```

### Из YOLO TXT в Pascal VOC XML

```python
# Скрипт будет добавлен в будущих версиях
# См. TODO.md для планируемых функций
```

## FAQ по данным

**Q: Могу ли я использовать изображения разных размеров?**
A: Да, изображения автоматически изменяются до размера, указанного при обучении (по умолчанию 640x640).

**Q: Что делать, если у меня только COCO формат?**
A: В будущих версиях будет добавлена поддержка COCO формата. Пока используйте инструменты конвертации.

**Q: Сколько данных нужно для обучения?**
A: Минимум 100-200 изображений на класс для приемлемых результатов. Для production рекомендуется 1000+ изображений.

**Q: Как сбалансировать классы?**
A: Используйте data augmentation и weighted sampling. Подробности в документации по обучению.
