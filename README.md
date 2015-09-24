#A quick router and cache for install party-like events

This repository contains a pair of Ansible playbooks that set a NAT environment from one ethernet card to a bridge of both another wired ethernet card and a wireless one.

Additionally, it sets an Squid cache for the Ubuntu repositories. A rewriter is used so the same file from different mirrors is cached only once.

These playbooks are written for a Ubuntu 14.04 environment.

To install, first edit `group_vars/all` and set appropriate values for each variable. Then, install ansible (e.g. from the Ubuntu repo) and run the playbook:

    ansible-playbook -i hosts router.yml

Once the event has finished, to uninstall the router-cache and return your computer to normal state, run this playbook:

    ansible-playbook -i hosts restore.yml
