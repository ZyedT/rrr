# Fiche Play Store AppForge — mise à niveau (octobre 2026)

> App : **AppForge** · package `com.tipro` · éditeur « BlueWave Apps. »
> Analyse faite le 07/10/2026 à partir de la fiche publique (versions FR/Tunisie et EN/États-Unis) et de vos documents Drive (fiches de juin, captures de septembre, notes de projet).
> Tout ce qui suit est prêt à coller dans la Play Console. Les visuels sont dans `assets/`, les outils pour les refaire dans `outils/`.

---

## 0. En une minute

**Pourquoi personne n'arrive sur la fiche (référencement).**

| Constat | Effet |
|---|---|
| Titre « AppForge » : 8 caractères sur 30, aucun mot-clé | Le titre est le premier critère de la recherche Play. Personne ne tape « AppForge ». |
| Le nom n'est pas unique : « AppForge - AI app builder » et « AppForge - Build Web2app » existent déjà | Sur la requête « AppForge », ces deux apps sortent avant la vôtre. |
| Description courte sans requête réelle (« Décrivez l'application que vous voulez, recevez-la prête à installer ») | Aucun des mots que les gens tapent : *créer une application, sans coder, IA, app builder*. |
| Catégorie « Professionnel » (Business) | Tous les concurrents sont en Productivité ou Outils. Vous n'apparaissez pas dans les bonnes listes « Applications similaires ». |
| 50+ installations, aucune note affichée, pas de vidéo | Play ne pousse pas une fiche sans signaux d'intérêt. |
| Aucune source de trafic hors Play | Pas de lien vers la fiche dans les apps livrées, pas de page web, pas de partage. |

**Pourquoi ceux qui arrivent n'installent pas (conversion).**

| Constat | Effet |
|---|---|
| 15 captures d'écran, dont **4 en double exact** et **8 de l'ancien design** de juin (« Ton APK est prêt », « 10 crédits », solde « 20 ») | Incohérent avec le design de septembre et avec la grille actuelle. Ça fait brouillon. |
| La première phrase visible présente le produit, pas le bénéfice ; l'offre de bienvenue n'apparaît nulle part | Le visiteur ne voit pas de raison d'essayer tout de suite. |
| « Crédits offerts et rechargés par l'administrateur » | Incompréhensible pour un inconnu : quel administrateur ? Comment en avoir ? |
| Icône : étincelle générique sur fond indigo | Identique à des dizaines d'apps « IA ». Rien ne dit « on fabrique votre app ». |
| Sécurité des données : « Aucune donnée collectée » | Faux (compte e-mail, texte des demandes, pièces jointes). Visible par tous, et motif de retrait par Google. |
| Notes de version : « Amélioration de l'interface » | Espace gaspillé sous « Nouveautés ». |

**Ce que contient ce dossier**

- Section 1 : la stratégie de référencement (mots-clés, titre, catégorie, langues).
- Sections 2 à 4 : les textes FR, EN et AR (optionnel), avec le nombre de caractères.
- Section 5 : les 8 captures d'écran FR dans l'ordre final (fichiers fournis) + 2 captures EN.
- Section 6 : image de présentation FR/EN et deux icônes candidates (fichiers fournis).
- Section 7 : les réglages Console à corriger (catégorie, sécurité des données, nom d'éditeur, avis, A/B).
- Section 8 : faire venir du monde en dehors de la recherche Play.
- Section 9 : le pas-à-pas dans la Console, dans l'ordre.

---

## 1. Référencement (ASO) — la stratégie

**Comment la recherche Play classe une fiche, par ordre d'importance :** le titre, la description courte, la description longue (et le texte des avis), la catégorie, puis les signaux d'usage (installations récentes, notes, désinstallations). Chaque langue de fiche est indexée séparément : une fiche FR ne fait pas remonter les requêtes EN, d'où une fiche par langue.

**Requêtes visées (ce que les gens tapent vraiment)**

| Français | Anglais |
|---|---|
| créer une application, créer une app | ai app builder, build apps with ai |
| créateur d'application, générateur d'application | no code app builder, app maker |
| application sans code, no code, sans coder | create android app, make an app without coding |
| créer une application android | app generator, custom app |
| intelligence artificielle, IA | vibe coding |
| créer un jeu, application mobile | build a game |

**Ce que font les concurrents (titres réels, octobre 2026)**

| App | Titre | Téléchargements |
|---|---|---|
| Base44 | « Base44: Build Apps with AI » | 500 k+ |
| Lovable | « Lovable: Build Apps With AI » | 500 k+ |
| Snapp AI | « Snapp AI : Créateur d'apps » | 10 k+ |
| App Maker | « App Maker: No Code App Builder » | 50 k+ |
| Lingguang | « Lingguang: AI App Builder » (livre aussi un APK) | 5 k+ |
| AppForge (vous) | « AppForge » | 50+ |

Le schéma qui marche : **Marque + deux-points + 3 ou 4 mots-clés**. On garde le nom AppForge et on lui accroche la requête principale.

**Avant / après**

| Champ | Avant | Après (FR) | Pourquoi |
|---|---|---|---|
| Titre (30) | AppForge | **AppForge : Créateur d'app IA** (28) | « créateur d'app » + « IA » = les deux requêtes les plus fortes en français |
| Description courte (80) | Décrivez l'application que vous voulez, recevez-la prête à installer | **Décrivez votre idée : l'IA crée une vraie app Android pour vous, sans coder.** (76) | « app Android », « sans coder », « IA » ; bénéfice en une phrase |
| Catégorie | Professionnel | **Productivité** | Catégorie de Base44, Lovable, Snapp : vous entrez dans leurs « Applications similaires » |
| Première ligne de la description longue | « AppForge transforme votre idée… » | « Créez votre application Android sans coder : décrivez-la… » | Seules les 2-3 premières lignes sont visibles sans cliquer sur « Plus » |
| Langues de fiche | FR, EN | FR, EN, **AR (optionnel)** | Une fiche arabe indexe les requêtes arabes (Tunisie, Maghreb, Moyen-Orient) |

**Le nom « AppForge ».** Deux autres apps l'utilisent. Le suffixe de mots-clés règle le problème dans la recherche. Si un jour vous changez de nom, choisissez-en un sans homonyme sur Play ; pour l'instant ce n'est pas la priorité.

**Ce que le texte seul ne fera pas.** Un titre optimisé fait remonter la fiche sur des requêtes de niche en quelques semaines, pas sur « créer une application » où des apps à 500 k installations dominent. Les deux autres moteurs sont les notes (section 7) et le trafic que vous amenez vous-même (section 8). Les trois ensemble, c'est ce qui fait décoller une fiche à 50 installations.

---

## 2. Textes français (fiche principale)

### Titre (28/30)

```
AppForge : Créateur d'app IA
```

### Description courte (76/80)

```
Décrivez votre idée : l'IA crée une vraie app Android pour vous, sans coder.
```

Variantes si vous préférez (à tester en A/B, section 7) :

- `Créez votre app Android sans coder : décrivez-la, l'IA la fabrique pour vous.` (77)
- `Une vraie app Android sur mesure, sans coder : décrivez, confirmez, installez.` (78)

### Description longue (2 801/4 000)

```
Créez votre application Android sans coder : décrivez-la en quelques phrases, AppForge la conçoit, la fabrique, la teste et vous la livre, prête à installer sur votre téléphone.

Vous ne construisez rien vous-même. Vous commandez votre application comme vous enverriez un message, et vous recevez une vraie application Android, sur mesure, pour votre usage personnel ou professionnel.

VOTRE PREMIÈRE APPLICATION EST OFFERTE
Des crédits de bienvenue vous sont offerts à l'inscription : assez pour une première application simple ou standard, sans rien payer. Le prix de chaque demande est annoncé avant de lancer, et rien n'est déduit si vous refusez.

COMMENT ÇA MARCHE
1. Décrivez l'application que vous voulez, avec vos propres mots (texte ou voix, avec des images si vous le souhaitez).
2. AppForge analyse votre demande et vous présente ce qui sera réalisé, avec un prix fixe en crédits.
3. Vous confirmez. L'application est fabriquée, puis vérifiée par des tests automatiques.
4. Elle arrive dans la discussion avec un bouton d'installation. Besoin d'un changement ? Demandez-le dans le même fil : une nouvelle version est produite.

CE QUE VOUS POUVEZ COMMANDER
• Des outils du quotidien : calculatrices, convertisseurs, minuteurs, listes, blocs-notes, suivis et compteurs.
• Des applications métier : gestion de chantier avec planning Gantt, plans annotés et rapports signés ; visites immobilières ; réservations ; inventaire ; quiz et formation.
• Des jeux, y compris des jeux 3D.
• Des applications en français, en anglais ou en arabe, qui fonctionnent hors ligne.

POURQUOI APPFORGE
• Aucune compétence technique : tout se passe en langage naturel.
• Un prix connu avant de commencer, jamais de surprise.
• Chaque application est testée automatiquement avant la livraison.
• Un design professionnel, adapté à votre activité.
• L'historique de vos projets, de vos conversations et de chaque version, toujours accessible.
• Vos données vous appartiennent : suppression de compte en un geste, à tout moment.

POUR QUI
Indépendants, artisans, commerçants, petites entreprises, enseignants, étudiants, associations, et tous ceux qui ont une idée d'application sans vouloir apprendre à programmer.

CRÉDITS
Le service fonctionne avec des crédits. Des crédits de bienvenue sont offerts à l'inscription ; pour en obtenir davantage, contactez-nous depuis l'application (WhatsApp ou e-mail). Les crédits ne sont pas vendus dans l'application.

BON À SAVOIR
L'application livrée est un fichier que vous installez sur votre appareil, pour votre usage personnel. Le nombre de crédits dépend de la complexité de la demande ; la fabrication prend de quelques dizaines de minutes à quelques heures.

Une question, une demande de crédits ou de suppression de compte ? Écrivez-nous à blue1wave.apps@gmail.com
```

Points de vigilance sur ce texte :

- « Votre première application est offerte » repose sur les crédits de bienvenue (100 crédits = 2 apps simples ou 1 standard, décision du 15/09). Si ce nombre change, mettez la fiche à jour le même jour.
- Aucun prix en dinars ni en euros, aucun nombre de crédits : conforme à votre contrainte « aucun prix dans les textes ». La phrase « Les crédits ne sont pas vendus dans l'application » reste, c'est elle qui vous couvre vis-à-vis de la politique de paiement de Play.
- Pas de mot « APK » dans le titre ni la description courte. La livraison d'un fichier à installer reste dite dans « Bon à savoir », comme aujourd'hui (la fiche actuelle a été acceptée avec cette formulation).

### Notes de version (394/500)

```
Nouveau dans cette version :
• Guide de démarrage au premier lancement : décrire, recevoir un devis, confirmer, installer.
• Demande de crédits en un geste, directement depuis l'application.
• Interface disponible en français et en anglais.
• Devis plus rapides, applications livrées avec tests automatiques et identité visuelle adaptée à votre activité.
Une question ? blue1wave.apps@gmail.com
```

---

## 3. Textes anglais (fiche en-US)

### Titre (28/30)

```
AppForge: Build Apps with AI
```

### Description courte (76/80)

```
Describe your idea. AI designs, builds and tests a real Android app for you.
```

### Description longue (2 364/4 000)

```
Build your own Android app without coding: describe it in a few sentences, and AppForge designs it, builds it, tests it and delivers it to you, ready to install on your phone.

You don't build anything yourself. You order your app the way you would send a message, and you receive a real, custom Android app for your personal or professional use.

YOUR FIRST APP IS ON US
Welcome credits are granted when you sign up: enough for a first simple or standard app, at no cost. The price of every request is announced before anything starts, and nothing is deducted if you decline.

HOW IT WORKS
1. Describe the app you want in your own words (text or voice, with pictures if you like).
2. AppForge analyses your request and shows you what will be built, with a fixed price in credits.
3. You confirm. The app is built, then checked by automated tests.
4. It arrives in the chat with an install button. Need a change? Ask in the same thread and a new version is produced.

WHAT YOU CAN ORDER
• Everyday tools: calculators, converters, timers, checklists, notepads, trackers and counters.
• Business apps: construction site management with Gantt planning, annotated plans and signed reports; property visits; bookings; inventory; quizzes and training.
• Games, including 3D games.
• Apps in English, French or Arabic that work offline.

WHY APPFORGE
• No technical skills needed: everything happens in plain language.
• A price you know before you start, never a surprise.
• Every app is tested automatically before delivery.
• A professional design, tailored to your activity.
• The history of your projects, conversations and every version, always available.
• Your data is yours: delete your account in one tap, at any time.

WHO IT'S FOR
Freelancers, tradespeople, shop owners, small businesses, teachers, students, associations, and anyone with an app idea who doesn't want to learn to code.

CREDITS
The service runs on credits. Welcome credits are granted at sign-up; to get more, contact us from the app (WhatsApp or e-mail). Credits are not sold inside the app.

GOOD TO KNOW
Your app is delivered as a file you install on your device, for your personal use. The number of credits depends on the complexity of the request; building takes from a few dozen minutes to a few hours.

Questions, credit requests or account deletion? Write to blue1wave.apps@gmail.com
```

### Notes de version (335/500)

```
New in this version:
• Getting-started guide on first launch: describe, get a quote, confirm, install.
• Request credits in one tap, right from the app.
• Interface available in English and French.
• Faster quotes, apps delivered with automated tests and a visual identity tailored to your activity.
Questions? blue1wave.apps@gmail.com
```

---

## 4. Textes arabes (fiche « ar », optionnel)

À activer si vous voulez capter les requêtes en arabe (Tunisie, Maghreb, Moyen-Orient). L'interface d'AppForge est en FR/EN ; le texte le dit clairement pour éviter les mauvaises surprises. Les apps commandées, elles, peuvent être en arabe.

### Titre (27/30)

```
AppForge: تطبيقك بدون برمجة
```

### Description courte (78/80)

```
صِف فكرتك بكلماتك، والذكاء الاصطناعي يصنع لك تطبيق أندرويد حقيقيًا بدون برمجة.
```

### Description longue (1 201/4 000)

```
أنشئ تطبيق أندرويد خاصًا بك بدون برمجة: صِف ما تريده بجمل بسيطة، ويقوم AppForge بتصميمه وبنائه واختباره، ثم يسلّمه لك جاهزًا للتثبيت على هاتفك.

تطبيقك الأول هدية
عند التسجيل تحصل على رصيد ترحيبي يكفي لطلب تطبيقك الأول البسيط أو المتوسط. سعر كل طلب يُعلن قبل البدء، ولا يُخصم شيء إذا رفضت.

كيف يعمل
1. صِف التطبيق الذي تريده بكلماتك (نصًا أو صوتًا، مع صور إن شئت).
2. يحلّل AppForge طلبك ويعرض عليك ما سيُنجز، بسعر ثابت بالرصيد.
3. تؤكّد، فيُبنى التطبيق ويُفحص باختبارات آلية.
4. يصلك في المحادثة مع زر للتثبيت. تريد تعديلًا؟ اطلبه في نفس المحادثة.

ماذا يمكنك أن تطلب
• أدوات يومية: آلات حاسبة، محوّلات، مؤقّتات، قوائم، مفكرات.
• تطبيقات مهنية: إدارة مواقع البناء (مخطط غانت، مخططات مشروحة، تقارير موقّعة)، زيارات عقارية، حجوزات، مخزون، اختبارات تعليمية.
• ألعاب، بما فيها ألعاب ثلاثية الأبعاد.
• تطبيقات بالعربية أو الفرنسية أو الإنجليزية، تعمل بدون إنترنت.

ملاحظة: واجهة AppForge متوفّرة حاليًا بالفرنسية والإنجليزية، أما التطبيقات التي تطلبها فيمكن أن تكون بالعربية.

الرصيد
تعمل الخدمة بنظام رصيد. يُمنح رصيد ترحيبي عند التسجيل، وللحصول على المزيد تواصل معنا من داخل التطبيق (واتساب أو بريد إلكتروني). لا يُباع الرصيد داخل التطبيق.

للأسئلة أو طلب الرصيد أو حذف الحساب: blue1wave.apps@gmail.com
```

---

## 5. Captures d'écran

**Règle Play rappelée :** 2 à 8 captures « téléphone », ratio 16:9 ou 9:16, chaque côté entre 320 et 3 840 px, le grand côté ≤ 2 × le petit. Les fichiers fournis font 1 440 × 2 560 (9:16), comme vos captures de septembre.

**À supprimer de la fiche :** les 8 anciennes captures 1 080 × 1 920 de juin (fond uni, « Ton APK est prêt », « Un devis clair : 10 crédits », « Suis tes crédits : 20 », « Décris ton app »), dont 4 sont des doublons exacts. Elles montrent l'ancien design et des montants qui ne correspondent plus à la grille.

**Ordre final (fichiers dans `assets/screenshots-fr/`)** — les trois premières sont celles que Play montre dans les résultats de recherche, elles portent tout le message :

| # | Fichier | Légende | Origine |
|---|---|---|---|
| 1 | `01-hero.png` | Décrivez votre app. Recevez-la, prête à installer. / Conçue, fabriquée et testée pour vous. Sans coder. | **Nouvelle** : deux téléphones (demande + livraison) |
| 2 | `02-decrivez-prix-fixe.png` | Décrivez votre application / Un simple message. Le prix est fixé avant de lancer. | Capture actuelle conservée |
| 3 | `03-recevez-installez.png` | Recevez-la, prête à installer / L'APK testé arrive directement dans la discussion. | Capture actuelle conservée |
| 4 | `04-premiere-app-offerte.png` | Votre première app est offerte / Crédits de bienvenue à l'inscription. Prix fixe annoncé avant de lancer. | **Nouvelle** : écran « Mes projets » actuel avec nouvelle légende |
| 5 | `05-exemple-gantt.png` | Gantt et chemin critique | Capture actuelle conservée |
| 6 | `06-exemple-tableau-de-bord.png` | Le chantier d'un coup d'œil | Capture actuelle conservée |
| 7 | `07-exemple-plans.png` | Plans annotés sur le terrain | Capture actuelle conservée |
| 8 | `08-jeu-3d.png` | Même des jeux 3D / Décrit en une phrase, livré prêt à jouer. | **Nouvelle** : votre capture réelle de Ping Crépuscule, placée dans le même cadre S26 |

La capture « Suivez chaque projet en direct » (ancienne n° 2) n'est pas perdue : son écran sert de support à la n° 4. Le quatrième écran ChantierPro (rapport journalier signé) est conservé dans `extras/`, Play n'acceptant que 8 captures.

**Option : la galerie d'exemples (`09-galerie-exemples.png`, EN : `09-gallery-en.png`).** Une capture « Déjà fabriquées avec AppForge » avec les icônes réelles de ChantierPro, Bon Choix et Ping Crépuscule, extraites des applications livrées, et une carte « La vôtre ? ». Pour l'utiliser, remplacez la n° 7 (plans annotés, troisième écran ChantierPro) par celle-ci : elle montre la variété (gestion, conseiller d'achat, jeu 3D) mieux qu'un troisième écran du même exemple.

**Fiche anglaise (`assets/screenshots-en/`)** : `01-hero-en.png`, `04-first-app-free-en.png` et `08-3d-game-en.png` remplacent les n° 1, 4 et 8 (et `09-gallery-en.png` si vous prenez l'option galerie). Les autres gardent leurs légendes françaises (comme aujourd'hui). Pour une fiche EN entièrement anglaise, refaites les six captures avec la méthode de votre note du 13/09 (AVD « S26Ultra_Captures », écrans 13/14/15 de la galerie debug, locale en-US) : c'est un chantier d'une heure, à faire après la mise en ligne de cette version.

**Capture à ajouter plus tard (quand vous aurez l'écran)** — à la place de la n° 7 : une app livrée dans une autre langue (arabe), légende « En français, en anglais ou en arabe ».

**Pour refaire les nouvelles captures :** `python3 outils/make_screens.py` (le fond est resynthétisé à partir de vos captures actuelles, le téléphone est découpé dedans, les légendes sont en Inter Display).

---

## 6. Image de présentation et icône

### Image de présentation (feature graphic, 1 024 × 500)

Fichiers : `assets/feature-graphic/feature_fr_1024x500.png` et `feature_en_1024x500.png`.

L'actuelle (bannière « Décrivez ce que vous voulez. Recevez l'application. ») est propre mais ne montre pas le produit. La nouvelle garde la marque et le slogan, ajoute l'écran de livraison et la mention « Première application offerte ». Cette image apparaît en tête de fiche dès que vous ajoutez une vidéo (section 7) et dans les mises en avant éditoriales.

### Icône (512 × 512)

Deux candidates dans `assets/icon/` :

| Fichier | Idée | Avis |
|---|---|---|
| `icon_a_bulle_512.png` | Bulle de conversation blanche + étincelle indigo | **Recommandée.** Elle dit « vous décrivez, l'app apparaît », garde l'étincelle actuelle (continuité) et reste lisible à 48 px. |
| `icon_b_enclume_512.png` | Enclume + étincelles (la forge) | Plus littérale, moins lisible en petit. |

Ne changez pas l'icône à l'aveugle : passez par une **expérimentation de fiche** (section 7) icône actuelle contre icône A, et gardez celle qui convertit le mieux. L'icône dans l'app (`ic_launcher`) doit suivre le jour où vous basculez.

Sources modifiables : `outils/icon_a_bulle.html`, `outils/icon_b_enclume.html`, `outils/feature_fr.html`, `outils/feature_en.html` ; rendu avec `node outils/render.js`.

---

## 7. Réglages Console à corriger

1. **Catégorie** : Professionnel → **Productivité**. (Paramètres de la fiche > Catégorie.) Dans « Tags », choisissez les étiquettes les plus proches de *création d'applications / outils / intelligence artificielle* parmi celles proposées, 5 maximum.
2. **Sécurité des données** (Contenu de l'application > Sécurité des données) : remplacer « Aucune donnée collectée » par la réalité :
   - Infos personnelles → **Adresse e-mail** : collectée, obligatoire, finalité « Gestion du compte ».
   - Messages → **Autres messages intégrés à l'application** (vos demandes et la discussion) : collectés, obligatoires, finalité « Fonctionnalités de l'application ».
   - Photos et vidéos → **Photos** (pièces jointes) : collectées, facultatives, finalité « Fonctionnalités de l'application ».
   - Fichiers et documents : collectés, facultatifs, même finalité (si les pièces jointes peuvent être des fichiers).
   - Données chiffrées en transit : **Oui**. L'utilisateur peut demander la suppression : **Oui** (dans l'app).
   - Aucune donnée partagée avec des tiers : à garder si c'est vrai (pas de SDK publicitaire, pas d'analytics tiers).
   - Play exige aussi une **URL de suppression de compte** pour toute app avec création de compte : hébergez une page courte sur `schedview-748f3.web.app` (ex. `/delete-account`) qui explique le bouton de l'app et l'e-mail de contact, puis renseignez-la dans « Suppression de données et de compte ».
3. **Nom d'éditeur** : « BlueWave Apps. » → **« BlueWave Apps »** (sans le point final ; le point donne un air négligé sur chaque carte de résultat).
4. **Coordonnées** : gardez l'e-mail ; ajoutez un site web dès que la page de la section 8 existe.
5. **Vidéo de présentation** : une vidéo YouTube de 30 secondes (décrire → devis → confirmer → installer, filmée à l'écran) place un bouton « lecture » en tête de fiche et affiche l'image de présentation. C'est le seul élément manquant que les concurrents à 100 k+ ont tous.
6. **Expérimentations de fiche** (Croissance > Présence sur le Store > Expérimentations de fiche) : testez d'abord l'icône (actuelle contre A), puis la description courte (texte principal contre variante). Une expérimentation à la fois, 2 à 4 semaines, même avec peu de trafic c'est gratuit.
7. **Avis et notes** : la fiche n'affiche aucune note. Deux actions : dans l'app, après un smiley positif sur une livraison, déclenchez la demande d'avis Play (API In-App Review) ; dans la Console, répondez à chaque avis sous 48 h (les réponses sont indexées et comptent dans la perception).
8. **Pays de distribution** : vérifiez que la Tunisie, le Maroc, l'Algérie, la France, la Belgique, la Suisse, le Canada et les pays anglophones sont cochés.
9. **Notes de version** : utilisez le texte de la section 2 à la prochaine mise en production, et changez-le à chaque version.

---

## 8. Faire venir du monde (hors recherche Play)

Une fiche à 50 installations ne se classe pas toute seule. Les leviers, du plus rentable au moins rentable :

1. **Les apps que vous livrez sont votre meilleure publicité.** L'écran « Made with AppForge » au démarrage de chaque app générée doit être touchable et ouvrir la fiche : `https://play.google.com/store/apps/details?id=com.tipro&referrer=utm_source%3Dmade_with_appforge`. Le paramètre `referrer` vous permettra de voir dans la Console (Statistiques > Acquisition) combien d'installations viennent de là. Ajoutez aussi un bouton « Partager AppForge » dans la discussion après une livraison.
2. **Une page web d'une seule vue** (sur `schedview-748f3.web.app` ou un domaine à vous) : le slogan, les 3 étapes, trois exemples (ChantierPro, Visite Immo, un jeu), le bouton Play. Google indexe cette page sur « créer une application sans coder Tunisie » bien plus vite que Play n'indexera la fiche, et elle sert de lien pour tout le reste.
3. **Preuves publiques** : une vidéo de 20 secondes « je décris → j'installe » par semaine (TikTok, Reels, LinkedIn), toujours avec le lien Play. ChantierPro et Visite Immo sont des démonstrations plus convaincantes qu'un discours.
4. **Groupes et communautés** : groupes Facebook tunisiens d'entrepreneurs, d'artisans, d'étudiants et de bricoleurs d'idées ; proposez-y de fabriquer une app gratuitement pour un membre, en public.
5. **Parrainage** : des crédits offerts au parrain et au filleul (changement produit, mais c'est le mécanisme qui a fait grandir toutes les apps à crédits).

Objectif réaliste à 60 jours : passer de 50+ à 500+ installations et obtenir une note affichée (il faut une dizaine de notes). À partir de là, le référencement Play commence à travailler pour vous.

---

## 9. Pas-à-pas dans la Play Console

Je n'ai pas pu agir dans votre Chrome depuis cette session cloud (le navigateur n'est pas visible d'ici). Voici l'ordre à suivre ; tout tient en une trentaine de minutes.

1. **Fiche Play Store principale** (Croissance > Présence sur le Store > Fiche Play Store principale, langue par défaut français) :
   - Nom de l'application → section 2 ; Description courte → section 2 ; Description complète → section 2.
   - Icône → gardez l'actuelle pour l'instant (l'icône se teste en A/B, point 6).
   - Image de présentation → `assets/feature-graphic/feature_fr_1024x500.png`.
   - Captures « Téléphone » → supprimez les 15 actuelles, téléversez les 8 fichiers de `assets/screenshots-fr/` dans l'ordre 01 à 08.
   - Enregistrer.
2. **Traductions** : ouvrez la fiche en-US → section 3 (titre, courte, longue), image de présentation EN, captures `assets/screenshots-en/01-hero-en.png` et `04-first-app-free-en.png` en positions 1 et 4. Si vous activez l'arabe : ajouter la langue « ar » → section 4.
3. **Paramètres de la fiche** : catégorie Productivité, tags, coordonnées.
4. **Contenu de l'application > Sécurité des données** : point 2 de la section 7, puis l'URL de suppression de compte.
5. **Compte de développeur > Page du développeur / Informations sur le compte** : nom « BlueWave Apps ».
6. **Présentation de la publication** : envoyez les modifications pour examen (les changements de fiche passent par la revue Google, en général sous 48 h).
7. Ensuite, dans l'ordre : vidéo (point 5), expérimentation icône (point 6), demande d'avis dans l'app (point 7), lien dans l'écran « Made with AppForge » (section 8).

Si vous voulez que je fasse ces clics moi-même, il faut une session qui tourne sur votre PC (Claude Desktop, ou `claude remote-control` dans un terminal) : de là, Chrome est accessible et ce document me sert de script.
