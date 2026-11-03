# Allons Bien オンラインショップ案内サイト

奈良・船橋商店街の焼き菓子店「Cafe & Bake Allons Bien（アロンビアン）」の公式サイトです。
商品の購入は楽天市場のショップ（https://www.rakuten.co.jp/allonsbien/）で行います。

## 構成
- `index.html` … トップ
- `cookie.html` `bake.html` `canele.html` `gift.html` `first.html` `matcha.html` `kotoka.html` `popular.html` `choco.html` `other.html` … カテゴリ
- `nara.html` … 奈良特集
- `journal.html` / `journal-*.html` … よみもの（ブログ）
- `assets/` … 画像・共通CSS・JS
- `sitemap.xml` `robots.txt` … 検索エンジン向け

## ブログ記事の追加
`python3 tools/new_post.py post.json` で、記事ページの作成・一覧・トップ・サイトマップの更新までまとめて行います。

## 修正のしかた
Claude に「〇〇を直して」と頼めば、このリポジトリを直して公開まで行います。

## IndexNow（Bing などに新しいページを自動で知らせる）
- 公開のあと、GitHub Actions が `tools/indexnow.py` を実行し、更新日が直近3日のページだけを送る。鍵は `f5583eafcedf018d704433ef65b0ce92`（鍵ファイル `f5583eafcedf018d704433ef65b0ce92.txt` はリポジトリ直下。消さない）。
- `tools/indexnow.py` と、Actions の IndexNow の手順は消さない。Google は IndexNow を使わないので、Google にはサイトマップ（Search Console）で知らせる。
