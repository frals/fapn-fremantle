#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
## GNU General Public License for more details.
##
import pypackager
import os

if __name__ == "__main__":
	try:
		os.chdir(os.path.dirname(sys.argv[0]))
	except:
		pass
	print

	p=pypackager.PyPackager("fapn") #This is the package name and MUST be in lowercase! (using e.g. "mClock" fails miserably...)
	p.description='GUI for adding a new GPRS APN'
	p.license='gpl'
	p.version = '0.5' #Version of your software, e.g. "1.2.0" or "0.8.2"
	p.buildversion = '1' #Build number, e.g. "1" for the first build of this version of your software. Increment for later re-builds of the same version of your software.
	p.author='Nick Leppänen Larsson'
	p.url='http://www.frals.se'
	p.email='frals@frals.se'
	p.depends = 'python2.5, python2.5-hildon, python2.5-gtk2, gnome-python, python-osso'
	p.section='user/network'
	p.icon = '/home/user/fapn/fapnx.png'
	p.arch='all' #should be all for python, any for all arch
	p.urgency='low' #not used in maemo onl for deb os
	p.distribution='fremantle'
	p.repository='extras-devel'
	p.bugtracker='mailto:frals@frals.se' 
	p.displayname='fAPN'
	p.changelog="""
	* non-ascii chars stripped from gconfdirname
* dots removed from gconfdirname
	"""
	#p.postinstall="""#!/bin/sh
	#/usr/bin/dbus-send --system --type=method_call --dest=com.nokia.wappush /com/nokia/wappush com.nokia.wappush.register string:'x-wap-application:mms.ua' string:'se.frals.mms' string:'/se/frals/mms'
	#/usr/bin/gconftool-2 -s /apps/fmms/firstlaunch --type int 1
	#return 0""" 
	
	#Set here your post install script
	#p.postremove="""#!/bin/sh
	#/usr/bin/dbus-send --system --type=method_call --dest=com.nokia.wappush /com/nokia/wappush com.nokia.wappush.deregister string:'x-wap-application:mms.ua'
	#return 0""" #Set here your post remove script
	
	#p.preinstall="""#!/bin/sh
	#chmod +x /usr/bin/mclock.py""" #Set here your pre install script
	#p.preremove="""#!/bin/sh\n"\
	#"/usr/bin/dbus-send --print-reply --system --type=method_call --dest=com.nokia.wappush /com/nokia/wappush com.nokia.wappush.deregister string:'x-wap-application:mms.ua'"""
	#Set here your pre remove script

	#Text with changelog information to be displayed in the package "Details" tab of the Maemo Application Manager
	

	dir_name = "src" #Name of the subfolder containing your package source files (e.g. usr\share\icons\hicolor\scalable\myappicon.svg, usr\lib\myapp\somelib.py). We suggest to leave it named src in all projects and will refer to that in the wiki article on maemo.org

	#Thanks to DareTheHair from talk.maemo.org for this snippet that recursively builds the file list 
	for root, dirs, files in os.walk(dir_name):
		real_dir = root[len(dir_name):]
		fake_file = []
		for f in files:
			fake_file.append(root + os.sep + f + "|" + f)
		if len(fake_file) > 0:
			p[real_dir] = fake_file

	print p
	print p.generate(build_binary=False,build_src=True)
	print p.generate(build_binary=True,build_src=False)
	#r = p.generate(version,build,changelog=changeloginformation,tar=True,dsc=True,changes=True,build=False,src=True)