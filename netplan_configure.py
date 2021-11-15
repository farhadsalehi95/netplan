#!/usr/bin/python3

#inpoty liberary we needed
import yaml
import os
import re
import sys

#list netplan files and choose one
ls_netplan_directory = os.popen('ls /etc/netplan').readlines()
netplan_files = [i[:-1] for i in ls_netplan_directory]
counter = 0
for x in netplan_files:
  counter += 1
  print (counter,"-",x)
choose_one = int(input ("choose one please... \n Your input number is : "))
if choose_one > counter:
  print ("\n please select right number.\n")
  sys.exit()
netplan_index_number = choose_one -1

#list network interfaces and choose one
ls_interfaces_list = os.popen('ls /sys/class/net').readlines()
interfaces_list = [i[:-1] for i in ls_interfaces_list]
counter = 0
for x in interfaces_list:
  counter += 1
  print (counter,"-",x)
choose_one = int(input ("choose one please... \n Your input number is : "))
if choose_one > counter:
  print ("\n please select right number.\n")
  sys.exit()
interface_index_number = choose_one -1

#input ip address such as 192.168.1.100
ip = input ('input your ip address : \n Example = 192.168.1.100/24 \n Your input ip is : ')

#spilt input ip address if interface have 2 ip address 
#ips is a list like ['192.168.1.100' , '192.168.1.200']
ips = ip.split()

#input syntax check with Regex you can search IP Regex in NET or use this
if not re.match(r'(?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9])\/(3[02]|[12][0-9]|[8-9])', ip):
  print ('\n Input invalid Please See Example \n')
  sys.exit()

#input gateway address such 192.168.1.1
gateway = input('input your gateway : \n Example = 192.168.1.1 \n Your input gateway is : ')

#Syntax Check
if not re.match(r'(?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9])', gateway):
    print ('\n Input invalid Please See Example \n')
    sys.exit()

#input DNS such as 8.8.8.8 
dns = input('input you dns servers : \n Example = 8.8.8.8 1.1.1.1 \n Your input dns is : ')

#spilt input DNS Address if interface have 2 DNS Address 
#ips is a list like ['8.8.8.8' , '1.1.1.1']
dnss = dns.split()

#Syntax Check
if not re.match(r'(?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9])', dns):
    print ('\n Input invalid Please See Example \n')
    sys.exit()

#Open netplan file you selected with yaml parser    
with open('/etc/netplan/{}'.format(netplan_files[netplan_index_number])) as file:
  ip_list = yaml.load(file, Loader=yaml.FullLoader)

#set input paramert into yaml structuer and write it to netplan file you selected.
ip_list.update({'network': {'ethernets': {interfaces_list[interface_index_number] : {'dhcp4': False , 'addresses': ips , 'gateway4' : gateway,'nameservers':{'addresses' : dnss}} }, 'version': 2}})
with open('/etc/netplan/{}'.format(netplan_files[netplan_index_number]),'w') as file:
  yaml.dump(ip_list ,file )

# run netplan apply
os.system('netplan apply')


#END