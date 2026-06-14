# 🌑 EXTRA: 隠しダンジョン群 — 上級トピック

> 魔王を倒した者だけが入れる、地図にないダンジョンたち。
> クリアは必須ではない。だが、ここで得られる宝は
> **本職のエンジニアが現場で本当に使っている知識**だ。
> 各ダンジョン攻略で **150 XP** + バッジ「🌑 深淵を覗く者」。

それぞれのダンジョンは「入口(動機)→ 試練(学ぶこと)→ 宝(リソース)」の構成。
リソースはすべて本家 [Coding Interview University](https://github.com/jwasham/coding-interview-university) の該当セクションにつながっている。

---

## 🏯 ダンジョン 1: 平衡木の塔

**入口**: World 3 で学んだとおり、素の BST はソート済み入力で O(n) に堕ちる。
この塔の住人たちは、**挿入のたびに木を回転させて高さ O(log n) を死守する**。

**試練**:
- **AVL 木** — 左右の高さ差を 1 以内に保つ厳格派。回転(rotation)の 4 パターンを理解せよ
- **赤黒木** — ノードに色を塗って緩めに平衡を保つ実用派。多くの言語の TreeMap / std::map の正体
- **B 木 / B+ 木** — 1 ノードに多数のキーを詰める巨人。**データベースのインデックスとファイルシステム**の心臓部。ディスクは「ブロック単位の読み出し」なので、World 7 の局所性の議論がそのまま効いてくる

**宝**: 本家 [Balanced search trees](https://github.com/jwasham/coding-interview-university#balanced-search-trees) セクションの動画群

## 🗝️ ダンジョン 2: 暗号の聖堂

**入口**: World 8 で HTTPS が「公開鍵で鍵交換し、共通鍵で会話する」と学んだ。聖堂ではその魔法陣の中身を見る。

**試練**:
- **共通鍵暗号(AES)** — 同じ鍵で暗号化・復号。速いが「鍵をどう渡すか」問題が残る
- **公開鍵暗号(RSA 等)** — 公開鍵で暗号化、秘密鍵で復号。鍵配送問題を解決
- **ハッシュ関数(SHA-2 等)** — 一方向の指紋。改ざん検出、パスワード保存(+ソルト)
- なぜパスワードは「ハッシュ化して保存」であり「暗号化して保存」ではないのか、説明できるようになれ

**宝**: 本家 [Cryptography](https://github.com/jwasham/coding-interview-university#cryptography) セクション(Khan Academy ほか)

## 🧭 ダンジョン 3: A* の天文台

**入口**: ダイクストラ法は全方向に探索を広げる。だが地図アプリは「目的地はあっちだ」と知っている。

**試練**:
- **ヒューリスティック関数 h(v)** — ゴールまでの距離の楽観的見積もり(例: 直線距離)
- A* は「これまでのコスト g + 見積もり h」が最小の頂点から探索する
- h が実コストを**決して過大評価しない(admissible)**とき、A* は最適解を保証する
- ゲームの NPC の経路探索、カーナビ、パズルソルバ(15 パズル)の標準装備

**宝**: 本家 [A*](https://github.com/jwasham/coding-interview-university#a) セクション

## 🎲 ダンジョン 4: 確率の賭博場

**入口**: 「正確さを少しだけ賭けると、メモリと速度が桁違いに手に入る」――そんな賭けが成立する建物。

**試練**:
- **ブルームフィルタ** — 「絶対に無い」or「たぶん有る」を数ビット/要素で答える。偽陽性はあるが偽陰性はない。Web クローラの訪問済み判定、DB の不要な読み込み回避などで活躍
- **HyperLogLog** — 数十億要素のユニーク数を 1.5 KB 程度で概算する魔法
- **スキップリスト** — コイン投げで階層を作る確率的ソート済みリスト。平衡木と同等の O(log n) を、回転なしで実現(Redis の Sorted Set の正体)

**宝**: 本家 [Bloom Filter](https://github.com/jwasham/coding-interview-university#bloom-filter) / [HyperLogLog](https://github.com/jwasham/coding-interview-university#hyperloglog) / [Skip lists](https://github.com/jwasham/coding-interview-university#skip-lists)

## 🤝 ダンジョン 5: 連合の円卓

**入口**: 「この 2 つの島は同じ国に属するか?」を爆速で答え続ける装置が円卓に置かれている。

**試練**:
- **Union-Find(素集合データ構造)** — `find(x)`(所属グループの代表を返す)と `union(x, y)`(グループ統合)
- **経路圧縮**と**ランクによる統合**の 2 つの最適化で、ほぼ O(1)(逆アッカーマン関数)に
- ネットワークの連結判定、クラスカル法(最小全域木)、画像の領域分割で活躍

**宝**: 本家 [Disjoint Sets & Union Find](https://github.com/jwasham/coding-interview-university#disjoint-sets--union-find)

## 📜 ダンジョン 6: 文字列の図書館

**入口**: 巨大な蔵書から一節を探す司書たちは、素朴な総当たり O(nm) では仕事にならない。

**試練**:
- **トライ木 (Trie)** — 文字を辺とする木。プレフィックス検索・オートコンプリートの定番
- **KMP 法** — パターン自身の構造(失敗関数)を前処理し、O(n + m) で検索
- **ラビン・カープ法** — ローリングハッシュで部分文字列を高速比較。盗作検出にも

**宝**: 本家 [String searching & manipulations](https://github.com/jwasham/coding-interview-university#string-searching--manipulations) / [Tries](https://github.com/jwasham/coding-interview-university#tries)

## 🏗️ ダンジョン 7: 大規模設計の天空城(経験者向けレイド)

**入口**: 「ユーザーが 1 億人になっても落ちない Twitter を設計せよ」。
1 人では挑めない大規模レイド。実務経験を積んでから挑むのが定石(本家でも 4 年以上の経験者向けの面接トピックとされる)。

**試練**:
- スケーラビリティの語彙: 垂直/水平スケール、ロードバランサ、レプリケーション、シャーディング、CAP 定理、キャッシュ(World 7 の知識が都市規模になる)
- 「要件確認 → 概算(封筒の裏計算)→ API 設計 → データモデル → ボトルネック潰し」という設計面接の型

**宝**: 本家 [System Design, Scalability, Data Handling](https://github.com/jwasham/coding-interview-university#system-design-scalability-data-handling) —
特に [The System Design Primer](https://github.com/donnemartin/system-design-primer) は天空城の完全攻略本

---

## さらなる深淵

まだ潜りたい者は、本家の以下のセクションへ。すべて「いつか出会う」類いの宝だ:

- [情報理論](https://github.com/jwasham/coding-interview-university#information-theory-videos) / [エントロピー](https://github.com/jwasham/coding-interview-university#entropy) / [圧縮](https://github.com/jwasham/coding-interview-university#compression)
- [並列プログラミング](https://github.com/jwasham/coding-interview-university#parallel-programming)
- [コンパイラ](https://github.com/jwasham/coding-interview-university#compilers)
- [k-D 木](https://github.com/jwasham/coding-interview-university#k-d-trees) / [線形計画法](https://github.com/jwasham/coding-interview-university#linear-programming-videos) / [幾何・凸包](https://github.com/jwasham/coding-interview-university#geometry-convex-hull-videos)
- [離散数学](https://github.com/jwasham/coding-interview-university#discrete-math)
- [コンピュータサイエンス公開講義一覧](https://github.com/jwasham/coding-interview-university#computer-science-courses)

> 冒険に終わりはない。だが君はもう、**どの扉も自力で開けられる**。それがこのゲームの真のクリア報酬だ。
