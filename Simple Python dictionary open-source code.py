import json
import requests
from bs4 import BeautifulSoup
import re
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import traceback
import logging
import sys
import os

# 在代码开头添加日志设置
def setup_logging():
    if getattr(sys, 'frozen', False):
        log_dir = os.path.dirname(sys.executable)
    else:
        log_dir = os.path.dirname(__file__)
    
    log_file = os.path.join(log_dir, 'dictionary_debug.log')
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

# 定义语言资源库
language_resources = {
    "english": {
        "menu": "Simple Python Dictionary",
        "options": {
            "lookup": "Look up a word",
            "add": "Add a new word",
            "delete": "Delete a word",
            "update": "Update a word's definition",
            "switch_language": "Switch to Chinese",
            "import_web": "Import from Web",
            "exit": "Exit"
        },
        "lookup_input": "Enter the word to look up:",
        "lookup_result": "Definition: ",
        "lookup_not_found": "Word not found.",
        "add_input_word": "Enter the word to add:",
        "add_input_def": "Enter the definition:",
        "add_success": "Word added successfully.",
        "delete_input": "Enter the word to delete:",
        "delete_success": "Word deleted successfully.",
        "delete_not_found": "Word not found in the dictionary.",
        "update_input_word": "Enter the word to update:",
        "update_input_def": "Enter the new definition:",
        "update_success": "Word updated successfully.",
        "update_not_found": "Word not found in the dictionary.",
        "switch_language": "Language switched successfully.",
        "web_import_url": "URL to import words from:",
        "web_import_success": "Words imported successfully from web.",
        "web_import_fail": "Failed to import words from web. Please check the URL.",
        "web_import_no_words": "No words found on the webpage.",
        "web_import_select_section": "Select section to import:",
        "web_import_importing": "Importing words from web...",
        "exit_message": "Exiting the dictionary.",
        "invalid_choice": "Invalid choice. Please choose again.",
        "all_sections": "All Sections",
        "word": "Word",
        "definition": "Definition",
        "actions": "Actions",
        "dictionary_content": "Dictionary Content",
        "refresh": "Refresh",
        "clear": "Clear",
        "submit": "Submit",
        "cancel": "Cancel",
        "get_sections": "Get Sections",
        "import_dialog_title": "Import Words from Web"
    },
    "chinese": {
        "menu": "简易 Python 词典",
        "options": {
            "lookup": "查找单词",
            "add": "添加新单词",
            "delete": "删除单词",
            "update": "更新单词释义",
            "switch_language": "切换到英文",
            "import_web": "从网页导入",
            "exit": "退出"
        },
        "lookup_input": "请输入要查找的单词：",
        "lookup_result": "释义：",
        "lookup_not_found": "未找到单词。",
        "add_input_word": "请输入要添加的单词：",
        "add_input_def": "请输入单词释义：",
        "add_success": "单词添加成功。",
        "delete_input": "请输入要删除的单词：",
        "delete_success": "单词删除成功。",
        "delete_not_found": "词典中未找到该单词。",
        "update_input_word": "请输入要更新的单词：",
        "update_input_def": "请输入新的释义：",
        "update_success": "单词更新成功。",
        "update_not_found": "词典中未找到该单词。",
        "switch_language": "语言切换成功。",
        "web_import_url": "要导入单词的URL：",
        "web_import_success": "成功从网页导入单词。",
        "web_import_fail": "从网页导入单词失败，请检查URL。",
        "web_import_no_words": "网页中未找到单词。",
        "web_import_select_section": "请选择要导入的部分：",
        "web_import_importing": "正在从网页导入单词...",
        "exit_message": "正在退出词典。",
        "invalid_choice": "无效选择，请重新选择。",
        "all_sections": "所有部分",
        "word": "单词",
        "definition": "释义",
        "actions": "操作",
        "dictionary_content": "词典内容",
        "refresh": "刷新",
        "clear": "清空",
        "submit": "提交",
        "cancel": "取消",
        "get_sections": "获取部分",
        "import_dialog_title": "从网页导入单词"
    }
}

