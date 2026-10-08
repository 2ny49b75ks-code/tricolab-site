#!/usr/bin/env python3
"""Génère le site Tricolab (FR + EN) sur le modèle du site SITE DIM :
fr/ et en/ (accueil, fonctionnalités, téléchargement, contact, confidentialité),
assets/, sitemap.xml, robots.txt, redirection de langue à la racine.
Les anciennes adresses (assistance.html, confidentialite.html, support-en.html,
privacy-en.html, support.html, privacy.html, en.html) sont conservées : elles sont
déjà inscrites dans App Store Connect.

Le texte de l'assistance, de la confidentialité et de l'accueil vient de contenu.py.
Lancer `python3 build.py` après toute modification, puis commit + push."""
import json
from datetime import date
from pathlib import Path

from contenu import EMAIL, EFFECTIVE, HOME, SUPPORT, PRIVACY

ROOT = Path(__file__).parent
# Adresse publique du site (Netlify, publié le 2026-10-01). GitHub Pages reste actif en parallèle.
SITE = "https://tricolab.netlify.app"
# Lien App Store (approuvée, ID 6817956569), une version par langue.
APPSTORE_BASE = "https://apps.apple.com/ca/app/tricolab/id6817956569"
APPSTORE = {"fr": APPSTORE_BASE + "?l=fr-CA", "en": APPSTORE_BASE + "?l=en-CA"}
TODAY = date.today().isoformat()
# Liens vers les autres apps de JDG inc. (pied de page de l'accueil)
JDG_APPS = {'fr': '<div class="jdg-apps" style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(127,127,127,.3);font-size:.88em;line-height:1.8;text-align:center"><strong>Les autres apps de JDG inc., Québec :</strong> <a href="https://camordtu.netlify.app/">CaMordTu</a> <span style="opacity:.75">(guide de pêche au Québec)</span> · <a href="https://sitedim.netlify.app/fr/index.html">SITE DIM</a> <span style="opacity:.75">(relevé de chantier en réalité augmentée)</span> · <a href="https://appmycreation.com/">MY CREATION</a> <span style="opacity:.75">(vos œuvres en relief 3D et en réalité augmentée)</span> · <a href="https://apps.apple.com/ca/app/id6810440422?l=fr-CA">Acoustic Detector</a> <span style="opacity:.75">(mesure sonore et traitement acoustique)</span> · <a href="https://apps.apple.com/ca/app/id6811432420?l=fr-CA">Fort et Château</a> <span style="opacity:.75">(forts et châteaux du monde)</span></div>', 'en': '<div class="jdg-apps" style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(127,127,127,.3);font-size:.88em;line-height:1.8;text-align:center"><strong>More apps by JDG inc., Quebec:</strong> <a href="https://camordtu.netlify.app/en.html">CaMordTu</a> <span style="opacity:.75">(Quebec fishing guide)</span> · <a href="https://sitedim.netlify.app/en/index.html">SITE DIM</a> <span style="opacity:.75">(AR construction measuring)</span> · <a href="https://appmycreation.com/index-en.html">MY CREATION</a> <span style="opacity:.75">(your artwork in 3D relief and AR)</span> · <a href="https://apps.apple.com/ca/app/id6810440422?l=en-CA">Acoustic Detector</a> <span style="opacity:.75">(sound measurement and acoustic treatment)</span> · <a href="https://apps.apple.com/ca/app/id6811432420?l=en-CA">Fort et Château</a> <span style="opacity:.75">(forts and castles of the world)</span></div>'}

FILES = {
    "home": {"fr": "index.html", "en": "index.html"},
    "features": {"fr": "fonctionnalites.html", "en": "features.html"},
    "download": {"fr": "telechargement.html", "en": "download.html"},
    "contact": {"fr": "contact.html", "en": "contact.html"},
    "privacy": {"fr": "confidentialite.html", "en": "privacy.html"},
}
NAV_ORDER = ["home", "features", "download", "contact"]
# (fichier racine, langue, page) : anciennes adresses déjà diffusées
LEGACY = [
    ("assistance.html", "fr", "contact"), ("support.html", "fr", "contact"), ("support-en.html", "en", "contact"),
    ("confidentialite.html", "fr", "privacy"), ("privacy.html", "fr", "privacy"), ("privacy-en.html", "en", "privacy"),
]

