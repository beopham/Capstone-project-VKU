# import thư viện cần thiết
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

# Nạp ảnh đầu vào và convert vào mảng NumPy rồi thay đổi kích thước, xác định chiều ---
print("[INFO] Nạp ảnh...")
image = load_img("input/cat.jpg")   # Đường dẫn chứa ảnh đầu vào
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# Khởi tạo bộ sinh ảnh (augmentation)
aug = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest"
)

total = 0
print("[INFO] Sinh ảnh...")

# Sinh ảnh và lưu vào thư mục "output"
imageGen = aug.flow(
    image,
    batch_size=1,
    save_to_dir="output",
    save_prefix="image",
    save_format="jpg"
)

# Sinh 100 ảnh mới
for _ in imageGen:
    total += 1
    if total == 100:
        break

print(f"[INFO] Hoàn thành! Đã tạo {total} ảnh mới trong thư mục 'output/'.")
