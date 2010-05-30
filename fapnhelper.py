#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" helper class for fAPN

@author: Nick Leppänen Larsson <frals@frals.se>
@license: GNU GPL
"""

try:
	import gnome.gconf as gconf
except:
	import gconf
import osso
import re

class fAPN_helper:
	def __init__(self):
		#self._fmmsdir = "/apps/fmms/"
		self._iapdir = "/system/osso/connectivity/IAP"
		self.client = gconf.client_get_default()
		#self.client.add_dir(self._fmmsdir, gconf.CLIENT_PRELOAD_NONE)
		
	def read_config(self):
		pass
		
	def add_new_apn(self, apname, simimsi):
		print "adding:", apname, simimsi
		gconfdir = re.search(r"[a-zA-Z0-9\ .]+", apname)
		gconfdir = gconfdir.group()
		gconfdir = gconfdir.replace(" ", "@32@")
		gconfdir = gconfdir.replace(".", "@46@")
		print gconfdir
		self.client.add_dir(self._iapdir + "/" + gconfdir, gconf.CLIENT_PRELOAD_NONE)
		self.client.set_string(self._iapdir + "/" + gconfdir + "/type", "GPRS")
		self.client.set_string(self._iapdir + "/" + gconfdir + "/name", apname)
		#self.client.set_string(self._iapdir + "/" + gconfdir + "/gprs_accesspointname", "changeme")
		self.client.set_string(self._iapdir + "/" + gconfdir + "/sim_imsi", simimsi)
		self.client.set_string(self._iapdir + "/" + gconfdir + "/ipv4_type", "AUTO")
		self.client.set_int(self._iapdir + "/" + gconfdir + "/user_added", 1)	
	
	def remove_apn(self, apname):
		print "preparing to remove", apname
		subdir = self._iapdir + "/" + apname
		useradded = self.client.get_int(self._iapdir + "/" + apname + "/user_added")
		if useradded == 1:
			print "really removing:", apname
			all_entries = self.client.all_entries(subdir)
			for entry in all_entries:
				(path, sep, shortname) = entry.key.rpartition('/')
				print "unsetting:", entry.key
				self.client.unset(entry.key)
			self.client.remove_dir(self._iapdir + "/" + apname)
			return 0
		else:
			print "not removing, not user_added"
			return -1
			
	def get_simimsi_from_apn(self):
		osso_ = osso.Context('fAPN', '0.1', False)
		rpc = osso.Rpc(osso_)
		imsi = rpc.rpc_run('com.nokia.phone.SIM', '/com/nokia/phone/SIM', 'Phone.Sim', 'get_imsi', (), True, True)
		#print imsi
		return imsi
		"""# get all IAP's
		dirs = self.client.all_dirs(self._iapdir)
		for subdir in dirs:
			# get all sub entries.. this might be costy?
			all_entries = self.client.all_entries(subdir)
			# this is a big loop as well, possible to make it easier?
			for entry in all_entries:
				(path, sep, shortname) = entry.key.rpartition('/')

				# this SHOULD always be a string
				if shortname == 'sim_imsi':				
					if entry.value.type == gconf.VALUE_STRING:
						_value = entry.value.get_string()
						return _value
		return None"""
	
	def get_apn_name_from_id(self, apnid):
		return self.client.get_string(self._iapdir + "/" + apnid + "/name")
	
	def get_apn_list_useradded(self):
		# get all IAP's
		dirs = self.client.all_dirs(self._iapdir)
		apnlist = []
		for subdir in dirs:
			# get all sub entries.. this might be costy?
			all_entries = self.client.all_entries(subdir)
			# this is a big loop as well, possible to make it easier?
			# make this faster
			for entry in all_entries:
				(path, sep, shortname) = entry.key.rpartition('/')
				# this SHOULD always be a int
				if shortname == 'user_added' and entry.value.type == gconf.VALUE_INT and entry.value.get_int() == 1:				
					# split it so we can get the id
					(spath, sep, apnid) = path.rpartition('/')		
					apnlist.append(apnid)					
		return apnlist
	
	def get_apnid_from_name(self, apnname):
		# get all IAP's
		dirs = self.client.all_dirs('/system/osso/connectivity/IAP')
		for subdir in dirs:
			# get all sub entries.. this might be costy?
			all_entries = self.client.all_entries(subdir)
			# this is a big loop as well, possible to make it easier?
			for entry in all_entries:
				(path, sep, shortname) = entry.key.rpartition('/')

				# this SHOULD always be a string
				if shortname == 'name':				
					if entry.value.type == gconf.VALUE_STRING:
						_value = entry.value.get_string()
					if _value == apnname:
						# split it so we can get the id
						(spath, sep, apnid) = path.rpartition('/')		
						return apnid		
		return None
	
		
if __name__ == '__main__':
	config = fAPN_helper()
	#config.remove_apn("NEWAPNNAME")
	#print config.get_simimsi_from_apn()
	#print config.get_apn_list_useradded()
	#config.add_new_apn("ä test 123.de ä ", config.get_simimsi_from_apn())
	#print config.get_simimsi_from_apn()