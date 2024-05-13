# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import os
from deep_translator import GoogleTranslator
from ebooklib import epub
import fitz # PyMuPDF (pip install PyMuPDF)
from bs4 import BeautifulSoup, NavigableString, Tag
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
def translate_text_single(text, target='zh-TW', max_retries=5, retry_delay=1):
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
                # print(f"[error] translate none: {text}")
                translated_text = text
            return translated_text
        except requests.exceptions.ConnectionError as e:
            print(f"连接错误，尝试重试... ({attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                print(f"retry...{attempt}")
                sleep(retry_delay)
            else:
                print("重试次数已用完，无法完成翻译。")
                sys.exit(1)
        except Exception as e:
            print(f"翻譯內容: {text}")
            print(f"翻译过程中出现未知错误: {e}")
            raise e

def translate_text(text, target='zh-TW', max_retries=5, retry_delay=1):
    """
    尝试翻译文本，如果遇到连接错误则重试指定次数。

    参数:
    - text: 要翻译的文本字符串。
    - target: 翻译的目标语言，默认为'zh-TW'。
    - max_retries: 最大重试次数，默认为5。
    - retry_delay: 重试之间的延迟时间（秒），默认为1。

    返回:
    - 翻译后的文本，或在重试失败后返回None。
    """
    # 如果文本长度超过4000字符，按行分割并逐行翻译
    if len(text) > 4000:
        print(f"\ntext to be translated too long:{len(text)}, split it in lines:")
        lines = text.split('\n')
        translated_lines = []
        for no, line in enumerate(lines):
            print(f"\r\tline complete:{100*no/len(lines):3.0f}%", end="")
            translated_line = translate_text_single(line, target=target, max_retries=max_retries, retry_delay=retry_delay)
            if translated_line is not None:
                translated_lines.append(translated_line)
            else:
                translated_lines.append(line)  # 如果翻译失败，保留原文
        print("")
        return '\n'.join(translated_lines)

    return translate_text_single(text, target=target, max_retries=max_retries, retry_delay=retry_delay)



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
def _epub_item_save_html_file(epubitem, filepath, output_dir, post_fix=""):
    # 获取文件名（不包括扩展名）作为目录名
    base_name = os.path.basename(filepath)
    directory_name = os.path.splitext(base_name)[0]

    # 在output_dir目录下创建以文件名为名称的目录
    output_subdir = os.path.join(output_dir, directory_name) + post_fix
    os.makedirs(output_subdir, exist_ok=True)

    if isinstance(epubitem, epub.EpubHtml):
        # 为每个HTML内容项生成文件名和路径
        file_name = os.path.basename(epubitem.file_name)
        output_path = os.path.join(output_subdir, file_name)

        # 将HTML内容写入文件
        with open(output_path, 'wb') as html_file:
            html_file.write(epubitem.content)

        print(f"\nSaved HTML content to {output_path}")



def process_epub_file(filepath, output_dir):
    book = epub.read_epub(filepath)
    for no, item in enumerate(book.get_items()):
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.content, 'html.parser')

            # 预处理：移除 <ruby> 中的 <rt>，并保留 <rb> 文本
            for ruby in soup.find_all('ruby'):
                for rt in ruby.find_all('rt'):
                    rt.decompose()  # 移除 <rt>
                ruby.unwrap()  # 移除 <ruby>，保留内容

            # 移除 <rb> 标签，保留其中的文本
            for rb in soup.find_all('rb'):
                rb.unwrap()


            # 翻譯前将HTML内容写入文件
            item.content = str(soup).encode('utf-8')
            _epub_item_save_html_file(item, filepath, output_dir, post_fix="_RAW" )

            # 執行翻譯，以<p>爲單位做翻譯
            p_tags = list(soup.find_all('p'))
            for p_no, p_tag in enumerate(p_tags):
                print(f"\rbook complete:{100*no/len(list(book.get_items())):3.0f}%\t<p> complete:{100*p_no/len(p_tags):3.0f}%", end="")

                try:
                    # 收集<p>标签内的所有文本
                    original_texts = list(p_tag.stripped_strings)
                    combined_text = ' '.join(original_texts)

                    # 翻译合并后的文本
                    translated_text = translate_text(combined_text)

                    # 在原始<p>内容后面插入<br>和灰色字体的翻译文本
                    p_tag.append(soup.new_tag("br"))  # 在<p>内容的最后插入<br>

                    # 创建一个<span>标签用于显示翻译文本，并设置样式为灰色
                    translated_span = soup.new_tag("span", style="color: gray;")
                    translated_span.string = f"({translated_text})"
                    p_tag.append(translated_span)

                    p_tag.append(soup.new_tag("br"))  # 在<p>内容的最后插入<br>

                except Exception as e:
                    print("\nexception occur, try not merge whole <p>.")
                    # 遍历<p>标签内的所有子元素
                    for content in p_tag.find_all(string=True):
                        # 检查子元素是否为NavigableString
                        if isinstance(content, NavigableString) and content.strip():
                            translated_text = translate_text(content)
                            # 使用新的翻译文本替换原始NavigableString
                            content.replace_with(f"{content} ({translated_text})")



            # # 执行原本的翻译动作
            # texts = soup.find_all(string=True)
            # for textno, text in enumerate(texts):
            #     print(f"\rbook complete:{100*no/len(list(book.get_items())):3.0f}%\titem complete:{100*textno/len(texts):3.0f}%", end="")
            #     if text.strip():
            #         parent = text.parent
            #         original_text = str(text)
            #         translated_text = translate_text(text)
            #         text.extract()  # Remove the original text

            #         # Insert original text
            #         parent.append(BeautifulSoup(original_text, 'html.parser'))
            #         # Insert <br> tags for spacing
            #         parent.append(soup.new_tag("br"))

            #         # Insert translated text within a styled span for visibility
            #         style_span = soup.new_tag("span", style="color: gray;")
            #         style_span.string = f"({translated_text})"
            #         parent.append(style_span)

            #         # Insert <br> tags for spacing
            #         parent.append(soup.new_tag("br"))

            item.content = str(soup).encode('utf-8')
            # 翻譯後的HTML
            _epub_item_save_html_file(item, filepath, output_dir , post_fix="_bilingual" )


        # print(f"\rbook complete:{100*no/len(list(book.get_items())):3.0f}%", end="")


    output_path = os.path.join(output_dir, os.path.basename(os.path.splitext(filepath)[0] + "_bilingual.epub"))
    epub.write_epub(output_path, book, {})
    print(f"\nfile saved: {output_path}")





