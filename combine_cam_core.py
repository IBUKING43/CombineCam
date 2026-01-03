import cv2
import numpy as np
from ultralytics import YOLO

class CombineCam:
    def __init__(self):
        # 軽量なPoseモデル（Androidでも動かしやすいサイズ）
        self.model = YOLO('yolo11n-pose.pt')
        self.cone_template = None
        self.is_ready = False
        self.start_time = None
        self.elapsed_time = 0.0

    def learn_cone(self, image_path):
        """コーンの写真を読み込んで特徴を覚える（プロトタイプ版）"""
        img = cv2.imread(image_path)
        # ここでは単純に特定のオレンジ色（HSV）を抽出するロジックの土台を作成
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 一般的なオレンジ色の範囲
        lower_orange = np.array([0, 100, 100])
        upper_orange = np.array([20, 255, 255])
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        self.cone_template = mask
        print("コーンの特徴を学習しました。")

    def run_analysis(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        while cap.isOpened():
            success, frame = cap.read()
            if not success: break

            # 1. 骨格検知
            results = self.model(frame, verbose=False)
            
            # 2. シンプルUIの描画 (背景が暗くても見える白文字+黒縁)
            status_text = "READY" if not self.start_time else "RUNNING"
            cv2.putText(frame, f"STATUS: {status_text}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(frame, f"STATUS: {status_text}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            if self.start_time:
                self.elapsed_time = (cap.get(cv2.CAP_PROP_POS_FRAMES) - self.start_frame) / fps
            
            cv2.putText(frame, f"TIME: {self.elapsed_time:.3f} s", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('CombineCam - Analysis', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = CombineCam()
    # app.learn_cone("cone_photo.jpg") # 写真があれば有効化
    # app.run_analysis("test_video.mp4") # 動画があれば有効化