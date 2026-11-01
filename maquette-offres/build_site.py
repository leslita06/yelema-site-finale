import re, glob, os, sys
# Usage : python3 maquette-offres/build_site.py [dossier_du_site]  (par défaut : le dossier courant)
os.chdir(sys.argv[1] if len(sys.argv) > 1 else '.')

# ---------- 1. menu ----------
LINKS = [('Équipes', 'index.html#equipes'), ('Offres', 'offres.html'), ('Comment ça marche', 'comment-ca-marche.html'),
         ('Sécurité', 'securite.html'), ('Clients', 'clients.html'), ('Ressources', 'ressources.html')]
AUDIT = 'https://leslita06.github.io/yelema-declic-equipes/'

def nav_html(fname, home):
    out = []
    for t, h in LINKS:
        base = h.split('#')[0]
        here = (base == fname) or (fname.startswith('offres-') and base == 'offres.html')
        hh = ('#equipes' if (home and h == 'index.html#equipes') else h)
        out.append('<a href="%s"%s>%s</a>' % (hh, ' aria-current="page" class="ici"' if here else '', t))
    return ''.join(out)

n_nav = 0
for f in glob.glob('*.html'):
    s = open(f).read()
    m = re.search(r'(<nav id="menu"[^>]*>)(.*?)(</nav>)', s, re.S)
    if not m:
        continue
    home = (f == 'index.html')
    new = m.group(1) + nav_html(f, home) + '<a class="btn btn-p menu-cta" href="%s" target="_blank" rel="noopener">Lancer l\'Auditeur</a>' % AUDIT + m.group(3)
    s = s[:m.start()] + new + s[m.end():]
    s = re.sub(r'<a class="btn btn-c btn-s nav-cta" href="[^"]*">Composer mon équipe</a>',
               '<a class="btn btn-c btn-s nav-cta" href="%s" target="_blank" rel="noopener">Lancer l\'Auditeur</a>' % AUDIT, s)
    open(f, 'w').write(s)
    n_nav += 1
print('menus mis à jour :', n_nav)

# ---------- 2. Sécurité : retirer les trois badges sans source ----------
s = open('securite.html').read()
badge = lambda svg_hint, txt: re.search(r'<span class="sx-b">(?:(?!</span>).)*?%s</span>' % re.escape(txt), s, re.S)
for txt in ["Conforme aux exigences de l'ARTCI", "Instances certifiées SOC&nbsp;2", "Surveillance 24h/24"]:
    m = badge('', txt)
    assert m, txt
    s = s[:m.start()] + s[m.end():]
extra = ''.join('<span class="sx-b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg>%s</span>' % t
                for t in ['Serveur dédié à votre entreprise', 'Aucun modèle entraîné sur vos données', 'Vos Experts et vos données vous appartiennent'])
i = s.find('<div class="sx-bs">') + len('<div class="sx-bs">')
s = s[:i] + extra + s[i:]
open('securite.html', 'w').write(s)
print('sécurité : ARTCI/SOC2/24h présents ?', any(k in s for k in ["Conforme aux exigences de l'ARTCI", 'SOC&nbsp;2', 'Surveillance 24h']))

# ---------- 3. Offres ----------
o = open('offres.html').read()
o = o.replace('des Experts IA à la carte, entre les six fonctions de l\'entreprise.', 'des Experts IA à la carte, entre les sept fonctions de l\'entreprise.')
o = o.replace('commercial, marketing, RH, finance, service client, investissement</li>', 'commercial, marketing, RH, finance, service client, opérations, investissement</li>')
o = o.replace('href="#demo"', 'href="#contact"')
o = re.sub(r'<script>\(function\(\)\{var c=document\.querySelector\("\[data-calc\]"\).*?\}\)\(\)</script>', '', o, flags=re.S)
mention = ('<p class="kf-mention center"><b>Tous les prix s\'entendent en francs CFA, hors taxes (HT).</b> '
           'Engagement minimum de six mois. Le chat d\'entreprise est inclus dans les trois offres.</p>')
o = o.replace('<div class="of-declic">', mention + '\n<div class="of-declic">', 1)
o = o.replace('href="https://leslita06.github.io/yelema-declic-equipes/" target="_blank" rel="noopener">Lancer l\'Auditeur d\'entreprise', 'href="%s" target="_blank" rel="noopener">Lancer l\'Auditeur d\'entreprise' % AUDIT, 1)
sub_links = ('<p class="kf-sous center">Le détail de chaque offre : '
             '<a href="offres-executif.html">Exécutif</a> · <a href="offres-entreprise.html">Entreprise</a> · <a href="offres-custom.html">Custom</a></p>')
