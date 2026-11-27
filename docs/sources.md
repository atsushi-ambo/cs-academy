# 取り込める教材とライセンス

2026-11-26に、各リポジトリのLICENSEファイルと公式ページで確認した。教材の作り方は [design.md](design.md) の12章。

## 区分

- **A. 取り込んで改変してよい**: 出典とライセンスを書けば、本文・問題・テストをこのアプリの教材に組み込める。
- **B. 個人の非商用なら改変してよい**: CC BY-NC-SA。このアプリは本人の私的利用なので取り込める。公開・配布するなら同じライセンスで出す必要がある。
- **C. 参照だけ**: リンクし、構成を参考にする。本文・問題はコピーしない。

| 教材 | 内容 | ライセンス（確認方法） | 区分 | 使い方 |
|---|---|---|---|---|
| Exercism Python track | Python の演習（テスト付き）、概念の解説 | MIT（GitHub `exercism/python`） | A | Stage 1〜2 の Code 課題の土台。テストの形式も近い |
| Exercism problem-specifications | 言語に依存しない問題文と正解データ（152問、2026-11-26時点）。`leap` の正解データからPythonのテストを自動生成し、合格することを確認済み | MIT（GitHub `exercism/problem-specifications`） | A | 正解データから Python・C の課題とテストを機械的に作れる |
| Kubernetes 公式ドキュメント | 概念・チュートリアル | CC BY 4.0（kubernetes.io のフッター、`kubernetes/website`） | A | Stage 6 のハンズオンの土台。出典を書けば改変可 |
| Python 公式ドキュメント | Tutorial、Library Reference | PSF License v2。ドキュメント内のコード例は Zero-Clause BSD との二重ライセンス（docs.python.org/3/license.html） | A（コード例）/ 参照（本文） | コード例は自由に使う。本文は参照が中心 |
| freeCodeCamp | Web・Python・データの課題 | リポジトリ全体は BSD-3-Clause（`LICENSE.md`）。以前はカリキュラムが CC BY-SA 4.0 だった | 要確認 | 取り込む前に、該当ディレクトリのライセンスを個別に確認する |
| MIT Missing Semester | シェル、Git、エディタ、デバッグ | CC BY-NC-SA 4.0（リポジトリの `license.md`） | B | Stage 0 のハンズオンの土台 |
| Think Python 3rd ed. | Python 入門の教科書（無料公開） | CC BY-NC-SA 4.0（greenteapress.com） | B | Stage 1 の解説の参考・下敷き |
| Composing Programs | SICP系のPython教科書 | CC BY-SA 3.0（GitHub のREADME） | A（同じライセンスの継承が必要） | Stage 1〜2 の発展 |
| CS50（x、P、SQL、AI など） | 講義・課題 | CC BY-NC-SA 4.0 | B | 講義動画へのリンク、課題の構成を参考にする |
| MIT OpenCourseWare | 講義ノート・課題 | CC BY-NC-SA 4.0 | B | Stage 2・4・7 の深掘り |
| OSTEP | OS の教科書（章ごとに無料公開） | 無料で読めるが、改変・再配布のライセンスは明示されていない | C | Stage 4 の参照 |
| Recursion | CS の日本語コース（初級は無料） | 商用サービス | C | 構成の参考と受講の対応表。本人がログインした画面で初級の形式を確認した（2026-11-27、[reference-platforms.md](reference-platforms.md)） |
| LeetCode / HackerRank | 問題、Explore カード、模擬面接 | 商用サービス | C | 問題番号とURLで「次の練習」にする |
| 手元の本（Shiori・Kindle） | 技術書 | 著作権あり | C | 読む範囲（章・ページ）を示す。本人が選んだページを根拠に、オリジナルの問題を作る |

## 取り込むときの決まり

- 取り込んだファイルには、出典・ライセンス・変更点を `unit.yaml` の `attribution` に書く。
- A・B の教材も、品質基準（design.md 12章）の検証を通してから `published` にする。
- B の教材を含むUnitは、公開・共有しない（本人のMacの中だけ）。
- C の教材の文章・問題・図はコピーしない。言い換えた要約も作らない。

## 効果の見込み

- Exercism の problem-specifications を使うと、Stage 1〜2 の Code 課題とテストの多くは「正解データから自動で作る → 解説だけ書く」で済む。
- Kubernetes 公式チュートリアルを改変して使えるので、Stage 6 のハンズオンを一から書かなくてよい。
- 一から書く必要が大きいのは、Predict（四択）、日本の実務に合わせた例、英語の難易度の調整、Boss。
