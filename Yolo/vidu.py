from ultralytics import YOLO

# # model=YOLO('yolo12n.pt')
# model=YOLO('yolo12l.pt')
# model=YOLO('yolo11n.pt')
model=YOLO('yolo11n-seg.pt')

# ketqua = model("D:/Hoc Ki Cuoi/Capstone-project-VKU/Yolo/Data/Video/v.mp4",save=True,show=True)