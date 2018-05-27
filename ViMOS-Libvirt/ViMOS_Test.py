#!/usr/bin/env python
from __future__ import print_function
import sys
import libvirt
import time
import os

print ('##################################################')
print ('#                Welcome to ViMOS                #')
print ('#             -VM Migration by ONOS-             #')
print ('#         Created by Galura MS & Dimas AM        #')
print ('##################################################')
print ('')
print ('Connecting hypervisor to get domain information....')

time.sleep (5)
os.system('clear')

#Hypervisor Connection 1

sconn = libvirt.open('qemu+ssh://galurams@10.10.1.89/system')
if sconn == None:
    print('Failed to open connection to qemu+ssh://desthost/system', file=sys.stderr)
    exit(1)

#Hypervisor Connection 2

dconn = libvirt.open('qemu+ssh://galurams@10.10.1.87/system')
if dconn == None:
    print('Failed to open connection to qemu+ssh://desthost/system', file=sys.stderr)
    exit(1)

#Connecting Storage Pool Hypervisor1

pool1 = sconn.storagePoolLookupByName('default')
if pool1 == None:
    print('Failed to locate any StoragePool objects.', file=sys.stderr)
    exit(1)

stgvols1 = pool1.listVolumes()

#Connecting Storage Pool Hypervisor2

pool2 = dconn.storagePoolLookupByName('default')
if pool2 == None:
    print('Failed to locate any StoragePool objects.', file=sys.stderr)
    exit(1)

stgvols2 = pool2.listVolumes()


#List Domain HYP1

dom1 = sconn.listAllDomains(0)
print ('List Domain pada Hypervisor Host1:')
if len(dom1) != 0:
	
    for domain in dom1:
        
        print(' ' + domain.name())
        
else:
    print(' None')

#list Storage HYP1

print ('\nStorage Detail:')
print(' Pool    : '+pool1.name())
for stgvolname in stgvols1:
    print(' Volume  : '+stgvolname)
    stgvol = pool1.storageVolLookupByName(stgvolname)
    info = stgvol.info()
    print(' VM Size : '+str(info[1]))
    


#List Domain HYP2

dom2 = dconn.listAllDomains(0)
print ('\nList Domain pada Hypervisor Host2:')
if len(dom2) != 0:
	
    for domain in dom2:
        
        print(' ' + domain.name())
else:
    print(' None')    

#list Storage HYP2

print ('\nStorage Detail:')
print(' Pool    : '+pool2.name())
for stgvolname in stgvols2:
    print(' Volume  : '+stgvolname)
    stgvol = pool2.storageVolLookupByName(stgvolname)
    info = stgvol.info()
    print(' VM Size : '+str(info[1]))


print ('\n\n\nMigration Ready')

# Target VM

domName = raw_input ('\n \nTuliskan VM yang akan di migrasikan: ')

# Modul Migrasi 

dom1= sconn.lookupByName(domName)
if dom1 == None:
    print('Failed to find the domain '+domName, file=sys.stderr)
    exit(1)

# Timer start
start_time = time.time()

new_dom = dom1.migrate(dconn, libvirt.VIR_MIGRATE_PERSIST_DEST + libvirt.VIR_MIGRATE_NON_SHARED_DISK, None, None, 0)
if new_dom == None:
    print('Could not migrate to the new domain', file=sys.stderr)
    exit(1)

#Timer stop
print('Domain was migrated successfully in %s seconds' % (time.time() - start_time), file=sys.stderr)

#Closing Hypervisor
sconn.close()
dconn.close()
exit(0)
