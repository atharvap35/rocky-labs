#!/bin/bash
set -e

echo "Provisioning Rocky Linux filesystem lab..."

# Update and install basic tools
dnf -y update
dnf -y install vim which net-tools openssh-server cloud-init

# Ensure SSH is running
systemctl enable --now sshd

# Create sample files and a broken fstab for troubleshooting lab
mkdir -p /opt/rlp-labs/filesystem
echo "Sample config" > /opt/rlp-labs/filesystem/README.txt

# Create a user for learners
useradd -m -s /bin/bash learner
echo "learner:learner" | chpasswd

# If a public key is provided in the synced folder, install it for the learner and disable password login
if [ -f /vagrant/labs/filesystem/learner_id_rsa.pub ]; then
	mkdir -p /home/learner/.ssh
	cat /vagrant/labs/filesystem/learner_id_rsa.pub > /home/learner/.ssh/authorized_keys
	chown -R learner:learner /home/learner/.ssh
	chmod 700 /home/learner/.ssh
	chmod 600 /home/learner/.ssh/authorized_keys
	# lock password to encourage key auth
	passwd -l learner || true
	echo "Installed learner public key and locked password."
fi

# ensure README is owned by learner with sensible perms for the lab
if [ -f /opt/rlp-labs/filesystem/README.txt ]; then
	chown learner:learner /opt/rlp-labs/filesystem/README.txt
	chmod 644 /opt/rlp-labs/filesystem/README.txt
fi

# Add a deliberately broken fstab entry for the troubleshooting lab
cp /etc/fstab /etc/fstab.orig
echo "# Broken fstab entry for troubleshooting lab" >> /etc/fstab
echo "UUID=0000-0000 /mnt/broken vfat defaults 0 2" >> /etc/fstab

echo "Provisioning complete."
