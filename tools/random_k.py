import os
import random
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser(description='随机挑选数据对')
    parser.add_argument('source_dir', help='源目录路径')
    parser.add_argument('dest_dir', help='目标目录路径')
    parser.add_argument('-n', '--num_samples', type=int, default=300,
                        help='需要挑选的数量（默认：300）')
    args = parser.parse_args()

    # 创建目标目录
    os.makedirs(args.dest_dir, exist_ok=True)

    # 创建文件存在性字典
    file_pairs = {}
    for filename in os.listdir(args.source_dir):
        base, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        if ext not in ('.png', '.txt'):
            continue
        
        if base not in file_pairs:
            file_pairs[base] = {'png': False, 'txt': False}
        
        if ext == '.png':
            file_pairs[base]['png'] = True
        else:
            file_pairs[base]['txt'] = True

    # 筛选有效文件对
    valid_bases = [base for base in file_pairs 
                   if file_pairs[base]['png'] and file_pairs[base]['txt']]

    # 检查有效文件数量
    if not valid_bases:
        print("错误：源目录中没有找到有效文件对")
        return

    # 调整实际取样数量
    sample_num = min(args.num_samples, len(valid_bases))
    if sample_num < args.num_samples:
        print(f"警告：只有 {len(valid_bases)} 对有效文件，将取样 {sample_num} 对")

    # 随机取样
    selected = random.sample(valid_bases, sample_num)

    # 执行文件复制
    count = 0
    for base in selected:
        for ext in ('.png', '.txt'):
            src = os.path.join(args.source_dir, f"{base}{ext}")
            dst = os.path.join(args.dest_dir, f"{base}{ext}")
            try:
                shutil.copy2(src, dst)
                count += 0.5  # 每个文件对计数1次（0.5*2）
            except Exception as e:
                print(f"复制失败 {src}: {str(e)}")

    print(f"成功复制 {int(count)} 对文件到 {args.dest_dir}")

if __name__ == '__main__':
    main()