# 🚀 Руководство по развертыванию на хостинге

Это руководство описывает несколько способов развертывания нейросети Faster RCNN Fire Detection на различных платформах хостинга для обеспечения доступа с любого устройства.

## 📋 Содержание

1. [Gradio Share - Быстрый старт](#1-gradio-share---быстрый-старт)
2. [Hugging Face Spaces - Рекомендуется](#2-hugging-face-spaces---рекомендуется)
3. [Docker - Универсальное решение](#3-docker---универсальное-решение)
4. [Railway.app - Простое развертывание](#4-railwayapp---простое-развертывание)
5. [Render.com - Бесплатный хостинг](#5-rendercom---бесплатный-хостинг)
6. [Google Cloud Run](#6-google-cloud-run)
7. [AWS EC2](#7-aws-ec2)

---

## 1. Gradio Share - Быстрый старт

**Самый простой способ для быстрого тестирования (временная ссылка на 72 часа)**

### Запуск с публичной ссылкой

```bash
# Установите переменную окружения
export GRADIO_SHARE=True

# Запустите приложение
python launch_ui.py
```

Или в Windows:
```cmd
set GRADIO_SHARE=True
python launch_ui.py
```

После запуска вы получите публичную ссылку вида: `https://xxxxx.gradio.live`

### С аутентификацией

```bash
export GRADIO_SHARE=True
export GRADIO_AUTH=username:password
python launch_ui.py
```

**Преимущества:**
- ✅ Мгновенное развертывание
- ✅ Не требует настройки
- ✅ HTTPS из коробки

**Недостатки:**
- ❌ Ссылка действует только 72 часа
- ❌ Ограниченная пропускная способность
- ❌ Не подходит для production

---

## 2. Hugging Face Spaces - Рекомендуется

**Лучший вариант для постоянного публичного доступа (бесплатно)**

### Шаг 1: Создайте Space на Hugging Face

1. Зарегистрируйтесь на [huggingface.co](https://huggingface.co)
2. Перейдите в [Spaces](https://huggingface.co/spaces)
3. Нажмите "Create new Space"
4. Выберите:
   - **Space name**: fire-detection (или любое другое)
   - **License**: MIT
   - **Space SDK**: Gradio
   - **Space hardware**: CPU basic (или GPU для лучшей производительности)

### Шаг 2: Настройте Space

Скопируйте следующие файлы в ваш Space:

```bash
# Клонируйте ваш Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/fire-detection
cd fire-detection

# Скопируйте необходимые файлы из репозитория
cp ../fasterrcnn_fire-detection/app.py .
cp ../fasterrcnn_fire-detection/requirements.txt .
cp -r ../fasterrcnn_fire-detection/models .
cp -r ../fasterrcnn_fire-detection/utils .
cp -r ../fasterrcnn_fire-detection/torch_utils .
cp -r ../fasterrcnn_fire-detection/data_configs .

# Переименуйте README для Hugging Face
cp ../fasterrcnn_fire-detection/README_HF.md ./README.md
```

### Шаг 3: Загрузите веса модели (опционально)

Если у вас есть обученная модель:

```bash
# Создайте директорию для весов
mkdir -p outputs/training/fire_model

# Скопируйте ваши веса
cp /path/to/your/best_model.pth outputs/training/fire_model/
```

### Шаг 4: Отправьте в Space

```bash
git add .
git commit -m "Initial deployment"
git push
```

Space автоматически соберется и запустится!

### Настройка окружения в Hugging Face

В настройках Space можете добавить переменные окружения:
- `GRADIO_AUTH=username:password` - для защиты паролем

**Преимущества:**
- ✅ Бесплатный постоянный хостинг
- ✅ Автоматический HTTPS
- ✅ Простое обновление (git push)
- ✅ Интеграция с сообществом ML
- ✅ Поддержка GPU (платно)

**Недостатки:**
- ❌ Ограничения на размер хранилища
- ❌ CPU версия может быть медленной для видео

**URL вашего приложения**: `https://huggingface.co/spaces/YOUR_USERNAME/fire-detection`

---

## 3. Docker - Универсальное решение

**Для развертывания на любой платформе с поддержкой Docker**

### Локальная сборка и запуск

```bash
# Соберите Docker образ
docker build -t fire-detection .

# Запустите контейнер
docker run -p 7860:7860 fire-detection
```

### С docker-compose (рекомендуется)

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f
```

### С GPU поддержкой

Раскомментируйте секцию GPU в `docker-compose.yml` и запустите:

```bash
docker-compose up -d
```

### С аутентификацией

```bash
docker run -p 7860:7860 \
  -e GRADIO_AUTH=username:password \
  fire-detection
```

**Преимущества:**
- ✅ Полная изоляция окружения
- ✅ Легко масштабировать
- ✅ Работает везде, где есть Docker
- ✅ Поддержка GPU

**Недостатки:**
- ❌ Требует базовых знаний Docker
- ❌ Больший размер образа

---

## 4. Railway.app - Простое развертывание

**Современная платформа с простым развертыванием из GitHub**

### Шаг 1: Подготовка

1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Подключите GitHub аккаунт
3. Создайте файл `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Шаг 2: Развертывание

1. Нажмите "New Project" в Railway
2. Выберите "Deploy from GitHub repo"
3. Выберите репозиторий `fasterrcnn_fire-detection`
4. Railway автоматически обнаружит Dockerfile и развернет приложение

### Шаг 3: Настройка переменных окружения

В Railway Dashboard → Variables:
- `GRADIO_SERVER_NAME=0.0.0.0`
- `GRADIO_SERVER_PORT=7860`
- `GRADIO_SHARE=False`
- `GRADIO_AUTH=username:password` (опционально)

**Преимущества:**
- ✅ Бесплатный план для начала
- ✅ Автоматическое развертывание из GitHub
- ✅ Простая настройка
- ✅ Автоматический HTTPS

**Недостатки:**
- ❌ Ограниченные бесплатные ресурсы
- ❌ Нет бесплатного GPU

**Ваше приложение будет доступно по**: `https://your-app.railway.app`

---

## 5. Render.com - Бесплатный хостинг

**Бесплатная альтернатива с автоматическим развертыванием**

### Шаг 1: Создайте render.yaml

```yaml
services:
  - type: web
    name: fire-detection
    env: docker
    dockerfilePath: ./Dockerfile
    plan: free
    region: oregon
    envVars:
      - key: GRADIO_SERVER_NAME
        value: 0.0.0.0
      - key: GRADIO_SERVER_PORT
        value: 7860
      - key: GRADIO_SHARE
        value: False
      # Uncomment for authentication
      # - key: GRADIO_AUTH
      #   value: username:password
```

### Шаг 2: Развертывание

1. Зарегистрируйтесь на [render.com](https://render.com)
2. Нажмите "New +" → "Web Service"
3. Подключите GitHub репозиторий
4. Render автоматически обнаружит `render.yaml` и развернет

**Преимущества:**
- ✅ Бесплатный план навсегда
- ✅ Автоматический HTTPS
- ✅ Простая настройка

**Недостатки:**
- ❌ Бесплатный план "засыпает" после 15 минут бездействия
- ❌ Медленный холодный старт
- ❌ Нет GPU на бесплатном плане

**URL**: `https://fire-detection.onrender.com`

---

## 6. Google Cloud Run

**Для масштабируемых производственных развертываний**

### Предварительные требования

```bash
# Установите Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Авторизуйтесь
gcloud auth login

# Создайте проект (если нет)
gcloud projects create fire-detection-project
gcloud config set project fire-detection-project
```

### Развертывание

```bash
# Соберите и отправьте образ в Google Container Registry
gcloud builds submit --tag gcr.io/fire-detection-project/fire-detection

# Разверните на Cloud Run
gcloud run deploy fire-detection \
  --image gcr.io/fire-detection-project/fire-detection \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --port 7860 \
  --set-env-vars GRADIO_SERVER_NAME=0.0.0.0,GRADIO_SERVER_PORT=7860
```

**Преимущества:**
- ✅ Автомасштабирование
- ✅ Оплата за использование
- ✅ Высокая доступность
- ✅ Интеграция с GCP

**Недостатки:**
- ❌ Требует настройки GCP
- ❌ Платный сервис

---

## 7. AWS EC2

**Для полного контроля над сервером**

### Шаг 1: Создайте EC2 инстанс

1. Войдите в AWS Console
2. Запустите EC2 инстанс:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t3.medium (или больше для GPU: g4dn.xlarge)
   - Security Group: Откройте порт 7860

### Шаг 2: Подключитесь и установите зависимости

```bash
# Подключитесь к инстансу
ssh -i your-key.pem ubuntu@your-ec2-ip

# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Клонируйте репозиторий
git clone https://github.com/Sabal1ne/fasterrcnn_fire-detection.git
cd fasterrcnn_fire-detection
```

### Шаг 3: Запустите приложение

```bash
# С Docker
docker-compose up -d

# Или без Docker
pip install -r requirements.txt
python app.py
```

### Шаг 4: Настройте Nginx (опционально, для HTTPS)

```bash
sudo apt install nginx certbot python3-certbot-nginx

# Создайте конфигурацию Nginx
sudo nano /etc/nginx/sites-available/fire-detection

# Добавьте:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Активируйте конфигурацию
sudo ln -s /etc/nginx/sites-available/fire-detection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Получите SSL сертификат
sudo certbot --nginx -d your-domain.com
```

**Преимущества:**
- ✅ Полный контроль
- ✅ Поддержка GPU
- ✅ Настраиваемая производительность

**Недостатки:**
- ❌ Требует администрирования
- ❌ Нужна ручная настройка безопасности
- ❌ Оплата 24/7

---

## 🔒 Безопасность

### Включение аутентификации

Для всех методов развертывания рекомендуется включить аутентификацию:

```bash
# Через переменную окружения
export GRADIO_AUTH=username:password

# Или в Docker
docker run -e GRADIO_AUTH=username:password ...
```

### Рекомендации по безопасности

1. **Всегда используйте HTTPS** в production
2. **Включите аутентификацию** для защиты от несанкционированного доступа
3. **Ограничьте доступ к API** с помощью firewall правил
4. **Регулярно обновляйте зависимости**: `pip install -r requirements.txt --upgrade`
5. **Используйте секреты** для чувствительных данных (не храните в коде)
6. **Мониторьте использование** для обнаружения аномалий

---

## 📊 Сравнение платформ

| Платформа | Бесплатно | Простота | GPU | Постоянный | Лучше для |
|-----------|-----------|----------|-----|------------|-----------|
| Gradio Share | ✅ | ⭐⭐⭐⭐⭐ | ❌ | ❌ (72h) | Тестирование |
| Hugging Face | ✅ | ⭐⭐⭐⭐ | 💰 | ✅ | Демо, публичный доступ |
| Railway | 💰 | ⭐⭐⭐⭐⭐ | ❌ | ✅ | Быстрый старт |
| Render | ✅ | ⭐⭐⭐⭐ | ❌ | ✅* | Малые проекты |
| Cloud Run | 💰 | ⭐⭐⭐ | ❌ | ✅ | Production |
| AWS EC2 | 💰 | ⭐⭐ | ✅ | ✅ | Полный контроль |

*Засыпает после бездействия на бесплатном плане

---

## 🛠️ Устранение неполадок

### Приложение не запускается

```bash
# Проверьте логи
docker-compose logs -f

# Или для Python
python app.py
```

### Ошибка "Port already in use"

```bash
# Измените порт
export GRADIO_SERVER_PORT=8080
python app.py
```

### Проблемы с GPU

```bash
# Проверьте CUDA
nvidia-smi

# Убедитесь, что PyTorch установлен с CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

### Медленная работа

1. Используйте GPU инстанс
2. Оптимизируйте размер модели
3. Включите кэширование
4. Используйте CDN для статических файлов

---

## 📝 Переменные окружения

Полный список поддерживаемых переменных:

```bash
# Основные настройки
GRADIO_SERVER_NAME=0.0.0.0      # IP адрес сервера
GRADIO_SERVER_PORT=7860          # Порт приложения
GRADIO_SHARE=False               # Публичная ссылка (True/False)

# Безопасность
GRADIO_AUTH=username:password    # Базовая аутентификация

# Опционально (для будущих расширений)
MODEL_PATH=/path/to/model.pth    # Путь к модели по умолчанию
CONFIG_PATH=/path/to/config.yaml # Путь к конфигу
DEVICE=cuda                      # Устройство (cuda/cpu)
```

---

## 🎯 Рекомендации

### Для тестирования и демо:
👉 **Gradio Share** или **Hugging Face Spaces**

### Для небольших проектов:
👉 **Hugging Face Spaces** (бесплатно) или **Railway** (простота)

### Для production:
👉 **Google Cloud Run** (масштабируемость) или **AWS EC2** (контроль)

### Для команды разработчиков:
👉 **Docker** + любая платформа

---

## 📚 Дополнительные ресурсы

- [Gradio Documentation](https://gradio.app/docs/)
- [Hugging Face Spaces Guide](https://huggingface.co/docs/hub/spaces)
- [Docker Documentation](https://docs.docker.com/)
- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)

---

## 🤝 Поддержка

Если у вас возникли проблемы:
1. Проверьте [Issues](https://github.com/Sabal1ne/fasterrcnn_fire-detection/issues)
2. Создайте новый Issue с описанием проблемы
3. Укажите платформу и логи ошибок

---

**Удачного развертывания! 🚀**
