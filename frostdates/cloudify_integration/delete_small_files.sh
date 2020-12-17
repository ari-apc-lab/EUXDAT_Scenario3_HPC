find export/ -type f | xargs -i bash -c 'if [ $(wc -l {}|cut -d" " -f1) -lt 30 ]; then rm -f {}; fi'
