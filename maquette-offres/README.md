# Maquette « offres » (1 novembre 2026)

Branche de travail : **aucune publication**, toutes les pages restent en `noindex`.

## Ce que fait la maquette
- Accueil : nouvelle section « Trois offres, et le chat d'entreprise pour tous » (Exécutif 300 000 F, Entreprise dès 500 000 F, Custom sur devis), liens vers l'Auditeur d'entreprise.
- Page Offres : « sept fonctions », mention « HT, engagement minimum de six mois », ancien calculateur (200 000 F par Expert ajouté) retiré, liens vers trois nouvelles sous-pages.
- Nouvelles pages : `offres-executif.html`, `offres-entreprise.html`, `offres-custom.html`.
- Menu des pages : Équipes, Offres, Comment ça marche, Sécurité, Clients, Ressources, « Lancer l'Auditeur ».
- Sécurité : retrait de « Conforme ARTCI », « SOC 2 » et « Surveillance 24h/24 » (aucune source), remplacés par trois engagements du deck de vente.

## Reproduire
Depuis la racine du dépôt, sur `main` :

    python3 maquette-offres/build_site.py .

Le script modifie les fichiers HTML en place (51 fichiers). Testé : résultat identique, fichier par fichier, à la maquette validée en local.

## Reste à faire (connu)
- Hero de l'accueil toujours « Composer mon équipe » ; sélecteur d'équipes à six fonctions (le deck en compte sept).
- Pages Clients et Ressources non refaites ; logos et témoignages sans accord écrit encore présents.
- Hauteurs inégales des trois cartes sur la page Offres ; bloc blanc vide sous l'offre Exécutif ; prix absent du premier écran.
- Liens et formulaire non testés ; pages Entreprise, Custom et Sécurité rendues mais non inspectées.

Source des prix : deck de vente B2B (planches 4, 5, 6 et 15).
