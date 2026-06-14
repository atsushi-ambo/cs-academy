# 🃏 付録 V: 概念フラッシュカード集 — 能動的想起で記憶に刻む

> ここは「記憶の神殿」。講義を読んだだけでは、概念は数日で消える。
> 記憶研究が示す最強の勉強法は **能動的想起 (active recall)** と **間隔反復 (spaced repetition)** ——
> 「思い出そうとする」行為そのものが記憶を強くする。
> このカードはそのための道具だ。**答えを見る前に、必ず声に出して(または書いて)答えよ。**

## 📖 使い方

1. 質問を読んだら、`<details>` を開く前に**自分の言葉で答える**(頭の中だけでなく、声か紙に)
2. 開いて答え合わせ。**間違えた/詰まったカードに印**をつける
3. **間隔反復**: 間違えたカードは翌日・3 日後・1 週間後・1 か月後に再挑戦
4. 1 日 1 ワールドぶん(10〜15 枚)を目安に。全部一気にやらない
5. [キャラクターシート](character-sheet.md)のリトライリストに、何度も間違えるカードを記録

> 💡 「見れば分かる」は記憶ではない。「**何も見ずに言える**」が記憶だ。その差をこのカードで埋める。

---

## 🏔️ World 1: 計算量

**Q1.** Big-O は何の「上限」を表すか? Θ(シータ)とどう違う?
<details><summary>答え</summary>Big-O は成長率の上限(これ以上悪くならない)。Θ は上限かつ下限(ぴったりその成長率)。</details>

**Q2.** O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ) を遅い順に並べると?
<details><summary>答え</summary>O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)(右ほど遅い)。</details>

**Q3.** 「n を半分にし続ける」ループの計算量は?
<details><summary>答え</summary>O(log n)。</details>

**Q4.** 「最悪計算量」と「償却計算量」の違いは?
<details><summary>答え</summary>最悪=一番意地悪な入力での 1 回のコスト。償却=たまに高くつく操作をならした 1 回あたりの平均コスト(例: 動的配列の append は償却 O(1))。</details>

**Q5.** なぜ実行時間を「秒」でなく成長率で測るのか?
<details><summary>答え</summary>秒数はマシンに依存して変わるが、入力サイズに対する操作回数の伸び方はアルゴリズム固有だから。</details>

---

## 🏘️ World 2: データ構造

**Q1.** 配列が連結リストに勝つ操作・負ける操作は?
<details><summary>答え</summary>勝つ: 添字アクセス O(1)。負ける: 先頭/中間の挿入・削除 O(n)(連結リストは先頭 O(1))。</details>

**Q2.** スタックとキューの順序規則は?
<details><summary>答え</summary>スタック = LIFO(後入れ先出し)。キュー = FIFO(先入れ先出し)。</details>

**Q3.** ハッシュテーブルの検索が平均 O(1) になる仕組みは?
<details><summary>答え</summary>ハッシュ関数でキーをバケツ番号に変換し、直接そのバケツを見るから。衝突がなければ計算 1 回。</details>

**Q4.** ハッシュテーブルが最悪 O(n) になるのはどんなとき?
<details><summary>答え</summary>全キーが同じバケツに衝突したとき(チェインが 1 本の長いリストになる)。</details>

**Q5.** 「重複チェック」「カウント」「対応表」と聞いたら何を疑う?
<details><summary>答え</summary>ハッシュテーブル(セット/辞書)。</details>

**Q6.** 連結リストに循環があるかを O(1) 空間で検出する方法は?
<details><summary>答え</summary>フロイドの「うさぎとかめ」。1 歩と 2 歩のポインタを走らせ、追いつけば循環あり。</details>

---

## 🌲 World 3: 木・BST・ヒープ

**Q1.** BST の不変条件を正確に言うと?
<details><summary>答え</summary>任意のノードで、左部分木の**全要素** < 自分 < 右部分木の**全要素**(直接の子だけでない)。</details>

**Q2.** BST の中順(inorder)走査で得られるものは?
<details><summary>答え</summary>値が昇順にソートされた列。</details>

**Q3.** BST の操作が O(log n) でなく O(n) に堕ちるのはどんな入力?
<details><summary>答え</summary>ソート済みの列を順に挿入したとき(木が一直線になる)。平衡木で防ぐ。</details>

**Q4.** 最大ヒープの掟は? 配列での親子の添字は?
<details><summary>答え</summary>親 ≥ 子。親 i の子は 2i+1, 2i+2、子 i の親は (i−1)//2。</details>

