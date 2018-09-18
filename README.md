# ViMOS
Virtual Machine Migration with ONOS

ViMOS is an application to migrate VM from a certain host to its destination. 
It is usually used for data center management to migrate VM due to several reasons, such as load balance and maintenance.

This application consist of two main function, that are migration and path selection. To migrate a VM with certain volume, it needs to manage the VM itself so it can be done smoothly. 
In this project, VM management is done using QEMU-KVM which is the migration task is done using some flags adjustment. 

Path selection later is used to define and choose the path that can be used as link for data transfer. In this task, path selection consider not only the hop count but also the configured bandwidth. The path selection application then developed using ONOS API, especially disjoint path and intent. 

To operate this whole application, first it needs to run the ViMos_Test.py so the VMs which are located inside the host can be detected. Later, the path selection can be run, to detect the information regarding the network abstraction. To develop the network, it is used mininet so the network componenet can be adjusted easily. 

Some information can be gathered from ONOS API such as IP, MAC ADDRESS, port, etc. MAC ADDRESS will be used to activate the disjoint path so all the path which construct the link from source to its destination can be shown. Later user can select one of them to be used and install intents on it. 

The last tas need to be done is the migration execution itself. Back to the first code, we need to enter the volume of VM need to be transferred, and the measurement can be done. 

Measurement is done by considering three variables which are migration time, downtime and overhead processing time. This migration is done using non live mechanism. In some references it can also said as warm migration. 
Migration time will measured all the time need since the VM is being turned off until it launches at the destination host while the downtime is measured since the VM unaccessible. To perform that measurement, it also need to do ping test. The last, overhead processing time is measured by substract the migration time with the theoritical transfer time. 

Thank you..


