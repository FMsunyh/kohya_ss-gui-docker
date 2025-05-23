import os
import argparse
from PIL import Image
from PIL import PngImagePlugin

PngImagePlugin.MAX_TEXT_CHUNK = 100 * 1024 * 1024  # 提升到100MB（不推荐）

def parse_args():
    parser = argparse.ArgumentParser(description="Write prefix to each image result file")
    parser.add_argument('--image_dir', type=str, required=True, help='Path to the image directory')
    parser.add_argument('--prefix', type=str, default="", help='Prefix to write into result text files')
    return parser.parse_args()

# 安全加载 PNG 图像（忽略元数据，仅验证图像有效）
def load_image(image_path: str) -> Image.Image:
    try:
        with Image.open(image_path) as img:
            img.load()
            return img.convert('RGB')
    except OSError as e:
        print(f"Error loading image {image_path}: {e}")
        raise

# 只保存 prefix
def save_result(image_name: str, output_dir: str, prefix: str):
    txt_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(prefix)

def main():
    args = parse_args()
    image_dir = args.image_dir
    prefix = args.prefix
    output_dir = image_dir

    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Image directory not found: {image_dir}")

    image_list = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_list:
        print(f"No image files found in {image_dir}")
        return

    for image_name in image_list:
        image_path = os.path.join(image_dir, image_name)
        try:
            load_image(image_path)  # 仅验证是否能成功打开图片
            save_result(image_name, output_dir, prefix)
            print(f"✅ Processed: {image_name} -> {prefix}")
        except Exception as e:
            print(f"❌ Error processing {image_name}: {e}")

if __name__ == "__main__":
    main()
