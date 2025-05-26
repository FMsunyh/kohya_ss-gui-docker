import argparse
from pathlib import Path

def merge_txt_files(input_dir: Path, output_file: Path):
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: Directory {input_dir} does not exist or is not a directory.")
        return

    txt_files = sorted(input_dir.glob("*.txt"))

    with output_file.open("w", encoding="utf-8") as outfile:
        for file in txt_files:
            with file.open("r", encoding="utf-8") as infile:
                content = infile.read()
                # outfile.write(f"--- 内容来自：{file.name} ---\n")
                outfile.write(content + "\n\n")

    print(f"合并完成，输出文件为：{output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="合并目录下所有txt文件内容到一个文件中。")
    parser.add_argument("input_dir", type=Path, help="要读取的txt文件目录")
    parser.add_argument("--output", "-o", type=Path, default=Path("output.txt"), help="输出文件路径（默认是 output.txt）")

    args = parser.parse_args()
    merge_txt_files(args.input_dir, args.output)
