from ebooklib import epub
from bs4 import BeautifulSoup
import re
import warnings

# 忽略 UserWarning 和 FutureWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def extract_text(epub_file):
    """提取EPUB文件中的所有文本内容，按章节分组。"""
    book = epub.read_epub(epub_file)
    chapters = []
    for item in book.get_items():
        if item.media_type == 'application/xhtml+xml':  # 判断是否为文档内容
            soup = BeautifulSoup(item.content, 'html.parser')
            text = soup.get_text()  # 提取纯文本
            # 按句子分割
            sentences = re.split(r'([。！？.!?])', text)  # 中文和英文句子结束符
            merged_sentences = ["".join(pair) for pair in zip(sentences[::2], sentences[1::2])]
            chapters.append(merged_sentences)
    return chapters

def create_bilingual_epub(chapters_cn, chapters_en, output_file):
    """创建双语EPUB文件。"""
    bilingual_book = epub.EpubBook()
    bilingual_book.set_title('双语小说')
    bilingual_book.set_language('zh-en')

    # 合并章节
    for i, (chapter_cn, chapter_en) in enumerate(zip(chapters_cn, chapters_en)):
        bilingual_chapter = epub.EpubHtml(title=f'Chapter {i+1}', file_name=f'chap_{i+1}.xhtml', lang='zh-en')
        content = ""
        for cn, en in zip(chapter_cn, chapter_en):
            content += f"<p>{cn}</p><p>{en}</p>"
        bilingual_chapter.content = content
        bilingual_book.add_item(bilingual_chapter)

    # 添加导航和目录
    bilingual_book.toc = tuple(bilingual_book.items)
    bilingual_book.spine = ['nav'] + list(bilingual_book.items)
    bilingual_book.add_item(epub.EpubNcx())
    bilingual_book.add_item(epub.EpubNav())

    # 保存文件
    epub.write_epub(output_file, bilingual_book)
    print(f"双语EPUB已生成：{output_file}")

# 使用示例
chapters_cn = extract_text('蛊真人_处理后_再次删除.epub')
chapters_en = extract_text('Reverend Insanity_处理后.epub')

# 确保两个文件的章节和句子数目一致
if len(chapters_cn) == len(chapters_en):
    create_bilingual_epub(chapters_cn, chapters_en, 'bilingual.epub')
else:
    print("中文和英文版本的章节数目不一致，请检查源文件。")

