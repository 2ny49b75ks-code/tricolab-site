#!/usr/bin/env python3
"""Génère le site Tricolab (FR + EN) : accueil, assistance, confidentialité.
Lancer `python3 build.py` après toute modification du contenu ci-dessous."""
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "jdgeg@icloud.com"
EFFECTIVE = {"fr": "1er octobre 2026", "en": "October 1, 2026"}

# Pages : (fichier FR, fichier EN)
FILES = {"home": ("index.html", "en.html"), "support": ("support.html", "support-en.html"), "privacy": ("privacy.html", "privacy-en.html")}

CSS = """
:root{--pink:#E16487;--pink-deep:#BE4368;--pink-soft:#FAE0E7;--teal:#28958C;--teal-deep:#166B65;--teal-soft:#D7EFEC;
--cream:#EAE0C8;--paper:#FBF7F1;--ink:#3A2E2A;--ink-soft:#6f6460;--card:#ffffff}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:ui-rounded,"SF Pro Rounded",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.55;
background-image:repeating-linear-gradient(60deg,rgba(234,224,200,.45) 0 3px,transparent 3px 14px),repeating-linear-gradient(-60deg,rgba(234,224,200,.45) 0 3px,transparent 3px 14px)}
a{color:var(--teal-deep)}
.wrap{max-width:960px;margin:0 auto;padding:0 16px}
header.top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--pink-deep);font-weight:800;font-size:1.35rem}
.brand img{width:44px;height:44px;border-radius:11px;object-fit:cover}
nav{display:flex;align-items:center;gap:14px;flex-wrap:wrap;font-weight:600;font-size:.95rem}
nav a{text-decoration:none}
.lang{display:inline-flex;background:#fff;border:1px solid var(--cream);border-radius:999px;padding:2px}
.lang a,.lang span{padding:3px 11px;border-radius:999px;font-weight:800;font-size:.8rem;text-decoration:none;color:var(--ink-soft)}
.lang span{background:var(--teal);color:#fff}
.hero{text-align:center;padding:28px 0 8px}
.hero img.logo{width:190px;height:190px;border-radius:42px;object-fit:cover;box-shadow:0 14px 34px rgba(225,100,135,.35)}
h1{font-size:clamp(2rem,6vw,3rem);margin:.5em 0 .1em;color:var(--pink-deep);font-weight:800;text-wrap:balance}
.tagline{font-size:1.2rem;font-weight:700;color:var(--teal-deep);margin:0}
.lead{max-width:640px;margin:14px auto 0;font-size:1.05rem;color:var(--ink-soft)}
.soon{display:inline-block;margin-top:18px;background:var(--pink);color:#fff;font-weight:800;padding:12px 22px;border-radius:16px}
h2{font-size:1.5rem;margin:1.8em 0 .6em;font-weight:800;text-wrap:balance}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.card{background:var(--card);border-radius:20px;padding:18px;box-shadow:0 4px 14px rgba(58,46,42,.07)}
.card h3{margin:.1em 0 .3em;font-size:1.08rem}
.card p{margin:0;color:var(--ink-soft);font-size:.97rem}
.card .emoji{font-size:1.7rem}
.shots{display:flex;gap:14px;overflow-x:auto;padding:6px 2px 16px;scroll-snap-type:x mandatory}
.shots img{height:440px;width:auto;border-radius:26px;box-shadow:0 6px 18px rgba(58,46,42,.16);scroll-snap-align:center;flex:none}
article{background:var(--card);border-radius:22px;padding:22px;box-shadow:0 4px 14px rgba(58,46,42,.07);margin:18px 0}
article h2{margin-top:1.2em;font-size:1.2rem}
article h2:first-child{margin-top:0}
.note{background:var(--teal-soft);border-radius:14px;padding:12px 14px;color:var(--teal-deep);font-weight:600}
footer{margin:36px 0 28px;text-align:center;color:var(--ink-soft);font-size:.9rem}
footer a{margin:0 8px}
@media (max-width:520px){.shots img{height:360px}.hero img.logo{width:150px;height:150px;border-radius:34px}}
"""

T = {
    "fr": {
        "nav": {"home": "Accueil", "support": "Assistance", "privacy": "Confidentialité"},
        "footer": "© 2026 JDG inc., Québec. Tous droits réservés.",
    },
    "en": {
        "nav": {"home": "Home", "support": "Support", "privacy": "Privacy"},
        "footer": "© 2026 JDG inc., Québec. All rights reserved.",
    },
}


