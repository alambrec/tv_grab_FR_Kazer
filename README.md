# French XML TV Grabber for TVHeadend

This is a simple script to recover EPG guide for TVHeadend backend.
It's optimized for Synology NAS but it must compatible on every Linux/GNU System. (Not on BSD like OSX)

My script recovers XMLTV file from https://xmltv.ch.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation on *Synology NAS*

1. Place `tv_grab_xmltv_ch` script in your TVHeadend binary folder `/var/packages/tvheadend/target/bin/` :

`mv tv_grab_xmltv_ch /var/packages/tvheadend/target/bin/.`

2. Change owner and group by `sc-tvheadend:tvheadend` : 

`chown sc-tvheadend:tvheadend /var/packages/tvheadend/target/bin/tv_grab_xmltv_ch`

3. Change permission to make it executable :

`chmod 755 /var/packages/tvheadend/target/bin/tv_grab_xmltv_ch`

4. Make a symbolic link in `/usr/local/bin` :

`ln -s /var/packages/tvheadend/target/bin/tv_grab_xmltv_ch /usr/local/bin/tv_grab_xmltv_ch`

5. Restart your `TVHeadend Service` by Synology Application Manager.

6. Set `XMLTV Ch` as Internal Grabber XMLTV on TVHeadend.
