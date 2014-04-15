#!/usr/bin/env python

# Quellen:
# https://github.com/akkana/gimp-plugins/blob/master/save-export-clean.py
# http://www.gimpdome.com/scripts-n-plugins/%28script-fu%29-copy-visible-and-paste-as-new-image/

from gimpfu import *
import gtk
import os
import collections

def file_save_dds_visible(img, drawable) :
	# Setze gespeicherten Export-Dateinamen als Default; falls der nicht existiert, setze aktuellen Dateinamen als Default
	parasite = img.parasite_find("file_save_dds_visible-filename")
	
	if parasite != None:
		filename = parasite.data
	else:
		if img.filename != None:
			(filename, ext) = os.path.splitext(img.filename)
			filename += ".dds"
		else:
			filename = "export.dds"
	
	chooser = gtk.FileChooserDialog(title=None,
					action=gtk.FILE_CHOOSER_ACTION_SAVE,
					buttons=(gtk.STOCK_CANCEL,
							gtk.RESPONSE_CANCEL,
							gtk.STOCK_SAVE,
							gtk.RESPONSE_OK))
							
	chooser.set_filename(filename)
	chooser.set_current_name(os.path.split(filename)[1])
	chooser.set_do_overwrite_confirmation(True)

	response = chooser.run()
	if response != gtk.RESPONSE_OK:
		return

	filename = chooser.get_filename()
	chooser.destroy()
	
	# Speichere gewaehlten Dateinamen im Bild als "Parasit"
	img.attach_new_parasite("file_save_dds_visible-filename", 0, filename)

	# Auswahl entfernen (sonst wird bei "Kopiere Sichtbares" nur die Auswahl kopiert)
	selection = pdb.gimp_selection_save(img)
	pdb.gimp_selection_none(img)
	
	# Kopiere alles Sichtbare in einen neuen Buffer und exportiere den als DDS:
	pdb.gimp_edit_named_copy_visible(img, "ImgVisible")
	outputVisible = pdb.gimp_edit_named_paste_as_new("ImgVisible")
	pdb.file_dds_save(
		outputVisible, pdb.gimp_image_get_active_drawable(outputVisible),
		filename, filename,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0,
		run_mode=RUN_INTERACTIVE)
	pdb.gimp_buffer_delete("ImgVisible")

	# Auswahl wiederherstellen
	pdb.gimp_image_select_item(img, CHANNEL_OP_REPLACE, selection)
	pdb.gimp_image_remove_channel(img, selection)

register(
	"file-save-dds-visible",
	"Sichtbares als DDS exportieren",
	"Sichtbares als DDS exportieren.",
	"Johannes",
	"(C) 2012",
	"09/11/2012",
	"<Image>/File/Sichtbares als DDS exportieren ...",
	"*",
	[],
	[],
	file_save_dds_visible
)

main()
