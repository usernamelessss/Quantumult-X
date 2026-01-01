import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
from PIL import Image, ImageTk, ImageDraw
import io
import os
import platform


class AppleIconFinalPro:
	def __init__(self, root):
		self.root = root
		self.root.title("iOS 图标全能下载器 (支持滚轮/PS 160px圆角)")
		self.root.geometry("1100x850")

		self.app_data_list = []
		self.check_vars = []
		self.img_refs = []

		self.regions = {
			"中国大陆": "cn", "美国": "us", "日本": "jp",
			"韩国": "kr", "中国香港": "hk", "中国台湾": "tw"
		}

		self.init_ui()

	def init_ui(self):
		# --- 顶部：搜索与区域选择 ---
		top_frame = ttk.Frame(self.root, padding=15)
		top_frame.pack(fill=tk.X)

		ttk.Label(top_frame, text="应用名称:").pack(side=tk.LEFT)
		self.search_entry = ttk.Entry(top_frame, width=30)
		self.search_entry.pack(side=tk.LEFT, padx=5)
		self.search_entry.bind('<Return>', lambda e: self.perform_search())

		ttk.Label(top_frame, text="商店区域:").pack(side=tk.LEFT, padx=(15, 0))
		self.region_combo = ttk.Combobox(top_frame, values=list(self.regions.keys()), width=12, state="readonly")
		self.region_combo.set("中国大陆")
		self.region_combo.pack(side=tk.LEFT, padx=5)

		ttk.Button(top_frame, text="开始搜索", command=self.perform_search).pack(side=tk.LEFT, padx=10)

		# --- 快捷工具栏 ---
		tool_bar = ttk.Frame(self.root, padding=(15, 0))
		tool_bar.pack(fill=tk.X)
		ttk.Button(tool_bar, text="全选", command=lambda: self.set_checks(True)).pack(side=tk.LEFT, padx=2)
		ttk.Button(tool_bar, text="取消全选", command=lambda: self.set_checks(False)).pack(side=tk.LEFT, padx=2)

		# --- 列表展示区 (增强滚轮支持) ---
		self.canvas_frame = ttk.Frame(self.root)
		self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

		self.canvas = tk.Canvas(self.canvas_frame, bg="#FFFFFF", highlightthickness=0)
		self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
		self.scroll_inner = ttk.Frame(self.canvas)

		# 绑定滚动区域自动更新
		self.scroll_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
		self.canvas.create_window((0, 0), window=self.scroll_inner, anchor="nw")
		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		# --- 绑定鼠标滚轮事件 ---
		self.bind_mouse_wheel(self.canvas)
		# 递归绑定，确保鼠标在图标或文字上时也能滚动
		self.scroll_inner.bind('<Enter>', lambda e: self.bind_mouse_wheel(self.canvas))

		# --- 底部：导出区域 ---
		bottom_frame = ttk.LabelFrame(self.root, text=" 导出设置 (勾选后将同时导出以下格式) ", padding=15)
		bottom_frame.pack(fill=tk.X, padx=15, pady=15)

		specs_text = "• 原始无损原图\n• 1024px 高清 (PS 160px 圆角)\n• 108px 小图标 (等比圆角)"
		ttk.Label(bottom_frame, text=specs_text, justify=tk.LEFT, font=("Arial", 9)).pack(side=tk.LEFT)

		self.btn_sel = ttk.Button(bottom_frame, text="下载选中项目", state="disabled",
		                          command=lambda: self.download_manager("selected"))
		self.btn_sel.pack(side=tk.RIGHT, padx=5)

		self.btn_all = ttk.Button(bottom_frame, text="一键下载全部结果", state="disabled",
		                          command=lambda: self.download_manager("all"))
		self.btn_all.pack(side=tk.RIGHT, padx=5)

	def bind_mouse_wheel(self, widget):
		"""跨平台滚轮绑定"""
		curr_os = platform.system()
		if curr_os == 'Windows':
			widget.bind_all("<MouseWheel>", self._on_mousewheel)
		elif curr_os == 'Darwin':  # macOS
			widget.bind_all("<MouseWheel>", self._on_mousewheel)
		else:  # Linux
			widget.bind_all("<Button-4>", self._on_mousewheel)
			widget.bind_all("<Button-5>", self._on_mousewheel)

	def _on_mousewheel(self, event):
		"""处理滚动逻辑"""
		if platform.system() == 'Windows':
			self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
		elif platform.system() == 'Darwin':  # macOS delta 不同
			self.canvas.yview_scroll(int(-1 * event.delta), "units")
		else:  # Linux
			if event.num == 4:
				self.canvas.yview_scroll(-1, "units")
			elif event.num == 5:
				self.canvas.yview_scroll(1, "units")

	def perform_search(self):
		query = self.search_entry.get().strip()
		if not query: return

		for w in self.scroll_inner.winfo_children(): w.destroy()
		self.app_data_list.clear()
		self.check_vars.clear()
		self.img_refs.clear()

		region_code = self.regions[self.region_combo.get()]
		url = f"https://itunes.apple.com/search?term={query}&entity=software&limit=28&country={region_code}"

		try:
			res = requests.get(url, timeout=10).json()
			if res.get('resultCount', 0) == 0:
				messagebox.showinfo("提示", "未找到结果")
				return

			for i, app in enumerate(res['results']):
				name = app.get('trackName', 'Unknown')
				max_url = app.get('artworkUrl512', '').replace("512x512bb", "1024x1024bb")

				thumb_data = requests.get(app.get('artworkUrl100')).content
				p_img = Image.open(io.BytesIO(thumb_data)).resize((100, 100), Image.Resampling.LANCZOS)
				photo = ImageTk.PhotoImage(p_img)
				self.img_refs.append(photo)

				self.app_data_list.append({"name": name, "url": max_url})
				var = tk.BooleanVar()
				self.check_vars.append(var)

				card = ttk.Frame(self.scroll_inner, padding=10)
				card.grid(row=i // 4, column=i % 4, padx=12, pady=12)

				# 即使鼠标在子组件上，也要支持滚动
				l = tk.Label(card, image=photo)
				l.pack()
				cb = ttk.Checkbutton(card, text=name[:10], variable=var)
				cb.pack(pady=5)

			self.btn_sel.config(state="normal")
			self.btn_all.config(state="normal")

		except Exception as e:
			messagebox.showerror("错误", f"请求失败: {e}")

	def set_checks(self, val):
		for v in self.check_vars: v.set(val)

	def process_and_save(self, raw_data, name, folder):
		clean_name = "".join(c for c in name if c.isalnum() or c in " _-")

		# 1. 原始无损高清原图
		with open(os.path.join(folder, f"{clean_name}_原始原图.png"), "wb") as f:
			f.write(raw_data)

		# 2. 1024px PS 160px圆角
		img = Image.open(io.BytesIO(raw_data)).convert("RGBA")
		img_1024 = img.resize((1024, 1024), Image.Resampling.LANCZOS)

		mask = Image.new("L", (1024, 1024), 0)
		draw = ImageDraw.Draw(mask)
		draw.rounded_rectangle((0, 0, 1024, 1024), radius=160, fill=255)

		rounded_big = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
		rounded_big.paste(img_1024, (0, 0), mask)
		rounded_big.save(os.path.join(folder, f"{clean_name}_1024px_PS圆角.png"))

		# 3. 108px 精致小图
		icon_108 = rounded_big.resize((108, 108), Image.Resampling.LANCZOS)
		icon_108.save(os.path.join(folder, f"{clean_name}_108px_R16.png"))

	def download_manager(self, mode):
		save_path = filedialog.askdirectory()
		if not save_path: return

		tasks = [self.app_data_list[i] for i, v in enumerate(self.check_vars) if mode == "all" or v.get()]
		if not tasks:
			messagebox.showwarning("提示", "未勾选项目")
			return

		for item in tasks:
			try:
				data = requests.get(item['url']).content
				self.process_and_save(data, item['name'], save_path)
			except Exception as e:
				print(f"Error saving {item['name']}: {e}")

		messagebox.showinfo("成功", f"下载完成！已导出三种格式。")


if __name__ == "__main__":
	root = tk.Tk()
	app = AppleIconFinalPro(root)
	root.mainloop()