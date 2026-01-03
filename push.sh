#!/bin/bash

# 1. すべての変更をステージに追加
git add .

# 2. コミットメッセージを入力（引数があればそれを使う、なければ定型文）
message=${1:-"Update CombineCam: $(date +'%Y-%m-%d %H:%M:%S')"}

# 3. コミット実行
git commit -m "$message"

# 4. GitHubへプッシュ
git push origin main

echo "-------------------------------"
echo "✅ GitHubへのアップロードが完了しました！"
echo "-------------------------------"