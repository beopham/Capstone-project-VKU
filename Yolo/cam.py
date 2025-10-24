from ultralytics import YOLO
import cv2

# 1. Tải mô hình YOLO
# Thay 'yolov8n.pt' bằng tên mô hình bạn muốn dùng (ví dụ: 'yolo12n.pt')
model = YOLO(r'D:\Hoc Ki Cuoi\Capstone-project-VKU\Yolo\yolo\yolo11n-seg.pt')

# 2. Mở kết nối với Camera
# cv2.VideoCapture(0) mở camera mặc định (thường là camera tích hợp của laptop)
# Nếu bạn có nhiều camera, bạn có thể thử các số khác (1, 2,...)
cap = cv2.VideoCapture(0)

# Kiểm tra xem camera đã mở chưa
if not cap.isOpened():
    print("Lỗi: Không thể mở camera.")
    exit()

# Thiết lập độ phân giải (Tùy chọn)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 3. Vòng lặp để đọc từng khung hình và nhận diện
while True:
    # Đọc khung hình
    # 'ret' là một giá trị boolean (True/False) cho biết việc đọc có thành công không
    # 'frame' là ma trận NumPy chứa dữ liệu ảnh
    ret, frame = cap.read()

    # Nếu không đọc được khung hình (ví dụ: hết video hoặc lỗi cam), thoát
    if not ret:
        print("Không thể nhận khung hình (Stream end?).")
        break

    # 4. Chạy nhận diện YOLO trên khung hình
    # 'frame' là nguồn đầu vào
    # 'stream=True' giúp tăng tốc độ xử lý khi làm việc với luồng video
    results = model(frame, stream=True)

    # 5. Vẽ kết quả lên khung hình
    # Lấy khung hình đã được vẽ hộp giới hạn và nhãn từ kết quả
    for r in results:
        # Lấy khung hình đã được chú thích (vẽ hộp, nhãn)
        annotated_frame = r.plot()

        # 6. Hiển thị khung hình đã nhận diện
        cv2.imshow('YOLO Live Detection', annotated_frame)

        # Thoát khỏi vòng lặp nếu người dùng nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 7. Giải phóng camera và đóng tất cả cửa sổ
cap.release()
cv2.destroyAllWindows()