class SimpleDictionary:
    def __init__(self):
        self.dictionary = {}
        self.file_name = "dictionary.json"
        self.language = "english"  # 默认语言为英文
        self.default_web_url = "https://f29369ab37bf3c2494e86056be69e9c0.serveo.net/wiki/%E4%B8%BA%E7%AE%80%E6%98%93%20Python%20%E8%AF%8D%E5%85%B8%E6%B7%BB%E5%8A%A0%E6%96%B0%E8%AF%8D"
        self.load_dictionary()

    def load_dictionary(self):
        try:
            # 检查文件是否存在
            if not os.path.exists(self.file_name):
                print("Dictionary file not found. Starting with an empty dictionary.")
                # 创建一个空的字典文件
                self.save_dictionary()
                return
                
            # 检查文件是否为空
            if os.path.getsize(self.file_name) == 0:
                print("Dictionary file is empty. Starting with an empty dictionary.")
                self.dictionary = {}
                return
                
            with open(self.file_name, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if not content:
                    print("Dictionary file is empty. Starting with an empty dictionary.")
                    self.dictionary = {}
                else:
                    self.dictionary = json.loads(content)
                    
        except json.JSONDecodeError as e:
            print(f"Error loading dictionary file: {e}")
            print("Starting with an empty dictionary.")
            self.dictionary = {}
        except Exception as e:
            print(f"Unexpected error loading dictionary: {e}")
            print("Starting with an empty dictionary.")
            self.dictionary = {}

    def save_dictionary(self):
        try:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(self.dictionary, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving dictionary: {e}")

    def lookup_word(self, word):
        return self.dictionary.get(word, None)

    def add_word(self, word, definition):
        self.dictionary[word] = definition
        self.save_dictionary()

    def delete_word(self, word):
        if word in self.dictionary:
            del self.dictionary[word]
            self.save_dictionary()
            return True
        else:
            return False

    def update_word(self, word, new_definition):
        if word in self.dictionary:
            self.dictionary[word] = new_definition
            self.save_dictionary()
            return True
        else:
            return False

    def switch_language(self):
        if self.language == "english":
            self.language = "chinese"
        else:
            self.language = "english"
        return self.language

    def get_resource(self, resource_key):
        return language_resources[self.language][resource_key]
    
    def get_sections_from_web(self, url=None):
        """从网页获取所有可用的部分"""
        if url is None:
            url = self.default_web_url
            
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            response.raise_for_status()
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找wiki-content div
            wiki_content = soup.find('div', class_='wiki-content')
            if not wiki_content:
                print("未找到wiki内容区域")
                return []
                
            # 查找所有标题 (h2, h3, h4等)
            headings = wiki_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            sections = [heading.get_text().strip() for heading in headings]
            
            return sections
            
        except Exception as e:
            print(f"Error getting sections: {e}")
            return []
    
    def import_words_from_web(self, url=None, selected_section=None, progress_callback=None):
        if url is None:
            url = self.default_web_url
            
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            response.raise_for_status()
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找wiki-content div
            wiki_content = soup.find('div', class_='wiki-content')
            if not wiki_content:
                return False, 0, "未找到wiki内容区域"
                
            # 获取所有标题和段落
            elements = wiki_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
            imported_count = 0
            current_section = None
            imported_words = []
            
            for element in elements:
                tag_name = element.name
                text = element.get_text().strip()
                
                # 如果是标题，更新当前部分
                if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    current_section = text
                    if progress_callback:
                        progress_callback(f"发现部分: {current_section}")
                
                # 如果是段落，且符合格式，且属于选定部分（如果有）
                elif tag_name == 'p' and text:
                    # 检查是否应该处理这个部分
                    if selected_section and selected_section != self.get_resource("all_sections") and current_section != selected_section:
                        continue
                        
                    # 尝试匹配格式：英文单词，可翻译为...
                    match = re.match(r'^([A-Za-z]+)，可翻译为(.+)$', text)
                    if match:
                        word = match.group(1).strip().lower()
                        definition = match.group(2).strip()
                        
                        # 添加单词到词典
                        self.add_word(word, definition)
                        imported_count += 1
                        imported_words.append((word, definition))
                        
                        if progress_callback:
                            progress_callback(f"已添加: {word} -> {definition}")
            
            return True, imported_count, f"成功导入 {imported_count} 个单词"
            
        except Exception as e:
            return False, 0, f"导入错误: {str(e)}"

class DictionaryGUI:
    def __init__(self):
        self.dictionary = SimpleDictionary()
        self.root = tk.Tk()
        self.root.title(self.dictionary.get_resource("menu"))
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 刷新词典内容显示
        self.refresh_dictionary_display()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", font=("Arial", 10))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("Header.TLabel", background="#4e73df", foreground="white", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
    def create_widgets(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面元素
        self.create_title()
        self.create_panels()
        
    def create_title(self):
        # 标题
        self.title_label = ttk.Label(self.main_frame, text=self.dictionary.get_resource("menu"), style="Header.TLabel")
        self.title_label.pack(fill=tk.X, pady=(0, 10))
        
    def create_panels(self):
        # 创建左右分栏
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧功能面板
        self.left_frame = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(self.left_frame, weight=1)
        
        # 右侧词典内容面板
        self.right_frame = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(self.right_frame, weight=2)
        
        # 左侧功能按钮
        self.create_left_panel()
        
        # 右侧词典内容
        self.create_right_panel()
        
    def create_left_panel(self):
        # 查找单词
        self.lookup_frame = ttk.Frame(self.left_frame)
        self.lookup_frame.pack(fill=tk.X, pady=5)
        
        self.lookup_label = ttk.Label(self.lookup_frame, text=self.dictionary.get_resource("lookup_input"))
        self.lookup_label.pack(anchor=tk.W)
        
        lookup_entry_frame = ttk.Frame(self.lookup_frame)
        lookup_entry_frame.pack(fill=tk.X, pady=5)
        
        self.lookup_entry = ttk.Entry(lookup_entry_frame)
        self.lookup_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.lookup_button = ttk.Button(lookup_entry_frame, text=self.dictionary.get_resource("submit"), 
                  command=self.lookup_word)
        self.lookup_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.lookup_result = ttk.Label(self.lookup_frame, text="", wraplength=300)
        self.lookup_result.pack(fill=tk.X, pady=5)
        
        # 添加单词
        self.add_frame = ttk.LabelFrame(self.left_frame, text=self.dictionary.get_resource("options")["add"], padding="5")
        self.add_frame.pack(fill=tk.X, pady=5)
        
        self.add_word_label = ttk.Label(self.add_frame, text=self.dictionary.get_resource("add_input_word"))
        self.add_word_label.pack(anchor=tk.W)
        self.add_word_entry = ttk.Entry(self.add_frame)
        self.add_word_entry.pack(fill=tk.X, pady=2)
        
        self.add_def_label = ttk.Label(self.add_frame, text=self.dictionary.get_resource("add_input_def"))
        self.add_def_label.pack(anchor=tk.W)
        self.add_def_entry = ttk.Entry(self.add_frame)
        self.add_def_entry.pack(fill=tk.X, pady=2)
        
        self.add_button = ttk.Button(self.add_frame, text=self.dictionary.get_resource("submit"), 
                  command=self.add_word)
        self.add_button.pack(pady=5)
        
        # 删除单词
        self.delete_frame = ttk.LabelFrame(self.left_frame, text=self.dictionary.get_resource("options")["delete"], padding="5")
        self.delete_frame.pack(fill=tk.X, pady=5)
        
        self.delete_label = ttk.Label(self.delete_frame, text=self.dictionary.get_resource("delete_input"))
        self.delete_label.pack(anchor=tk.W)
        
        delete_entry_frame = ttk.Frame(self.delete_frame)
        delete_entry_frame.pack(fill=tk.X, pady=5)
        
        self.delete_entry = ttk.Entry(delete_entry_frame)
        self.delete_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.delete_button = ttk.Button(delete_entry_frame, text=self.dictionary.get_resource("submit"), 
                  command=self.delete_word)
        self.delete_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 更新单词
        self.update_frame = ttk.LabelFrame(self.left_frame, text=self.dictionary.get_resource("options")["update"], padding="5")
        self.update_frame.pack(fill=tk.X, pady=5)
        
        self.update_word_label = ttk.Label(self.update_frame, text=self.dictionary.get_resource("update_input_word"))
        self.update_word_label.pack(anchor=tk.W)
        self.update_word_entry = ttk.Entry(self.update_frame)
        self.update_word_entry.pack(fill=tk.X, pady=2)
        
        self.update_def_label = ttk.Label(self.update_frame, text=self.dictionary.get_resource("update_input_def"))
        self.update_def_label.pack(anchor=tk.W)
        self.update_def_entry = ttk.Entry(self.update_frame)
        self.update_def_entry.pack(fill=tk.X, pady=2)
        
        self.update_button = ttk.Button(self.update_frame, text=self.dictionary.get_resource("submit"), 
                  command=self.update_word)
        self.update_button.pack(pady=5)
        
        # 底部按钮
        self.bottom_frame = ttk.Frame(self.left_frame)
        self.bottom_frame.pack(fill=tk.X, pady=10)
        
        self.language_button = ttk.Button(self.bottom_frame, text=self.dictionary.get_resource("options")["switch_language"], 
                  command=self.switch_language)
        self.language_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.import_button = ttk.Button(self.bottom_frame, text=self.dictionary.get_resource("options")["import_web"], 
                  command=self.open_import_dialog)
        self.import_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.exit_button = ttk.Button(self.bottom_frame, text=self.dictionary.get_resource("options")["exit"], 
                  command=self.root.quit)
        self.exit_button.pack(side=tk.RIGHT)
        
    def create_right_panel(self):
        # 词典内容标题和刷新按钮
        self.header_frame = ttk.Frame(self.right_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.content_label = ttk.Label(self.header_frame, text=self.dictionary.get_resource("dictionary_content"), 
                 font=("Arial", 12, "bold"))
        self.content_label.pack(side=tk.LEFT)
        
        self.refresh_button = ttk.Button(self.header_frame, text=self.dictionary.get_resource("refresh"), 
                  command=self.refresh_dictionary_display)
        self.refresh_button.pack(side=tk.RIGHT)
        
        # 词典内容表格
        columns = ("word", "definition")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show="headings", height=20)
        
        # 设置列标题
        self.update_tree_columns()
        
        # 添加滚动条
        self.scrollbar = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_tree_double_click)
    
    def update_tree_columns(self):
        # 设置列标题
        self.tree.heading("word", text=self.dictionary.get_resource("word"))
        self.tree.heading("definition", text=self.dictionary.get_resource("definition"))
        
        # 设置列宽
        self.tree.column("word", width=150)
        self.tree.column("definition", width=400)
        
    def refresh_dictionary_display(self):
        # 清空现有内容
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 添加词典内容
        for word, definition in self.dictionary.dictionary.items():
            self.tree.insert("", tk.END, values=(word, definition))
    
    def update_ui_texts(self):
        """更新所有UI元素的文本"""
        # 更新窗口标题
        self.root.title(self.dictionary.get_resource("menu"))
        
        # 更新标题
        self.title_label.config(text=self.dictionary.get_resource("menu"))
        
        # 更新左侧面板
        self.lookup_label.config(text=self.dictionary.get_resource("lookup_input"))
        self.lookup_button.config(text=self.dictionary.get_resource("submit"))
        
        self.add_frame.config(text=self.dictionary.get_resource("options")["add"])
        self.add_word_label.config(text=self.dictionary.get_resource("add_input_word"))
        self.add_def_label.config(text=self.dictionary.get_resource("add_input_def"))
        self.add_button.config(text=self.dictionary.get_resource("submit"))
        
        self.delete_frame.config(text=self.dictionary.get_resource("options")["delete"])
        self.delete_label.config(text=self.dictionary.get_resource("delete_input"))
        self.delete_button.config(text=self.dictionary.get_resource("submit"))
        
        self.update_frame.config(text=self.dictionary.get_resource("options")["update"])
        self.update_word_label.config(text=self.dictionary.get_resource("update_input_word"))
        self.update_def_label.config(text=self.dictionary.get_resource("update_input_def"))
        self.update_button.config(text=self.dictionary.get_resource("submit"))
        
        self.language_button.config(text=self.dictionary.get_resource("options")["switch_language"])
        self.import_button.config(text=self.dictionary.get_resource("options")["import_web"])
        self.exit_button.config(text=self.dictionary.get_resource("options")["exit"])
        
        # 更新右侧面板
        self.content_label.config(text=self.dictionary.get_resource("dictionary_content"))
        self.refresh_button.config(text=self.dictionary.get_resource("refresh"))
        
        # 更新表格列标题
        self.update_tree_columns()
        
        # 清空查找结果
        self.lookup_result.config(text="")
    
    def lookup_word(self):
        word = self.lookup_entry.get().strip()
        if not word:
            messagebox.showwarning("输入错误", "请输入要查找的单词")
            return
            
        definition = self.dictionary.lookup_word(word)
        if definition:
            self.lookup_result.config(text=f"{self.dictionary.get_resource('lookup_result')}{definition}")
        else:
            self.lookup_result.config(text=self.dictionary.get_resource("lookup_not_found"))
    
    def add_word(self):
        word = self.add_word_entry.get().strip()
        definition = self.add_def_entry.get().strip()
        
        if not word or not definition:
            messagebox.showwarning("输入错误", "请输入单词和释义")
            return
            
        self.dictionary.add_word(word, definition)
        messagebox.showinfo("成功", self.dictionary.get_resource("add_success"))
        self.add_word_entry.delete(0, tk.END)
        self.add_def_entry.delete(0, tk.END)
        self.refresh_dictionary_display()
    
    def delete_word(self):
        word = self.delete_entry.get().strip()
        if not word:
            messagebox.showwarning("输入错误", "请输入要删除的单词")
            return
            
        if self.dictionary.delete_word(word):
            messagebox.showinfo("成功", self.dictionary.get_resource("delete_success"))
            self.delete_entry.delete(0, tk.END)
            self.refresh_dictionary_display()
        else:
            messagebox.showwarning("错误", self.dictionary.get_resource("delete_not_found"))
    
    def update_word(self):
        word = self.update_word_entry.get().strip()
        definition = self.update_def_entry.get().strip()
        
        if not word or not definition:
            messagebox.showwarning("输入错误", "请输入单词和新释义")
            return
            
        if self.dictionary.update_word(word, definition):
            messagebox.showinfo("成功", self.dictionary.get_resource("update_success"))
            self.update_word_entry.delete(0, tk.END)
            self.update_def_entry.delete(0, tk.END)
            self.refresh_dictionary_display()
        else:
            messagebox.showwarning("错误", self.dictionary.get_resource("update_not_found"))
    
    def switch_language(self):
        new_lang = self.dictionary.switch_language()
        self.update_ui_texts()
        messagebox.showinfo("成功", self.dictionary.get_resource("switch_language"))
    
    def on_tree_double_click(self, event):
        item = self.tree.selection()[0]
        word, definition = self.tree.item(item, "values")
        self.update_word_entry.delete(0, tk.END)
        self.update_word_entry.insert(0, word)
        self.update_def_entry.delete(0, tk.END)
        self.update_def_entry.insert(0, definition)
    
    def open_import_dialog(self):
        dialog = ImportDialog(self.root, self.dictionary)
        if dialog.result:
            self.refresh_dictionary_display()
    
    def run(self):
        self.root.mainloop()

class ImportDialog:
    def __init__(self, parent, dictionary):
        self.dictionary = dictionary
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(self.dictionary.get_resource("import_dialog_title"))
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # 居中对话框
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL 输入
        self.url_label = ttk.Label(main_frame, text=self.dictionary.get_resource("web_import_url"))
        self.url_label.pack(anchor=tk.W, pady=(0, 5))
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.insert(0, self.dictionary.default_web_url)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        
        # 部分选择
        self.section_label = ttk.Label(main_frame, text=self.dictionary.get_resource("web_import_select_section"))
        self.section_label.pack(anchor=tk.W, pady=(0, 5))
        
        section_frame = ttk.Frame(main_frame)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.section_var = tk.StringVar()
        self.section_combo = ttk.Combobox(section_frame, textvariable=self.section_var, state="readonly")
        self.section_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.get_sections_button = ttk.Button(section_frame, text=self.dictionary.get_resource("get_sections"), command=self.fetch_sections)
        self.get_sections_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 进度显示
        self.progress_text = scrolledtext.ScrolledText(main_frame, height=10, width=50)
        self.progress_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.submit_button = ttk.Button(button_frame, text=self.dictionary.get_resource("submit"), 
                  command=self.start_import)
        self.submit_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cancel_button = ttk.Button(button_frame, text=self.dictionary.get_resource("cancel"), 
                  command=self.dialog.destroy)
        self.cancel_button.pack(side=tk.RIGHT)
    
    def fetch_sections(self):
        url = self.url_entry.get().strip()
        if not url:
            url = self.dictionary.default_web_url
            
        sections = self.dictionary.get_sections_from_web(url)
        if sections:
            self.section_combo['values'] = [self.dictionary.get_resource("all_sections")] + sections
            self.section_combo.set(self.dictionary.get_resource("all_sections"))
            self.log_message("成功获取部分列表")
        else:
            self.log_message("未能获取到部分列表")
    
    def log_message(self, message):
        self.progress_text.insert(tk.END, f"{message}\n")
        self.progress_text.see(tk.END)
        self.progress_text.update_idletasks()
    
    def start_import(self):
        url = self.url_entry.get().strip()
        if not url:
            url = self.dictionary.default_web_url
            
        selected_section = self.section_var.get()
        if not selected_section:
            selected_section = self.dictionary.get_resource("all_sections")
            
        self.log_message(self.dictionary.get_resource("web_import_importing"))
        
        # 在新线程中执行导入，避免界面冻结
        thread = threading.Thread(target=self.do_import, args=(url, selected_section))
        thread.daemon = True
        thread.start()
    
    def do_import(self, url, selected_section):
        def progress_callback(message):
            self.progress_text.after(0, lambda: self.log_message(message))
            
        success, count, message = self.dictionary.import_words_from_web(
            url, selected_section, progress_callback)
            
        if success:
            self.progress_text.after(0, lambda: self.log_message(
                f"{self.dictionary.get_resource('web_import_success')} ({count} 个单词)"))
            self.progress_text.after(0, lambda: self.dialog.destroy())
            self.result = True
        else:
            self.progress_text.after(0, lambda: self.log_message(
                f"{self.dictionary.get_resource('web_import_fail')}: {message}"))

def main():
    try:
        setup_logging()
        logging.info("程序启动")
    # 创建并运行GUI应用
        app = DictionaryGUI()
        app.run()
        
    except Exception as e:
        logging.error(f"程序崩溃: {str(e)}")
        logging.error(traceback.format_exc())
        
        # 显示错误对话框
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("程序错误", f"程序运行出错:\n{str(e)}\n\n详细信息请查看日志文件: dictionary_debug.log")
        root.destroy()

if __name__ == "__main__":
    main()
