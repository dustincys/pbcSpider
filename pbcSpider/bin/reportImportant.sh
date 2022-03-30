#!/usr/bin/env bash

files=$(ls /home/dustin/temp/pbccoin.important*.txt)
for tempFile in $files
do
    /usr/bin/cat $tempFile | /usr/bin/neomutt -s "中国银行货币金银局: $(/usr/bin/head -n 1 $tempFile)" yanshuochu@qq.com
    /home/dustin/bin/notmuchUpdate.sh
    /usr/bin/notify-send "中国银行货币金银局:" "$(/usr/bin/head -n 1 $tempFile)"

    # if /usr/bin/cat $tempFile | grep -E "(渔|鱼)"; then
    #     /usr/bin/cat $tempFile | /usr/bin/neomutt -s "HoustonBBS: $(/usr/bin/head -n 1 $tempFile)" tianyh@pku.edu.cn bzhu80928@163.com
    #     /home/dustin/bin/notmuchUpdate.sh
    #     /usr/bin/notify-send "Important houstonbbs news" "$(/usr/bin/head -n 1 $tempFile)"
    # fi

    # if /usr/bin/cat $tempFile | grep -E "(幼|婴|儿童|小孩|车)"; then
    #     /usr/bin/cat $tempFile | /usr/bin/neomutt -s "HoustonBBS: $(/usr/bin/head -n 1 $tempFile)" bzhu80928@163.com
    #     /home/dustin/bin/notmuchUpdate.sh
    #     /usr/bin/notify-send "Important houstonbbs news" "$(/usr/bin/head -n 1 $tempFile)"
    # fi
done
