# Groverの反射・回転の図と説明の追加

検証日: 2026-09-18 JST

## 追加内容

[補章AのGrover節](../ja/09-algorithm-worked-examples.md#algorithm-grover-geometry)に、4候補・正解1個の振幅計算を二次元の平面へ対応させる説明を追加した。

- 不正解3候補を正規化してまとめた状態と、正解11の状態を、横軸・縦軸の方向として導入した。横座標と各不正解候補の振幅の違い、縦座標の二乗と成功確率の対応を説明した。
- オラクルの横軸に関する反射と、拡散演算子の初期状態の方向の直線に関する反射を図示した。二つの合成が60度の回転になることを、角度の変化から導いた。
- 0〜3回の反復で30・90・150・210度へ進む図と表を追加し、成功確率、振幅の符号、3回後の全体位相を既存の計算へ結び付けた。

本文は外部スライドへの言及なしで読める構成にした。

図の再生成元は[draw_grover_geometry.py](draw_grover_geometry.py)。既存の[補章検証器](verify_algorithm_examples.py)からも呼び出し、図の出力・参照の一致と、二次元の座標から四つの振幅への復元を検証する。

```text
python -X utf8 -B manuscript/validation/draw_grover_geometry.py
```

図にはNumPy・Matplotlibを使う。日本語ラベルはYu Gothic、Meiryo、Noto Sans CJK JP、IPAexGothicの順に利用可能なフォントを選ぶ。今回の表示確認ではYu Gothicを使用した。

## 確認した範囲

- 新しい二つの軸の正規直交性、オラクルと拡散演算子の二次元行列、0〜3回の符号付き座標をQiskitの状態ベクトルと照合した。
- 掲載コード7例の出力が本文と一致した。既存のDeutsch・Grover・VQEの数学的検証関数も通過した。コード実行中のネットワーク接続は遮断した。
- 既存3枚と追加2枚、合計5枚の図の生成と参照が一致した。
- 追加図をPNGで開き、軸、反射の直線、回転角、符号、投影線、成功確率の表示を目視確認した。反復の図は本文の画像幅でも比較しやすい2行2列とした。
- 原稿のMarkdown表の列数、数式の区切り、KaTeXによる数式表示を確認した。

## 実行環境と限界

今回利用したローカル環境はQiskit 2.2.3 / NumPy 2.5.2 / SciPy 1.18.0 / Matplotlib 3.11.1 / pylatexenc 2.11 / Pillow 12.3.0。原稿の基準版とは異なるため、固定版を要求する検証器のmainは呼び出さず、run_examples、check_deutsch、check_grover、check_vqeの各関数を実行した。検証器の固定版チェックとrequirements.txtは維持した。

基準版の環境での通常の再検証コマンドは次のとおり。

```text
python -X utf8 -B manuscript/validation/verify_algorithm_examples.py
node manuscript/validation/verify_manuscript_render.cjs
git diff --check
```

今回、基準版環境での再実行、実機実行、PDF組版の確認は行っていない。
