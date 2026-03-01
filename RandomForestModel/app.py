import os
import joblib
import numpy as np
import filetype
import json
import magic # Import python-magic
from flask import Flask, request, jsonify

# 获取脚本所在的目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 初始化 Flask 应用
app = Flask(__name__)

# 加载训练好的随机森林模型 (使用相对路径)
model_filename = "random_forest_file_classification_model_50.pkl"
model_path = os.path.join(SCRIPT_DIR, model_filename)

if not os.path.exists(model_path):
    print(f"ERROR: Model file not found at {model_path}.")
    # 根据需要，您可以在模型找不到时采取其他行动，例如退出程序
    # exit()

print(f"Loading model from: {model_path}")
model = joblib.load(model_path)

# 文件标签映射 (已修正所有条目的语法)
label_map = {
    0: '.txt', 1: '.json', 2: '.py', 3: '.png', 4: '.docx',
    5: '.csv', 6: '.html', 7: '.xml', 8: '.jpg', 9: '.gif',
    10: '.pdf', 11: '.xls', 12: '.xlsx', 13: '.ppt', 14: '.pptx',
    15: '.zip', 16: '.tar', 17: '.rar', 18: '.exe', 19: '.bat',
    20: '.sh', 21: '.mp3', 22: '.wav', 23: '.mp4', 24: '.avi',
    25: '.mov', 26: '.mkv', 27: '.flv', 28: '.iso', 29: '.bin',
    30: '.rtf', 31: '.md', 32: '.yml', 33: '.ini', 34: '.log',
    35: '.c', 36: '.cpp', 37: '.java', 38: '.class', 39: '.js',
    40: '.ts', 41: '.css', 42: '.scss', 43: '.go', 44: '.rb',
    45: '.php', 46: '.swift', 47: '.kt', 48: '.dart', 49: '.h'
}

