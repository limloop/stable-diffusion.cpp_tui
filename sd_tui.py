#!/usr/bin/env python
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import subprocess
import shlex
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


DEFAULT_PATH = Path("path to your folder with models/lora/vae etc.")
SD_PATH = "path to stable-diffusion.cpp executable"

SAMPLING_METHODS = ["euler", "euler_a", "heun", "dpm2", "dpm++2s_a", "dpm++2m", "dpm++2mv2", "ipndm", "ipndm_v", "lcm", "ddim_trailing", "tcd"]
IMAGE_SIZES = [256, 512, 768, 1024, 2048]

# Language dictionaries
TRANSLATIONS = {
    "en": {
        "title": "Stable Diffusion Configurator",
        "select_config": "Select configuration file:",
        "no_configs": "No configuration files available.",
        "load_error": "Error loading configuration: {error}",
        "current_settings": "Current settings: {name}",
        "model": "Model",
        "vae": "VAE",
        "sampling_method": "Sampling method",
        "image_size": "Image size",
        "guidance": "Guidance",
        "clip_skip": "CLIP skip",
        "steps": "Steps",
        "prompt": "Prompt",
        "negative_prompt": "Negative prompt",
        "additional_params": "Additional parameters",
        "not_set": "not set",
        "main_menu": "Select action:",
        "method": "1. Sampling method",
        "size": "2. Image size",
        "guidance": "3. Guidance level",
        "clip_skip": "4. CLIP skip",
        "steps": "5. Number of steps",
        "prompt": "6. Prompt",
        "negative": "7. Negative prompt",
        "additional": "8. Additional parameters",
        "generate": "🚀 Start generation",
        "exit": "❌ Exit",
        "select_method": "Sampling method:",
        "select_height": "Image height:",
        "select_width": "Image width:",
        "enter_guidance": "Guidance level:",
        "enter_clip_skip": "CLIP skip level:",
        "enter_steps": "Number of steps:",
        "enter_prompt": "Enter prompt:",
        "enter_negative": "Enter negative prompt:",
        "enter_additional": "Additional parameters:",
        "available_embeddings": "Available embedding models: {embeddings}",
        "embedding_usage": "To use embedding, just enter its name in the prompt.",
        "available_loras": "Available LORA models: {loras}",
        "lora_usage": 'To use LORA use format: "<lora:model_name:1.0>"',
        "edit_prompt_title": " Editing prompt ",
        "edit_negative_title": " Editing negative prompt ",
        "output_path": "Output path:",
        "invalid_dir": "Directory does not exist!",
        "command_preview": "\nGenerated command:",
        "confirm_generate": "Start generation with these parameters?",
        "generation_started": "\nStarting image generation...",
        "generation_success": "✅ Generation completed successfully!",
        "saved_to": "Result saved to: {path}",
        "last_output": "\nLast output lines:",
        "generation_error": "❌ Error executing command:",
        "error_code": "Error code: {code}",
        "error_message": "Error: {message}",
        "critical_error": "❌ Critical error: {error}",
        "generation_canceled": "Generation canceled.",
        "press_any_key": "\nPress any key to continue.",
    },
    "ru": {
        "title": "Stable Diffusion Конфигуратор",
        "select_config": "Выберите конфигурационный файл:",
        "no_configs": "Нет доступных конфигурационных файлов.",
        "load_error": "Ошибка загрузки конфигурации: {error}",
        "current_settings": "Текущие настройки: {name}",
        "model": "Модель",
        "vae": "VAE",
        "sampling_method": "Метод сэмплирования",
        "image_size": "Размер изображения",
        "guidance": "Guidance",
        "clip_skip": "CLIP skip",
        "steps": "Шаги",
        "prompt": "Промпт",
        "negative_prompt": "Негативный промпт",
        "additional_params": "Дополнительные параметры",
        "not_set": "не задан",
        "main_menu": "Выберите действие:",
        "method": "1. Метод сэмплирования",
        "size": "2. Размер изображения",
        "guidance": "3. Уровень guidance",
        "clip_skip": "4. CLIP skip",
        "steps": "5. Количество шагов",
        "prompt": "6. Промпт",
        "negative": "7. Негативный промпт",
        "additional": "8. Дополнительные параметры",
        "generate": "🚀 Начать генерацию",
        "exit": "❌ Выход",
        "select_method": "Метод сэмплирования:",
        "select_height": "Высота изображения:",
        "select_width": "Ширина изображения:",
        "enter_guidance": "Уровень guidance:",
        "enter_clip_skip": "Уровень CLIP skip:",
        "enter_steps": "Количество шагов:",
        "enter_prompt": "Введите промпт:",
        "enter_negative": "Введите негативный промпт:",
        "enter_additional": "Дополнительные параметры:",
        "available_embeddings": "Доступные embedding модели: {embeddings}",
        "embedding_usage": "Для использования embedding просто введите его название в промпте.",
        "available_loras": "Доступные LORA модели: {loras}",
        "lora_usage": 'Для использования LORA используйте формат: "<lora:название_модели:1.0>"',
        "edit_prompt_title": " Редактирование промпта ",
        "edit_negative_title": " Редактирование негативного промпта ",
        "output_path": "Путь для сохранения:",
        "invalid_dir": "Директория не существует!",
        "command_preview": "\nСобранная команда:",
        "confirm_generate": "Запустить генерацию с этими параметрами?",
        "generation_started": "\nНачинаю генерацию изображения...",
        "generation_success": "✅ Генерация успешно завершена!",
        "saved_to": "Результат сохранён в: {path}",
        "last_output": "\nПоследние строки вывода:",
        "generation_error": "❌ Ошибка при выполнении команды:",
        "error_code": "Код ошибки: {code}",
        "error_message": "Ошибка: {message}",
        "critical_error": "❌ Критическая ошибка: {error}",
        "generation_canceled": "Генерация отменена.",
        "press_any_key": "\nНажмите любую клавишу для продолжения.",
    }
}