o = o.replace(mention, mention + sub_links, 1)
KF_CSS = ('<style id="kf-css">.kf-mention{margin:28px auto 6px;max-width:760px;color:var(--ink);font-size:15px}'
          '.kf-sous{margin:0 auto 24px;font-size:15px;color:var(--muted)}.kf-sous a{color:var(--bleu);font-weight:600}'
          '.v2of.kf-un{grid-template-columns:minmax(0,600px);justify-content:center}'
          '.kf-off{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}'
          '.kf-c{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:28px;display:flex;flex-direction:column;gap:12px}'
          '.kf-c.kf-star{background:var(--deep);color:#fff;border-color:var(--bord)}.kf-c.kf-star h3{color:#fff}'
          '.kf-c .kf-tag{font:600 12px var(--h);letter-spacing:.06em;text-transform:uppercase;color:var(--violet-t)}.kf-star .kf-tag{color:var(--lav)}'
          '.kf-c h3{font-size:26px;color:var(--nuit)}.kf-p{font:700 30px/1.1 var(--h)}.kf-p small{display:block;font:400 15px var(--b);margin-top:6px;opacity:.85}'
          '.kf-c ul{list-style:none;display:grid;gap:8px;font-size:16px}.kf-c li{padding-left:22px;position:relative}'
          '.kf-c li:before{content:"";position:absolute;left:0;top:.55em;width:10px;height:6px;border-left:2px solid var(--vert);border-bottom:2px solid var(--vert);transform:rotate(-45deg)}'
          '.kf-star li:before{border-color:var(--lav)}.kf-c .btn{margin-top:auto;justify-content:center}'
          '.kf-note{text-align:center;margin-top:22px;font-size:15px}'
          '@media(max-width:900px){.kf-off{grid-template-columns:1fr}}</style>')
o = o.replace('</head>', KF_CSS + '</head>', 1)
open('offres.html', 'w').write(o)

# ---------- 4. Sous-pages d'offre ----------
head_end = o.find('<section class="ph" id="haut">')
hero_end = o.find('</section>', head_end) + len('</section>')
grid_start = o.find('<div class="v2of">')
cards = [m.start() for m in re.finditer(r'<div class="v2of-c', o)]
grid_end = o.find('<div class="of-declic">')
c1, c2, c3 = cards[0], cards[1], cards[2]
card_html = [o[c1:c2], o[c2:c3], o[c3:o.rfind('</div>\n', c3, grid_end) + len('</div>\n')]]
def sec(idv):
    a = o.find('<section id="%s"' % idv)
    return o[a:o.find('</section>', a) + len('</section>')]
details = {'executif': sec('executif'), 'entreprise': sec('entreprise'), 'custom': sec('custom')}
demo_a = o.find('<section class="pad" id="contact">')
demo_html = o[demo_a:o.find('</section>', demo_a) + len('</section>')]
tail = o[o.find('<footer class="ftr p2">'):]
pre_main = o[:head_end]
subs = {
 'executif': dict(file='offres-executif.html', eyebrow='Offre Exécutif', h1='Djénéba, la cheffe de cabinet du dirigeant.',
                  lede='300 000 F par mois HT, installation offerte. Elle travaille depuis votre téléphone : vocaux, agenda, e-mails, documents et chiffres. Rien ne part sans votre accord.',
                  title='Offre Exécutif | Yelema', desc="L'offre Exécutif : Djénéba, la cheffe de cabinet du dirigeant, 300 000 F CFA par mois HT.", card=0),
 'entreprise': dict(file='offres-entreprise.html', eyebrow='Offre Entreprise', h1='Vos équipes d\'Experts IA, composées à la carte.',
                  lede='Dès 500 000 F par mois HT, soit 250 000 F par Expert, deux Experts au minimum, Djénéba toujours incluse. Le chat d\'entreprise est inclus.',
                  title='Offre Entreprise | Yelema', desc="L'offre Entreprise : des Experts IA à la carte, dès 500 000 F CFA par mois HT.", card=1),
 'custom': dict(file='offres-custom.html', eyebrow='Offre Custom', h1='Des agents IA sur mesure, sur un maillon de votre chaîne.',
                  lede='Sur devis, après un atelier de cadrage. Pour les grands groupes, les administrations et les programmes de déploiement à grande échelle.',
                  title='Offre Custom | Yelema', desc="L'offre Custom : des agents ou workflows IA sur mesure, sur devis après un atelier de cadrage.", card=2),
}
def build_hero(sd):
    h = o[head_end:hero_end]
    h = re.sub(r'<p class="eyebrow e-lav">.*?</p>', '<p class="eyebrow e-lav">%s</p>' % sd['eyebrow'], h, 1, re.S)
    h = re.sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % sd['h1'], h, 1, re.S)
    h = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">%s</p>' % sd['lede'], h, 1, re.S)
    return h