**Q5.** 配列からヒープを作る heapify の計算量は? (ひっかけ)
<details><summary>答え</summary>O(n)。n log n ではない(大半のノードが底近くで高さが小さいため)。</details>

**Q6.** 「常に上位 k 個を保持したい」。何を使う?
<details><summary>答え</summary>サイズ k の最小ヒープ。1 要素 O(log k)。</details>

---

## 🌋 World 4: ソート

**Q1.** 「安定なソート」とは?
<details><summary>答え</summary>同じキーの要素の元の順序が保たれるソート。</details>

**Q2.** マージソートとクイックソートの最悪計算量は?
<details><summary>答え</summary>マージ O(n log n)(常に)、クイック O(n²)(最悪、ランダムピボットで回避)。</details>

**Q3.** クイックソートが最悪 O(n²) になる入力と回避策は?
<details><summary>答え</summary>ソート済みで端をピボットに選ぶと偏る。ランダムピボットや中央値三点取りで回避。</details>

**Q4.** 比較ソートが超えられない下界は? なぜ?
<details><summary>答え</summary>Ω(n log n)。n! 通りの並びを比較(1 回で半減)で区別するには log₂(n!) ≒ n log n 回必要。</details>

**Q5.** 値域が小さい整数を O(n) でソートする方法は?
<details><summary>答え</summary>カウンティングソート(比較しないので n log n の壁を越える)。</details>

---

## 🌊 World 5: グラフ

**Q1.** 「最短経路(重みなし)」に使うのは BFS か DFS か?
<details><summary>答え</summary>BFS(距離 0,1,2,… の順に発見するため最初の到達が最短)。</details>

**Q2.** BFS と DFS が使うデータ構造は?
<details><summary>答え</summary>BFS はキュー、DFS はスタック(または再帰)。</details>

**Q3.** トポロジカルソートが存在する条件は?
<details><summary>答え</summary>グラフが DAG(閉路のない有向グラフ)であること。</details>

**Q4.** ダイクストラ法が壊れるのはどんな辺があるとき?
<details><summary>答え</summary>負の重みの辺(確定した距離が後で縮む可能性があり、貪欲の前提が崩れる)。</details>

**Q5.** 隣接リストと隣接行列、疎なグラフに向くのは?
<details><summary>答え</summary>隣接リスト(メモリ O(V+E))。隣接行列は O(V²) だが辺の有無確認が O(1)。</details>

---

## 🏜️ World 6: 再帰と動的計画法

**Q1.** 再帰関数が停止する 2 条件は?
<details><summary>答え</summary>基底ケースが存在する。再帰のたびに確実に基底ケースへ近づく。</details>

**Q2.** DP が使える 2 つの条件は?
<details><summary>答え</summary>部分問題の重複、最適部分構造。</details>

**Q3.** メモ化(トップダウン)とボトムアップ DP の違いは?
<details><summary>答え</summary>メモ化=再帰のまま結果をキャッシュ。ボトムアップ=小さい問題から表を埋める。どちらも各部分問題を 1 回だけ解く。</details>

**Q4.** 素朴な再帰フィボナッチが O(2ⁿ) なのはなぜ? メモ化で O(n) になるのは?
<details><summary>答え</summary>同じ部分問題を指数回重複して解くから。部分問題は実は n+1 個しかなく、メモ化すれば各 1 回で O(n)。</details>

**Q5.** 貪欲法でなく DP が必要なのはどんなとき?
<details><summary>答え</summary>局所最適の選択が全体最適を保証しないとき(選択の影響が後に波及する)。</details>

---

## ⚙️ World 7: 機械の内側

**Q1.** コンパイラとインタプリタの違いは?
<details><summary>答え</summary>コンパイラ=実行前に全体を機械語に翻訳。インタプリタ=実行時に逐次解釈。</details>

**Q2.** メモリ階層を速い順に 4 段以上挙げると?
<details><summary>答え</summary>レジスタ → L1/L2/L3 キャッシュ → メインメモリ → SSD/ディスク。</details>

**Q3.** キャッシュが効く 2 種類の局所性は?
<details><summary>答え</summary>時間的局所性(同じデータの再利用)、空間的局所性(隣接データの利用)。</details>

**Q4.** プロセスとスレッドのメモリの違いは?
<details><summary>答え</summary>プロセスはメモリ空間が独立。スレッドは同じプロセス内でメモリを共有(各自スタックは別)。</details>

**Q5.** `0.1 + 0.2 == 0.3` が偽になる理由は?
<details><summary>答え</summary>0.1 や 0.2 は 2 進で無限循環小数になり、丸め誤差を含むから。</details>

