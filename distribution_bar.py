#! /usr/bin/env python
# encoding:utf-8
from __future__ import division
import sys
import os
import matplotlib.pyplot as plt


class Generater():
	def __init__(self, cost_file, interval_length, pic_name):
		self.cost_file = cost_file
		self.interval_length = int(interval_length)

		self.cost_list = []
		self.interval_list = []
		self.result_dict = {}
		
		self.section_list = []
		self.density_list = []
		self.xlist = []
		self.ylist = []
		
		self.pic_name = pic_name
	  
	  
	def loadData(self):
		try:
			filed = open(self.cost_file, 'r')
		except:
			print ('open logfile fail,exit')
			return
		
		for s in filed:
			self.cost_list.append(int(s.strip()))


		for i in range(0, self.cost_list[-1] + self.interval_length, self.interval_length):
			self.interval_list.append(i)
    
		for cost in self.cost_list:
			current = 0
			find_key = 0
			for i in range(current, len(self.interval_list)-1):
				if self.interval_list[i] not in self.result_dict.keys():
					self.result_dict[ self.interval_list[i] ] = []
				if cost >= self.interval_list[i] and cost < self.interval_list[i+1]:				
					self.result_dict[ self.interval_list[i] ].append(cost)	 
					current = i
					find_key = 1
					break
			if find_key == 0:
				if -1 not in self.result_dict.keys():
					self.result_dict[-1] = []
				self.result_dict[-1].append(cost)
				
		if -1 in self.result_dict.keys():
			print ("theris values in result_dict[-1], please check")  	
		
		filed.close()


	def calculateDistribution(self):
		total = len (self.cost_list)
		for i in range(0, len(self.interval_list)-2):
			self.section_list.append( str(self.interval_list[i])+'-'+str(self.interval_list[i+1]) )
			
			num_i = len( self.result_dict[self.interval_list[i]] )
			self.density_list.append('{:.2%}'.format(num_i/total))
			#self.density_list.append('%.2f' %float(num_i/total*100))
		  
		print(self.section_list[:])
		print(self.density_list[:])
			

	def generateXY(self):
		total = len (self.cost_list)
		for i in range(0, len(self.interval_list)-2):
			num_i = len(self.result_dict[self.interval_list[i]])
			i_ratio = round(num_i/total*100, 2)
			if i_ratio > 0:
				self.xlist.append( str(self.interval_list[i])+'-'+str(self.interval_list[i+1]) )
				#self.ylist.append('{:.2%}'.format(num_i/total))
				self.ylist.append(i_ratio)
		  
		print(self.xlist[:])
		print(self.ylist[:])
			
	
	def paint(self):
		
		#plt.figure(figsize=(12,4)) 
		plt.switch_backend('agg')
		
		plt.figure(figsize=(24,12)) 
		plt.xlabel('sections: us')
		plt.ylabel('ratio: y * %')
		plt.title(self.cost_file+'__distribution')
		#plt.tight_layout()
	
		
		my_bar = plt.bar(range(len(self.ylist)), self.ylist, tick_label=self.xlist)
		plt.xticks(rotation=-60)
		plt.tick_params(axis='x', labelsize=10)  
		
		for data in my_bar:
			y = data.get_height()
			x = data.get_x()
			plt.text(x, y, str(y), va='bottom', fontsize=10, rotation=60)
		
		#plt.grid()	
		plt.savefig( self.pic_name+'.png')
		plt.close()		
	

def usage():
	print ('use like this: python test.py sorted_cost_filename interval_length pic_name,')
	print ('NOTE :the sorted_cost_filename must be sorted in ascending sequence!!!')
	print ('REQUIREMENTS: need to install matplotlib before run')
	print ('my env is pyhon 3.5')
	    			
       
if __name__ == '__main__':   
	
	if len(sys.argv) != 4:
		usage()
	else:
		cost_file = sys.argv[1]
		interval_length = sys.argv[2]
		pic_name = sys.argv[3]
		
		g = Generater(cost_file, interval_length, pic_name)
		g.loadData()
		g.calculateDistribution()
		g.generateXY()
		g.paint()