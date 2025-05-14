import os
import sys
import warnings
from PIL import Image
from PIL.Image import DecompressionBombWarning

def is_image_file(filename):
    """检查文件扩展名是否为常见图片格式"""
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    return os.path.splitext(filename)[1].lower() in allowed_extensions

def process_directory(root_dir):
    """遍历目录处理图片文件"""
    # 将解压缩炸弹警告转换为异常
    warnings.simplefilter('error', DecompressionBombWarning)
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not is_image_file(file):
                continue

            try:
                with Image.open(file_path) as img:
                    # 显式加载图片数据
                    img.load()
            except DecompressionBombWarning as e:
                print(f"发现解压缩炸弹文件: {file_path} - 文件大小: {os.path.getsize(file_path)//1024}KB")
                handle_deletion(file_path)
            except Exception as e:
                print(f"发现损坏文件: {file_path} - 错误类型: {type(e).__name__}")
                handle_deletion(file_path)

def handle_deletion(file_path):
    """处理文件删除操作"""
    try:
        os.remove(file_path)
        print(f"已成功删除: {file_path}")
    except Exception as delete_error:
        print(f"删除失败: {file_path} - 错误: {delete_error}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python image_safety_check.py <目录路径>")
        print("示例: python image_safety_check.py ./photos")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"错误: 目录不存在 - {target_dir}")
        sys.exit(1)
    
    print(f"开始安全扫描: {target_dir}")
    process_directory(target_dir)
    print("安全扫描完成")