**Q6.** 配列走査が連結リスト走査より実測で速い理由は(計算量は同じ O(n) なのに)?
<details><summary>答え</summary>配列は連続メモリでキャッシュラインの先読みが効くが、連結リストは散在しほぼ毎回キャッシュミスするから。</details>

---

## 📡 World 8: ネットワーク

**Q1.** TCP と UDP の最大の違いは?
<details><summary>答え</summary>TCP は到達・順序を保証(接続あり、重い)。UDP は保証なし(接続なし、軽い・速い)。</details>

**Q2.** TCP の 3 ウェイハンドシェイクの 3 パケットは?
<details><summary>答え</summary>SYN → SYN+ACK → ACK(双方の初期シーケンス番号を同期)。</details>

**Q3.** TCP が信頼性を作る仕組みを 3 つ?
<details><summary>答え</summary>シーケンス番号で順序復元、ACK とタイムアウトで再送、チェックサムで破損検出(+フロー/輻輳制御)。</details>

**Q4.** DNS は何をする仕組み? どんなデータ構造に似ている?
<details><summary>答え</summary>ドメイン名 → IP アドレスを引く分散データベース。階層的な木構造+各段のキャッシュ。</details>

**Q5.** HTTP が「ステートレス」とは? ログイン状態はどう保つ?
<details><summary>答え</summary>各リクエストが独立でサーバは前を覚えない。Cookie(セッションID)やトークンで状態を持つ。</details>

---

## 🌌 World 9: 離散数学

**Q1.** P → Q と同値なのは、逆・裏・対偶のどれ?
<details><summary>答え</summary>対偶(¬Q → ¬P)のみ。</details>

**Q2.** 数学的帰納法の 2 ステップは?
<details><summary>答え</summary>基底(P(0) を示す)、帰納段階(P(k) を仮定して P(k+1) を示す)。</details>

**Q3.** ユークリッドの互除法の漸化式と計算量は?
<details><summary>答え</summary>gcd(a,b) = gcd(b, a mod b)。O(log min(a,b))。</details>

**Q4.** 期待値の線形性が強力なのはなぜ?
<details><summary>答え</summary>E[X+Y] = E[X]+E[Y] が**独立でなくても**成り立つから(複雑な依存があっても足せる)。</details>

**Q5.** カントールの対角線論法は何を示す?
<details><summary>答え</summary>実数全体は自然数で番号付けできない(非可算)。後に停止問題の決定不能性で再登場。</details>

---

## 🏛️ World 10: OS

**Q1.** ユーザモードとカーネルモードを分ける理由は?
<details><summary>答え</summary>アプリの暴走や悪意からハードウェアと他プロセスを守る隔離のため。</details>

**Q2.** `fork()` の直後、親と子はどこから実行を続ける?
<details><summary>答え</summary>両方が fork の次の行から(親には子の PID、子には 0 が返る)。</details>

**Q3.** 条件変数の wait をなぜ while で囲む?
<details><summary>答え</summary>偽の起床や他スレッドの横取りで、起きても条件が成立しているとは限らないから(再確認が必要)。</details>

**Q4.** ページフォールトとは? どう解決される?
<details><summary>答え</summary>アクセスしたページが物理メモリにない例外。カーネルがディスクから読み込み、ページテーブルを更新して命令を再実行(デマンドページング)。</details>

**Q5.** スラッシングとは?
<details><summary>答え</summary>物理メモリ不足でページの追い出しと読み込みが往復し、CPU がほぼ I/O 待ちになる状態。</details>

**Q6.** ジャーナリング(WAL)がクラッシュ一貫性を保つ原則は?
<details><summary>答え</summary>「変更を本体に書く前に、先にログを書く」。再起動時にコミット済みは再適用、未完了は破棄。</details>

---

## 🗄️ World 11: データベース

**Q1.** ACID の 4 文字は?
<details><summary>答え</summary>Atomicity(原子性)、Consistency(一貫性)、Isolation(分離性)、Durability(永続性)。</details>

**Q2.** B+木が BST でなくDB の標準インデックスである理由は?
<details><summary>答え</summary>1 ノード=1 ページに数百キーを詰めて木を低くし、ディスク I/O 回数を最小化できるから。</details>

**Q3.** 「コミットの瞬間」とは物理的に何が起きた瞬間?
<details><summary>答え</summary>コミットレコードを含むログがディスクに永続化(fsync)された瞬間。データページの書き込みは後でよい。</details>

**Q4.** MVCC で「読みが書きをブロックしない」のはなぜ?
<details><summary>答え</summary>書き込みは新しい版を作るだけで、読む側は自分の開始時点のスナップショット(古い版)を読み続けられるから。</details>

