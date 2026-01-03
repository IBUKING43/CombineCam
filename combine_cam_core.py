import cv2
from ultralytics import YOLO
import time

class CombineCam:
    def __init__(self, model_path='yolo11n-pose.pt'):
        # Ryzen 8500GならCPUでもこの軽量モデルは爆速です
        self.model = YOLO(model_path)
        self.start_frame = None
        self.is_running = False

    def analyze_40yard(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        
        prev_wrist_y = None
        # 電気計測並みの精度を出すための「動きのしきい値」
        # 動画の解像度に合わせて調整が必要ですが、まずは15ピクセル程度でテスト
        THRESHOLD = 15 

        print(f"解析開始: {video_path} (FPS: {fps})")

        while cap.isOpened():
            success, frame = cap.read()
            if not success: break

            # PyTorchで骨格検知を実行
            results = self.model(frame, verbose=False)
            
            for r in results:
                if r.keypoints and len(r.keypoints.xy) > 0:
                    # 手首（Index 9 or 10）の座標を取得
                    # 3ポイントスタンスで地面についている方の手を追跡
                    points = r.keypoints.xy[0].cpu().numpy()
                    left_wrist = points[9]
                    right_wrist = points[10]
                    
                    # 地面に近い方の手首を選択
                    current_wrist_y = max(left_wrist[1], right_wrist[1])

                    if prev_wrist_y is not None:
                        movement = abs(current_wrist_y - prev_wrist_y)
                        
                        # 手が上に動いた（地面から離れた）瞬間を検知
                        if movement > THRESHOLD and not self.is_running:
                            self.start_frame = frame_count
                            self.is_running = True
                            start_time_sec = self.start_frame / fps
                            print(f"★スタート検知！ フレーム: {self.start_frame} ({start_time_sec:.3f}秒)")

                    prev_wrist_y = current_wrist_y
            
            frame_count += 1
        
        cap.release()
        print("解析完了。")

if __name__ == "__main__":
    cam = CombineCam()
    # ここにテスト用の動画ファイルを指定してください
    # cam.analyze_40yard("test_sprint.mp4")