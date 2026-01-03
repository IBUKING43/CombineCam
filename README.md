# CombineCam (コンバインカム)

0.001秒誤差を実現する、AI駆動型スポーツ計測・解析アプリ。

## 主な機能
- **高精度計測**: 40y走, プロアジリティ, 垂直跳び等の自動計測(1ms精度)
- **AR設置ガイド**: コーンを置く位置をカメラ越しに指示
- **3Dフォーム解析 (Premium)**: 走る姿を3Dモデル化し、バイオメカニクスに基づいた指導
- **ラベル管理**: 選手・種目ごとに結果をデータベース保存

## 技術スタック
- OS: Linux (Ubuntu)
- Language: Python 3.12
- AI: PyTorch, YOLOv11 (Pose Estimation)
- Library: OpenCV, NumPy
