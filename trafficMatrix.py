#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Javier Artiga Garijo (v0.1)
#date: 12/10/2018
#version: 0.1
#
# returns a traffic matrix from a .pcap
#
#usage: python3 trafficMatrix.py trozoX.pcap.gz
#
#recommended: python3 trafficMatrix.py trozo9.pcap.gz | column -t

#TODO: filter by type of traffic
#TODO: review if srcIPs,destIPs have to be separated

import argparse
import subprocess
import os
import re

srcIPs = []
destIPs = []
order = 950 # estimation (here we know there are 910 IPv4 addresses)
matrix = [[0 for col in range(order)] for row in range(order)]
# python note: be careful with REFERENCE SHARING!!!
# this would reference each element to each other: matrix = [[0]*order]*order

def genMatrix(filename):
	plainFile = filename+'.txt'
	tsharkCommand = "tshark -r {}.pcap.gz >> {}".format(filename,plainFile)
	# IP address pattern (IPv4 ONLY)
	pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

	# this chunk should be necessary only once:
	if not os.path.isfile(plainFile):
		#print("let's get .pcap as plain text! wait for it..")
		subprocess.call(tsharkCommand, shell=True)

	# parse the file:
	if os.path.isfile(plainFile):
		#print("\nlet's see how many ips there are in the capture file:")
		with open(plainFile) as f:
			for line in f:
				x,y = '',''
				ipSrc = line.split()[2]
				ipDst = line.split()[4]
				length = line.split()[6]
				if ipSrc not in srcIPs:
					if pattern.match(ipSrc):
						srcIPs.append(ipSrc)
						destIPs.append(ipSrc)
				if ipDst not in srcIPs:
					if pattern.match(ipDst):
						srcIPs.append(ipDst)
						destIPs.append(ipDst)
				try:
					x = srcIPs.index(ipSrc)
					y = destIPs.index(ipDst)
					matrix[x][y]=matrix[x][y]+int(length)
				except ValueError:
					pass # ipSrc or ipDst is an invalid IPv4 address

	#print ips to file:
	with open('ips.txt','w') as f:
		print(srcIPs,file=f)
	
	#print matrix to file:
	with open('matrix.txt','w') as f:
		for row in matrix:
			print(row,file=f)

	#print the beginning of the matrix:
	print("beginning_of_the_matrix:")
	print('.               ',end=" ") #(first cell empty)
	print(' '.join(srcIPs[:10]))
	for i in range(10):
		print(srcIPs[i],end=" ")
		print(matrix[i][:10])

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('file')
	args = parser.parse_args()

	genMatrix(args.file.split(".")[0])