# Global language variable
LANGUAGE = "en"

def t(key: str, **kwargs) -> str:
    """Translation function"""
    return TRANSLATIONS[LANGUAGE].get(key, key).format(**kwargs)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class SDConfigEditor:
    def __init__(self):
        self.base_path = DEFAULT_PATH
        self.configs_dir = DEFAULT_PATH / "configs"
        self.config = {}
        self.additional_args = "-s -1 --diffusion-fa"
        self.current_config_name = ""
        
    def get_available_configs(self) -> List[str]:
        if not self.configs_dir.exists():
            print(f"Directory {self.configs_dir} does not exist")
            return []
            
        return [
            f.stem for f in self.configs_dir.glob("*.json") 
            if f.is_file()
        ]
    
    def select_config(self) -> bool:
        configs = self.get_available_configs()
        if not configs:
            print(t("no_configs"))
            return False
            
        self.current_config_name = inquirer.select(
            message=t("select_config"),
            choices=configs,
            default=None,
        ).execute()
        
        return self.load_config(self.current_config_name)
    
    def load_config(self, config_name: str) -> bool:
        config_path = self.configs_dir / f"{config_name}.json"
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
                self._set_default_prompts()
            return True
        except Exception as e:
            print(t("load_error", error=e))
            return False
    
    def _set_default_prompts(self):
        self.config.setdefault("prompt", self.config.get("default_prompt", ""))
        self.config.setdefault("negative_prompt", self.config.get("default_negative", ""))
    
    def display_settings(self):
        """Display current settings in table format"""
        print("\n" + "="*60)
        print(t("current_settings", name=self.current_config_name).center(60))
        print("="*60)
        
        # Main parameters
        params = [
            (t("model"), self.config.get("model", t("not_set"))),
            (t("vae"), self.config.get("vae", t("not_set"))),
            (t("sampling_method"), self.config.get("sampling-method", t("not_set"))),
            (t("image_size"), f"{self.config.get('height', 0)}x{self.config.get('width', 0)}"),
            (t("guidance"), self.config.get("guidance", 0)),
            (t("clip_skip"), self.config.get("clip-skip", 0)),
            (t("steps"), self.config.get("steps", 0)),
            (t("prompt"), self._truncate(self.config.get("prompt", ""), 50)),
            (t("negative_prompt"), self._truncate(self.config.get("negative_prompt", ""), 50)),
            (t("additional_params"), self.additional_args),
        ]
        
        for name, value in params:
            print(f"  {name:<25}: {value}")
        
        print("="*60 + "\n")
    
    def _truncate(self, text: str, max_len: int) -> str:
        return text[:max_len] + "..." if len(text) > max_len else text

    def main_menu(self):
        """Main menu with parameter navigation"""
        while True:
            clear_screen()
            self.display_settings()
            
            action = inquirer.select(
                message=t("main_menu"),
                choices=[
                    Choice(value="method", name=t("method")),
                    Choice(value="size", name=t("size")),
                    Choice(value="guidance", name=t("guidance")),
                    Choice(value="clip_skip", name=t("clip_skip")),
                    Choice(value="steps", name=t("steps")),
                    Choice(value="prompt", name=t("prompt")),
                    Choice(value="negative", name=t("negative")),
                    Choice(value="additional", name=t("additional")),
                    Separator(),
                    Choice(value="generate", name=t("generate")),
                    Choice(value="exit", name=t("exit")),
                ],
                default=None,
            ).execute()
            
            if action == "exit":
                return False
            elif action == "generate":
                return True
            else:
                # Call corresponding editor
                getattr(self, f"edit_{action}")()
    
    def edit_method(self):
        self.config["sampling-method"] = inquirer.select(
            message=t("select_method"),
            choices=SAMPLING_METHODS,
            default=self.config.get("sampling-method", SAMPLING_METHODS[0]),
        ).execute()
    
    def edit_size(self):
        # Edit height and width separately
        height = inquirer.select(
            message=t("select_height"),
            choices=[str(s) for s in IMAGE_SIZES],
            default=str(self.config.get("height", 512)),
        ).execute()
        
        width = inquirer.select(
            message=t("select_width"),
            choices=[str(s) for s in IMAGE_SIZES],
            default=str(self.config.get("width", 512)),
        ).execute()
        
        self.config["height"] = int(height)
        self.config["width"] = int(width)
    
    def edit_guidance(self):
        self.config["guidance"] = inquirer.number(
            message=t("enter_guidance"),
            float_allowed=True,
            default=self.config.get("guidance", 7.5),
            min_allowed=0.1,
            max_allowed=30.0,
        ).execute()
    
    def edit_clip_skip(self):
        self.config["clip-skip"] = inquirer.number(
            message=t("enter_clip_skip"),
            float_allowed=True,
            default=self.config.get("clip-skip", 1),
            min_allowed=0,
            max_allowed=12,
        ).execute()
    
    def edit_steps(self):
        self.config["steps"] = inquirer.number(
            message=t("enter_steps"),
            default=self.config.get("steps", 25),
            min_allowed=1,
            max_allowed=200,
        ).execute()
    
    def display_embedding_info(self):
        """Show available embedding models"""
        embedding_dir = self.base_path / "embedding"
        if embedding_dir.exists():
            embeddings = [f.stem for f in embedding_dir.glob("*") if f.is_file()]
            if embeddings:
                print(t("available_embeddings", embeddings=", ".join(embeddings)))
                print(t("embedding_usage"))

    def display_lora_info(self):
        """Show available LORA models"""
        lora_dir = self.base_path / "lora"
        if lora_dir.exists():
            loras = [f.stem for f in lora_dir.glob("*") if f.is_file()]
            if loras:
                print(t("available_loras", loras=", ".join(loras)))
                print(t("lora_usage"))

    def edit_prompt(self):
        clear_screen()
        print("="*60)
        print(t("edit_prompt_title").center(60, "="))
        print("="*60)
        
        self.display_embedding_info()
        self.display_lora_info()
        print("\n" + "="*60 + "\n")
        
        self.config["prompt"] = inquirer.text(
            message=t("enter_prompt"),
            default=self.config.get("prompt", ""),
            multiline=True,
        ).execute()

    def edit_negative(self):
        clear_screen()
        print("="*60)
        print(t("edit_negative_title").center(60, "="))
        print("="*60)
        
        self.display_embedding_info()
        self.display_lora_info()
        print("\n" + "="*60 + "\n")
        
        self.config["negative_prompt"] = inquirer.text(
            message=t("enter_negative"),
            default=self.config.get("negative_prompt", ""),
            multiline=True,
        ).execute()
    
    def edit_additional(self):
        self.additional_args = inquirer.text(
            message=t("enter_additional"),
            default=self.additional_args,
        ).execute()


