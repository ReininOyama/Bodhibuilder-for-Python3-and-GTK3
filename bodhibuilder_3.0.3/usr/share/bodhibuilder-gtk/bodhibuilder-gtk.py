#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#
# Bodhibuilder script to create or backup a Bodhi Linux ISO
# 
# Modified to bodhibuilder from remastersys.
#
# For use on Bodhi Linux 3.0.0 and up.
#
# Copyright (C) 2015
# Stace Fauske <stace.fauske@gmail.com> <-sef>
# Jeff Hoogland <JeffHoogland@Linux.com>
# Charles van de Beek <charles.beek@gmail.com> Charles@Bodhi
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ORIGINAL COMMENTS:
#Licence: GPLv3.0
#Copyright: Krasimir S. Stefanov <lokiisyourmaster@gmail.com>
#Modified by: Tony Brijeski <tb6517@yahoo.com>
#Modified to 'bodhibuilder' by: Stace Fauske <stace.fauske@gmail.com> <-sef> - (C) 2015
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import sys
import os
import os.path
import stat
import locale
import gettext
import re
import shutil
import datetime
import time
import subprocess
import shlex
import configparser
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Vte, GLib

APP = "bodhibuilder"
DIR = "/usr/share/locale"
APP_VERSION = "3.0.3"

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_ = gettext.gettext

LOCALE = locale.getlocale()[0]


