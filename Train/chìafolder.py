import os
import shutil
import random

# --- 1.1 Tỉ lệ chia tập dữ liệu ---
# 70% -> train folder
# 15% -> val folder
# 15% -> test folder

# --- 1.2 Cấu hình đường dẫn dataset ---
# ĐƯỜNG DẪN NGUỒN CHÍNH (Thư mục Data_chicken)
main_folder = 'D:/Hoc Ki Cuoi/Capstone-project-VKU/Data_chicken'

# ĐƯỜNG DẪN ĐÍCH
train_folder = 'D:/Hoc Ki Cuoi/Capstone-project-VKU/Data_chicken_train'
val_folder = 'D:/Hoc Ki Cuoi/Capstone-project-VKU/Data_chicken_val'  # Thư mục mới
test_folder = 'D:/Hoc Ki Cuoi/Capstone-project-VKU/Data_chicken_test'

# --- 1.3 Đảm bảo thư mục đích tồn tại ---
os.makedirs(train_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)  # Tạo thư mục validation
os.makedirs(test_folder, exist_ok=True)

# --- 1.4 Khám phá thư mục con (các lớp) ---
subfolders = []
for f in os.scandir(main_folder):
    if f.is_dir():
        subfolders.append(f.path)

# --- 1.5 Định nghĩa tỉ lệ chia ---
TRAIN_PERCENTAGE = 70
VAL_PERCENTAGE = 15
# TEST_PERCENTAGE sẽ là 100 - 70 - 15 = 15

# --- 1.6 Xử lý từng lớp: tạo thư mục, liệt kê/xáo trộn tệp, tính toán chia ---
for subfolder in subfolders:
    subfolder_name = os.path.basename(subfolder)

    # Đường dẫn cho thư mục con của lớp này
    train_subfolder = os.path.join(train_folder, subfolder_name)
    val_subfolder = os.path.join(val_folder, subfolder_name)
    test_subfolder = os.path.join(test_folder, subfolder_name)

    # Tạo thư mục con trong train/val/test
    os.makedirs(train_subfolder, exist_ok=True)
    os.makedirs(val_subfolder, exist_ok=True)
    os.makedirs(test_subfolder, exist_ok=True)

    # Liệt kê và xáo trộn tất cả tệp
    files = [f.path for f in os.scandir(subfolder) if f.is_file()]
    random.shuffle(files)
    total_files = len(files)

    # --- Tính toán số lượng tệp ---
    # 70% cho Train
    num_train = int(total_files * (TRAIN_PERCENTAGE / 100))

    # 15% cho Validation
    num_val = int(total_files * (VAL_PERCENTAGE / 100))

    # Phần còn lại cho Test (đảm bảo tổng không vượt quá 100%)
    num_test = total_files - num_train - num_val

    # --- Chia tệp ---
    train_files = files[:num_train]
    val_files = files[num_train: num_train + num_val]
    test_files = files[num_train + num_val:]

    # 1.6.8 Copy tệp Train
    for file in train_files:
        shutil.copy(file, os.path.join(train_subfolder, os.path.basename(file)))

    # 1.6.9 Copy tệp Validation
    for file in val_files:
        shutil.copy(file, os.path.join(val_subfolder, os.path.basename(file)))

    # 1.6.10 Copy tệp Test
    for file in test_files:
        shutil.copy(file, os.path.join(test_subfolder, os.path.basename(file)))

# --- 1.7 Thông báo hoàn tất ---
print("✅ Hoàn tất chia và sao chép tệp vào các thư mục Train (70%), Validation (15%), và Test (15%).")