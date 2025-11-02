import cv2
import os
import albumentations as A

# --- CẤU HÌNH ---
INPUT_DIR = r"D:\Hoc Ki Cuoi\Capstone-project-VKU\DataAugmentation\input\he22"
OUTPUT_DIR = r"D:\Hoc Ki Cuoi\Capstone-project-VKU\DataAugmentation\output\tc_he"

NUM_AUGMENTED_IMAGES_PER_ORIGINAL = 5
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- PIPELINE ---
transform = A.Compose([
    # 1️⃣ Biến đổi hình học
    A.Affine(
        rotate=(-20, 20),
        translate_percent=(0.05, 0.05),
        scale=(0.9, 1.1),
        shear=(-5, 5),
        fit_output=False,
        border_mode=cv2.BORDER_CONSTANT,
        p=0.8
    ),
    A.HorizontalFlip(p=0.5),

    # 2️⃣ Biến đổi màu sắc
    A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.15, p=0.8),
    A.HueSaturationValue(hue_shift_limit=8, sat_shift_limit=20, val_shift_limit=15, p=0.6),

    # 3️⃣ Nhiễu & làm mờ
    A.GaussNoise(var_limit=10, p=0.2),
    A.MotionBlur(blur_limit=3, p=0.15),

    # 4️⃣ Resize về 224x224 cho EfficientNet
    A.Resize(224, 224)
])

print("[INFO] Bắt đầu quá trình tăng cường dữ liệu...")

# --- XỬ LÝ ---
image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
total_original_images = len(image_files)
processed_count = 0

for filename in image_files:
    image_path = os.path.join(INPUT_DIR, filename)
    image = cv2.imread(image_path)

    if image is None:
        print(f"[CẢNH BÁO] Không thể đọc ảnh: {image_path}. Bỏ qua.")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    base_name = os.path.splitext(filename)[0]

    for i in range(NUM_AUGMENTED_IMAGES_PER_ORIGINAL):
        augmented = transform(image=image)
        augmented_image = cv2.cvtColor(augmented['image'], cv2.COLOR_RGB2BGR)
        output_filename = os.path.join(OUTPUT_DIR, f"{base_name}_aug_{i+1}.jpg")
        cv2.imwrite(output_filename, augmented_image)

    processed_count += 1
    if processed_count % 10 == 0 or processed_count == total_original_images:
        print(f"[INFO] Đã xử lý {processed_count}/{total_original_images} ảnh.")

print(f"[INFO] ✅ Hoàn thành tăng cường dữ liệu.")
print(f"[INFO] Tổng ảnh gốc: {total_original_images}")
print(f"[INFO] Tổng ảnh mới tạo: {len(os.listdir(OUTPUT_DIR))}")