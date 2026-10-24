"""新しい記事を追加して、よみもの一覧・トップ・サイトマップを更新する。
使い方: python3 tools/new_post.py post.json
post.json は次の形（data_posts.json の1件と同じ）:
{"id":"p20261023","date":"2026-10-23","category":"焼き菓子について","title":"...","slug":"english-slug",
 "keywords":["...",...],"description":"80〜120字","lead":"...","body":["段落", "## 小見出し", "段落", ...]}
"""
import os, re, sys, json, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = open(os.path.join(ROOT, 'tools', 'BASE')).read().strip()
SHOP = 'https://www.rakuten.co.jp/allonsbien/'


def journal_item(p, href):
    date = p['date'].replace('-', '.')
    return (f'<a href="{href}" style="display: grid; grid-template-columns: 7.5em 1fr; gap: 4px 24px; padding: 24px 0; border-bottom: 1px solid #E4DED4; text-decoration: none; color: #2A2623">'
            f'<span style="display: flex; flex-direction: column; font-size: 12px; color: #6B625A"><span>{date}</span><span style="color: #8A6D10; font-weight: 500">{p["category"]}</span></span>'
            f'<span style="display: flex; flex-direction: column; gap: 6px"><span style="font-size: 19px; font-weight: 500; line-height: 1.6">{H.escape(p["title"])}</span><span style="font-size: 14px; color: #6B625A">{H.escape(p["lead"])}</span></span></a>')


def post_href(p):
    return f'journal-{p["slug"]}.html'


def article_html(p):
    date = p['date'].replace('-', '.')
    body = ''
    for para in p['body']:
        if para.startswith('## '):
            body += f'<h2 style="margin: 2em 0 0.6em; font-size: 20px; font-weight: 700; line-height: 1.6">{H.escape(para[3:])}</h2>'
        else:
            body += f'<p style="margin: 0 0 1.4em">{H.escape(para)}</p>'
    return f'''<article style="max-width: 720px; margin: 0 auto; padding: 48px clamp(16px, 4vw, 32px) 72px">
<p style="margin: 0; font-size: 12px; color: #6B625A"><time datetime="{p['date']}">{date}</time>　<span style="color: #8A6D10; font-weight: 500">{p['category']}</span></p>
<h1 style="margin: 12px 0 0; font-weight: 500; font-size: clamp(24px, 4.6vw, 32px); line-height: 1.55">{H.escape(p['title'])}</h1>
<p style="margin: 18px 0 0; font-size: 16px; color: #6B625A">{H.escape(p['lead'])}</p>
<div style="margin-top: 32px; font-size: 16px; line-height: 2">{body}</div>
<p style="margin: 40px 0 0; padding-top: 20px; border-top: 1px solid #E4DED4; font-family: 'Instrument Serif', serif; font-style: italic; font-size: 20px; color: #6B625A">Allons bien ― さあ、元気になろう。</p>
<div style="margin-top: 32px; padding: 22px 24px; background: #FFFFFF; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px 20px">
<p style="margin: 0; font-size: 14px">お店の焼き菓子は、オンラインショップから全国へお届けしています（一部商品を除き送料無料）。</p>
<a href="{SHOP}" rel="noopener" style="display: inline-flex; align-items: center; gap: 8px; min-height: 46px; padding: 0 22px; border-radius: 999px; background: #2A2623; color: #F6F3EE; text-decoration: none; font-size: 13px">楽天で買う →</a>
</div>
<p style="margin: 32px 0 0"><a href="journal.html" style="font-size: 13px; letter-spacing: 0.08em">← よみもの一覧へ</a></p>
</article>'''




def main():
    new = json.load(open(sys.argv[1], encoding='utf-8'))
    for k in ('id', 'date', 'category', 'title', 'slug', 'keywords', 'description', 'lead', 'body'):
        assert k in new, 'missing ' + k
    assert re.fullmatch(r'[a-z0-9-]+', new['slug']), 'slug は英小文字・数字・ハイフンのみ'
    dp = os.path.join(ROOT, 'data_posts.json')
    posts = json.load(open(dp, encoding='utf-8'))
    posts = [p for p in posts if p['id'] != new['id']]
    posts.insert(0, new)
    posts.sort(key=lambda p: p['date'], reverse=True)
    json.dump(posts, open(dp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tpl = open(os.path.join(ROOT, 'tools', 'post_template.html'), encoding='utf-8').read()
    for p in posts:
        path = post_href(p)
        ld = [{'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'トップ', 'item': BASE},
                {'@type': 'ListItem', 'position': 2, 'name': 'よみもの', 'item': BASE + 'journal.html'},
                {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': BASE + path}]},
              {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['description'],
               'datePublished': p['date'], 'dateModified': p['date'], 'inLanguage': 'ja', 'keywords': ','.join(p['keywords']),
               'mainEntityOfPage': BASE + path, 'author': {'@type': 'Organization', 'name': 'Cafe & Bake Allons Bien'},
               'publisher': {'@type': 'Organization', 'name': 'Cafe & Bake Allons Bien'}}]
        out = (tpl.replace('{{TITLE}}', H.escape(p['title'])).replace('{{DESC}}', H.escape(p['description']))
               .replace('{{PATH}}', path).replace('{{KEYWORDS}}', H.escape(','.join(p['keywords'])))
               .replace('<script type="application/ld+json">{"{{LD}}": 1}</script>', ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>' for o in ld))
               .replace('<!--ARTICLE-->', article_html(p))
               .replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow">'))
        open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(out)

    def relist(fname, items, tweak=None):
        fp = os.path.join(ROOT, fname)
        s = open(fp, encoding='utf-8').read()
        block = ''.join((tweak(journal_item(p, post_href(p))) if tweak else journal_item(p, post_href(p))) for p in items)
        s = re.sub(r'<!--POSTS-->.*?<!--/POSTS-->', lambda m: '<!--POSTS-->' + block + '<!--/POSTS-->', s, count=1, flags=re.S)
        open(fp, 'w', encoding='utf-8').write(s)
    relist('journal.html', posts)
    relist('index.html', posts[:3], lambda h: h.replace('padding: 24px 0;', 'padding: 20px 0;', 1))
    sm = os.path.join(ROOT, 'sitemap.xml')
    s = open(sm, encoding='utf-8').read()
    loc = BASE + post_href(new)
    if loc not in s:
        s = s.replace('</urlset>', f'<url><loc>{loc}</loc><lastmod>{new["date"]}</lastmod></url>\n</urlset>')
    s = re.sub(r'(<loc>' + re.escape(BASE + 'journal.html') + r'</loc><lastmod>)[^<]*', r'\g<1>' + new['date'], s)
    s = re.sub(r'(<loc>' + re.escape(BASE) + r'</loc><lastmod>)[^<]*', r'\g<1>' + new['date'], s)
    open(sm, 'w', encoding='utf-8').write(s)
    print('ok', post_href(new), len(posts), 'posts')


if __name__ == '__main__':
    main()
