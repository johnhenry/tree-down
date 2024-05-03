#!/usr/bin/env python

import os
import argparse
import base64

binaries_tuple = ('.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.bmp', '.tif', '.tiff', '.svg', '.eps', '.psd', '.ai', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.tar', '.gz', '.bz2', '.7z', '.exe', '.dll', '.so', '.lib', '.obj', '.class', '.jar', '.pyc', '.o', '.a', '.deb', '.rpm', '.dmg', '.app', '.pkg', '.iso', '.bin', '.cue', '.img', '.mdf', '.nrg', '.vcd', '.wav', '.mp3', '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.swf', '.webm', '.ogg', '.opus', '.aac', '.wma', '.flac', '.m4a', '.exe')

def get_file_content(file_path, binary_mode):
    with open(file_path, 'rb') as file:
        if binary_mode == 'base64':
            content = base64.b64encode(file.read()).decode('utf-8')
            return f"```base64\n{content}\n```"
        elif binary_mode == 'placeholder':
            return "```base64\n<Binary file content omitted>\n```"
        else:
            return None

def generate_tree(directory, output_file=None, ignore_files=None, binary_mode=None):
    tree = ''
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if ignore_files and any(file_path.endswith(pattern) for pattern in ignore_files):
                continue
            if os.path.isfile(file_path):
                tree += f"\n- {file_path[len(directory):]}\n"
                if file.endswith(binaries_tuple):
                    content = get_file_content(file_path, binary_mode)
                    if content:
                        tree += content + '\n'
                    else:
                        tree += "Binary file - content omitted\n"
                elif file.endswith(('.md', '.mdx')):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        tree += f"```{file.split('.')[-1]}\n"
                        for line in f:
                            tree += f"  {line}"  # Indent each line
                        tree += "```\n"
                else:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        tree += f"```{file.split('.')[-1]}\n{f.read()}```\n"
    if output_file:
        with open(output_file, 'w') as f:
            f.write(tree)
    else:
        print(tree)


def main():
    parser = argparse.ArgumentParser(description='Generate a markdown tree of files in a directory.')
    parser.add_argument('directory', help='Directory to generate markdown tree from')
    parser.add_argument('--output', '-o', help='Output file for the markdown tree')
    parser.add_argument('--ignore', '-i', action='append', help='Files to ignore (glob pattern)')
    parser.add_argument('--ignore-file', '-I', help='File containing patterns to ignore')
    parser.add_argument('--binary', '-b', choices=['base64', 'placeholder'], help='Include content of binary files (default: omitted)')
    args = parser.parse_args()

    ignore_files = set()
    if args.ignore:
        ignore_files.update(args.ignore)
    if args.ignore_file:
        with open(args.ignore_file, 'r') as f:
            ignore_files.update(line.strip() for line in f.readlines())

    generate_tree(args.directory, args.output, ignore_files, args.binary)

if __name__ == "__main__":
    main()
