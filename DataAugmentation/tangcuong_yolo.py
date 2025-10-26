import os
import cv2
import albumentations as A
from tqdm import tqdm  # thanh tiến trình cho vui

input_dir = r"D:\Hoc Ki Cuoi\Capstone-project-VKU\DataAugmentation\input\Sal"
output_dir = r"D:\Hoc Ki Cuoi\Capstone-project-VKU\DataAugmentation\output\Tangcuong_sal"

os.makedirs(output_dir, exist_ok=True)

# ⚙️ Cấu hình augmentations
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.3),
    A.RandomBrightnessContrast(p=0.5),
    A.Rotate(limit=30, p=0.5),
    A.Blur(blur_limit=3, p=0.2),
    A.RandomGamma(p=0.4),
    A.HueSaturationValue(p=0.4),
    A.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0), p=0.3),  # ✅ bản mới dùng size
])

# 🔁 Tăng cường dữ liệu
for filename in tqdm(os.listdir(input_dir), desc="Augmenting images"):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_dir, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"⚠️ Lỗi đọc ảnh: {filename}, bỏ qua.")
            continue

        for i in range(5):
            augmented = transform(image=img)['image']
            new_name = f"{os.path.splitext(filename)[0]}_aug{i+1}.jpg"
            cv2.imwrite(os.path.join(output_dir, new_name), augmented)

print("✅ Tăng cường dữ liệu hoàn tất!")



# import os
# import cv2
# import albumentations as A
#
# # 🖼️ Ảnh đầu vào
# input_path = r"D:\Hoc Ki Cuoi\Capstone-project-VKU\DataAugmentation\input\cat.jpg"
# # 🗂️ Thư mục đầu ra
# output_dir = r"D:\Hoc Ki Cuoi\Capstone-project-VKU\DataAugmentation\output\cat_augmented"
# os.makedirs(output_dir, exist_ok=True)
#
# # ⚙️ Cấu hình augmentations
# transform = A.Compose([
#     A.HorizontalFlip(p=0.5),
#     A.VerticalFlip(p=0.3),
#     A.RandomBrightnessContrast(p=0.5),
#     A.Rotate(limit=30, p=0.5),
#     A.Blur(blur_limit=3, p=0.2),
#     A.RandomGamma(p=0.4),
#     A.HueSaturationValue(p=0.4),
#     A.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0), p=0.3),
# ])
#
# # Đọc ảnh gốc
# img = cv2.imread(input_path)
# if img is None:
#     raise ValueError("❌ Không đọc được ảnh, kiểm tra lại đường dẫn input_path!")
#
# # Tạo 10 ảnh tăng cường
# for i in range(10):
#     augmented = transform(image=img)['image']
#     new_name = f"cat_aug{i+1}.jpg"
#     cv2.imwrite(os.path.join(output_dir, new_name), augmented)
#
# print("✅ Tăng cường dữ liệu xong rồi bro! Ảnh mới nằm trong thư mục output.")