# 提取文件特征
def extract_features(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        file_size = len(data)
        byte_distribution = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
        return np.concatenate([[file_size], byte_distribution])
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# 预测文件类型
def predict_file_type(file_path):
    features = extract_features(file_path)
    if features is None:
        return 'unknown' # Should match what Java expects for unknown
    predicted_label = model.predict([features])[0]
    return label_map.get(predicted_label, 'unknown')

# MIME类型到常见后缀的简单映射 (可以扩展)
MIME_TO_EXTENSION = {
    'application/pdf': '.pdf',
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'text/plain': '.txt',
    'text/html': '.html',
    'text/xml': '.xml',
    'application/json': '.json',
    'application/zip': '.zip',
    'application/x-rar-compressed': '.rar',
    'application/x-tar': '.tar',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/msword': '.doc',
    'application/vnd.ms-excel': '.xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/vnd.ms-powerpoint': '.ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'video/mp4': '.mp4',
    'audio/mpeg': '.mp3',
    'application/x-python-code': '.py', # Common for .py if text/plain isn't specific enough
    'application/javascript': '.js',
    'application/octet-stream': None, #明确地将通用类型映射为None，以便后续处理
    # 根据需要添加更多映射
}

def get_extension_from_mime(mime_type):
    if mime_type is None:
        return None
    
    ext = MIME_TO_EXTENSION.get(mime_type.lower())
    if ext is not None: # Check for explicit None for octet-stream
        return ext

    # 尝试从MIME类型中提取更通用的部分或后缀
    if '/' in mime_type:
        general_type, specific_type = mime_type.split('/', 1)
        # 例如: 'text/x-python' -> '.py'
        if general_type == 'text' and specific_type.startswith('x-'):
             potential_ext = '.' + specific_type[2:] # e.g. x-python -> .python
             # 这里可以有一个已知文本子类型的列表进行核对
             if potential_ext == '.python': return '.py'
             if potential_ext == '.c': return '.c'


        if '+' in specific_type: # e.g., 'image/svg+xml'
            base_specific_type = specific_type.split('+', 1)[0]
            # 尝试 general_type/base_specific_type, e.g. image/svg
            ext_plus = MIME_TO_EXTENSION.get(f"{general_type}/{base_specific_type}".lower())
            if ext_plus: return ext_plus
            
            # 尝试使用 '+' 后面的部分作为后缀, e.g., 'xml' from 'svg+xml'
            suffix_after_plus = '.' + specific_type.split('+')[-1].lower()
            # 简单的检查，确保它像一个有效的文件后缀
            if len(suffix_after_plus) > 1 and suffix_after_plus[1:].isalnum():
                 # 对于如 '.xml' '.json' 等常见后缀可以信任
                 if suffix_after_plus in ['.xml', '.json', '.zip']: #白名单
                    return suffix_after_plus
    return None

# 检测文件实际类型
def detect_actual_file_type(file_path, file_content_for_magic=None):
    original_filename = os.path.basename(file_path)
    _, file_extension = os.path.splitext(original_filename)
    file_extension = file_extension.lower()

    # 优先级1: python-magic (基于内容)
    try:
        buffer_to_use = file_content_for_magic
        if buffer_to_use is None: # 如果没有提供内存中的内容，则从文件读取
            with open(file_path, 'rb') as f:
                buffer_to_use = f.read(2048) # 读取文件头部一小部分用于检测

        if buffer_to_use:
             mime_type_magic = magic.from_buffer(buffer_to_use, mime=True)
             if mime_type_magic:
                print(f"python-magic MIME for {original_filename}: {mime_type_magic}")
                ext_from_magic = get_extension_from_mime(mime_type_magic)
                if ext_from_magic:
                    print(f"Extension from python-magic for {original_filename}: {ext_from_magic}")
                    return ext_from_magic
    except Exception as e:
        print(f"Error using python-magic for {original_filename}: {e}")

    # 优先级2: filetype.py (基于内容)
    try:
        kind = filetype.guess(file_path) # filetype.guess 需要文件路径
        if kind:
            print(f"filetype.py identified for {original_filename}: .{kind.extension}")
            return f".{kind.extension}"
    except Exception as e:
        print(f"Error using filetype.py for {original_filename}: {e}")

    # 优先级3: 如果基于内容的检测都失败了，并且原始文件有后缀名，则使用原始后缀名
    # (除非它是非常通用的如.bin, .dat，这种情况下我们可能宁愿返回unknown)
    # 这里可以添加一个模糊后缀列表，如果匹配到则倾向于返回unknown而不是这些后缀
    generic_extensions = ['.bin', '.dat', '.tmp', '.temp'] 
    if file_extension and file_extension not in generic_extensions:
        print(f"Falling back to original extension for {original_filename}: {file_extension}")
        return file_extension
        
    # 优先级4: 如果都没有识别出来，返回 "unknown"
    print(f"All detection methods failed for {original_filename}, returning 'unknown'.")
    return "unknown"

# 定义 Flask 路由来处理 Java 的请求
@app.route('/process_file', methods=['POST'])
def classify_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    original_filename = file.filename or "uploaded_file" # 处理空文件名

    # 临时文件目录 (相对于脚本位置)
    temp_dir = os.path.join(SCRIPT_DIR, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)

    # 使用安全的文件名处理，避免路径遍历等问题
    safe_filename = os.path.basename(original_filename)
    file_path = os.path.join(temp_dir, safe_filename)
    
    file_content = None
    try:
        file_content = file.read()
        file.seek(0) # 重置文件指针，以便后续保存或再次读取
        with open(file_path, 'wb') as f:
            f.write(file_content)
    except Exception as e:
        print(f"Error saving or reading uploaded file {original_filename}: {e}")
        return jsonify({"error": f"Error processing uploaded file: {e}"}), 500

    # 使用随机森林模型进行文件类型预测
    predicted_type = predict_file_type(file_path)

    # 检测文件实际类型 (传入文件路径和已读取的内容)
    actual_type = detect_actual_file_type(file_path, file_content_for_magic=file_content)
    
    # 比较预测类型和实际类型
    # Java 端会根据 "unknown" 的 actual_type 做最终判断
    comparison_result = 0
    if actual_type != "unknown":
        comparison_result = 1 if predicted_type == actual_type else 0
    # 如果 actual_type 是 "unknown"，comparison_result 保持 0，让 Java 端处理

    response_data = {
        "predicted-type": predicted_type,
        "actual-type": actual_type,
        "comparison-result": comparison_result
    }
    
    # 清理临时文件 (可选)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting temp file {file_path}: {e}")

    return jsonify(response_data)

# 启动 Flask 应用
if __name__ == "__main__":
    # 确保 temp 目录存在 (相对于脚本位置)
    temp_dir = os.path.join(SCRIPT_DIR, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5001)