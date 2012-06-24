DESTDIR=/usr
INSTALL=install -D -m 0644 -p
APP_NAME=kde-plasma-alarm-clock
KAPPS=share/kde4/apps
KSERV=share/kde4/services
PLASMA=plasma/plasmoids
CODE=contents/code
ICONS=contents/icons
ICON_PATH=/usr/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/alarm.png

build:
	@echo "Nothing to build"

install: build
	sed -i 's|Icon=.*|Icon='$(ICON_PATH)'|' metadata.desktop
	$(INSTALL) metadata.desktop $(DESTDIR)/$(KSERV)/$(APP_NAME).desktop
	$(INSTALL) metadata.desktop $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/metadata.desktop
	$(INSTALL) $(CODE)/main.py $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/main.py
	$(INSTALL) $(CODE)/AppletSettings.py $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/AppletSettings.py
	$(INSTALL) $(CODE)/Blank.py $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/Blank.py
	$(INSTALL) $(CODE)/Functions.py $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/Functions.py
	$(INSTALL) $(ICONS)/alarm.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/alarm.png
	$(INSTALL) $(ICONS)/alarm1.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/alarm1.png
	$(INSTALL) $(ICONS)/alarm2.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/alarm2.png
	$(INSTALL) $(ICONS)/alarm_disabled.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/alarm_disabled.png

clean:
	rm -rf $(DESTDIR)/$(KSERV)/$(APP_NAME).desktop
	rm -rf $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)