class SDProcessRunner:
    def __init__(self, config: Dict[str, Any], additional_args: str):
        self.config = config
        self.additional_args = additional_args
        self.base_path = DEFAULT_PATH
    
    def get_output_path(self) -> Path:
        default_path = Path.cwd() / "output.png"
        path = inquirer.filepath(
            message=t("output_path"),
            default=str(default_path),
            only_files=True,
            validate=lambda path: Path(path).parent.exists(),
            invalid_message=t("invalid_dir"),
        ).execute()
        
        return Path(path)
    
    def build_command(self, output_path: Path) -> List[str]:
        cmd = [SD_PATH]
        
        # Main parameters
        params_map = {
            "--sampling-method": "sampling-method",
            "--height": "height",
            "--width": "width",
            "--guidance": "guidance",
            "--clip-skip": "clip-skip",
            "--steps": "steps",
        }
        
        for arg, key in params_map.items():
            if key in self.config:
                cmd.extend([arg, str(self.config[key])])
        
        # Prompts
        cmd.extend(["--prompt", f'"{self.config["prompt"]}"'])
        cmd.extend(["--negative-prompt", f'"{self.config["negative_prompt"]}"'])

        # Model paths
        cmd.extend(["--model", str(self.base_path / "model" / self.config["model"])])
        cmd.extend(["--vae", str(self.base_path / "vae" / self.config["vae"])])

        # Resource paths
        cmd.extend(["--lora-model-dir", str(self.base_path / "lora")])
        cmd.extend(["--embd-dir", str(self.base_path / "embedding")])
        
        # Output file
        cmd.extend(["--output", str(output_path)])
        
        # Additional arguments
        if self.additional_args:
            cmd.extend(shlex.split(self.additional_args))
        
        return cmd
    
    def run(self):
        output_path = self.get_output_path()
        command = self.build_command(output_path)
        
        print(t("command_preview"))
        print(" ".join(command))
        
        if inquirer.confirm(
            message=t("confirm_generate"),
            default=True
        ).execute():
            print(t("generation_started"))
            try:
                result = subprocess.run(
                    command,
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(t("generation_success"))
                print(t("saved_to", path=output_path))
                
                # Show last lines of output
                if result.stdout:
                    print(t("last_output"))
                    print(result.stdout.strip().split('\n')[-5:])
                    
            except subprocess.CalledProcessError as e:
                print(t("generation_error"))
                print(t("error_code", code=e.returncode))
                print(t("error_message", message=e.stderr))
            except Exception as e:
                print(t("critical_error", error=str(e)))
        else:
            print(t("generation_canceled"))


def select_language():
    """Language selection at startup"""
    global LANGUAGE
    language = inquirer.select(
        message="Select language / Выберите язык:",
        choices=[
            Choice(value="en", name="English"),
            Choice(value="ru", name="Русский"),
        ],
        default="en",
    ).execute()
    LANGUAGE = language


def main():
    clear_screen()
    
    # Select language first
    select_language()
    
    print("\n" + "="*50)
    print(t("title").center(50, "="))
    print("="*50)
    
    editor = SDConfigEditor()
    
    # Configuration selection
    if not editor.select_config():
        return
    
    # Main menu
    while True:
        if editor.main_menu():
            runner = SDProcessRunner(editor.config, editor.additional_args)
            runner.run()
            input(t("press_any_key"))
        else:
            break


if __name__ == '__main__':
    main()