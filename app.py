from flask import Flask, render_template, request, flash, redirect, url_for
import os
import json

app = Flask(__name__)
app.secret_key = "photo_upload_2026"

# 配置文件路径
CONFIG_FILE = "config.json"

# 初始化配置文件
def init_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"save_path": ""}, f, ensure_ascii=False, indent=2)

# 读取持久化保存的路径
def get_saved_path():
    init_config()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("save_path", "")

# 保存路径到配置文件（永久生效）
def save_path_to_config(path):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"save_path": path}, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    # 打开页面自动读取上次保存的路径
    last_path = get_saved_path()
    return render_template('index.html', last_path=last_path)

@app.route('/upload', methods=['POST'])
def upload():
    save_dir = request.form.get('save_dir', '').strip()
    if not os.path.isdir(save_dir):
        flash('目标路径不存在，请检查本地盘/网络盘文件夹！')
        return redirect(url_for('index'))
    
    # 提交上传时自动把新路径永久保存
    save_path_to_config(save_dir)

    files = request.files.getlist('photos')
    if not files or len(files) == 0:
        flash('请选择至少一张图片')
        return redirect(url_for('index'))

    success = 0
    for file in files:
        if file.filename == '':
            continue
        suffix = os.path.splitext(file.filename)[1].lower()
        if suffix in ['.jpg','.jpeg','.png','.gif','.bmp']:
            save_path = os.path.join(save_dir, file.filename)
            file.save(save_path)
            success += 1

    flash(f'上传完成！成功保存 {success} 张图片，路径已永久记录')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)