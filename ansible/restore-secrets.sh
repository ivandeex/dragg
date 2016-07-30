#!/bin/bash
inp=group_vars/all/vault.yml
out=secrets.yml
cd $(dirname $(readlink -f $0))
chmod 600 $inp && cp $inp $out && ansible-vault decrypt $out && chmod 600 $out
