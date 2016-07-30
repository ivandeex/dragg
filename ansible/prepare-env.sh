#!/bin/bash
cd $(dirname $(readlink -f $0))
test secrets.yml -nt group_vars/all/vault.yml && ./make-secrets.sh
ansible-playbook -i hosts task-env.yml