def process_epub_file_old(filepath, output_dir):
    book = epub.read_epub(filepath)
    for no,item in enumerate(book.get_items()):
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.content, 'html.parser')
            texts = soup.find_all(string=True)
            for text in texts:
                if text.strip():
                    parent = text.parent
                    original_text = str(text)
                    translated_text = translate_text(text)

                    text.extract()  # Remove the original text

                    # Insert original text
                    parent.append(BeautifulSoup(original_text, 'html.parser'))

                    # Insert <br> tags for spacing
                    parent.append(soup.new_tag("br"))


                    # # Insert translated text
                    # translated_text_element = soup.new_string(f"({translated_text})")
                    # parent.append(translated_text_element)

                    # # Insert translated text in italics
                    # italic_tag = soup.new_tag("i")
                    # italic_tag.string = f"({translated_text})"
                    # parent.append(italic_tag)

                    # # Insert translated text with underline
                    # underline_tag = soup.new_tag("u")
                    # underline_tag.string = f"({translated_text})"
                    # parent.append(underline_tag)

                    # Insert translated text within a styled span for visibility
                    style_span = soup.new_tag("span", style="color: gray;")  # Example style
                    style_span.string = f"({translated_text})"
                    parent.append(style_span)

                    # Insert <br> tags for spacing
                    parent.append(soup.new_tag("br"))

            item.content = str(soup).encode('utf-8')
        print(f"\r{100*no/len(list(book.get_items())):3.0f}%", end="")

    output_path = os.path.join(output_dir, os.path.basename(os.path.splitext(filepath)[0] + "_bilingual.epub"))
    epub.write_epub(output_path, book, {})
    print(f"\nfile saved:{output_path}")

    save_epub_as_html(filepath, output_dir)

#...................................
# Epub Helper
#...................................
def save_epub_as_html(epub_path, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取EPUB文件
    book = epub.read_epub(epub_path)

    # 遍历EPUB中的所有项目
    for item in book.get_items():
        # 筛选出HTML内容
        if isinstance(item, epub.EpubHtml):
            # 生成HTML文件的路径
            file_name = os.path.basename(item.file_name)
            output_path = os.path.join(output_dir, file_name)

            # 将HTML内容写入文件
            with open(output_path, 'wb') as html_file:
                html_file.write(item.content)

            print(f"Saved HTML content to {output_path}")

"""
-----------------------------------------------
*.pdf Microsoft JhengHei 微軟正黑體
-----------------------------------------------
"""
def process_pdf_file(filepath, output_dir):
    # 读取PDF文件
    doc = fitz.open(filepath)
    new_doc = fitz.open()  # 创建一个新的PDF文档用于输出

    fontfile = r"C:\Windows\Fonts\msjh.ttc"
    # font = fitz.Font(fontfile)  # 选择一个支持繁体中文的字体，确保系统中有这个字体
    font = fitz.open_font(fontfile)
    # font = fitz.open_font(fontfile)  # 选择一个支持繁体中文的字体，确保系统中有这个字体

    # 遍历PDF中的每一页
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()  # 提取文本

        # 翻译文本
        translated_text = translate_text(text)

        # 合并原文和翻译文本
        bilingual_text = f"Original Text:\n{text}\n\nTranslated Text:\n{translated_text}"

        # 创建新的PDF页面，并添加双语文本
        new_page = new_doc.new_page(-1, width=595, height=842)  # A4 size in points
        new_page.insert_text(fitz.Point(72, 72), bilingual_text, fontsize=11, font=font)  # 添加文本到新页面

        #show progress
        print(f"\r{100*page_num/len(doc):3.0f}%", end="")

    # 保存新的PDF文件
    output_path = os.path.join(output_dir, os.path.basename(os.path.splitext(filepath)[0] + "_bilingual.pdf"))
    new_doc.save(output_path)
    print(f"File saved: {output_path}")

    # 关闭文档
    new_doc.close()
    doc.close()


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
    elif filepath.endswith('.pdf'):
        process_pdf_file(filepath, output_dir)
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
