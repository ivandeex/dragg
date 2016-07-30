#!/bin/bash
cd $(dirname $(readlink -f $0))
inp=secrets.yml
out=group_vars/all/vault.yml
chmod 600 $inp && cp $inp $out && ansible-vault encrypt $out && chmod 600 $out
