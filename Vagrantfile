Vagrant.configure("2") do |config|
  config.vm.box = "rocky/8"
  config.vm.hostname = "rlp-filesystem-lab"
  config.vm.network "private_network", ip: "192.168.56.101"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provision "shell", path: "./labs/filesystem/provision.sh"
end
