# mol_simulation

## 気体分子シミュレーションソフト

youtube

[![粒子シミュレーション](https://i.ytimg.com/vi/fWzYb2FtJ6A/hqdefault.jpg?sqp=-oaymwE2CNACELwBSFXyq4qpAygIARUAAIhCGAFwAcABBvABAfgB3gOAAuADigIMCAAQARh_IBMoEzAP&rs=AOn4CLDlj0b2silFyfIcqpcb5a7zts1A9Q)](https://www.youtube.com/watch?v=fWzYb2FtJ6A)

mol.pyを使用するためにはopen-cvが必要です。

```bash
pip install opencv-python
```

mol.pyを実行すると粒子シミュレーションに従った動画用の画像が生成されimageディレクトリの中に保存されます。

real_gas.pyを実行すると、簡単な粒子シミュレーションのGUIを表示します。

## 注意

- 初期設定で粒子同士を近づけすぎると（粒子間距離を0以下にすると）うまく動作しません

- スピンや摩擦は考慮していません。
