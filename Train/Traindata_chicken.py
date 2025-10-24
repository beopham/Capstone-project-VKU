import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# 2.1.2 Import supporting libraries
import numpy as np
import os
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
# Sửa lại import: Sử dụng tensorflow.keras cho callbacks
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

# 2.1.3 Define target image size (all images resized to 224x224)
IMAGE_SIZE = 224
# --- 2.2 Load class names & count ---
# 2.2.1 Path to dataset folder containing class subfolders
# ĐÃ SỬA: Giữ nguyên đường dẫn để đọc tên lớp
imageFolder = "D:/Hoc Ki Cuoi/Capstone-project-VKU/Data_chicken/Data"
# 2.2.2 Get a list of class names (folder names)
CLASSES = os.listdir(imageFolder)
# 2.2.3 Count number of classes
num_classes = len(CLASSES)
# 2.2.4 Print class names
print("Classes found:", CLASSES)
# 2.2.5 Print number of classes
print("Number of classes:", num_classes)

# --- 2.3 Load pre-trained base model (EfficientNetV2S) ---
base_model = tf.keras.applications.EfficientNetV2S(
    weights='imagenet',
    input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
    include_top=False
)
base_model.trainable = True

# --- 2.4 Build the full model ---
model = tf.keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(1024, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

# --- 2.5 Compile the model ---
adam_opt = Adam(learning_rate=0.0001)
model.compile(
    optimizer=adam_opt,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# --- 2.6 Data generators (augmentation for training) ---
# 2.6.1 Create training data generator with augmentation
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
# 2.6.2 Create validation data generator (no augmentation, only rescale)
val_datagen = ImageDataGenerator(rescale=1. / 255) # Đổi tên thành val_datagen

# 2.6.3 Paths to split datasets (ĐÃ SỬA ĐƯỜNG DẪN CHUẨN XÁC)
train_folder = 'D:/Hoc Ki Cuoi/Capstone-project-VKU/Data_chicken/Data_chicken_train'
val_folder = 'D:/Hoc Ki Cuoi/Capstone-project-VKU/Data_chicken/Data_chicken_val'
# Lưu ý: Sửa đường dẫn lưu file model
best_model_file = 'D:/Hoc Ki Cuoi/Capstone-project-VKU/best_chicken_model_efficientnetv2.h5'

# 2.6.4 Training set generator
train_generator = train_datagen.flow_from_directory(
    train_folder,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=8,
    class_mode='categorical',
    color_mode='rgb',
    shuffle=True
)

# 2.6.5 Validation set generator (SỬ DỤNG TẬP VAL)
val_generator = val_datagen.flow_from_directory(
    val_folder,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=8,
    class_mode='categorical',
    color_mode='rgb'
)

# --- 2.7 Training parameters & callbacks ---
# 2.7.1 Number of epochs for training (ĐÃ SỬA TỪ 300 XUỐNG 50)
EPOCHS = 50

# 2.7.4 Define callbacks
callbacks = [
    # Save the best model based on validation accuracy
    ModelCheckpoint(best_model_file, verbose=1, save_best_only=True, monitor="val_accuracy"),
    # Reduce learning rate if validation accuracy plateaus
    ReduceLROnPlateau(monitor="val_accuracy", patience=15, factor=0.1, verbose=1, min_lr=1e-6), # Giảm patience
    # Stop training early if no improvement
    EarlyStopping(monitor="val_accuracy", patience=25, verbose=1)
]

# --- 2.8 Train the model ---
# 2.8.1 Fit model on training data with validation (DÙNG val_generator)
print("\n--- Bắt đầu huấn luyện mô hình (Max Epochs: 50) ---")
result = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator, # SỬ DỤNG val_generator
    callbacks=callbacks
)
# --- 2.9 Find best validation accuracy ---
best_val_acc_epoch = np.argmax(result.history['val_accuracy'])
best_val_acc = result.history['val_accuracy'][best_val_acc_epoch]
print("\nBest validation accuracy : " + str(best_val_acc))

# --- 2.10 Plot accuracy curves ---
plt.figure(figsize=(10, 5))
plt.plot(result.history['accuracy'], label='train acc')
plt.plot(result.history['val_accuracy'], label='val acc')
plt.title('Accuracy over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# --- 2.11 Plot loss curves ---
plt.figure(figsize=(10, 5))
plt.plot(result.history['loss'], label='train loss')
plt.plot(result.history['val_loss'], label='val loss')
plt.title('Loss over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()