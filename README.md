# XML TV Grabber for TVheadend

This is a simple script to recover EPG guide for TVHeadend backend.
It's optimized for Synology NAS but it must compatible on every Linux/GNU System. (Not on BSD like OSX)

My script support 2 website for recover XMLTV :
 - https://www.kazer.org
 - http://xmltv.dtdns.net
 
Like I have some problem in using kazer.org, I add also support for http://xmltv.dtdns.net

## Installation

1. Replace `userhash` or `username` on the script
 - for Kazer.org : replace at the line 8 `your_userhash_here` by your userhash on kazer.org (available on tab 'Mes Chaînes')
 - for Dtdns.net : replace at the line 9 `your_username_here` by your username on xmltv.dtdns.net.org 
2. Place your script on your binary folder (for Synology NAS in `/usr/bin/`).
3. Change owner and group : `chown root:root tv_grab_kazer`
4. Change permission to make it executable :  `chmod 755 tv_grab_kazer`
5. Test your script in running like this : `tv_grab_kazer  --debug`
  * you must see on the screen the content of XML.
6. Set France Kazer or France Telerama like Internal Grabber XMLTV on TVHeadEnd.

## Tutorial for script of Kazer.org on NAS Synology DS212j (in French)
http://www.inrepublica.fr/2013/06/11/un-vrai-guide-des-programmes-avec-tvheadend-tnt-fr/