T = {
    "fr": {
        "nav": {"home": "Accueil", "features": "Fonctionnalités", "download": "Téléchargement", "contact": "Contact", "privacy": "Confidentialité"},
        "cta": "Télécharger", "soon": "Bientôt sur l'App Store", "store": "Télécharger sur l'App Store",
        "footer": "© 2026 JDG inc. — Québec, Canada. Tricolab est une marque de JDG inc.",
        "menu": "Menu", "locale": "fr_CA", "alt_locale": "en_CA",
    },
    "en": {
        "nav": {"home": "Home", "features": "Features", "download": "Download", "contact": "Contact", "privacy": "Privacy"},
        "cta": "Download", "soon": "Coming soon to the App Store", "store": "Download on the App Store",
        "footer": "© 2026 JDG inc. — Quebec, Canada. Tricolab is a trademark of JDG inc.",
        "menu": "Menu", "locale": "en_CA", "alt_locale": "fr_CA",
    },
}

SHOT = {  # clé → fichier de capture (jeu 1.1 + couverture magazine 1.2)
    "home": "01-accueil", "counter": "02-compteur-patron", "three": "03-vue-3d-avancement", "garments": "04-vetements", "pattern": "05-fiche-vetement",
    "grid": "06-grille-crop-circle", "gen": "07-generateur-chevalier", "lab": "08-labo", "card": "09-carte-a-partager", "full": "10-tricolab-complet", "magazine": "magazine",
}

# ----------------------------------------------------------------- contenu propre aux nouvelles pages
HOME2 = {
    "fr": dict(
        eyebrow="Tricot · crochet · scrapbook",
        h_free="Gratuite, avec un achat unique facultatif",
        free="Le compteur mains libres, le lecteur de patrons, 5 patrons de lancement, 3 motifs crop circle, l'aperçu 3D et en réalité augmentée, le Labo, les défis et les cartes à partager sont inclus. L'achat unique « Tricolab Complet » (4,99 $ CA) débloque les 31 autres patrons et les 27 autres motifs. Pas d'abonnement.",
        cta_h="Prêt à tricoter, crocheter, créer ?", cta_p="Tricolab est disponible sur l'App Store, pour iPhone et iPad. Gratuite, avec un achat unique facultatif.",
        more="Voir toutes les fonctionnalités",
        news_badge="Nouveautés", news_h="Vêtements, 3D, réalité augmentée et magazine",
        news=["Collection Vêtements, du S au 2XL : pull, gilet à capuchon, veston, gilet sans manches, jupe, housse d'appuie-tête et couvre-siège d'auto",
              "Ta pièce en 3D et en réalité augmentée, à taille réelle, avec l'avancement en couleur",
              "Choix des couleurs sur chaque patron, 4 palettes assorties et 10 nouveaux motifs (course et chevalier)",
              "Exportation style magazine : transforme ton projet terminé en couverture de magazine à partager"],
        news_status="Version 1.1 : en cours de vérification chez Apple · Exportation magazine : prévue dans la version 1.2.",

        meta=[("iOS 17+", "requis"), ("iPhone", "et iPad"), ("FR / EN", "bilingue"), ("0 $", "sans publicité")],
        title="Tricolab — compteur de rangs, patrons et motifs pour le tricot et le crochet",
    ),
    "en": dict(
        eyebrow="Knitting · crochet · scrapbook",
        h_free="Free, with one optional purchase",
        free="The hands-free counter, the pattern reader, 5 launch patterns, 3 crop circle motifs, the 3D and augmented-reality preview, the Lab, challenges and shareable cards are included. The one-time \"Tricolab Complete\" purchase (CA$4.99) unlocks the 31 other patterns and the 27 other motifs. No subscription.",
        cta_h="Ready to knit, crochet, create?", cta_p="Tricolab is available on the App Store, for iPhone and iPad. Free, with one optional purchase.",
        more="See all features",
        news_badge="What's new", news_h="Clothing, 3D, augmented reality and magazine",
        news=["Clothing collection, S to 2XL: sweater, hooded cardigan, jacket, sleeveless vest, skirt, headrest cover and car seat pad",
              "Your piece in 3D and augmented reality, at real size, with progress shown in colour",
              "Colour choices on every pattern, 4 matching palettes and 10 new motifs (racing and knight)",
              "Magazine-style export: turn a finished project into a magazine cover to share"],
        news_status="Version 1.1: under review at Apple · Magazine export: planned for version 1.2.",

        meta=[("iOS 17+", "required"), ("iPhone", "and iPad"), ("FR / EN", "bilingual"), ("$0", "no ads")],
        title="Tricolab — row counter, patterns and motifs for knitting and crochet",
    ),
}

