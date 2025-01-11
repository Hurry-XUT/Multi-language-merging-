from ebooklib import epub
from bs4 import BeautifulSoup
import warnings

# 忽略 UserWarning 和 FutureWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def extract_chapter_titles(epub_file):
    """提取EPUB文件中的章节标题和文件名。"""
    book = epub.read_epub(epub_file, options={"ignore_ncx": True})
    chapter_info = []  # 用于存储章节文件名和标题
    print(f"正在处理文件：{epub_file}")

    for item in book.get_items():
        if item.media_type == 'application/xhtml+xml':  # 判断是否为文档内容
            file_name = item.file_name
            soup = BeautifulSoup(item.content, 'html.parser')

            # 尝试提取特定标题标签
            title_tag = soup.find(['h1', 'h2', 'h3', 'title'])  # 优先寻找标题
            if title_tag:
                title = title_tag.get_text().strip()
            else:
                # 如果没有标题标签，使用章节内容的第一行作为标题
                text = soup.get_text().strip()
                title = text.split('\n')[0] if text else "(无标题内容)"

            chapter_info.append((file_name, title))

    print(f"总章节数：{len(chapter_info)}")
    for i, (file_name, title) in enumerate(chapter_info, 1):
        print(f"章节 {i}: 文件名: {file_name}, 标题: {title}")

    return chapter_info


# 检查英文版本的章节目录
chapters_en_info = extract_chapter_titles('Reverend Insanity_处理后.epub')
# chapters_cn_info = extract_chapter_titles('蛊真人_处理后_再次删除.epub')