**Q5.** ハッシュ結合の仕組みは?
<details><summary>答え</summary>小さい方の表でメモリ上にハッシュ表を作り、大きい方を 1 行ずつ流して照合(O(M+N))。</details>

---

## 🐉 World 12: コンパイラ

**Q1.** コンパイラの主要 6 段は?
<details><summary>答え</summary>字句解析 → 構文解析 → 意味解析 → IR 生成 → 最適化 → コード生成。</details>

**Q2.** 字句解析は正規表現で書けるのに、構文解析に CFG が要るのはなぜ?
<details><summary>答え</summary>括弧の対応など任意の深さの入れ子は有限状態では数えられず、スタック(再帰)を持つ CFG が必要だから。</details>

**Q3.** `1 + 2 * 3` が `1 + (2*3)` と解釈される仕組みは?
<details><summary>答え</summary>演算子の優先順位が文法の階層に埋め込まれている(`*` が `+` より深い規則にある)。</details>

**Q4.** 参照カウント GC の弱点は?
<details><summary>答え</summary>循環参照を回収できない(互いに参照し合うとカウントが 0 にならない)。</details>

**Q5.** 世代別 GC が基づく経験則は?
<details><summary>答え</summary>「ほとんどのオブジェクトは若くして死ぬ」。だから新世代だけを頻繁に小さく回収する。</details>

---

## 🔮 World 13: 計算理論

**Q1.** DFA・PDA・チューリングマシンの記憶の違いは?
<details><summary>答え</summary>DFA は有限状態のみ、PDA は+スタック 1 本、TM は+自由に読み書きできる無限テープ。</details>

**Q2.** ポンピング補題は何を証明するのに使う?
<details><summary>答え</summary>ある言語が正規言語で**ない**こと(例: aⁿbⁿ)。</details>

**Q3.** 停止問題の結論は?
<details><summary>答え</summary>任意のプログラムと入力について停止するか判定するプログラムは存在しない(決定不能)。</details>

**Q4.** P と NP の定義は?
<details><summary>答え</summary>P=多項式時間で解ける。NP=答えの証拠を多項式時間で検証できる。</details>

**Q5.** 自分の問題が NP 完全だと分かったら、次に何をすべき?
<details><summary>答え</summary>厳密な多項式解を諦め、近似アルゴリズム・ヒューリスティック・特殊ケース・分枝限定に切り替える。</details>

---

## ⚗️ World 14: 上級アルゴリズム

**Q1.** マスター定理 T(n)=aT(n/b)+O(n^d) で、マージソート(a=2,b=2,d=1)の解は?
<details><summary>答え</summary>d = log_b a = 1 なので O(n^d log n) = O(n log n)。</details>

**Q2.** 貪欲法の正しさを示す定番の論法は?
<details><summary>答え</summary>交換論法(最適解の選択を貪欲の選択に交換しても悪化しないことを示す)。</details>

**Q3.** Kruskal 法で閉路判定に使うデータ構造は?
<details><summary>答え</summary>Union-Find(素集合データ構造)。</details>

**Q4.** 残余グラフの「逆辺」は何のため?
<details><summary>答え</summary>一度流した流れを取り消して別経路に振り直すため(貪欲の失敗を償う)。</details>

**Q5.** ラスベガス型とモンテカルロ型の乱択の違いは?
<details><summary>答え</summary>ラスベガス=答えは常に正しく時間が変動。モンテカルロ=時間は固定で答えがたまに誤る。</details>

---

## ☁️ GRAD 1: 分散システム

**Q1.** CAP 定理を正確に言うと?
<details><summary>答え</summary>ネットワーク分断(P)が起きている間、一貫性(C)と可用性(A)は両立できない。平常時は両方提供できる。</details>

**Q2.** 「タイムアウトしたから相手は死んだ」がなぜ危険?
<details><summary>答え</summary>相手は生きていて遅いだけかもしれず、区別できない。誤判定でスプリットブレインを起こしうる。</details>

**Q3.** Raft の 5 ノードは何台の故障まで書き込み継続できる?
<details><summary>答え</summary>2 台(過半数 3 が残る)。だからクラスタは奇数にする。</details>

**Q4.** 「過半数の重なり」が安全性をどう支える?
<details><summary>答え</summary>どの 2 つの過半数も必ず重なるので、コミット済みエントリを持たない候補は当選できない。</details>

**Q5.** 「いいね数」と「在庫数」で許される一貫性が違う理由は?
<details><summary>答え</summary>いいねは古くても実害がなく結果整合で十分。在庫は古い値の同時参照で二重販売の実害が出るため強い一貫性が要る。</details>

---