FEATURES = {
    "fr": dict(
        title="Fonctionnalités — Tricolab", desc="Compteur mains libres, patrons qui suivent ta ligne, 36 patrons originaux, vêtements, 3D et réalité augmentée, générateur de motifs, Labo, cartes à partager et exportation style magazine : tout ce que fait Tricolab.",
        h1="Tout ce que fait Tricolab", intro="Un seul labo pour compter, suivre un patron, créer des motifs et garder tes projets bien rangés.",
        blocks=[
            ("counter", "Un compteur de rangs mains libres",
             "Pensé pour les mains occupées : tu n'as pas à lâcher tes aiguilles.",
             ["Un très gros bouton +, accessible d'un pouce", "Dis « suivant » ou « retour » : le compteur avance tout seul", "L'écran reste allumé pendant que tu travailles", "Motif répété, objectif de rangs, annulation, temps passé"]),
            ("pattern", "Un patron qui ne perd jamais ta place",
             "Importe un PDF, photographie un patron papier ou colle son texte.",
             ["La ligne en cours est surlignée, ta position est sauvegardée", "Les abréviations sont traduites en clair, en français comme en anglais", "36 patrons originaux en 6 styles : Classique, Moderne, Rustique, Émoticône, Crop circle et Vêtements", "Dessin de l'objet fini, schéma coté, et tailles qui recalculent les instructions"]),
            ("gen", "Un générateur de motifs",
             "30 motifs en grille — crop circle, pêche, construction, feuilles, course, chevalier et plus.",
             ["Choisis la taille, deux couleurs et la technique (tricot double face ou crochet tapisserie)", "Les instructions s'écrivent toutes seules, rang par rang", "Le compteur suit ton avancement directement sur la grille"]),
            ("lab", "Le Labo",
             "Tout pour apprendre et calculer, sans quitter l'app.",
             ["Techniques pas à pas pour le tricot et le crochet", "Fibres, aiguilles, crochets et accessoires expliqués", "Exemples de schémas et dictionnaire d'abréviations", "Calculateurs : jauge, changement de taille, quantité de laine, tailles d'aiguilles"]),
            ("garments", "Des vêtements, du S au 2XL",
             "Une collection complète à tricoter, avec les instructions qui se recalculent à ta taille.",
             ["Pull, gilet à capuchon, veston, gilet sans manches et jupe évasée", "Housse d'appuie-tête et couvre-siège d'auto", "Ajustement au corps en option : élastique ou cordon aux poignets et à la taille", "Choisis tes couleurs, ou pars d'une des 4 palettes assorties"]),
            ("three", "Ta pièce en 3D et en réalité augmentée",
             "Vois ton projet à taille réelle avant même de commencer, puis suis-le en 3D.",
             ["Pose-le sur ta table ou au mur, déplace-le et tourne-le du doigt", "Ta main passe devant la pièce", "Pendant le projet, les rangs faits sont en couleur et le reste en pâle", "La caméra de la réalité augmentée n'enregistre rien"]),
            ("magazine", "Exportation style magazine",
             "Ton projet terminé devient la couverture d'un magazine à ton nom.",
             ["Grand titre, sous-titre et nom ou pseudo à ta façon", "Patron, laine, temps, rangs et outils remplis automatiquement", "Enregistre dans Photos : format Publication ou Story, ou PDF à imprimer", "Code QR vers l'App Store et présentoir de tous tes magazines dans ton profil"]),
            ("card", "Partage et motivation",
             "Montre ce que tu as créé, et garde le plaisir de continuer.",
             ["Une carte de fin de projet prête pour tes réseaux", "Un défi par mois avec son mot-clic", "Des badges à débloquer et à partager", "Ton bilan annuel : rangs, heures, laine utilisée, projets terminés"]),
            ("home", "Tes projets, bien rangés",
             "Une fiche par création, sur iPhone comme sur iPad.",
             ["Photos, patron, laine, notes et avancement au même endroit", "Inventaire de laine", "Tout reste sur ton appareil : aucun compte, aucune publicité, aucun traceur"]),
        ],
        h_cmp="Gratuit ou Tricolab Complet", cmp_cols=("", "Gratuit", "Complet"),
        cmp_rows=[("Compteur mains libres", "✓", "✓"), ("Lecteur de patrons (PDF, photo, texte)", "✓", "✓"), ("Le Labo et ses calculateurs", "✓", "✓"),
                  ("Défis du mois et cartes à partager", "✓", "✓"), ("Aperçu 3D et réalité augmentée", "✓", "✓"), ("Patrons originaux", "5", "36"), ("Motifs en grille", "3", "30")],
        cmp_note="« Tricolab Complet » est un achat unique de 4,99 $ CA, sans abonnement.",
    ),
    "en": dict(
        title="Features — Tricolab", desc="Hands-free counter, patterns that keep your place, 36 original patterns, clothing, 3D and augmented reality, motif generator, the Lab, shareable cards and magazine-style export: everything Tricolab does.",
        h1="Everything Tricolab does", intro="One lab to count, follow a pattern, create motifs and keep your projects organized.",
        blocks=[
            ("counter", "A hands-free row counter",
             "Built for busy hands: you never have to put your needles down.",
             ["One very big + button, right under your thumb", "Say \"next\" or \"back\": the counter moves by itself", "The screen stays on while you work", "Pattern repeats, row goal, undo, time spent"]),
            ("pattern", "A pattern that never loses your place",
             "Import a PDF, photograph a paper pattern or paste its text.",
             ["Your current line is highlighted and your position is saved", "Abbreviations are explained in plain words, in English and French", "36 original patterns in 6 styles: Classic, Modern, Rustic, Emoticon, Crop circle and Clothing", "A drawing of the finished item, a measured schematic, and sizes that recalculate the instructions"]),
            ("gen", "A motif generator",
             "30 chart motifs — crop circles, fishing, construction, leaves, racing, knight and more.",
             ["Choose the size, two colours and the technique (double knitting or tapestry crochet)", "Row-by-row instructions are written automatically", "The counter follows your progress right on the chart"]),
            ("lab", "The Lab",
             "Everything to learn and calculate, without leaving the app.",
             ["Step-by-step techniques for knitting and crochet", "Fibres, needles, hooks and notions explained", "Chart examples and an abbreviation dictionary", "Calculators: gauge, resizing, yarn quantity, needle sizes"]),
            ("garments", "Clothing, from S to 2XL",
             "A complete collection to knit, with instructions that recalculate to your size.",
             ["Sweater, hooded cardigan, jacket, sleeveless vest and A-line skirt", "Headrest cover and car seat pad", "Optional body fit: elastic or drawstring at the cuffs and waist", "Pick your colours, or start from one of 4 matching palettes"]),
            ("three", "Your piece in 3D and augmented reality",
             "See your project at real size before you even start, then follow it in 3D.",
             ["Place it on your table or wall, move it and turn it with your finger", "Your hand passes in front of the piece", "While you knit, finished rows show in colour and the rest faded", "The augmented-reality camera records nothing"]),
            ("magazine", "Magazine-style export",
             "Your finished project becomes the cover of a magazine with your name on it.",
             ["Big headline, subtitle and name or nickname your way", "Pattern, yarn, time, rows and tools filled in automatically", "Save to Photos: Post or Story format, or a printable PDF", "QR code to the App Store, and a rack of all your magazines in your profile"]),
            ("card", "Share and stay motivated",
             "Show what you made, and keep the joy of going on.",
             ["A finished-project card ready for your socials", "A monthly challenge with its hashtag", "Badges to unlock and share", "Your year in review: rows, hours, yarn used, projects finished"]),
            ("home", "Your projects, organized",
             "One page per creation, on iPhone and iPad alike.",
             ["Photos, pattern, yarn, notes and progress in one place", "Yarn stash", "Everything stays on your device: no account, no ads, no trackers"]),
        ],
        h_cmp="Free or Tricolab Complete", cmp_cols=("", "Free", "Complete"),
        cmp_rows=[("Hands-free counter", "✓", "✓"), ("Pattern reader (PDF, photo, text)", "✓", "✓"), ("The Lab and its calculators", "✓", "✓"),
                  ("Monthly challenges and shareable cards", "✓", "✓"), ("3D and augmented-reality preview", "✓", "✓"), ("Original patterns", "5", "36"), ("Chart motifs", "3", "30")],
        cmp_note="\"Tricolab Complete\" is a one-time CA$4.99 purchase, with no subscription.",
    ),
}

