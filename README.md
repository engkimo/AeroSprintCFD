# AeroSprintCFD

Webブラウザで動作する軽量な自動車空力シミュレーター（デモ用）です。
React + Three.js による可視化と、Python による簡易ポテンシャル流れソルバーを組み合わせています。

## 必要要件

*   **Node.js**: v18以上
*   **Python**: v3.10以上
*   **パッケージマネージャー**:
    *   Frontend: `pnpm`
    *   Backend: `uv` (推奨) または `pip`

## セットアップと起動方法

ターミナルを2つ開き、FrontendとBackendをそれぞれ起動してください。

### 1. Backend (Python/FastAPI)

```bash
cd backend

# 仮想環境の作成と依存関係のインストール
uv venv
uv pip install -r requirements.txt
# または直接インストール:
# uv pip install fastapi uvicorn numpy scipy pyvista trimesh python-multipart

# サーバーの起動
uv run uvicorn main:app --reload --port 8000
```

### 2. Frontend (React/Vite)

```bash
cd frontend

# 依存関係のインストール
pnpm install

# 開発サーバーの起動
pnpm dev
```

### 3. デモ用モデルの生成（オプション）

テスト用の簡易的な車の形状（STLファイル）を生成するスクリプトを用意しています。

```bash
cd backend
uv run python generate_demo_model.py
```
`backend/uploads/drivaer_demo.stl` が生成されます。

## 使い方

1.  ブラウザで `http://localhost:5173` にアクセスします。
2.  **Upload STL** ボタンをクリックし、STLファイル（または生成した `drivaer_demo.stl`）を選択します。
3.  **Resolution**（解像度）と **Wind Speed**（風速）を調整します。
4.  **Start Simulation** をクリックします。
5.  計算が完了すると、3Dビューア上に流線（Streamlines）が表示されます。

## 注意事項

*   本シミュレーターは**デモンストレーション用**です。物理的な厳密さよりも、視覚的な分かりやすさと応答性を重視しています。
*   ソルバーは簡易的なポテンシャル流れ（非粘性・非圧縮）を解いており、剥離や渦放出などの複雑な現象は再現されません。
