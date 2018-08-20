import requests
from requests.auth import HTTPBasicAuth
import json
import urllib
import time

print "\nWELCOME TO VIMOS\n"
def pilihan1():
	while True:
		print "For Switch Information Press 1\n"
		print "For Migration Press 2 (It informs you all host first)\n"
		print "To Quit from apps Press 0"
		b =input("\nEnter your choice:")

		if b == 1:
			print "\nSWITCH INFORMATION"
			print "---------------------"
			url1 = 'http://127.0.0.1:8181/onos/v1/devices'
			response = requests.get(url1, auth=HTTPBasicAuth('karaf','karaf'))
			qu = json.loads(response.content)
			for y in qu['devices']:
				y1 = (y['type'])
				y2 = (y['id'])
				y3 = (y['hw'])
				y4 = (y['mfr'])
				y5 = (y['annotations']['protocol'])
				y6 = (y['annotations']['channelId'])
				print ('\nDevices=' + y1)
				print ('ID=' + y2)
				print ('Hardware=' + y3)
				print ('Manufactur=' + y4)
				print ('Protocol=' + y5)
				print ('Channel=' + y6)
		elif b == 2:
			print "\nHOST INFORMATION"
			print "--------------------"
			url2 = 'http://127.0.0.1:8181/onos/v1/hosts'
			response2 = requests.get(url2, auth=HTTPBasicAuth('karaf','karaf'))
			qu2 = json.loads(response2.content)
			for x in qu2['hosts']:
				x1 = (x['mac'])
				x2 = (x['ipAddresses'][0])
				x3 = (x['locations'][0]['port'])
				x4 = (x['locations'][0]['elementId'])
				x5 = (x['id'])
				x6 = (x['vlan'])
				print ('\nHost ID=' + x5)
				print ('IP Address=' + x2)
				print ('MAC Address=' + x1)
				#print ('VLAN=' + x6)
				print ('Connecting SWITCH ID=' + x4)
				print ('Connecting PORT=' + x3)

			time.sleep(3)
			print "\nYou will do MIGRATION TASK\nPLEASE INPUT SRC AND DST MAC ADDRESS"
			print "------------------------------"
			src = raw_input('HOST-MAC Source: ')
			dst = raw_input('HOST-MAC Destination: ')
			src2 = src + '/None'
			dst2 = dst + '/None'
			src1 = urllib.quote_plus(src2)
			dst1 = urllib.quote_plus(dst2)
			urla1 = 'http://127.0.0.1:8181/onos/v1/paths/'+src1+'/'+dst1+'/disjoint'
			output = requests.get(urla1, auth=HTTPBasicAuth('karaf','karaf'))
			data = json.loads(output.content)

			for t in data['paths']:
				t1 = (t['primary']['cost'])
				t2 = (t['backup']['cost'])
				print "\nPATH CHECKING PROCESS......"
				print ('\nHOP COUNT FOR PATH I= %d') %(t1)
				print ('HOP COUNT FOR PATH II= %d') %(t2)

				a = len(t['primary']['links'])
				t5 = (t['primary']['links'][0]['dst']['device'])
				t6 = (t['primary']['links'][0]['dst']['port'])
				t7 = (t['primary']['links'][a-1]['src']['device'])
				t8 = (t['primary']['links'][a-1]['src']['port'])
				print ('\nPATH I MEMBER:\n')
				print (t5 + "/" + t6)
				for d in range(1,a-1):
					t4 = (t['primary']['links'][d]['src']['port'])
					t9 = (t['primary']['links'][d]['src']['device'])
					t10 = (t['primary']['links'][d]['dst']['port'])
					t11 = (t['primary']['links'][d]['dst']['device'])
					print (t9 + "/" + t4)
					print (t11 +"/" +t10)
				print (t7 +"/"+ t8)
				print "-------------------------------"
	
				b = len(t['backup']['links'])
				t12 = (t['backup']['links'][0]['dst']['device'])
				t13 = (t['backup']['links'][0]['dst']['port'])
				print ('PATH II MEMBER:\n')
				print (t12 + "/" + t13)
				for f in range(1,b-1):
					t14 = (t['backup']['links'][f]['src']['port'])
					t15 = (t['backup']['links'][f]['src']['device'])
					t16 = (t['backup']['links'][f]['dst']['port'])
					t17 = (t['backup']['links'][f]['dst']['device'])
					print (t15 + "/" + t14)
					print (t17 +"/" +t16)
				t18 = (t['backup']['links'][b-1]['src']['device'])
				t19 = (t['backup']['links'][b-1]['src']['port'])
				print (t18 +"/"+ t19)


			print ("CHOOSE PATH TO BE INSTALLED INTENT\nPRESS 1 FOR PATH I and PRESS 2 FOR PATH II")
			print "-------------------------------------"

			pilihan =input("ENTER YOUR CHOICE:")

			if pilihan == 1:
				"""ingress fwd"""
				devin=[]  
				devin.append(t5)
				for e in range (1,a):
					te = (t['primary']['links'][e]['src']['device'])
					devin.append(te)
				del devin[a-1]
				del devin[1]
				#print devin

				portin=[]  
				portin.append(t6)
				for f in range (1,a):
					tf = (t['primary']['links'][f]['src']['port'])
					portin.append(tf)
				del portin[a-1]
				del portin[1]
				#print portin

				"""egress fwd"""
				deveg= []
				for g in range (1,a):
					tg = (t['primary']['links'][g]['src']['device'])
					deveg.append(tg)
				deveg.append(t5)
				del deveg[a-1]
				del deveg[0]
				#print deveg

				porteg = []
				for h in range (1,a):
					th = (t['primary']['links'][h]['src']['port'])
					porteg.append(th)
				porteg.append(t6)
				del porteg[a-1]
				del porteg[0]
				#print porteg

				"""eksekusi intent fwd"""

				urlb = 'http://127.0.0.1:8181/onos/v1/intents'
				d = len(porteg)
				print 'FORWARD INTENT INSTALLATION'
				for w in range (0,d):
					di = devin[w]
					pi = portin[w]
					de = deveg[w]
					pe = porteg[w]
					print ('SRC DEVICE: %s') %(di)
					print ('SRC PORT  : %s') %(pi)
					print ('DST DEVICE: %s') %(de)
					print ('DST PORT  : %s') %(pe)
					data=	{
						  "type": "PointToPointIntent",
						  "appId": "org.onosproject.cli",
						  "resources": [],
						  "state": "INSTALLED",
						  "selector": {
						    "criteria": []
						  },
						  "treatment": {
						    "instructions": [
						      {
							"type": "NOACTION"
						      }
						    ],
						    "deferred": []
						  },
						  "priority": 100,
						  "constraints": [],
						  "ingressPoint": {
						    "port": (pi),
						    "device": (di)
						  },
						  "egressPoint": {
						    "port": (pe),
						    "device": (de)
						  }
					}

					headers = {'content-type': 'application/json'}
					req = requests.post(urlb, data = json.dumps(data), headers = headers, auth=HTTPBasicAuth('karaf','karaf'))

					print ('responce: %d\n') %(req.status_code)

				print "-------------------------------------\n"

				"""ingress backward"""
				deveg.reverse()
				devin2 = deveg
				#print devin2

				porteg.reverse()
				portin2 = porteg
				#print portin2

				"""egress backward"""
				devin.reverse()
				deveg2 = devin
				#print deveg2

				portin.reverse()
				porteg2 = portin
				#print porteg2

				urlb = 'http://127.0.0.1:8181/onos/v1/intents'

				print 'BACKWARD INTENT INSTALLATION'
				for x in range (0,d):
					di2 = devin2[x]
					pi2 = portin2[x]
					de2 = deveg2[x]
					pe2 = porteg2[x]
					print ('SRC DEVICE: %s') %(di2)
					print ('SRC PORT  : %s') %(pi2)
					print ('DST DEVICE: %s') %(de2)
					print ('DST PORT  : %s') %(pe2)
					data=	{
						  "type": "PointToPointIntent",
						  "appId": "org.onosproject.cli",
						  "resources": [],
						  "state": "INSTALLED",
						  "selector": {
						    "criteria": []
						  },
						  "treatment": {
						    "instructions": [
						      {
							"type": "NOACTION"
						      }
						    ],
						    "deferred": []
						  },
						  "priority": 100,
						  "constraints": [],
						  "ingressPoint": {
						    "port": (pi2),
						    "device": (di2)
						  },
						  "egressPoint": {
						    "port": (pe2),
						    "device": (de2)
						  }
					}

					headers = {'content-type': 'application/json'}
					req = requests.post(urlb, data = json.dumps(data), headers = headers, auth=HTTPBasicAuth('karaf','karaf'))

					print ('responce: %d\n') %(req.status_code)

				print "-------------------------------------\n"


			elif pilihan == 2:

				"""ingress fwd backup"""
				devbin = []
				devbin.append(t12)
				for z in range (1,b):
					ze = (t['backup']['links'][z]['src']['device'])
					devbin.append(ze)
				del devbin[b-1]
				del devbin[1]
				#print devbin

				portbin = []
				portbin.append(t13)
				for y in range (1,b):
					ya = (t['backup']['links'][y]['src']['port'])
					portbin.append(ya)
				del portbin[b-1]
				del portbin[1]
				#print portbin

				"""egress fwd backup"""
				devbeg = []
				for s in range (1,b):
					sa = (t['backup']['links'][s]['src']['device'])
					devbeg.append(sa)
				devbeg.append(t12)
				del devbeg[b-1]
				del devbeg[0]
				#print devbeg

				portbeg = []
				for r in range (1,b):
					ra = (t['backup']['links'][r]['src']['port'])
					portbeg.append(ra)
				portbeg.append(t13)
				del portbeg[b-1]
				del portbeg[0]
				#print portbeg

				"""eksekusi intent fwd"""

				urlb = 'http://127.0.0.1:8181/onos/v1/intents'
				db = len(portbeg)
				print 'FORWARD INTENT INSTALLATION'
				for v in range (0,db):
					di = devbin[v]
					pi = portbin[v]
					de = devbeg[v]
					pe = portbeg[v]
					print ('SRC DEVICE: %s') %(di)
					print ('SRC PORT  : %s') %(pi)
					print ('DST DEVICE: %s') %(de)
					print ('DST PORT  : %s') %(pe)
					data3=	{
						  "type": "PointToPointIntent",
						  "appId": "org.onosproject.cli",
						  "resources": [],
						  "state": "INSTALLED",
						  "selector": {
						    "criteria": []
						  },
						  "treatment": {
						    "instructions": [
						      {
							"type": "NOACTION"
						      }
						    ],
						    "deferred": []
						  },
						  "priority": 100,
						  "constraints": [],
						  "ingressPoint": {
						    "port": (pi),
						    "device": (di)
						  },
						  "egressPoint": {
						    "port": (pe),
						    "device": (de)
						  }
					}

					headers = {'content-type': 'application/json'}
					req = requests.post(urlb, data = json.dumps(data3), headers = headers, auth=HTTPBasicAuth('karaf','karaf'))

					print ('responce: %d\n') %(req.status_code)

				print "-------------------------------------\n"

				"""ingress backward"""
				devbeg.reverse()
				devbin2 = devbeg
				#print devbin2

				portbeg.reverse()
				portbin2 = portbeg
				#print portbin2

				"""egress backward"""
				devbin.reverse()
				devbeg2 = devbin
				#print devbeg2

				portbin.reverse()
				portbeg2 = portbin
				#print portbeg2

				urlb = 'http://127.0.0.1:8181/onos/v1/intents'
				dh = len(portbeg2)
				print 'BACKWARD INTENT INSTALLATION'
				for k in range (0,dh):
					di = devbin2[k]
					pi = portbin2[k]
					de = devbeg2[k]
					pe = portbeg2[k]
					print ('SRC DEVICE: %s') %(di)
					print ('SRC PORT  : %s') %(pi)
					print ('DST DEVICE: %s') %(de)
					print ('DST PORT  : %s') %(pe)
					data3=	{
						  "type": "PointToPointIntent",
						  "appId": "org.onosproject.cli",
						  "resources": [],
						  "state": "INSTALLED",
						  "selector": {
						    "criteria": []
						  },
						  "treatment": {
						    "instructions": [
						      {
							"type": "NOACTION"
						      }
						    ],
						    "deferred": []
						  },
						  "priority": 100,
						  "constraints": [],
						  "ingressPoint": {
						    "port": (pi),
						    "device": (di)
						  },
						  "egressPoint": {
						    "port": (pe),
						    "device": (de)
						  }
					}

					headers = {'content-type': 'application/json'}
					req = requests.post(urlb, data = json.dumps(data3), headers = headers, auth=HTTPBasicAuth('karaf','karaf'))

					print ('responce: %d\n') %(req.status_code)

				print "-------------------------------------\n"

			else:
				print("Your decision out of choices \nRestart Program PLEASE!")
				break
		elif b == 0:
			break
		else:
			print "YOUR CHOICE OUT OF LIST.\nIt available only 1 and 2\n"
			continue	
pilihan1()



