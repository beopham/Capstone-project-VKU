
import cv2
import os
import numpy as np
import albumentations as A

# --- CẤU HÌNH ---
# Sửa lỗi: Đảm bảo INPUT_DIR là một thư mục, nơi chứa các ảnh gốc của lớp 'cat'
# Giá trị này đã được sửa thành thư mục "input/cat" (Bỏ .jpg)
# Chỉnh lại cấu hình để chỉ xử lý MỘT FILE DUY NHẤT: cat.jpg

INPUT_FILE_PATH = "input/cat.jpg"  # <-- FILE GỐC ĐỂ TĂNG CƯỜNG
OUTPUT_DIR = "output/cat_augmented"  # Thư mục chứa ảnh tăng cường
NUM_AUGMENTED_IMAGES_PER_ORIGINAL = 10  # Số ảnh mới tạo từ mỗi ảnh gốc

# Đảm bảo thư mục đầu ra tồn tại
os.makedirs(OUTPUT_DIR, exist_ok=True)
# ----------------

# --- ĐỊNH NGHĨA PHÉP BIẾN ĐỔI (augmentation pipeline) ---
# Sử dụng Albumentations
transform = A.Compose([
    # 1️⃣ Biến đổi hình học
    A.Rotate(limit=30, p=0.8),  # Xoay ngẫu nhiên ±30 độ
    A.ShiftScaleRotate(
        shift_limit=0.2, scale_limit=0.15, rotate_limit=0,
        p=0.8, border_mode=cv2.BORDER_REPLICATE
    ),
    A.HorizontalFlip(p=0.5),  # Lật ngang 50%

    # 2️⃣ Biến đổi màu sắc
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.8),
    A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=30, val_shift_limit=20, p=0.7),

    # 3️⃣ Tăng cường bằng làm mờ / nhiễu
    A.GaussNoise(p=0.3),
    A.MotionBlur(blur_limit=3, p=0.2),
])

print("[INFO] Bắt đầu quá trình tăng cường dữ liệu...")
print(f"[INFO] File ảnh gốc: {INPUT_FILE_PATH}")
print(f"[INFO] Thư mục lưu trữ ảnh mới: {OUTPUT_DIR}")

# --- XỬ LÝ MỘT ẢNH DUY NHẤT ---
# Nạp ảnh gốc
image = cv2.imread(INPUT_FILE_PATH)

if image is None:
    print(f"\n[LỖI NGHIÊM TRỌNG] Không thể nạp ảnh tại đường dẫn: {INPUT_FILE_PATH}")
    print("Vui lòng đảm bảo file 'cat.jpg' tồn tại trong thư mục 'input' của dự án.")
    exit()

# Lấy tên file không có đuôi mở rộng (cat)
base_name = os.path.splitext(os.path.basename(INPUT_FILE_PATH))[0]
processed_count = 0

# Albumentations hoạt động tốt nhất với ảnh RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Sinh ảnh mới
for i in range(NUM_AUGMENTED_IMAGES_PER_ORIGINAL):
    # Áp dụng các phép biến đổi
    augmented = transform(image=image)
    augmented_image = augmented['image']

    # Chuyển lại về BGR để lưu bằng OpenCV
    augmented_image = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)

    # Tạo tên file mới và lưu (ví dụ: cat_aug_1.jpg)
    output_filename = os.path.join(OUTPUT_DIR, f"{base_name}_aug_{i + 1}.jpg")
    cv2.imwrite(output_filename, augmented_image)
    processed_count += 1

# --- THỐNG KÊ ---
total_new_images = processed_count
print(f"\n[STATUS] Đã xử lý 1 ảnh gốc.")
print("\n[INFO] Hoàn thành tăng cường dữ liệu.")
print(f"[INFO] Tổng số ảnh mới được tạo: {total_new_images}")
