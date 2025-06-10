<details>
<summary>🇬🇧 English...</summary>

# Stable Diffusion Configurator and Generator

This script provides an interactive interface for configuring parameters and running Stable Diffusion with convenient control over all aspects of image generation.

## Features

- 🖼️ Interactive menu with parameter navigation
- ⚙️ Loading and editing preset configurations
- 📋 Viewing available embedding and LORA models
- ✏️ Editing prompts with format hints
- 🚀 Launching image generation with custom parameters
- 📂 Specifying output path for results

## Requirements

- Python 3.7+
- Installed dependencies:
  ```
  pip install InquirerPy
  ```

## Path Configuration

Before use, you need to configure the base path and folder structure:

1. Open the script in a text editor
2. Locate the `DEFAULT_PATH` definition line and modify it:
   ```python
   DEFAULT_PATH = Path("path to your folder with models/lora/vae etc.")
   ```
3. Change the path to your base models directory
4. Ensure the following subdirectories exist in the base directory:
   ```
   ├── configs/       - JSON configuration files
   ├── embedding/     - Embedding models
   ├── lora/         - LORA models
   ├── model/        - Main Stable Diffusion models
   └── vae/          - VAE models
   ```
5. Locate the `SD_PATH` definition line and modify it:
   ```python
   SD_PATH = "path to stable-diffusion.cpp executable"
   ```

Example file structure:
```
.../sd_models/
├── configs
│   ├── portrait.json
│   ├── landscape.json
│   └── anime.json
├── embedding
│   ├── portrait_style.pt
│   └── landscape_style.pt
├── lora
│   ├── watercolor_effect.safetensors
│   └── oil_painting.safetensors
├── model
│   ├── sd_xl_base.gguf
│   └── realistic_vision.safetensors
└── vae
    ├── sdxl_vae.safetensors
    └── ft_mse.safetensors
```

## Usage

1. Run the script:
   ```
   python sd_tui.py
   ```

2. Select a configuration file from available options

3. In the main menu:
   - View current settings
   - Select parameter to edit:
     - **Sampling method**: Generation algorithm selection
     - **Image size**: Setting width and height
     - **Guidance**: Prompt adherence level
     - **CLIP skip**: CLIP layers to skip
     - **Steps**: Number of generation iterations
     - **Prompt**: Main generation text
     - **Negative prompt**: What to exclude from generation
     - **Additional parameters**: Custom SD flags

4. When editing prompts:
   - View available embedding and LORA models (they will be displayed at the top if available)
   - Use format hints:
     - For embedding: simply enter the model name
     - For LORA: use format `<lora:model_name:weight>`
       Example: `<lora:watercolor_effect:0.8>`

5. When all parameters are configured:
   - Select "🚀 Start generation"
   - Specify output path
   - Confirm generation launch

6. After completion:
   - Image will be saved at specified path
   - The console will display the last lines of generation log

## Example Configuration File

`configs/portrait.json`:
```json
{
  "model": "realistic_vision.safetensors",
  "vae": "ft_mse.safetensors",
  "sampling-method": "euler_a",
  "height": 768,
  "width": 512,
  "guidance": 7.5,
  "clip-skip": 2,
  "steps": 30,
  "default_prompt": "portrait of a woman, detailed eyes, professional photography",
  "default_negative": "blurry, deformed, ugly"
}
```

## Additional Parameters

When launching generation, you can specify additional Stable Diffusion flags, for example:
```
-s -1 --diffusion-fa --rpi
```

</details>

<details>
<summary>🇷🇺 Русский...</summary>

# Stable Diffusion Конфигуратор и Генератор

Этот скрипт предоставляет интерактивный интерфейс для настройки параметров и запуска Stable Diffusion с возможностью удобного управления всеми аспектами генерации изображений.

## Особенности

- 🖼️ Интерактивное меню с навигацией между параметрами
- ⚙️ Загрузка и редактирование предустановленных конфигураций
- 📋 Просмотр доступных embedding и LORA моделей
- ✏️ Редактирование промптов с подсказками по формату
- 🚀 Запуск генерации изображений с пользовательскими параметрами
- 📂 Указание пути для сохранения результатов

## Требования

- Python 3.7+
- Установленные зависимости:
  ```
  pip install InquirerPy
  ```

## Настройка путей

Перед использованием необходимо настроить базовый путь и структуру папок:

1. Откройте скрипт в текстовом редакторе
2. Найдите строку с определением `DEFAULT_PATH` и измените ее:
   ```python
   DEFAULT_PATH = Path("путь до вашей папки с моделями/lora/vae и другом")
   ```
3. Измените путь на ваш базовый каталог с моделями
4. Убедитесь, что в базовом каталоге созданы следующие поддиректории:
   ```
   ├── configs/       - JSON-файлы конфигураций
   ├── embedding/     - Модели embedding
   ├── lora/          - Модели LORA
   ├── model/         - Основные модели Stable Diffusion
   └── vae/           - VAE модели
   ```
5. Найдите строку с определением `SD_PATH` и измените ее:
   ```python
   SD_PATH = "путь до исполняемого файла stable-diffusion.cpp"
   ```

Пример структуры файлов:
```
.../sd_models/
├── configs
│   ├── portrait.json
│   ├── landscape.json
│   └── anime.json
├── embedding
│   ├── portrait_style.pt
│   └── landscape_style.pt
├── lora
│   ├── watercolor_effect.safetensors
│   └── oil_painting.safetensors
├── model
│   ├── sd_xl_base.gguf
│   └── realistic_vision.safetensors
└── vae
    ├── sdxl_vae.safetensors
    └── ft_mse.safetensors
```

## Использование

1. Запустите скрипт:
   ```
   python sd_tui.py
   ```

2. Выберите конфигурационный файл из списка доступных

3. В главном меню:
   - Просмотрите текущие настройки
   - Выберите параметр для редактирования:
     - **Метод сэмплирования**: Выбор алгоритма генерации
     - **Размер изображения**: Установка ширины и высоты
     - **Guidance**: Уровень соответствия промпту
     - **CLIP skip**: Пропуск слоев CLIP
     - **Шаги**: Количество итераций генерации
     - **Промпт**: Основной текст для генерации
     - **Негативный промпт**: Что исключить из генерации
     - **Дополнительные параметры**: Произвольные флаги SD

4. При редактировании промптов:
   - Просмотрите доступные embedding и LORA модели (они отобразятся вверху, если есть)
   - Используйте подсказки по формату:
     - Для embedding: просто введите название модели
     - Для LORA: используйте формат `<lora:название_модели:вес>`
       Пример: `<lora:watercolor_effect:0.8>`

5. Когда все параметры настроены:
   - Выберите "🚀 Начать генерацию"
   - Укажите путь для сохранения результата
   - Подтвердите запуск генерации

6. После завершения:
   - Изображение сохранится по указанному пути
   - В консоли отобразятся последние строки лога генерации

## Пример конфигурационного файла

`configs/portrait.json`:
```json
{
  "model": "realistic_vision.safetensors",
  "vae": "ft_mse.safetensors",
  "sampling-method": "euler_a",
  "height": 768,
  "width": 512,
  "guidance": 7.5,
  "clip-skip": 2,
  "steps": 30,
  "default_prompt": "portrait of a woman, detailed eyes, professional photography",
  "default_negative": "blurry, deformed, ugly"
}
```

## Дополнительные параметры

При запуске генерации можно указать дополнительные флаги для Stable Diffusion, например:
```
-s -1 --diffusion-fa --rpi
```

</details>