class appgui:
    def __init__(self):
        self.pathname = os.path.dirname(sys.argv[0])
        self.abspath = os.path.abspath(self.pathname)
        self.gladefile = self.abspath + "/bodhibuilder-gtk.ui"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.window1 = self.builder.get_object("window1")
        self.working_dir = os.path.expanduser("~")
        self.callback_id = 0
        dic = {
            "on_button1_clicked" : self.on_button1_clicked,
            "on_button2_clicked" : self.on_button2_clicked,
            "on_button3_clicked" : self.on_button3_clicked,
            "on_button4_clicked" : self.on_button4_clicked,
            "on_button5_clicked" : self.on_button5_clicked,
            "on_button6_clicked" : self.on_button6_clicked,
            "on_button7_clicked" : self.quit,
            "on_button8_clicked" : self.on_button8_clicked,
            "on_button9_clicked" : self.on_button9_clicked,
            "on_button10_clicked" : self.on_button10_clicked,
            "on_button11_clicked" : self.on_button11_clicked,
            "on_button12_clicked" : self.on_button12_clicked,
            "on_button13_clicked" : self.on_button13_clicked,
            "on_window1_delete_event" : self.quit
        }
        self.builder.connect_signals(self)
        #self.window1.signal_autoconnect (dic)
        self.v = Vte.Terminal()
        self.builder.get_object("vbox2").add(self.v)
        self.v.show()
        self.load_settings()
        msg_info(_("It is necessary to close all other windows and unmount any network shares while running Bodhibuilder Backup. Please do so now and then click OK when you are ready to continue."), self.builder.get_object("window1"))
    
    def on_button7_clicked(self,widget):
        self.update_conf()
        self.window1.destroy()
        exit(0)
    
    def on_window1_delete_event(self,widget,data = None):
        self.update_conf()
    
    def on_window2_delete_event(self,widget,data = None):
        self.update_conf()
    
    def on_window3_delete_event(self,widget,data = None):
        self.update_conf()
     
    def run_command(self, cmd, done_callback):
        argv1 = shlex.split(cmd)
        self.callback_id = self.v.connect ("child-exited", done_callback)
        #self.v.fork_command(argv[0], argv)
        #self.v.feed_child('set -e\n')
        self.builder.get_object("notebook1").set_current_page(2)
        #self.v.show()
        # async
        self.v.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            argv1,
            None,
            GLib.SpawnFlags.DEFAULT,
            None, None,
            -1, None,
            None,
            None
        )
        #self.window1.set_child(self.v)
        #self.v.feed_child(cmd+'\nexit 0\n')

    #~ Backup Button
    def on_button1_clicked(self,widget):
        self.update_conf()
        if not msg_confirm(_("You have selected Backup Mode. Do not interrupt this process. Click OK to Start the Backup LiveCD/DVD process."), self.builder.get_object("window1")):
            return
        self.run_command('bodhibuilder backup', self.on_backup_done)

    def on_backup_done(self, widget, status):
        if status == 0:
            WORKDIR = self.builder.get_object("entry6").get_text()
            CUSTOMISO = self.builder.get_object("entry3").get_text()
            msg_info(_("Your %(iso)s and %(iso)s.md5 files are ready in %(dir)s. It is recommended to test it in a virtual machine or on a rewritable cd/dvd to ensure it works as desired. Click on OK to return to the main menu.") 
                % ({"iso" : CUSTOMISO, "dir" : WORKDIR+'/bodhibuilder'}), self.builder.get_object("window1"))
        else:
            msg_error(_("The process was not started!"), self.builder.get_object("window1"))
        self.builder.get_object("notebook1").set_current_page(0)
        self.v.handler_disconnect(self.callback_id)

    #~ Dist Button
    def on_button2_clicked(self,widget):
        self.update_conf()
        if not msg_confirm(_("You have selected Dist Mode. Click OK to Start the Distributable LiveCD/DVD process."), self.builder.get_object("window1")):
            return
        self.run_command('bodhibuilder dist', self.on_dist_done)

    def on_dist_done(self, widget, status):
        
        if status == 0:
            WORKDIR = self.builder.get_object("entry6").get_text()
            CUSTOMISO = self.builder.get_object("entry3").get_text()
            msg_info(_("Your %(iso)s and %(iso)s.md5 files are ready in %(dir)s. It is recommended to test it in a virtual machine or on a rewritable cd/dvd to ensure it works as desired. Click on OK to return to the main menu.") % ({"iso" : CUSTOMISO, "dir" : WORKDIR+'/bodhibuilder'}))
        else:
            msg_error(_("The process was net started!"), self.builder.get_object("window1"))
        self.builder.get_object("notebook1").set_current_page(0)
        self.v.handler_disconnect(self.callback_id)
        
    #~ Distcdfs Button
    def on_button3_clicked(self,widget):
        self.update_conf()
        if not msg_confirm(_("You have selected Dist CDFS Mode. Click OK to Start the Distributable LiveCD/DVD filesystem build process.")):
            return
        self.run_command('bodhibuilder dist cdfs', self.on_dist_cdfs_done)

    def on_dist_cdfs_done(self, widget, pid, error, data = None):
        if pid == 0:
            WORKDIR = self.builder.get_object("entry6").get_text()
            CUSTOMISO = self.builder.get_object("entry3").get_text()
            msg_info(_("Your livecd filesystem is ready in %s. You can now add files to the cd and then run the Distiso option when you are done. Click on OK to return to the main menu.") % WORKDIR+'/bodhibuilder')
        else:
            msg_error(_("The process was not started!"), self.builder.get_object("window1"))
        self.builder.get_object("notebook1").set_current_page(0)
        self.v.handler_disconnect(self.callback_id)
    
    #~ Distiso Button
    def on_button4_clicked(self,widget):
        self.update_conf()
        WORKDIR = self.builder.get_object("entry6").get_text()
        if os.path.exists(WORKDIR+'/bodhibuilder/ISOTMP/casper/filesystem.squashfs'):
            if not msg_confirm(_("You have selected Dist ISO Mode. Click OK to create the iso file.")):
                self.builder.get_object("window1").show()
                return
            self.run_command('bodhibuilder dist iso', self.on_dist_iso_done)
        else:
            msg_error(_("The livecd filesystem does not exist. Click OK to go back to the main menu and try the normal Dist mode or the Dist CDFS again."))

    def on_dist_iso_done(self, widget, pid, error, data = None):
        if pid != 0:
            WORKDIR = self.builder.get_object("entry6").get_text()
            CUSTOMISO = self.builder.get_object("entry3").get_text()
            msg_info(_("Your %(iso)s and %(iso)s.md5 files are ready in %(dir)s. It is recommended to test it in a virtual machine or on a rewritable cd/dvd to ensure it works as desired. Click on OK to return to the main menu.") % ({"iso" : CUSTOMISO, "dir" : WORKDIR+'/bodhibuilder'}))
        else:
            msg_error(_("The process not started!"), self.builder.get_object("window1"))
        self.builder.get_object("notebook1").set_current_page(0)
        self.v.handler_disconnect(self.callback_id)
        
    #~ Clear Button
    def on_button5_clicked(self,widget):
        self.update_conf()
        if not msg_confirm(_("This will remove all the files from the temporary directory. Click OK to proceed.")):
            return
        #os.system('bodhibuilder clean')
        self.run_command('bodhibuilder clean', self.on_clean_done)
        #msg_info(_("Completed. Click OK to return to the main menu."))

    def on_clean_done(self, widget, pid, error, data = None):
        if pid != 0:
            msg_info(_("Completed. Click OK to return to the main menu."))
        else:
            msg_error(_("The process was not started!"), self.builder.get_object("window1"))
        self.builder.get_object("notebook1").set_current_page(0)
        self.v.handler_disconnect(self.callback_id)
        
    #~ About button
    def on_button6_clicked(self,widget):
        # show about dialog
        about = Gtk.AboutDialog()
        about.set_position(Gtk.WindowPosition.CENTER)
        about.set_program_name(_("Bodhibuilder"))
        about.set_version(APP_VERSION)
        about.set_authors([_(" "),
            _("       -- bodhibuilder --"),
            _("Stace Fauske <stace.fauske@gmail.com>"),
            _("Jeff Hoogland <JeffHoogland@Linux.com>"),
            _("Charles van de Beek <charles.beek@gmail.com> Charles@Bodhi"),
            _(" "),
            _("       -- remastersys --"),
            _("Krasimir S. Stefanov <lokiisyourmaster@gmail.com>"),
            _("Tony Brijeski <tb6517@yahoo.com>")
        ])
        about.set_website("http://forums.bodhilinux.com/")
        translators = [
            _("Bulgarian - Krasimir S. Stefanov <lokiisyourmaster@gmail.com>"),
            _("English - Krasimir S. Stefanov <lokiisyourmaster@gmail.com>"), 
            _("Traditional Chinese - Kent Chang <kentxchang@gmail.com>")
        ]

        about.set_translator_credits('\n'.join(translators))
        about.set_logo_icon_name('bodhibuilder-gtk')
        license = _('''PyGTK GUI for Bodhibuilder
Copyright (C) 2011 Krasimir S. Stefanov, Tony Brijeski
Modified to Bodhibuilder by Stace Fauske - (C) 2015
This is Free Software
Originally Remastersys, modified to Bodhibuilder
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
Licence: GPLv3.0
http://www.gnu.org/licenses/.''')
        about.set_license(license)
        about.run()
        about.hide()

    #~ Working dir selection pop-up
    def on_button8_clicked(self,widget):
        dialog = Gtk.FileChooserDialog(_("Select working directory"),
            None,
            Gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            
        dialog.set_default_response(Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.builder.get_object("entry6").set_text(dialog.get_filename())
        dialog.destroy()

    #~ Select boot menu picture for Live CD
    def on_button9_clicked(self,widget):
        dialog = Gtk.FileChooserDialog(title=_("Select 640x480 PNG image..."),action=Gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_current_folder(self.working_dir)
        
        filter = Gtk.FileFilter()
        filter.set_name(_("PNG Images"))
        filter.add_mime_type("image/png")
        dialog.add_filter(filter)

        filter = Gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            now = datetime.datetime.now()
            filename = dialog.get_filename()
            dialog.destroy()  
            self.working_dir = os.path.dirname(filename)
            shutil.move("/etc/bodhibuilder/isolinux/splash.png", "/etc/bodhibuilder/isolinux/splash.png." + now.strftime("%Y%m%d%H%M%S"))
            shutil.copy(filename, "/etc/bodhibuilder/isolinux/splash.png")
            msg_info(_("%s has been copied to /etc/bodhibuilder/isolinux/splash.png becoming the default background for the LIVE menu.") % filename)
        else:
            dialog.destroy()                  

    #~ Select boot menu picture for installed environment
    def on_button10_clicked(self,widget):
        dialog = Gtk.FileChooserDialog(title=_("Select image..."),action=Gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_current_folder(self.working_dir)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            now = datetime.datetime.now()
            filename = dialog.get_filename()
            self.working_dir = os.path.dirname(filename)
            name, ext = os.path.splitext(filename)
            grub_bg = "/etc/bodhibuilder/grub" + ext
            shutil.copy(filename, grub_bg)
            dialog.destroy()
            
            
            grub = open('/etc/default/grub').read()
            
            m = re.search('(#?)GRUB_BACKGROUND=.*', grub)
            if m != None:
                grub.replace(m.group(0), 'GRUB_BACKGROUND="%s"' % grub_bg)
            else:
                grub += '\nGRUB_BACKGROUND="%s"' % grub_bg
            
            f = open('/etc/default/grub', 'w+')
            f.write(grub)
            f.close()
            
            msg_info(_("%(filename)s has been copied to %(grub_bg)s and is the default background for grub. Click OK to update grub with the new settings so you can see your picture on the next boot.") % ({'filename':filename, 'grub_bg':grub_bg}))
            self.builder.get_object("label17").hide()
            self.builder.get_object("progressbar1").show()
            process = subprocess.Popen(['update-grub'], stdout=subprocess.PIPE, stderr=None)
            while process.poll() == None:
                while Gtk.events_pending():
                    Gtk.main_iteration_do()
                time.sleep(.1) 
                self.builder.get_object("progressbar1").pulse()
            process.wait()
            self.builder.get_object("progressbar1").hide()
            self.builder.get_object("label17").show()
            msg_info(_("GRUB has been updated."))
        else:
            dialog.destroy()        

    #~ Select user whose settings to use
    def on_button11_clicked(self,widget):
        self.builder.get_object("window1").hide()
        def cancel(widget, other = None):
            ns.builder.get_object("window2").destroy()
            self.builder.get_object("window1").show()
        
        def ok(widget, other = None):
            model, treeiter = ns.builder.get_object("treeview1").get_selection().get_selected()
            username = model.get(treeiter, 0)[0]
            ns.builder.get_bject("progressbar1").show()
            ns.builder.get_object("hbuttonbox1").set_sensitive(False)
            process = subprocess.Popen(['bodhibuilder-skelcopy', username], stdout=subprocess.PIPE, stderr=None)
            while process.poll() == None:
                while Gtk.events_pending():
                    Gtk.main_iteration_do()
                time.sleep(.1) 
                ns.builder.get_object("progressbar1").pulse()
            process.wait()
            ns.builder.get_object("progressbar1").hide()
            ns.builder.get_object("hbuttonbox1").set_sensitive(True)
            ns.builder.get_object("window2").destroy()
            self.builder.get_object("window1").show()
            
        
        ns = Namespace()
#       ns.window = Gtk.glade.XML(self.gladefile,"window2" ,APP)
        ns.builder = self.builder
        Gtk.glade.bindtextdomain(APP,DIR)
        dic = {
            "on_window2_delete_event" : (cancel)
            , "on_button1_clicked" :  (cancel)
            , "on_button2_clicked" :  (ok)
        }
#        ns.window.signal_autoconnect (dic)


        ns.liststore = Gtk.ListStore(str, str)
        ns.builer.get_object("treeview1").set_model(ns.liststore)
        ns.tvcolumn1 = Gtk.TreeViewColumn(_('User'))        
        ns.tvcolumn2 = Gtk.TreeViewColumn(_('Home directory'))        
        
        ns.cell1 = Gtk.CellRendererText()
        ns.cell2 = Gtk.CellRendererText()

        ns.tvcolumn1.pack_start(ns.cell1, True)
        ns.tvcolumn2.pack_start(ns.cell2, True)
        ns.tvcolumn1.set_attributes(ns.cell1, text=0)
        ns.tvcolumn2.set_attributes(ns.cell2, text=1)

        ns.builder.get_object("treeview1").append_column(ns.tvcolumn1)
        ns.builder.get_object("treeview1").append_column(ns.tvcolumn2)
        

        passwd = open('/etc/passwd', 'r').read().strip().split('\n')
        for row in passwd:
            data = row.split(':')
            if int(data[2]) >= 1000 and int(data[2]) <= 1100:
                ns.liststore.append([data[0], data[5]])
        ns.builder.get_object("window2").show()
    
    def on_button20_clicked(self,widget):
        self.update_conf()
    
    def on_button102_clicked(self,widget):
        self.update_conf()
    
    def on_button21_clicked(self,widget):
        self.update_conf()
    
    def on_button300_clicked(self,widget):
        self.update_conf()
    
    def on_button400_clicked(self,widget):
        self.update_conf()
    
    def on_button104_clicked(self,widget):
        self.update_conf()
    
    def on_checkbutton100_toggled(self,widget):
        self.update_conf()
    
    #~ Select Plymouth Theme
    def on_button12_clicked(self,widget):
        self.builder.get_object("window1").hide()

        def auto(widget, other = None):
            active = ns.builder.get_object("checkbutton1").get_active()
            ns.builder.get_object("treeview1").set_sensitive(not active)
            
        def update_initramfs():
            ns.builder.get_object("progressbar1").show()
            ns.builder.get_object("hbuttonbox1").set_sensitive(False)
            uname = os.popen('uname -r').read().strip()
            process = subprocess.Popen(['mkinitramfs', '-o', '/boot/initrd.img-'+uname, uname], stdout=subprocess.PIPE, stderr=None)
            while process.poll() == None:
                while Gtk.events_pending():
                    Gtk.main_iteration_do()
                time.sleep(.1) 
                ns.builder.get_object("progressbar1").pulse()
            process.wait()
            ns.builder.get_object("progressbar1").hide()
            ns.builder.get_object("hbuttonbox1").set_sensitive(True)
        
        def cancel(widget, other = None):
            ns.builder.get_object("window3").destroy()
            self.builder.get_object("window1").show()
        
        def ok(widget, other = None):
            if ns.builder.get_object("checkbutton1").get_active():
                os.system("update-alternatives --auto default.plymouth")
                update_initramfs()
                msg_info(_("Done! Now plymouth will use the default, auto-selected theme."))
            else:
                model, treeiter = ns.builder.get_object("treeview1").get_selection().get_selected()
                if treeiter == None:
                    msg_error(_("Please, select a theme!"))
                    return
                theme = model.get(treeiter, 1)[0]
                os.system('update-alternatives --set default.plymouth "%s"' % theme)
                update_initramfs()
            ns.builder.get_object("window3").destroy()
            self.builder.get_object("window1").show()
            
        def create(widget, other = None):
            theme_name = msg_input('', _('Enter your plymouth theme name. eg. Bodhibuilder Theme (please use only alphanumeric characters)'), _('Name:'), 'Bodhibuilder Theme')          
            if theme_name == False or theme_name == None:
                return
            elif theme_name == '':
                msg_error(_("You must specify theme name!"))
                return
            
            theme_name_fixed = theme_name.replace(' ','-').replace('/','-').replace('..','-').replace('\\','-')
            theme_dir = "/lib/plymouth/themes/" + theme_name_fixed
            
            if os.path.exists(theme_dir):
                overwrite = msg_confirm(_('The theme "%s" already exists! Do you want to overwrite it?') % theme_name)
                if overwrite:
                    shutil.rmtree(theme_dir)
                else:
                    return
            
            dialog = Gtk.FileChooserDialog(title=_("Select 1920x1080 PNG image..."),action=Gtk.FILE_CHOOSER_ACTION_OPEN,
                buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
            dialog.set_default_response(Gtk.ResponseType.OK)
            dialog.set_current_folder(self.working_dir)
            
            filter = Gtk.FileFilter()
            filter.set_name(_("PNG Images"))
            filter.add_mime_type("image/png")
            dialog.add_filter(filter)

            filter = Gtk.FileFilter()
            filter.set_name(_("All files"))
            filter.add_pattern("*")
            dialog.add_filter(filter)
            
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                filename = dialog.get_filename()
                self.working_dir = os.path.dirname(filename)
                dialog.destroy()
                while Gtk.events_pending():
                    Gtk.main_iteration_do()
                os.makedirs(theme_dir)
                now = datetime.datetime.now()
                theme_pic = os.path.join(theme_dir, os.path.basename(filename))
                shutil.copy(filename, theme_pic)
                shutil.copy('/etc/bodhibuilder/plymouth/bodhibuilder-theme/progress_bar.png', theme_dir+'/progress_bar.png')
                shutil.copy('/etc/bodhibuilder/plymouth/bodhibuilder-theme/progress_box.png', theme_dir+'/progress_box.png')
                script_name = "/lib/plymouth/themes/"+theme_name_fixed+"/"+theme_name_fixed+".script"
                script = open("/etc/bodhibuilder/plymouth/bodhibuilder-theme/bodhibuilder-theme.script").read().replace("__THEMEPIC__", os.path.basename(theme_pic))
                open(script_name, 'w+').write(script)
                
                config_name = "/lib/plymouth/themes/"+theme_name_fixed+"/"+theme_name_fixed+".plymouth"
                config = open("/etc/bodhibuilder/plymouth/bodhibuilder-theme/bodhibuilder-theme.plymouth").read()
                config = config.replace("__THEMENAME__", theme_name)
                config = config.replace("__THEMEDIR__", theme_name_fixed)
                open(config_name, 'w+').write(config)
                
                
                os.system('update-alternatives --install /lib/plymouth/themes/default.plymouth default.plymouth "%(config_name)s" 80' % ({'config_name': config_name}))
                os.system('update-alternatives --set default.plymouth "%(config_name)s"' % ({'config_name': config_name}))
                
                ns.builder.get_object("checkbutton1").set_active(False)
                
                update_initramfs()
                
                msg_info(_("Your plymouth theme named %(theme_name)s with the picture %(theme_pic)s has been created.") % ({'theme_name': theme_name, 'theme_pic': theme_pic}))
            else:
                dialog.destroy()
                shutil.rmtree(theme_dir)
            list_themes()
            
        def preview(widget, other = None):
            if not os.path.isfile('/lib/plymouth/renderers/x11.so'):
                msg_error(_("In order to be able to preview plymouth themes, you have to install plymouth-x11!"))
                return
                
            output = os.popen('update-alternatives --display default.plymouth').read().strip()
            m = re.search('default.plymouth - (manual|auto) mode', output)
            if m == None:
                ns.builder.get_object("window3").show()
                return
            mode = m.group(1)
            
            if mode == 'auto':
                ns.builder.get_object("window3").hide()
                while Gtk.events_pending():
                    Gtk.main_iteration_do()
                os.system("plymouth-preview")
                ns.builder.get_object("window3").show()
            else:
                model, treeiter = ns.builder.get_object("treeview1").get_selection().get_selected()
                if treeiter == None:
                    msg_error(_("Please, select a theme!"))
                    return
                theme = model.get(treeiter, 1)[0]
                ns.builder.get_object("window3").hide()
                while Gtk.events_pending():
                    Gtk.main_iteration_do()
                    
                    
                output = os.popen('update-alternatives --display default.plymouth').read().strip()
                m = re.search('default.plymouth - (manual|auto) mode', output)
                if m == None:
                    ns.builder.get_object("window3").show()
                    return
                mode = m.group(1)
                
                m = re.search('link\s*currently\s*points\s*to\s*(.*)', output)
                if m == None:
                    ns.builder.get_object("window3").show()
                    return
                link = m.group(1)

                os.system('update-alternatives --set default.plymouth "%s"' % theme)
                os.system("plymouth-preview")
                ns.builder.get_object("window3").show()
                
                if mode == 'auto':
                    os.system('update-alternatives --auto default.plymouth')
                else:
                    os.system('update-alternatives --set default.plymouth "%s"' % link)
        
        def list_themes():
            ns.liststore.clear()
            output = os.popen('update-alternatives --display default.plymouth').read().strip()
            m = re.search('default.plymouth - (manual|auto) mode', output)
            if m == None:
                ns.builder.get_object("window3").show()
                return
            mode = m.group(1)
            m = re.search('link\s*currently\s*points\s*to\s*(.*)', output)
            if m == None:
                ns.builder.get_object("window3").show()
                return
            link = m.group(1)
            lines = os.popen('update-alternatives --list default.plymouth').read().strip().split('\n')
            for row in lines:
                if row != "":
                    config = ConfigParser.ConfigParser()
                    config.readfp(open(row))
                    name = config.get('Plymouth Theme', 'Name')
                    iter = ns.liststore.append([name, row])
                    if mode == 'manual' and row == link:
                        ns.builder.get_object("treeview1").get_selection().select_iter(iter)
            ns.builder.get_object("checkbutton1").set_active(mode == 'auto')
            
        ns = Namespace()
#        ns.window = Gtk.glade.XML(self.gladefile,"window3" ,APP)
        ns.builder = self.builder
        Gtk.glade.bindtextdomain(APP,DIR)
        dic = {
            "on_window3_delete_event" : (cancel)
            , "on_button1_clicked" :  (cancel)
            , "on_button2_clicked" :  (ok)
            , "on_button3_clicked" :  (create)
            , "on_button4_clicked" :  (preview)
            , "on_checkbutton1_toggled" :  (auto)
        }
#        ns.window.signal_autoconnect (dic)


        ns.liststore = Gtk.ListStore(str, str)
        ns.builder.get_object("treeview1").set_model(ns.liststore)
        ns.tvcolumn1 = Gtk.TreeViewColumn(_('Name'))        
        ns.tvcolumn2 = Gtk.TreeViewColumn(_('Directory'))        
        
        ns.cell1 = Gtk.CellRendererText()
        ns.cell2 = Gtk.CellRendererText()

        ns.tvcolumn1.pack_start(ns.cell1, True)
        ns.tvcolumn2.pack_start(ns.cell2, True)
        ns.tvcolumn1.set_attributes(ns.cell1, text=0)
        ns.tvcolumn2.set_attributes(ns.cell2, text=1)

        ns.builder.get_object("treeview1").append_column(ns.tvcolumn1)
        ns.builder.get_object("treeview1").append_column(ns.tvcolumn2)
        list_themes()
        ns.builder.get_object("window3").show()
        
    #~ Clear /etc/skel button
    def on_button13_clicked(self,widget):
        if msg_confirm(_("Are you sure you want to delete the contents of /etc/skel?")):
            shutil.rmtree('/etc/skel/')
            os.makedirs('/etc/skel/')
       
    def quit(self, widget, data = None):
        self.update_conf()
#        Gtk.main_quit()
        self.window1.destroy()
        exit(0)
        
    def load_settings(self):
        config_f = open("/etc/bodhibuilder.conf")
        config_txt = config_f.read()
        config_f.close()
        
        self.builder.get_object("entry1").set_text(
            self.getvalue('LIVEUSER', config_txt, 'custom'))

        self.builder.get_object("entry2").set_text(
            self.getvalue('LIVECDLABEL', config_txt, 'Custom Live CD'))

        self.builder.get_object("entry3").set_text(
            self.getvalue('CUSTOMISO', config_txt, 'custom-$1.iso'))

        self.builder.get_object("entry4").set_text(
            self.getvalue('EXCLUDES', config_txt, ''))
    
        self.builder.get_object("entry5").set_text(
            self.getvalue('LIVECDURL', config_txt, 'http://www.bodhilinux.com'))

        self.builder.get_object("entry7").set_text(
            self.getvalue('SQUASHFSOPTS', config_txt, '-no-recovery -always-use-fragments -b 1M -no-duplicates'))

        self.builder.get_object("checkbutton1").set_active(
            self.getvalue('BACKUPSHOWINSTALL', config_txt, '1') == '1')
        
        workdir = self.getvalue('WORKDIR', config_txt, '/home/bodhibuilder')
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        self.builder.get_object("entry6").set_text(workdir)
        
        self.builder.get_object("checkbutton1").set_active(
            self.getvalue('BACKUPSHOWINSTALL', config_txt, '1').upper() == '1')

        self.builder.get_object("entry8").set_text(
            self.getvalue('DISTICONS', config_txt, ''))

        self.builder.get_object("entry9").set_text(
            self.getvalue('DISTLOCALE', config_txt, ''))

        self.builder.get_object("entry10").set_text(
            self.getvalue('DISTNAME', config_txt, 'Bodhi Linux'))

    def update_conf(self):
        if self.builder.get_object("checkbutton1").get_active():
            BACKUPSHOWINSTALL = '1'
        else:
            BACKUPSHOWINSTALL = '0'
            
        conf_content = '''
#Bodhibuilder Global Configuration File


# This is the temporary working directory and won't be included on the cd/dvd
WORKDIR="%(WORKDIR)s"


# Here you can add any other files or directories to be excluded from the live filesystem
#   Use absolute paths (from the root directory)
#   Exclude specific files using the path to the file = /path/to/file
#   Exclude specific directories using a trailing slash = /path/to/directory/
#   Exclude all directory contents with an asterisk = /path/to/directory/*
#   Exclude all matching sets of files or directories using an asterisk as a wildcard = /path/to/something*
#   If the entry does not exist as an actual file or directory, rsync & mksquashfs will simply skip over it
#   Separate each entry with a space
EXCLUDES="%(EXCLUDES)s"


# Here you can change the livecd/dvd username
#  In a 'dist' spin, this will be both the username and password.
#  In a 'backup' spin AND if lightdm autologin is enabled:
#  this will be the first attempted username for autlogin, if
#  this username is not found the currently logged-in username
#  will be used for autologin.
LIVEUSER="%(LIVEUSER)s"


# Here you can change the name of the livecd/dvd label
# This will be in the ubiquity icon label on the ISO
LIVECDLABEL="%(LIVECDLABEL)s"


# Here you can change the name of the ISO file that is created
#  I don't recommend spaces in this var due to it being used in a path location
#  If you desire spaces or other characters, some form of REGEX formatting
#  may work you'll have to test it out
CUSTOMISO="%(CUSTOMISO)s"


# Here you can change the mksquashfs options
#   OK to leave this empty, the defaults will use the best compression I know of (as of this writing)
SQUASHFSOPTS="%(SQUASHFSOPTS)s"


# Here you can prevent the Install icon from showing up on the desktop in backup mode. 0 - to not show 1 - to show 
BACKUPSHOWINSTALL="%(BACKUPSHOWINSTALL)s"


# Here you can change the url for the usb-creator info
LIVECDURL="%(LIVECDURL)s"


# Here you can specify icons or icon sets to INCLUDE.
#   List here the icons or sets you want to keep that are in this path:
#     /usr/share/icons/(icon or icon set name)
#   Do not list the whole path, just the set or icon name in that path.
#   ** If this var is empty, all icons will be included.
#   WARNING: This option may cause problems with the installer on the live ISO.
#            If so, try tweaking this option or leaving it blank.
DISTICONS="%(DISTICONS)s"
# Example:
#~ DISTICONS="AwOken-Bodhi hicolor myfavoriteicon1.png myfavoriteicon2.png"


# Here you can specify locales to INCLUDE.
#   List here the locales you want to keep that are in this path:
#     /usr/share/locale/(locale name)
#   Do not list the whole path, just the directories of the locales you wish to INCLUDE in that path.
#   ** If this var is empty, all locales will be included.
DISTLOCALE="%(DISTLOCALE)s"
# Example:
#~ DISTLOCALE="en en_AU en_CA en_GB de"


# Choose the distribution name you want to show up in GRUB
# This will also be the DISTRIB_DESCRIPTION in /etc/lsb-release
DISTNAME="%(DISTNAME)s"

''' % ({
        "WORKDIR" : self.builder.get_object("entry6").get_text(),
        "EXCLUDES" : self.builder.get_object("entry4").get_text(),
        "LIVEUSER" : self.builder.get_object("entry1").get_text(),
        "LIVECDLABEL" : self.builder.get_object("entry2").get_text(),
        "CUSTOMISO" : self.builder.get_object("entry3").get_text(),
        "SQUASHFSOPTS" : self.builder.get_object("entry7").get_text(),
        "BACKUPSHOWINSTALL" : BACKUPSHOWINSTALL,
        "LIVECDURL" : self.builder.get_object("entry5").get_text(),
        "DISTICONS" : self.builder.get_object("entry8").get_text(),
        "DISTLOCALE" : self.builder.get_object("entry9").get_text(),
        "DISTNAME" : self.builder.get_object("entry10").get_text()
        })
        
        conf = open('/etc/bodhibuilder.conf', 'w+')
        conf.write(conf_content)
        conf.close()
        
    def getvalue(self, name, conf, default):
        try:
            m = re.search(name+'="(.*)"',conf)
            return m.group(1)
        except:
            return default


def msg_error(msg, window = None):
    dialog = Gtk.MessageDialog(
        window,
        Gtk.DialogFlags.MODAL,
        Gtk.MessageType.ERROR,
        Gtk.ButtonsType.OK, msg
    )
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.run()
    dialog.destroy()
            
def msg_info(msg, window = None):
    dialog = Gtk.MessageDialog(
        window,
        Gtk.DialogFlags.MODAL,
        Gtk.MessageType.INFO,
        Gtk.ButtonsType.OK,
        msg
    )
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.run()
    dialog.destroy()        

def msg_confirm(msg, window = None):
    dialog = Gtk.MessageDialog(
        window
        , Gtk.DialogFlags.DESTROY_WITH_PARENT
        , Gtk.MessageType.QUESTION
        , Gtk.ButtonsType.OK_CANCEL
        , msg
    )
    dialog.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
    response = dialog.run()
    dialog.destroy()

    if response == Gtk.ResponseType.OK:
        return True
    else:
        return False

def msg_input(title, message, label, default = '', window = None, password = False):
    def responseToDialog( entry, dialog, response):
        dialog.response(response)

    dialog = Gtk.MessageDialog(
        window,
        Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        Gtk.MessageType.QUESTION,
        Gtk.ButtonsType.OK_CANCEL,
        None
    )
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_markup(message)
    dialog.set_title(title)

    entry = Gtk.Entry()
    entry.set_text(default)
    entry.set_visibility(not password)
    entry.connect("activate", responseToDialog, dialog, Gtk.ResponseType.OK)
    hbox = Gtk.HBox()
    hbox.pack_start(Gtk.Label(label), False, 5, 5)
    hbox.pack_end(entry, True, True, 0)
    dialog.vbox.pack_end(hbox, True, True, 0)
    dialog.show_all()
    response = dialog.run()
    text = entry.get_text()
    dialog.destroy()
    
    if response == Gtk.ResponseType.OK:
        return text
    else:
        return None

class Namespace: pass

if os.popen('whoami').read().strip() != 'root':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if os.system('which gksu')==0:
        if os.path.exists('/usr/share/applications/bodhibuilder-gtk.desktop'):
            os.system('gksu -D "%s" ./bodhibuilder-gtk.py' % _('Bodhibuilder'))
        else:
            os.system('gksu -D "%s" ./bodhibuilder-gtk.py' % '/usr/share/applications/bodhibuilder-gtk.desktop')
    elif os.system('which kdesudo')==0:
        os.system('kdesudo ./bodhibuilder-gtk.py' )
    elif os.system('which sudo')==0:
        password = msg_input(_(''), _('Enter your password to perform administrative tasks'), 'Password:', '', None, True)
        if password:
            os.popen('sudo -S ./bodhibuilder-gtk.py','w').write(password)
else:
    if __name__ == '__main__':
        app = appgui()
        Gtk.main()