def page(lang, key, title, description, body):
    other = "en" if lang == "fr" else "fr"
    idx = 0 if lang == "fr" else 1
    oidx = 1 - idx
    nav = "".join(f'<a href="{FILES[k][idx]}">{T[lang]["nav"][k]}</a>' for k in ("home", "support", "privacy"))
    switch = (f'<span>FR</span><a href="{FILES[key][oidx]}" lang="en" hreflang="en">EN</a>' if lang == "fr"
              else f'<a href="{FILES[key][oidx]}" lang="fr" hreflang="fr">FR</a><span>EN</span>')
    foot = "".join(f'<a href="{FILES[k][idx]}">{T[lang]["nav"][k]}</a>' for k in ("home", "support", "privacy"))
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="alternate" hreflang="{other}" href="{FILES[key][oidx]}">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="icon" href="assets/apple-touch-icon.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="assets/logo.jpg">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <a class="brand" href="{FILES['home'][idx]}"><img src="assets/logo.jpg" alt="">Tricolab</a>
  <nav>{nav}<span class="lang">{switch}</span></nav>
</header>
{body}
<footer><div>{foot}</div><p>{T[lang]['footer']}</p></footer>
</div>
</body>
</html>
"""


def cards(items):
    return '<div class="grid">' + "".join(
        f'<div class="card"><div class="emoji">{e}</div><h3>{h}</h3><p>{p}</p></div>' for e, h, p in items) + "</div>"


def shots(lang, alts):
    names = ["01-accueil", "02-compteur-patron", "03-grille-crop-circle", "04-fiche-patron", "05-generateur-motifs", "08-carte-a-partager"]
    return '<div class="shots">' + "".join(
        f'<img src="assets/{lang}-{n}.jpg" alt="{a}" loading="lazy">' for n, a in zip(names, alts)) + "</div>"


HOME = {
    "fr": dict(
        title="Tricolab — compteur de rangs, patrons et motifs pour le tricot et le crochet",
        desc="Tricolab : compteur de rangs mains libres, patrons originaux qui suivent ta ligne et générateur de motifs crop circle. Pour iPhone et iPad.",
        tagline="Le labo de tes créations",
        lead="Un compteur de rangs pensé pour les mains occupées, des patrons qui ne perdent jamais ta place et des motifs que tu ne trouveras nulle part ailleurs. Tricot et crochet, en français et en anglais.",
        soon="Bientôt sur l'App Store · iPhone et iPad",
        h_features="Ce que fait Tricolab",
        features=[
            ("🧶", "Compteur mains libres", "Un très gros bouton +, l'écran qui reste allumé, et la voix : dis « suivant » ou « retour » sans lâcher tes aiguilles."),
            ("📖", "Un patron qui suit ta ligne", "Importe un PDF, photographie un patron papier ou colle son texte. La ligne en cours est surlignée et les abréviations sont traduites en clair."),
            ("🧢", "30 patrons originaux", "Cinq styles : Classique, Moderne, Rustique, Émoticône et Crop circle. Dessin de l'objet fini, schéma coté et tailles qui recalculent les instructions."),
            ("🛸", "Générateur de motifs", "20 motifs en grille — crop circle, pêche, construction, feuilles — à ta taille et à tes couleurs, avec les rangs écrits automatiquement."),
            ("🧪", "Le Labo", "Techniques pas à pas, matériel, exemples de schémas, dictionnaire d'abréviations et calculateurs de jauge, de taille et de laine."),
            ("🎀", "Partage et motivation", "Une carte de fin de projet à partager, un défi par mois, des badges et ton bilan annuel."),
        ],
        h_shots="Aperçu",
        alts=["Écran d'accueil avec le projet en cours", "Compteur de rangs et patron surligné", "Grille crop circle suivie par le compteur",
              "Fiche d'un patron avec le dessin de l'objet fini", "Générateur de motifs", "Carte de fin de projet à partager"],
        h_privacy="Tes données restent chez toi",
        privacy='Aucun compte, aucune publicité, aucun traceur. Tes projets, photos et patrons restent sur ton appareil. <a href="privacy.html">Lire la politique de confidentialité</a>.',
    ),
    "en": dict(
        title="Tricolab — row counter, patterns and motifs for knitting and crochet",
        desc="Tricolab: hands-free row counter, original patterns that keep your place and a crop circle motif generator. For iPhone and iPad.",
        tagline="The lab for your creations",
        lead="A row counter built for busy hands, patterns that never lose your place and motifs you won't find anywhere else. Knitting and crochet, in English and French.",
        soon="Coming soon to the App Store · iPhone and iPad",
        h_features="What Tricolab does",
        features=[
            ("🧶", "Hands-free counter", "One very big + button, a screen that stays on, and your voice: say \"next\" or \"back\" without putting your needles down."),
            ("📖", "A pattern that keeps your place", "Import a PDF, photograph a paper pattern or paste its text. Your current line is highlighted and abbreviations are explained in plain words."),
            ("🧢", "30 original patterns", "Five styles: Classic, Modern, Rustic, Emoticon and Crop circle. A drawing of the finished item, a measured schematic and sizes that recalculate the instructions."),
            ("🛸", "Motif generator", "20 chart motifs — crop circles, fishing, construction, leaves — in your size and colours, with the rows written out automatically."),
            ("🧪", "The Lab", "Step-by-step techniques, materials, chart examples, an abbreviation dictionary and calculators for gauge, sizing and yarn."),
            ("🎀", "Share and stay motivated", "A finished-project card to share, a monthly challenge, badges and your year in review."),
        ],
        h_shots="Preview",
        alts=["Home screen with the current project", "Row counter with the highlighted pattern", "Crop circle chart followed by the counter",
              "Pattern page with a drawing of the finished item", "Motif generator", "Finished-project card to share"],
        h_privacy="Your data stays with you",
        privacy='No account, no ads, no trackers. Your projects, photos and patterns stay on your device. <a href="privacy-en.html">Read the privacy policy</a>.',
    ),
}

SUPPORT = {
    "fr": dict(
        title="Assistance — Tricolab", desc="Aide, questions fréquentes et contact pour l'app Tricolab.",
        h1="Assistance",
        intro=f'Une question, un bogue à signaler ou une idée de patron ? Écris-nous : chaque message est lu.',
        contact=f'Courriel : <a href="mailto:{EMAIL}?subject=Tricolab">{EMAIL}</a><br>Précise si possible ton modèle d\'iPhone ou d\'iPad et ta version d\'iOS.',
        h_faq="Questions fréquentes",
        faq=[
            ("Comment fonctionne le compteur mains libres ?", "Ouvre le Compteur, touche « Mains libres » et autorise le micro et la reconnaissance vocale. Dis ensuite « suivant » pour ajouter un rang ou « retour » pour en retirer un. La reconnaissance se fait sur ton appareil."),
            ("La commande vocale ne réagit pas. Que faire ?", "Vérifie dans Réglages → Tricolab que le micro et la reconnaissance vocale sont autorisés, et dans Réglages → Général → Clavier que la dictée est activée. Parle clairement, un mot à la fois."),
            ("Comment ajouter mon propre patron ?", "Dans la fiche d'un projet, touche « Ajouter un patron » : tu peux importer un PDF, photographier un patron papier ou coller son texte. Touche une ligne pour la suivre ; ta position est sauvegardée."),
            ("Le texte numérisé contient des erreurs.", "La numérisation peut confondre certains caractères (1 et l, 0 et O). Tu peux relire et corriger le texte avant de l'enregistrer. Une photo bien éclairée, à plat et nette donne les meilleurs résultats."),
            ("Comment choisir la taille d'un patron ?", "Pour les bonnets, tuques, mitaines, cache-cous et écharpes, la fiche du patron propose plusieurs tailles. Choisis la tienne : les nombres de mailles et les mesures se recalculent. Vérifie toujours ta jauge avec un échantillon."),
            ("Comment utiliser une grille de motif ?", "Dans Labo → Générateur de motifs, choisis un motif, sa taille, deux couleurs et la technique. L'app crée un projet : la grille surligne le rang à faire et les instructions avancent avec ton compteur."),
            ("Où sont enregistrées mes données ?", "Sur ton appareil seulement. Elles sont incluses dans la sauvegarde de ton iPhone ou iPad si tu l'as activée, ce qui permet de les retrouver en changeant d'appareil. Supprimer l'app efface ses données."),
            ("L'app est-elle offerte en anglais ?", "Oui. Les boutons FR / EN en haut de l'écran changent la langue à tout moment, et chaque patron existe dans les deux langues."),
            ("L'app existe-t-elle sur Android ?", "Pas pour l'instant. Tricolab fonctionne sur iPhone et iPad (iOS 17 ou plus récent)."),
        ],
    ),
    "en": dict(
        title="Support — Tricolab", desc="Help, frequently asked questions and contact for the Tricolab app.",
        h1="Support",
        intro="A question, a bug to report or a pattern idea? Write to us: every message is read.",
        contact=f'Email: <a href="mailto:{EMAIL}?subject=Tricolab">{EMAIL}</a><br>If you can, tell us your iPhone or iPad model and your iOS version.',
        h_faq="Frequently asked questions",
        faq=[
            ("How does the hands-free counter work?", "Open the Counter, tap \"Hands-free\" and allow the microphone and speech recognition. Then say \"next\" to add a row or \"back\" to remove one. Recognition happens on your device."),
            ("Voice control doesn't react. What should I do?", "Check in Settings → Tricolab that the microphone and speech recognition are allowed, and in Settings → General → Keyboard that Dictation is enabled. Speak clearly, one word at a time."),
            ("How do I add my own pattern?", "On a project page, tap \"Add a pattern\": you can import a PDF, photograph a paper pattern or paste its text. Tap a line to follow it; your position is saved."),
            ("The digitized text has mistakes.", "Digitizing can confuse some characters (1 and l, 0 and O). You can proofread and fix the text before saving. A sharp, well-lit, flat photo gives the best results."),
            ("How do I choose a pattern size?", "For hats, mitts, cowls and scarves, the pattern page offers several sizes. Pick yours: stitch counts and measurements recalculate. Always check your gauge with a swatch."),
            ("How do I use a motif chart?", "In Lab → Motif generator, choose a motif, its size, two colours and the technique. The app creates a project: the chart highlights the row to work and the instructions advance with your counter."),
            ("Where is my data stored?", "On your device only. It is included in your iPhone or iPad backup if you have one enabled, so you can get it back when you change devices. Deleting the app erases its data."),
            ("Is the app available in French?", "Yes. The FR / EN buttons at the top of the screen switch language at any time, and every pattern exists in both languages."),
            ("Is there an Android version?", "Not at the moment. Tricolab runs on iPhone and iPad (iOS 17 or later)."),
        ],
    ),
}

PRIVACY = {
    "fr": dict(
        title="Politique de confidentialité — Tricolab", desc="Tricolab ne collecte aucune donnée personnelle : tout reste sur ton appareil.",
        h1="Politique de confidentialité",
        note="En bref : Tricolab ne collecte, ne transmet et ne vend aucune donnée personnelle. Tout ce que tu crées reste sur ton appareil.",
        sections=[
            ("Qui sommes-nous", f"Tricolab est une application éditée par JDG inc., au Québec (Canada). Pour toute question sur cette politique : <a href=\"mailto:{EMAIL}?subject=Tricolab%20-%20Confidentialit%C3%A9\">{EMAIL}</a>."),
            ("Les données que nous collectons", "Aucune. L'app n'a pas de compte utilisateur, pas de serveur, pas de publicité, pas d'outil de mesure d'audience ni de traceur, et n'intègre aucun service tiers."),
            ("Ce qui est enregistré sur ton appareil", "Tes projets, photos, patrons importés ou numérisés, notes, matériel, inventaire de laine, compteurs, temps passé et réglages sont enregistrés uniquement dans l'espace de l'app, sur ton iPhone ou ton iPad. Nous n'y avons pas accès."),
            ("Sauvegardes", "Si tu as activé la sauvegarde de ton appareil (iCloud ou ordinateur), les données de l'app en font partie. Ces sauvegardes sont gérées par Apple selon sa propre politique de confidentialité."),
            ("Caméra", "La caméra sert uniquement à photographier tes créations et tes patrons papier, quand tu le demandes. Les photos restent sur ton appareil. La lecture du texte d'un patron (numérisation) se fait sur l'appareil."),
            ("Micro et reconnaissance vocale", "Le micro n'est utilisé que lorsque tu actives le mode « Mains libres » du compteur, pour reconnaître des mots comme « suivant » et « retour ». La reconnaissance se fait sur ton appareil : le son n'est ni enregistré, ni conservé, ni envoyé à un serveur. L'écoute s'arrête dès que tu désactives le mode ou que tu quittes le compteur."),
            ("Photos", "Pour ajouter une photo, l'app utilise le sélecteur de photos du système : elle ne reçoit que les images que tu choisis et n'a pas accès au reste de ta photothèque. Pour enregistrer une carte ou un badge, elle demande seulement la permission d'ajouter une image."),
            ("Partage", "Quand tu partages une carte, une grille ou un badge, c'est toi qui choisis l'app ou la personne destinataire. Ce contenu est alors soumis aux règles du service que tu as choisi."),
            ("Enfants", "Tricolab convient à tous les âges et ne collecte aucune donnée, y compris auprès des enfants."),
            ("Supprimer tes données", "Tu peux supprimer un projet à tout moment dans l'app. Supprimer l'app efface toutes ses données de l'appareil."),
            ("Modifications", "Si cette politique change, la nouvelle version sera publiée sur cette page avec sa date d'entrée en vigueur."),
        ],
    ),
    "en": dict(
        title="Privacy Policy — Tricolab", desc="Tricolab collects no personal data: everything stays on your device.",
        h1="Privacy Policy",
        note="In short: Tricolab does not collect, transmit or sell any personal data. Everything you create stays on your device.",
        sections=[
            ("Who we are", f"Tricolab is an app published by JDG inc., in Québec (Canada). For any question about this policy: <a href=\"mailto:{EMAIL}?subject=Tricolab%20-%20Privacy\">{EMAIL}</a>."),
            ("Data we collect", "None. The app has no user account, no server, no advertising, no analytics and no trackers, and includes no third-party services."),
            ("What is stored on your device", "Your projects, photos, imported or digitized patterns, notes, materials, yarn stash, counters, time spent and settings are stored only in the app's own space on your iPhone or iPad. We have no access to them."),
            ("Backups", "If you have turned on device backups (iCloud or computer), the app's data is part of them. Those backups are handled by Apple under its own privacy policy."),
            ("Camera", "The camera is used only to photograph your creations and paper patterns, when you ask for it. Photos stay on your device. Reading a pattern's text (digitizing) happens on the device."),
            ("Microphone and speech recognition", "The microphone is used only when you turn on the counter's \"Hands-free\" mode, to recognize words such as \"next\" and \"back\". Recognition happens on your device: audio is not recorded, stored or sent to a server. Listening stops as soon as you turn the mode off or leave the counter."),
            ("Photos", "To add a photo, the app uses the system photo picker: it receives only the images you choose and has no access to the rest of your library. To save a card or a badge, it asks only for permission to add an image."),
            ("Sharing", "When you share a card, a chart or a badge, you choose the app or person that receives it. That content is then subject to the rules of the service you chose."),
            ("Children", "Tricolab is suitable for all ages and collects no data, including from children."),
            ("Deleting your data", "You can delete a project at any time in the app. Deleting the app erases all of its data from the device."),
            ("Changes", "If this policy changes, the new version will be published on this page with its effective date."),
        ],
    ),
}


def build():
    for lang in ("fr", "en"):
        idx = 0 if lang == "fr" else 1
        h = HOME[lang]
        body = f"""<section class="hero">
  <img class="logo" src="assets/logo.jpg" alt="Tricolab" width="190" height="190">
  <h1>Tricolab</h1>
  <p class="tagline">{h['tagline']}</p>
  <p class="lead">{h['lead']}</p>
  <div class="soon">{h['soon']}</div>