DOWNLOAD = {
    "fr": dict(
        title="Téléchargement — Tricolab", desc="Télécharge Tricolab sur l'App Store pour iPhone et iPad. Gratuite, avec un achat unique facultatif.",
        h1="Télécharger Tricolab", intro="Tricolab est gratuite et disponible sur l'App Store, pour iPhone et iPad.",
        status_h="Disponibilité", status="Disponible maintenant sur l'App Store, pour iPhone et iPad (iOS 17 ou plus récent).",
        faq_h="Avant de télécharger",
        faq=[("Mon appareil est-il compatible ?", "Tricolab fonctionne sur iPhone et iPad avec iOS 17 ou plus récent."),
             ("Combien ça coûte ?", "L'app est gratuite. L'achat unique facultatif « Tricolab Complet » (4,99 $ CA) débloque tous les patrons et motifs, sans abonnement."),
             ("Faut-il un compte ?", "Non. Aucun compte, aucune publicité, aucun traceur : tes projets restent sur ton appareil."),
             ("En quelles langues ?", "Entièrement en français et en anglais, avec un bouton FR / EN dans l'app. Chaque patron existe dans les deux langues."),
             ("Et sur Android ?", "Pas pour l'instant : Tricolab est seulement sur iPhone et iPad."),
             ("Comment obtenir de l'aide ?", f'Écris-nous à <a href="mailto:{EMAIL}">{EMAIL}</a> ou consulte la page <a href="contact.html">Contact</a>.')],
    ),
    "en": dict(
        title="Download — Tricolab", desc="Download Tricolab on the App Store for iPhone and iPad. Free, with one optional purchase.",
        h1="Download Tricolab", intro="Tricolab is free and available on the App Store, for iPhone and iPad.",
        status_h="Availability", status="Available now on the App Store, for iPhone and iPad (iOS 17 or later).",
        faq_h="Before you download",
        faq=[("Is my device compatible?", "Tricolab runs on iPhone and iPad with iOS 17 or later."),
             ("How much does it cost?", "The app is free. The optional one-time \"Tricolab Complete\" purchase (CA$4.99) unlocks every pattern and motif, with no subscription."),
             ("Do I need an account?", "No. No account, no ads, no trackers: your projects stay on your device."),
             ("Which languages?", "Fully in English and French, with an FR / EN button in the app. Every pattern exists in both languages."),
             ("What about Android?", "Not at the moment: Tricolab is for iPhone and iPad only."),
             ("How do I get help?", f'Email us at <a href="mailto:{EMAIL}">{EMAIL}</a> or visit the <a href="contact.html">Contact</a> page.')],
    ),
}

