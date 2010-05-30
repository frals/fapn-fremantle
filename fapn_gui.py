#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
""" GUI for adding APN in maemo fremantle

@author: Nick Leppänen Larsson <frals@frals.se>
@license: GNU GPL
"""
import gtk
import hildon
import time
import osso
import fapnhelper

class fAPN_GUI(hildon.Program):

	def __init__(self):
		self.helper = fapnhelper.fAPN_helper()
		
		hildon.Program.__init__(self)
		self.program = hildon.Program.get_instance()
		
		self.window = hildon.StackableWindow()
		self.window.set_title("fAPN")
		self.program.add_window(self.window)
		self.osso_c = osso.Context("fAPN", "0.1", False)
		self.osso_rpc = osso.Rpc(self.osso_c)
		self.plugin = osso.Plugin(self.osso_c)
		self.window.connect("delete_event", self.quit)
		
		self.pan = hildon.PannableArea()
		self.pan.set_property("mov-mode", hildon.MOVEMENT_MODE_BOTH)
		
		butVBox = gtk.VBox()
		
		button = hildon.GtkButton(gtk.HILDON_SIZE_FINGER_HEIGHT)
		button.set_label("Add new APN")
		button.connect('clicked', self.adder_clicked)
		
		butVBox.pack_start(button, False, False, 0)

		self.create_buttons()
		
		butVBox.pack_start(self.buttonsVBox, False, False, 10)

		self.pan.add_with_viewport(butVBox)
		#pan.add_with_viewport(buttonsVBox)
		
		self.window.add(self.pan)
	
		self.menu = self.create_menu()
		self.window.set_app_menu(self.menu)
		self.window.show_all()
		self.add_window(self.window)

	
	def create_buttons(self):
		self.buttonsVBox = gtk.VBox()	
		apnlist = self.helper.get_apn_list_useradded()
		for apid in apnlist:
			bHBox = gtk.HBox()
			label = gtk.Label("Delete APN:")
			button = hildon.GtkButton(gtk.HILDON_SIZE_FINGER_HEIGHT)
			button.set_label(self.helper.get_apn_name_from_id(apid))
			button.connect('clicked', self.confirm_dialog, button, bHBox)
		
			bHBox.pack_start(label, True, True, 0)
			bHBox.pack_start(button, True, True, 0)
			
			bHBox.show_all()
			self.buttonsVBox.pack_start(bHBox, False, False, 0)
		self.buttonsVBox.show_all()
	
	def remove_apn(self, widget, apnid):
		self.confirm_dialog(apnid)
	
	def confirm_dialog(self, widget, apnid, bHBox):
		dialog = gtk.Dialog()
		dialog.set_transient_for(self.window)
		dialog.set_title("Confirm deletion")

		allVBox = gtk.VBox()
	
		apname = str(self.helper.get_apnid_from_name(apnid.get_label()))

		apnHBox = gtk.HBox()
		apn_label = gtk.Label("Are you sure you want to delete " + apname)
		apnHBox.pack_start(apn_label, False, True, 0)

		allVBox.pack_start(apnHBox, False, False, 0)

		#allVBox.pack_end(buttonHBox)
		allVBox.show_all()
		dialog.vbox.add(allVBox)
		dialog.add_button("Yes", gtk.RESPONSE_APPLY)
		#dialog.add_button("No", gtk.RESPONSE_CANCEL)
		#dialog.show_all()
		while 1:
			ret = dialog.run()
			print ret
			ret2 = self.confirm_dialog_clicked(ret, apname)
			if ret2 == 0:
				print "DESTROYING"
				apnid.destroy()
				bHBox.destroy()
				break
			elif ret2 == None: 
				break
		dialog.destroy()
		return ret
	
	def confirm_dialog_clicked(self, action, apname):
		if action == gtk.RESPONSE_APPLY:
			ret = self.helper.remove_apn(apname)
			if ret == 0:
				banner = hildon.hildon_banner_show_information(self.window, "", "APN " + apname + " deleted")
				return 0
			else:
				banner = hildon.hildon_banner_show_information(self.window, "", "Failed to delete " + apname)
		else:
			pass
	
	def adder_clicked(self, widget):
		self.adder_dialog()
		
	def adder_dialog(self):
		dialog = gtk.Dialog()
		dialog.set_transient_for(self.window)
		dialog.set_title("Add new APN")
		
		allVBox = gtk.VBox()
		
		apnHBox = gtk.HBox()
		apn_label = gtk.Label("Name:")
		self.apnEntry = hildon.Entry(gtk.HILDON_SIZE_FINGER_HEIGHT)
		
		apnHBox.pack_start(apn_label, False, True, 0)
		apnHBox.pack_start(self.apnEntry, True, True, 0)
		
		allVBox.pack_start(apnHBox, False, False, 0)
		
		allVBox.show_all()
		dialog.vbox.add(allVBox)
		dialog.add_button("Add", gtk.RESPONSE_APPLY)
		#dialog.show_all()
		while 1:
			ret = dialog.run()
			ret2 = self.adder_button_clicked(ret, dialog)
			if ret2 == 0 or ret2 == None: 
				break
			
		dialog.destroy()
		return ret
		
	def adder_button_clicked(self, action, dialog):
		if action == gtk.RESPONSE_APPLY:
			imsi = self.helper.get_simimsi_from_apn()
			self.helper.add_new_apn(self.apnEntry.get_text(), imsi)
			note = osso.SystemNote(self.osso_c)
			note = hildon.hildon_note_new_information(self.window, "APN ADDED!\nExit this program and edit it in the Control Panel.\nThank you!")
			dialog.hide()
			note.run()
			note.destroy()
			bHBox = gtk.HBox()
			label = gtk.Label("Delete APN:")
			button = hildon.GtkButton(gtk.HILDON_SIZE_FINGER_HEIGHT)
			button.set_label(self.apnEntry.get_text())
			button.connect('clicked', self.confirm_dialog, button, bHBox)

			bHBox.pack_start(label, True, True, 0)
			bHBox.pack_start(button, True, True, 0)

			bHBox.show_all()
			self.buttonsVBox.pack_start(bHBox, False, False, 0)
			return 0
		else:
			pass
		
	def create_menu(self):
		menu = hildon.AppMenu()
		
		about = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
		about.set_label("About")
		about.connect('clicked', self.menu_button_clicked)

		netconnsettings = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
		netconnsettings.set_label("Internet Connection Settings")
		netconnsettings.connect('clicked', self.menu_button_clicked)

		menu.append(netconnsettings)
		menu.append(about)
		menu.show_all()
		return menu
		
	def menu_button_clicked(self, button):
		buttontext = button.get_label()
		if buttontext == "About":
			ret = self.create_about_dialog()
		elif buttontext == "Internet Connection Settings":
			self.plugin.plugin_execute("libinternetsettings.so", True, self.window)
		
	def create_about_dialog(self):
		dialog = gtk.AboutDialog()
		dialog.set_transient_for(self.window)
		dialog.set_name("fAPN")
		fapn_logo = gtk.gdk.pixbuf_new_from_file("/opt/fapn/fapn_64px.png")
		dialog.set_logo(fapn_logo)                                   
		dialog.set_comments('Adding GPRS APN in Fremantle')
		dialog.set_version("0.5")                                                
		dialog.set_copyright("By Nick Leppänen Larsson (aka frals)")
		gtk.about_dialog_set_url_hook(lambda dialog, link: self.osso_rpc.rpc_run_with_defaults("osso_browser", "open_new_window", (link,)))
		dialog.set_website("http://www.frals.se/")                                  
		dialog.connect("response", lambda d, r: d.destroy())                      
		dialog.show() 

	""" lets call it quits! """
	def quit(self, *args):
		gtk.main_quit()

	def run(self):
		self.window.show_all()
		gtk.main()
		
if __name__ == "__main__":
	app = fAPN_GUI()
	app.run()