</section>
<h2>{h['h_features']}</h2>
{cards(h['features'])}
<h2>{h['h_shots']}</h2>
{shots(lang, h['alts'])}
<h2>{h['h_privacy']}</h2>
<p class="note">{h['privacy']}</p>"""
        (ROOT / FILES["home"][idx]).write_text(page(lang, "home", h["title"], h["desc"], body), encoding="utf-8")

        s = SUPPORT[lang]
        faq = "".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in s["faq"])
        body = f"""<h1>{s['h1']}</h1>
<article><p>{s['intro']}</p><p class="note">{s['contact']}</p></article>
<h2>{s['h_faq']}</h2>
<article>{faq}</article>"""
        (ROOT / FILES["support"][idx]).write_text(page(lang, "support", s["title"], s["desc"], body), encoding="utf-8")

        p = PRIVACY[lang]
        sections = "".join(f"<h2>{t}</h2><p>{c}</p>" for t, c in p["sections"])
        label = "En vigueur le" if lang == "fr" else "Effective"
        body = f"""<h1>{p['h1']}</h1>
<p>{label} {EFFECTIVE[lang]}</p>
<p class="note">{p['note']}</p>
<article>{sections}</article>"""
        (ROOT / FILES["privacy"][idx]).write_text(page(lang, "privacy", p["title"], p["desc"], body), encoding="utf-8")
    print("Site généré :", ", ".join(f for pair in FILES.values() for f in pair))


if __name__ == "__main__":
    build()
