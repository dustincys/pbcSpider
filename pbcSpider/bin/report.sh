#!/usr/bin/env bash

cat /home/dustin/temp/pbccoin.plain.txt | /usr/bin/neomutt -s "中国人民银行货币金银局 $(/usr/bin/date +'%X')" yanshuochu@qq.com

/home/dustin/bin/notmuchUpdate.sh

/usr/bin/notify-send "PBC Coin News" "$(/usr/bin/cat /home/dustin/temp/houston.plain.txt)"
