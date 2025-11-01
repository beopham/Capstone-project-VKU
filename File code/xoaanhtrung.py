import os
from PIL import Image
import imagehash

folder =r"D:\Hoc Ki Cuoi\Capstone-project-VKU\Data_new\New Castle Disease"  # ✅ thay đường dẫn thư mục

hash_dict = {}

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    try:
        img = Image.open(path)
    except:
        continue

    h = str(imagehash.average_hash(img))

    if h not in hash_dict:
        hash_dict[h] = [file]
    else:
        hash_dict[h].append(file)

# Xóa ảnh trùng
deleted = 0

for h, files in hash_dict.items():
    if len(files) > 1:
        print(f"\n🔁 Trùng nhau (hash={h}):")
        print("Giữ lại:", files[0])

        for f in files[1:]:   # xóa file sau
            fp = os.path.join(folder, f)
            os.remove(fp)
            print("❌ Xóa:", f)
            deleted += 1

print(f"\n✅ Hoàn tất — đã xóa {deleted} ảnh trùng!")
