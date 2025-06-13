for filename in *.sh; do sed -i "s/USERNAME/${USER}/" ${filename}; done