## 🛡️ GRAD 2: セキュリティ

**Q1.** ケルクホフスの原理とは?
<details><summary>答え</summary>アルゴリズムは公開してよい。秘密は鍵だけにせよ(隠蔽による安全は脆い)。</details>

**Q2.** なぜパスワードは「暗号化」でなく「ハッシュ化」して保存する?
<details><summary>答え</summary>暗号化は鍵があれば復元できるが、ハッシュは一方向でサーバすら元を知る必要がない。ソルト+低速ハッシュ(bcrypt等)で守る。</details>

**Q3.** RSA の安全性が依存する数学的困難性は?
<details><summary>答え</summary>大きな合成数の素因数分解の困難性(量子のショアのアルゴリズムが脅威)。</details>

**Q4.** SQL インジェクションとバッファオーバーフローの共通の根本原因は?
<details><summary>答え</summary>データとコード(命令/構文)の境界が曖昧なこと。防御は分離(プリペアドステートメント、境界チェック)。</details>

**Q5.** 前方秘匿性(forward secrecy)があると何が守られる?
<details><summary>答え</summary>長期鍵が将来漏れても、使い捨てセッション鍵のおかげで過去の通信は守られる。</details>

---

## 🔭 GRAD 3: 機械学習

**Q1.** 機械学習の本質的な目標は?
<details><summary>答え</summary>見たことのないデータでうまくやること(汎化)。訓練データの丸暗記は学習でない。</details>

**Q2.** 勾配降下法の更新式は?
<details><summary>答え</summary>w ← w − η・∂Loss/∂w(η は学習率=歩幅)。</details>

**Q3.** 過学習とは? 検出法は?
<details><summary>答え</summary>訓練データのノイズまで覚え未知データで外す現象。訓練精度と検証精度の乖離で検出。</details>

**Q4.** なぜニューラルネットに非線形活性化が必須?
<details><summary>答え</summary>線形変換を何層重ねても 1 つの線形変換に潰れ、表現力が増えないから。</details>

**Q5.** 誤差逆伝播は数学的に何をしている?
<details><summary>答え</summary>連鎖律(合成関数の微分)を計算グラフ上で出力側から入力側へ再帰適用し、各重みの勾配を求めている。</details>

**Q6.** LLM が「自信満々に間違える」理由と対処は?
<details><summary>答え</summary>確率的に「もっともらしい」語を選ぶよう訓練され事実性の保証がないから(ハルシネーション)。出典確認・人間の監督で対処。</details>

---

## ⚛️ GRAD 4: アーキテクチャ

**Q1.** ISA(命令セットアーキテクチャ)とは何の「契約」?
<details><summary>答え</summary>ハードウェアとソフトウェアの契約。これを守れば異なる実装でも同じプログラムが動く。</details>

**Q2.** 分岐予測が外れると何が失われる? なぜループは予測しやすい?
<details><summary>答え</summary>投機実行した命令を捨ててパイプラインを流し直すサイクル。ループは大半で「継続」するので予測が当たり続ける。</details>

**Q3.** アムダールの法則の式と教訓は?
<details><summary>答え</summary>高速化 = 1/((1−p)+p/n)。逐次部分 (1−p) が天井を決めるので、コアを増やすより逐次ボトルネックを減らす方が本質的。</details>

**Q4.** キャッシュコヒーレンスは何を保証する?
<details><summary>答え</summary>複数コアのキャッシュにある同一データの複製を整合させ、古い値を読まないようにする。</details>

**Q5.** フォルスシェアリングはなぜ起きる?
<details><summary>答え</summary>論理的に無関係な変数が同じキャッシュライン(64B)に同居し、片方の更新でライン全体が無効化されるから。</details>

---

## 🏆 記憶の神殿クリアの心得

このカードを **何も見ずに 8 割言える**ようになったら、君の知識は「読んだ」から「身についた」へ変わった。

| 勉強法 | 効果 |
|---|---|
| ただ読み返す | 弱い(分かった気になるだけ) |
| **能動的想起**(このカード) | 強い(思い出す行為が記憶を固める) |
| **間隔反復**(日を空けて再挑戦) | 最強(忘れる直前に思い出すと定着する) |

> 長老の言葉: 「概念を本当に学んだ者は、教科書を閉じても語れる。
> このカードは、その『閉じても語れる』状態へ君を運ぶ唯一の橋だ。
> 一度解いて終わりにするな。**忘れた頃にもう一度**。それが記憶の神殿の掟だ。」

➡️ 戻る: [CS Quest ホーム](README.md) ・ [実装クエスト解答集](appendix-04-implementation-solutions.md)