for k, sd in subs.items():
    pre = pre_main
    pre = re.sub(r'<title>.*?</title>', '<title>%s</title>' % sd['title'], pre, 1)
    pre = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % sd['desc'], pre, 1)
    body = (build_hero(sd) + '<div class="anc"><section class="pad"><div class="wrap"><div class="v2of kf-un">' + card_html[sd['card']] + '</div>'
            + mention + '<p class="kf-sous center"><a href="offres.html">← Comparer les trois offres</a></p></div></section>'
            + details[k] + demo_html + '</div></main>')
    page = pre + body + tail
    m = re.search(r'(<nav id="menu"[^>]*>)(.*?)(</nav>)', page, re.S)
    page = page[:m.start()] + m.group(1) + nav_html(sd['file'], False) + '<a class="btn btn-p menu-cta" href="%s" target="_blank" rel="noopener">Lancer l\'Auditeur</a>' % AUDIT + m.group(3) + page[m.end():]
    open(sd['file'], 'w').write(page)
    print('créé', sd['file'], len(page))

# ---------- 5. Accueil : section Offres ----------
x = open('index.html').read()
x = x.replace('href="#demo"', 'href="#contact"') if 'id="demo"' not in x else x
cards_home = '''<section class="pad" id="offres"><div class="wrap">
<div class="sh rv"><p class="eyebrow">Nos offres</p><h2>Trois offres, et le chat d'entreprise pour tous.</h2>
<p>Commencez par le dirigeant, étendez fonction par fonction.</p></div>
<div class="kf-off">
<div class="kf-c"><span class="kf-tag">Pour commencer</span><h3>Exécutif</h3><p>Djénéba, la cheffe de cabinet du dirigeant.</p>
<div class="kf-p">300 000 F<small>par mois HT, installation offerte</small></div>
<ul><li>Elle vous répond à la voix</li><li>Votre agenda et vos e-mails, réponses préparées</li><li>Chaque document reçu analysé</li><li>Chat d'entreprise pour tous vos salariés</li></ul>
<a class="btn btn-primary" href="offres-executif.html">Voir l'offre Exécutif</a></div>
<div class="kf-c kf-star"><span class="kf-tag">Pour vos équipes</span><h3>Entreprise</h3><p>Des Experts IA à la carte, entre les sept fonctions de l'entreprise.</p>
<div class="kf-p">Dès 500 000 F<small>par mois HT, 250 000 F par Expert, deux au minimum</small></div>
<ul><li>Djénéba toujours incluse</li><li>Branchés sur vos outils et vos règles</li><li>Opérés et améliorés chaque mois par notre équipe</li><li>Chat d'entreprise pour tous vos salariés</li></ul>
<a class="btn btn-c" href="offres-entreprise.html">Voir l'offre Entreprise</a></div>
<div class="kf-c"><span class="kf-tag">Sur mesure</span><h3>Custom</h3><p>Des agents ou des workflows IA, sur un maillon de votre chaîne de valeur.</p>
<div class="kf-p">Sur devis<small>après un atelier de cadrage</small></div>
<ul><li>Serveur dédié, ou dans vos locaux si vous l'exigez</li><li>Conçus et opérés par notre équipe</li><li>Chat d'entreprise pour tous vos salariés</li></ul>
<a class="btn btn-primary" href="offres-custom.html">Voir l'offre Custom</a></div>
</div>
<p class="kf-note"><b>Tous les prix s'entendent en francs CFA, hors taxes (HT).</b> Engagement minimum de six mois. <a href="offres.html">Comparer les trois offres →</a></p>
<p class="kf-note">Pas sûr de l'offre qu'il vous faut ? <a href="%s" target="_blank" rel="noopener"><b>Lancez l'Auditeur d'entreprise</b></a> : cinq minutes pour chiffrer les heures que votre équipe perd chaque semaine.</p>
</div></section>
''' % AUDIT
anchor = '<section class="pad soft" id="chat-entreprise">'
assert anchor in x
x = x.replace(anchor, cards_home + anchor, 1)
x = x.replace('</head>', KF_CSS + '</head>', 1)
open('index.html', 'w').write(x)
print('ok')
