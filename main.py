import os
import json

# --- 配置 ---
# 存放图片的目录 (相对于仓库根目录)
IMAGE_DIR = 'icons/'
# 生成的配置文件的路径
CONFIG_FILE = 'icons/icon_remote.json'
# 远程访问的基础 URL (替换为您的 GitHub Pages 或 Raw 链接)
# 格式: https://raw.githubusercontent.com/用户名/仓库名/分支名/
BASE_URL = 'https://raw.githubusercontent.com/Parantric/Quantumult-X/master/'


# ----------------

def generate_image_config_json():
	"""扫描图片目录并生成 JSON 配置文件。"""
	image_list = []

	# 确保图片目录存在
	if not os.path.isdir(IMAGE_DIR):
		print("当前工作目录:", os.getcwd())
		print(f"Error: Image directory not found at {IMAGE_DIR}")
		return

	# 递归遍历图片目录
	for root, _, files in os.walk(IMAGE_DIR):
		for file in files:
			# 只处理常见的图片格式
			if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
				# 计算相对路径，例如: assets/images/photo.jpg
				# 注意：这里使用 '/' 确保路径在 URL 中正确
				relative_path = os.path.join(root, file).replace(os.path.sep, '/')

				# 拼接完整的远程订阅 URL
				remote_url = BASE_URL + relative_path

				# 提取文件名作为 ID 或名称
				file_id = os.path.splitext(file)[0]

				image_list.append(
					{
						'name': file_id,
						'url': remote_url
					}
				)

	# 确保配置文件的父目录存在 (例如，创建 _data 目录)
	os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

	# 写入 JSON 文件
	# 使用 indent=4 使 JSON 文件更具可读性
	config_data = {
		'name': r'荒的图标库',
		'description': r'荒的图标库',
		'icons': image_list
	}

	with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
		json.dump(config_data, f, indent=4, ensure_ascii=False)

	print(f"Successfully generated {len(image_list)} entries in {CONFIG_FILE}")


if __name__ == '__main__':
	generate_image_config_json()
