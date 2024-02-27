#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import os
from deep_translator import GoogleTranslator
from ebooklib import epub
from bs4 import BeautifulSoup
import requests
from time import sleep
import sys

"""
-----------------------------------------------
Translate ANY to zh-TW
-----------------------------------------------
"""
# def translate_text(text, target='zh-TW'):
#     translator = GoogleTranslator(source='auto', target=target)
#     ret = translator.translate(text)
#     if ret is None:
#         print(f"[error] translate none: {text}")
#         ret = text
#     return ret

def translate_text(text, target='zh-TW', max_retries=5, retry_delay=1):
    """
    尝试翻译文本，如果遇到连接错误则重试指定次数。

    参数:
    - text: 要翻译的文本字符串。
    - max_retries: 最大重试次数，默认为5。
    - retry_delay: 重试之间的延迟时间（秒），默认为1。

    返回:
    - 翻译后的文本，或在重试失败后返回None。
    """
    translator = GoogleTranslator(source='auto', target=target)
    for attempt in range(max_retries):
        try:
            translated_text = translator.translate(text)
            if translated_text is None:
                print(f"[error] translate none: {text}")
                translated_text = text
            return translated_text
        except requests.exceptions.ConnectionError as e:
            print(f"连接错误，尝试重试... ({attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                sleep(retry_delay)
            else:
                print("重试次数已用完，无法完成翻译。")
                sys.exit(1)
        except Exception as e:
            print(f"翻译过程中出现未知错误: {e}")
            sys.exit(1)


"""
-----------------------------------------------
*.srt
-----------------------------------------------
"""
def process_srt_file(filepath, output_dir):
    new_lines = []
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for no, line in enumerate(lines):
            # '\ufeff' is Byte Order Mark, BOM
            if line.strip().isnumeric() or '-->' in line or line.strip() == "" or '\ufeff' in line:
                new_lines.append(line)
            else:
                translation = translate_text(line.strip())
                new_lines.append(line.rstrip() + "\n" + translation + "\n")
            print(f"\r{100*no/len(lines):3.0f}%", end="")

            # [test]
            # if no > 50:
            #     break

    new_filepath = os.path.join(output_dir, os.path.basename(os.path.splitext(filepath)[0] + "_bilingual.srt"))
    with open(new_filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    print(f"\nfile saved:{new_filepath}")

"""
-----------------------------------------------
*.epub
-----------------------------------------------
"""
def process_epub_file(filepath, output_dir):
    book = epub.read_epub(filepath)
    for no,item in enumerate(book.get_items()):
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.content, 'html.parser')
            texts = soup.find_all(string=True)
            for text in texts:
                if text.strip():
                    translated_text = translate_text(text)
                    text.replace_with(text + "\n" + translated_text)
            item.content = str(soup).encode('utf-8')
        print(f"\r{100*no/len(list(book.get_items())):3.0f}%", end="")

    output_path = os.path.join(output_dir, os.path.basename(os.path.splitext(filepath)[0] + "_bilingual.epub"))
    epub.write_epub(output_path, book, {})
    print(f"\nfile saved:{output_path}")


"""
-----------------------------------------------
Misc files
-----------------------------------------------
"""
def process_other_file(filepath, output_dir):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        translation = translate_text(content)
        bilingual_content = content + "\n\n" + translation
    new_filepath = os.path.join(output_dir, os.path.basename(os.path.splitext(filepath)[0] + "_bilingual" + os.path.splitext(filepath)[1]))
    with open(new_filepath, 'w', encoding='utf-8') as file:
        file.write(bilingual_content)
    print(f"file saved:{new_filepath}")


"""
-----------------------------------------------
Main Process
-----------------------------------------------
"""
def translate_file(filepath, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    if filepath.endswith('.srt'):
        process_srt_file(filepath, output_dir)
    elif filepath.endswith('.epub'):
        process_epub_file(filepath, output_dir)
    else:
        process_other_file(filepath, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Translate files to bilingual format")
    parser.add_argument("filename", type=str, help="File to be translated")
    args = parser.parse_args()

    output_dir = os.path.join(os.getcwd(), "out")
    translate_file(args.filename, output_dir)

if __name__ == "__main__":
    main()