CONTACT_EXTRA = {
    "fr": dict(title="Contact et assistance — Tricolab", desc="Aide, questions fréquentes et contact pour l'app Tricolab.", h1="Contact et assistance",
               mail_h="Nous écrire", mail_p="Précise si possible ton modèle d'iPhone ou d'iPad et ta version d'iOS. Chaque message est lu.", biz="JDG inc. · Québec, Canada"),
    "en": dict(title="Contact and support — Tricolab", desc="Help, frequently asked questions and contact for the Tricolab app.", h1="Contact and support",
               mail_h="Write to us", mail_p="If you can, tell us your iPhone or iPad model and your iOS version. Every message is read.", biz="JDG inc. · Quebec, Canada"),
}


# ----------------------------------------------------------------- gabarit
def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def page(lang, key, title, desc, body, depth=1, jsonld=None):
    """depth=1 : fichier dans fr/ ou en/ ; depth=0 : ancienne adresse à la racine."""
    t = T[lang]
    other = "en" if lang == "fr" else "fr"
    up = "../" if depth else ""
    own = "" if depth else f"{lang}/"          # préfixe vers les pages de la même langue
    oth = f"../{other}/" if depth else f"{other}/"
    nav = "".join(
        f'<li><a href="{own}{FILES[k][lang]}"{" aria-current=\"page\"" if k == key else ""}>{t["nav"][k]}</a></li>' for k in NAV_ORDER + ["privacy"])
    foot = "".join(f'<li><a href="{own}{FILES[k][lang]}">{t["nav"][k]}</a></li>' for k in NAV_ORDER + ["privacy"])
    sw_fr = f'<a href="{(oth if lang == "en" else "")}{FILES[key]["fr"]}" hreflang="fr" lang="fr"{" class=\"active\"" if lang == "fr" else ""}>FR</a>'
    sw_en = f'<a href="{(oth if lang == "fr" else "")}{FILES[key]["en"]}" hreflang="en" lang="en"{" class=\"active\"" if lang == "en" else ""}>EN</a>'
    if depth == 0:  # racine : les deux liens passent par le dossier de langue
        sw_fr = f'<a href="fr/{FILES[key]["fr"]}" hreflang="fr" lang="fr"{" class=\"active\"" if lang == "fr" else ""}>FR</a>'
        sw_en = f'<a href="en/{FILES[key]["en"]}" hreflang="en" lang="en"{" class=\"active\"" if lang == "en" else ""}>EN</a>'
    canon = f"{SITE}/{lang}/{'' if key == 'home' else FILES[key][lang]}"
    alt = {l: f"{SITE}/{l}/{'' if key == 'home' else FILES[key][l]}" for l in ("fr", "en")}
    og = f"{SITE}/assets/img/og-image-{lang}.png"
    ld = f'<script type="application/ld+json">\n{json.dumps(jsonld, ensure_ascii=False, indent=2)}\n</script>\n' if jsonld else ""
    cta = (f'<a href="{own}{FILES["download"][lang]}" class="btn btn--primary btn--sm">{t["cta"]}</a>')
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="fr" href="{alt['fr']}">
<link rel="alternate" hreflang="en" href="{alt['en']}">
<link rel="alternate" hreflang="x-default" href="{alt['fr']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tricolab">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{t['alt_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#FBF7F1">
{ld}<link rel="icon" href="{up}assets/apple-touch-icon.png">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="stylesheet" href="{up}assets/css/style.css">
</head>
<body>

<header class="site-header">
  <div class="container site-header__row">
    <a href="{own}index.html" class="brand"><img src="{up}assets/img/logo-mark.png" alt="" class="brand-mark" width="42" height="42">Tricolab</a>
    <nav class="main-nav" id="main-nav" aria-label="{t['menu']}">
      <ul class="main-nav__links">{nav}</ul>
    </nav>
    <div class="header-actions">
      <div class="lang-switch">{sw_fr}{sw_en}</div>
      {cta}
      <button class="nav-toggle" aria-label="{t['menu']}" aria-expanded="false" aria-controls="main-nav"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="container">
    <div class="site-footer__row">
      <a href="{own}index.html" class="site-footer__brand"><img src="{up}assets/img/logo-mark.png" alt="" class="brand-mark" width="42" height="42">Tricolab</a>
      <nav><ul>{foot}</ul></nav>
    </div>
    {JDG_APPS[lang]}
    <div class="site-footer__meta">{t['footer']}</div>
  </div>
</footer>

<script src="{up}assets/js/main.js"></script>
</body>
</html>
"""


def store_button(lang, small=False):
    t = T[lang]
    if APPSTORE:
        return f'<a href="{APPSTORE[lang]}" class="btn btn--primary" target="_blank" rel="noopener">{t["store"]}</a>'
    return f'<span class="btn btn--soon">{t["soon"]}</span>'


def shot(lang, key, alt, depth=1, cls=""):
    up = "../" if depth else ""
    return f'<img src="{up}assets/{lang}-{SHOT[key]}.jpg" alt="{esc(alt)}" loading="lazy"{f" class=\"{cls}\"" if cls else ""}>'


def jsonld(lang):
    desc = HOME[lang]["desc"]
    return {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": "Tricolab",
        "operatingSystem": "iOS 17+", "applicationCategory": "LifestyleApplication",
        "url": f"{SITE}/{lang}/", "description": desc, "inLanguage": ["fr", "en"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"},
        "sameAs": [APPSTORE_BASE], "installUrl": APPSTORE[lang],
        "publisher": {"@type": "Organization", "name": "JDG inc.",
                      "address": {"@type": "PostalAddress", "addressRegion": "Québec", "addressCountry": "CA"}},
    }


# ----------------------------------------------------------------- pages
def home(lang):
    h, h2, t = HOME[lang], HOME2[lang], T[lang]
    feats = "".join(f'<div class="card"><div class="emoji">{e}</div><h3>{a}</h3><p>{b}</p></div>' for e, a, b in h["features"])
    alts = {"fr": ["Accueil avec le projet en cours", "Compteur de rangs et patron surligné", "Vue 3D qui montre l'avancement du projet", "La collection Vêtements",
                   "Fiche d'un vêtement avec choix de taille et de couleurs", "Grille crop circle suivie par le compteur", "Générateur de motifs Chevalier", "Le Labo : techniques, matériel et calculateurs",
                   "Couverture de magazine de ton projet terminé", "Carte de fin de projet à partager"],
            "en": ["Home screen with the current project", "Row counter with the highlighted pattern", "3D view showing the project's progress", "The Clothing collection",
                   "Garment page with size and colour choices", "Crop circle chart followed by the counter", "Knight motif generator", "The Lab: techniques, materials and calculators",
                   "Magazine cover of your finished project", "Finished-project card to share"]}[lang]
    shots = "".join(shot(lang, k, a) for k, a in zip(["home", "counter", "three", "garments", "pattern", "grid", "gen", "lab", "magazine", "card"], alts))
    meta = "".join(f"<span><strong>{a}</strong> {b}</span>" for a, b in h2["meta"])
    body = f"""<section class="hero">
  <div class="container hero__grid">
    <div>
      <p class="eyebrow">{h2['eyebrow']}</p>
      <h1>{h['tagline']}</h1>
      <p class="lead">{h['lead']}</p>
      <div class="hero__actions">{store_button(lang)}<a href="{FILES['features'][lang]}" class="btn btn--outline">{h2['more']}</a></div>
      <div class="hero__meta">{meta}</div>
    </div>
    <div class="hero__visual">
      <img class="logo" src="../assets/img/logo-large.jpg" alt="Tricolab" width="420" height="420">
    </div>
  </div>
</section>

<div class="container"><hr class="stitch"></div>

<section>
  <div class="container">
    <div class="card card--news">
      <span class="badge-new">{h2['news_badge']}</span>
      <h2>{h2['news_h']}</h2>
      <ul>{"".join(f"<li>{x}</li>" for x in h2['news'])}</ul>
      <p class="news-status">{h2['news_status']}</p>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head"><h2>{h['h_features']}</h2></div>
    <div class="grid-3">{feats}</div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head"><h2>{h['h_shots']}</h2></div>
    <div class="shots">{shots}</div>
  </div>
</section>

<section>
  <div class="container grid-2">
    <div class="card"><div class="emoji">🎁</div><h3>{h2['h_free']}</h3><p>{h2['free']}</p></div>
    <div class="card"><div class="emoji">🔒</div><h3>{h['h_privacy']}</h3><p>{h['privacy'].replace('privacy-en.html', FILES['privacy']['en']).replace('href="confidentialite.html"', 'href="' + FILES['privacy']['fr'] + '"')}</p></div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-band">
      <h2>{h2['cta_h']}</h2>
      <p>{h2['cta_p']}</p>
      {store_button(lang)}
    </div>
  </div>
</section>"""
    return page(lang, "home", h2["title"], h["desc"], body, jsonld=jsonld(lang))


def features(lang):
    f = FEATURES[lang]
    blocks = ""
    for key, title, lead, bullets in f["blocks"]:
        li = "".join(f"<li>{b}</li>" for b in bullets)
        blocks += f"""<div class="feature">
  <div class="feature__text"><h2>{title}</h2><p>{lead}</p><ul>{li}</ul></div>
  <div class="feature__img">{shot(lang, key, title)}</div>
</div>
"""
    c0, c1, c2 = f["cmp_cols"]
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in f["cmp_rows"])
    body = f"""<div class="container page-head"><p class="eyebrow">Tricolab</p><h1>{f['h1']}</h1><p>{f['intro']}</p></div>
<section><div class="container">
{blocks}
</div></section>
<section><div class="container">
  <div class="section-head"><h2>{f['h_cmp']}</h2></div>
  <table class="compare"><thead><tr><th>{c0}</th><th>{c1}</th><th>{c2}</th></tr></thead><tbody>{rows}</tbody></table>
  <p style="text-align:center;color:var(--ink-soft);margin-top:14px">{f['cmp_note']}</p>
</div></section>
<section><div class="container"><div class="cta-band"><h2>{HOME2[lang]['cta_h']}</h2><p>{HOME2[lang]['cta_p']}</p>{store_button(lang)}</div></div></section>"""
    return page(lang, "features", f["title"], f["desc"], body)


def download(lang):
    d = DOWNLOAD[lang]
    faq = "".join(f'<div class="card"><h3>{q}</h3><p>{a}</p></div>' for q, a in d["faq"])
    body = f"""<div class="container page-head"><p class="eyebrow">Tricolab</p><h1>{d['h1']}</h1><p>{d['intro']}</p></div>
<section><div class="container">
  <div class="card" style="text-align:center;padding:34px 22px">
    <img src="../assets/img/logo-mark.png" alt="" width="96" height="96" style="margin:0 auto 14px;border-radius:24px;box-shadow:0 10px 24px rgba(225,100,135,.35)">
    <h3 style="font-size:1.3rem">{d['status_h']}</h3>
    <p style="margin:8px auto 18px;max-width:520px">{d['status']}</p>
    {store_button(lang)}
  </div>
</div></section>
<section><div class="container">
  <div class="section-head"><h2>{d['faq_h']}</h2></div>
  <div class="grid-2">{faq}</div>
</div></section>"""
    return page(lang, "download", d["title"], d["desc"], body)


def contact(lang, depth=1):
    s, c = SUPPORT[lang], CONTACT_EXTRA[lang]
    faq = "".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in s["faq"])
    body = f"""<div class="container page-head"><p class="eyebrow">Tricolab</p><h1>{c['h1']}</h1><p>{s['intro']}</p></div>
<section><div class="container">
  <article class="doc contact-card"><h2>{c['mail_h']}</h2>
    <p class="mail"><a href="mailto:{EMAIL}?subject=Tricolab">{EMAIL}</a></p>
    <p>{c['mail_p']}</p><p>{c['biz']}</p></article>
  <div class="section-head" style="margin-top:34px"><h2>{s['h_faq']}</h2></div>
  <article class="doc">{faq}</article>
</div></section>"""
    return page(lang, "contact", c["title"], c["desc"], body, depth=depth)


def privacy(lang, depth=1):
    p = PRIVACY[lang]
    sections = "".join(f"<h2>{t}</h2><p>{c}</p>" for t, c in p["sections"])
    label = "En vigueur le" if lang == "fr" else "Effective"
    body = f"""<div class="container page-head"><p class="eyebrow">Tricolab</p><h1>{p['h1']}</h1><p>{label} {EFFECTIVE[lang]}</p></div>
<section><div class="container">
  <div class="callout">{p['note']}</div>
  <article class="doc">{sections}</article>
</div></section>"""
    return page(lang, "privacy", p["title"], p["desc"], body, depth=depth)


def redirect(dest, auto=True):
    script = """<script>
  (function () {
    var lang = (navigator.language || "fr").toLowerCase();
    window.location.replace(lang.indexOf("fr") === 0 ? "fr/index.html" : "en/index.html");
  })();
</script>
""" if auto else ""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={dest}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tricolab</title>
<link rel="canonical" href="{SITE}/{dest}">
{script}</head>
<body><p><a href="fr/index.html">Français</a> — <a href="en/index.html">English</a></p></body>
</html>
"""


def sitemap():
    urls = []
    for key in NAV_ORDER + ["privacy"]:
        for lang in ("fr", "en"):
            path = lambda l: f"{SITE}/{l}/{'' if key == 'home' else FILES[key][l]}"
            prio = "1.0" if key == "home" else ("0.8" if key in ("features", "download") else "0.5")
            freq = "weekly" if key == "home" else "monthly"
            urls.append(f"""  <url>
    <loc>{path(lang)}</loc>
    <xhtml:link rel="alternate" hreflang="fr" href="{path('fr')}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{path('en')}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{path('fr')}"/>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n\n' + "\n\n".join(urls) + "\n</urlset>\n")


def build():
    for lang in ("fr", "en"):
        d = ROOT / lang
        d.mkdir(exist_ok=True)
        (d / FILES["home"][lang]).write_text(home(lang), encoding="utf-8")
        (d / FILES["features"][lang]).write_text(features(lang), encoding="utf-8")
        (d / FILES["download"][lang]).write_text(download(lang), encoding="utf-8")
        (d / FILES["contact"][lang]).write_text(contact(lang), encoding="utf-8")
        (d / FILES["privacy"][lang]).write_text(privacy(lang), encoding="utf-8")
    for name, lang, key in LEGACY:
        html = contact(lang, depth=0) if key == "contact" else privacy(lang, depth=0)
        (ROOT / name).write_text(html, encoding="utf-8")
    (ROOT / "index.html").write_text(redirect("fr/index.html"), encoding="utf-8")
    (ROOT / "en.html").write_text(redirect("en/index.html", auto=False).replace('lang="fr"', 'lang="en"', 1), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("Site généré (fr/, en/, anciennes adresses, sitemap, robots).")


if __name__ == "__main__":
    build()
