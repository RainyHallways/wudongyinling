# 导入所需的库
import cv2
import mediapipe as mp

# 初始化 MediaPipe Pose 模型
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 初始化 MediaPipe 的绘图工具
mp_drawing = mp.solutions.drawing_utils

# 打开电脑的默认摄像头 (摄像头编号通常为 0)
cap = cv2.VideoCapture('0')

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("错误：无法打开摄像头。")
    exit()

# 开始一个循环，实时处理摄像头的每一帧
while cap.isOpened():
    # 读取摄像头的一帧画面
    success, image = cap.read()
    if not success:
        print("忽略了一个空帧。")
        continue

    image.flags.writeable = False

    # MediaPipe 模型需要 RGB 格式的图像，而 OpenCV 读取的是 BGR 格式，所以需要转换
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用 MediaPipe Pose 模型处理图像，得到姿态结果
    results = pose.process(image_rgb)

    image.flags.writeable = True

    # 在图像上绘制骨骼
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
        )

    # 将处理后的图像水平翻转，看起来像镜子一样
    flipped_image = cv2.flip(image, 1)

    # 创建一个窗口并显示处理后的图像
    cv2.imshow('Real-time Dance Skeleton by MediaPipe', flipped_image)

    # 等待按键，如果按下 'q' 键或 ESC 键 (ASCII 码 27)，就退出循环
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q') or key == 27:
        break

# 循环结束后，释放摄像头资源并关闭所有窗口
cap.release()
cv2.destroyAllWindows()()