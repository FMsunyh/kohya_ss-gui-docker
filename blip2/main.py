import os
import argparse
import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import PngImagePlugin
PngImagePlugin.MAX_TEXT_CHUNK = 100 * 1024 * 1024  # 提升到100MB（不推荐）

def parse_args():
    parser = argparse.ArgumentParser(description="Process images with BLIP2 on GPU 0")
    parser.add_argument('--image_dir', type=str, required=True, help='Path to the image directory')
    parser.add_argument('--prefix', type=str, default="", help='Optional prefix to add to each result')
    return parser.parse_args()

# 安全加载 PNG 图像（忽略元数据）
def load_image(image_path: str) -> Image.Image:
    try:
        with Image.open(image_path) as img:
            img.load()  # 加载图像数据，忽略 metadata
            return img.convert('RGB')
    except OSError as e:
        print(f"Error loading image {image_path}: {e}")
        raise

def process_image(image: Image.Image, model, processor, device) -> str:
    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True).strip()

def save_result(image_name: str, result: str, output_dir: str, prefix: str):
    txt_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"{prefix},{result}" if prefix else result)

def main():
    args = parse_args()
    image_dir = args.image_dir
    prefix = args.prefix
    output_dir = image_dir

    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Image directory not found: {image_dir}")

    model_name = "Salesforce/blip2-opt-2.7b"
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    print("🔧 Loading processor and model to GPU 0...")
    processor = Blip2Processor.from_pretrained(model_name)
    model = Blip2ForConditionalGeneration.from_pretrained(model_name).to(device)

    image_list = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_list:
        print(f"No image files found in {image_dir}")
        return

    for image_name in image_list:
        image_path = os.path.join(image_dir, image_name)
        try:
            image = load_image(image_path)
            result = process_image(image, model, processor, device)
            save_result(image_name, result, output_dir, prefix)
            print(f"✅ Processed: {image_name} -> {prefix},{result}" if prefix else f"✅ Processed: {image_name} -> {result}")
        except Exception as e:
            print(f"❌ Error processing {image_name}: {e}")

if __name__ == "__main__":
    # 强制只用第0张卡
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    main()
