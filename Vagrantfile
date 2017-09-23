# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
    config.cache.enable :apt
  end

  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |v|
      v.memory = 2048
      v.cpus = 2
  end
  config.vm.define "twanalytics"
  config.vm.hostname = "twanalytics.com"
  config.vm.network :private_network, ip: "192.168.33.10"
  config.vm.network "forwarded_port", guest:8888, host:8888
  config.vm.network "forwarded_port", guest:4040, host:4040
  config.vm.network "forwarded_port", guest:5601, host:5601
  config.vm.synced_folder ".", "/apps/twitter_analytics"
  
  config.ssh.forward_agent = true
  config.ssh.insert_key = false

  config.vm.provision "ansible" do |ansible|
      ansible.playbook = "provision/provision.yml"
      ansible.extra_vars = {use_vagrant: "true"}
      ansible.inventory_path = "provision/hosts"
      ansible.limit = "localhost"
      ansible.verbose = 'vvvv'
  end
end
