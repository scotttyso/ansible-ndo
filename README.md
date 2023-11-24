# ansible-ndo

This repository contains example Ansible Playbooks to Configure Nexus Dashboard Orchestrator

## Install Ansible

```bash
sudo pip install ansible
```

## Install Galaxy Collections: ND, MSO

```bash
ansible-galaxy collection install cisco.mso
ansible-galaxy collection install cisco.nd
```

## Run the Playbook

```bash
cd bd-epg-display-name
ansible-playbook -i production playbook.yaml
```