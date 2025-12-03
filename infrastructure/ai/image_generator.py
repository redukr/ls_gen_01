
import os
import threading
from typing import List, Optional, Callable
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
import torch

class ImageGenerator:
    def __init__(self, model_path: str = "ai/models/realvisxl"):
        self.model_path = model_path
        self.pipe = None
        self.current_model = None
        self._lock = threading.Lock()

        # Налаштування для оптимізації
        torch.set_float32_matmul_precision("medium")

    def _load_model(self):
        """Завантажує модель, якщо вона ще не завантажена"""
        with self._lock:
            if self.pipe is not None and self.current_model == self.model_path:
                return

            print(f"[INFO] Завантаження моделі: {self.model_path}")

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            dtype = torch.float16

            self.pipe = StableDiffusionXLPipeline.from_pretrained(
                self.model_path,
                torch_dtype=dtype,
                use_safetensors=True,
                variant="fp16"
            ).to(device)

            # Оптимізації для RTX 3060
            self.pipe.enable_attention_slicing()
            try:
                self.pipe.vae.enable_slicing()
            except:
                pass

            try:
                self.pipe.vae.enable_tiling()
            except:
                pass

            # Використовуємо швидкий та якісний scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)

            # Прогрів моделі
            try:
                _ = self.pipe(
                    prompt="warmup test",
                    num_inference_steps=1,
                    width=512,
                    height=512
                )
            except:
                pass

            self.current_model = self.model_path

    def generate_images(
        self, 
        prompt: str, 
        count: int = 1, 
        width: int = 664, 
        height: int = 1040, 
        is_aborted: Optional[Callable[[], bool]] = None
    ) -> List[str]:
        """Генерує зображення за промптом"""
        self._load_model()

        images = []
        os.makedirs("export", exist_ok=True)

        for i in range(count):
            if is_aborted and is_aborted():
                break

            # Генерація зображення
            image = self.pipe(
                prompt=prompt,
                negative_prompt="low quality, jpeg artifacts, blurry, distorted, watermark, text, logo, signature, extra limbs, extra fingers, mutation, disfigured, poorly drawn hands, malformed anatomy, long neck, duplicate body",
                num_inference_steps=25,
                width=width,
                height=height,
                guidance_scale=5.0,
            ).images[0]

            # Збереження зображення
            output_path = f"export/ai_{i+1}.png"
            image.save(output_path)
            images.append(output_path)

        return images
