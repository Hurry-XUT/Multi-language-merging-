from ebooklib import epub
import warnings

# 忽略 UserWarning 和 FutureWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def remove_chapters(epub_file, output_file, chapters_to_remove):
    """从EPUB文件中删除指定章节并保存为新文件。

    Args:
        epub_file (str): 输入的EPUB文件路径。
        output_file (str): 输出的EPUB文件路径。
        chapters_to_remove (list): 要删除的章节文件名列表。
    """
    # 加载EPUB文件
    book = epub.read_epub(epub_file, options={"ignore_ncx": True})
    print(f"正在处理文件：{epub_file}")

    # 创建新书对象
    new_book = epub.EpubBook()

    # 复制元数据
    title = book.get_metadata('DC', 'title')[0][0]
    language = book.get_metadata('DC', 'language')[0][0]
    creators = book.get_metadata('DC', 'creator')

    new_book.set_title(title)
    new_book.set_language(language)
    for creator in creators:
        new_book.add_metadata('DC', 'creator', creator[0])

    # 初始化未匹配的章节列表
    unmatched_chapters = list(chapters_to_remove)

    # 复制书籍内容（排除需要删除的章节）
    for item in book.get_items():
        if item.file_name in chapters_to_remove:
            print(f"删除章节: {item.file_name}")
            unmatched_chapters.remove(item.file_name)  # 从未匹配列表中移除
        else:
            new_book.add_item(item)

    # 清理 TOC（目录）
    new_toc = []
    if book.toc:
        for toc_entry in book.toc:
            if hasattr(toc_entry, 'href') and toc_entry.href not in chapters_to_remove:
                new_toc.append(toc_entry)
        new_book.toc = new_toc

    # 清理 Spine（书脊）
    new_spine = []
    if book.spine:
        for spine_item in book.spine:
            # Spine 项目可能是元组，取第一个元素作为实际章节
            item = spine_item[0] if isinstance(spine_item, tuple) else spine_item
            if hasattr(item, 'href') and item.href not in chapters_to_remove:
                new_spine.append(spine_item)
        new_book.spine = new_spine

    # 打印未匹配的章节
    if unmatched_chapters:
        print(f"未找到以下章节文件，无法删除: {unmatched_chapters}")

    # 保存修改后的EPUB
    epub.write_epub(output_file, new_book)
    print(f"已保存新的EPUB文件：{output_file}")


# 示例：执行章节删除
if __name__ == "__main__":
    # 输入文件路径
    input_file = "Reverend Insanity (蛊真人, Gu_ (Z-Library).epub"  # 英文EPUB文件
    output_file = "Reverend Insanity_处理后.epub"  # 输出EPUB文件路径

    # 指定需要删除的章节文件名
    chapters_to_remove = [
        "Text/Cover.xhtml",  # 示例章节文件名，请替换为实际需要删除的文件
        "Text/0000_Information.xhtml",
        "Text/acknowledgements.xhtml"
    ]

    # 调用函数删除章节
    remove_chapters(input_file, output_file, chapters_to_remove)

