import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 获取脚本所在的目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 标签映射，映射50种文件类型
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

# 反向映射，预测时使用
reverse_label_map = {v: k for k, v in label_map.items()}

# 特征提取函数
def extract_features(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        # 提取文件大小
        file_size = len(data)
        # 提取文件中每个字节的分布（0-255的频率）
        byte_distribution = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
        # 返回文件大小和字节分布
        return np.concatenate([[file_size], byte_distribution])
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# 构建数据集
def build_dataset(folder_path):
    features = []
    labels = []
    print(f"Building dataset from: {folder_path}")
    if not os.path.isdir(folder_path):
        print(f"Error: Data folder '{folder_path}' not found.")
        return np.array(features), np.array(labels)

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # 从文件名本身提取后缀，而不是从子目录名提取
            file_extension = os.path.splitext(file_name)[1].lower()
            if not file_extension:
                # print(f"Skipping file without extension: {file_path}")
                continue

            if file_extension in reverse_label_map:
                feature = extract_features(file_path)
                if feature is not None:
                    features.append(feature)
                    labels.append(reverse_label_map[file_extension])
            # else:
                # print(f"Skipping file with unmapped extension '{file_extension}': {file_path}")
                
    if not features:
        print("No features extracted. Check if files with mapped extensions exist and are readable.")
    return np.array(features), np.array(labels)

# 训练随机森林模型
def train_random_forest(X_train, y_train):
    # 使用与您当前环境匹配的scikit-learn版本训练
    # 可以调整n_estimators等参数以优化模型
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42) 
    print("Training RandomForestClassifier...")
    rf_model.fit(X_train, y_train)
    print("Training complete.")
    return rf_model

# 主程序
if __name__ == "__main__":
    # 数据集位于相对于脚本的 'data' 文件夹下
    folder_path = os.path.join(SCRIPT_DIR, "data")
    # 模型将保存在脚本所在的目录下
    model_save_path = os.path.join(SCRIPT_DIR, 'random_forest_file_classification_model_50.pkl')

    # 构建数据集
    X, y = build_dataset(folder_path)

    # 如果数据集为空，输出错误提示
    if X.size == 0 or y.size == 0:
        print("No valid data found in the dataset. Please ensure the 'data' folder is populated correctly.")
    else:
        print(f"Dataset built successfully: {len(X)} samples found.")
        # 切分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")

        # 训练随机森林模型
        model = train_random_forest(X_train, y_train)

        # 预测并评估模型
        print("Evaluating model...")
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Test Accuracy: {accuracy:.4f}")

        # 动态生成 target_names
        unique_labels_in_test = sorted(list(np.unique(y_test)))
        actual_target_names = [label_map[i] for i in unique_labels_in_test if i in label_map]
        
        # 确保y_pred中的标签也在label_map中，或者在报告中处理它们
        # 对于classification_report, labels参数应包含y_true和y_pred中所有出现过的标签
        present_labels = sorted(list(np.unique(np.concatenate((y_test, y_pred)))))
        report_target_names = [label_map[i] for i in present_labels if i in label_map]
        # 如果report_target_names中的标签数量与present_labels不一致，可能需要调整
        # 这里假设所有标签都在label_map中

        print(classification_report(y_test, y_pred, labels=present_labels, target_names=report_target_names, zero_division=0))

        # 保存模型
        print(f"Saving model to: {model_save_path}")
        joblib.dump(model, model_save_path)
        print("Model saved successfully.")