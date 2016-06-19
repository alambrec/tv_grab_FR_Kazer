# tv grab FR Kazer

Il s'agit d'un simple script sh utilisé pour récupérer les infos EPG (guide électronique des programmes) destiné à être transmis vers le logiciel TVHeadEnd.
Télécharge les infos EPG via le site http://www.kazer.org

## Installation

- Dans le script, remplacez à la ligne 8 `your_userhash_here` par votre userhash de kazer.org (disponible dans l'onglet Mes Chaînes).
- Placer le script à l'endroit approprié ( `/usr/bin/` si utilisé sur un NAS Synology).
- Changer l'utilisateur et le groupe du script avec la commande suivante `chown root:root tv_grab_kazer`
- Changer les droits d'accès au fichier à l'aide de cette commande `chmod 755 tv_grab_kazer`
- Tester le script en le lançant à l'aide de la commande `tv_grab_kazer  --debug`
  * vous devriez voir sur l'écran des données XML.
- Configurer TVHeadEnd en lui indiquant dans Internal Grabber XMLTV : France Kazer

## Installation sur NAS Synology

Un tuto détaillé pour l'installation sur un NAS Synology DS212j -> http://www.inrepublica.fr/2013/06/11/un-vrai-guide-des-programmes-avec-tvheadend-tnt-fr/
