Summary:	Basic filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du système de fichiers
Summary(pl):	Podstawa uk³ad katalogów systemu Linux
Summary(tr):	Temel dosya sistemi yapýsý
Name:		filesystem
Version:	1.5
Release:	1
Copyright:	Public Domain
Group:		Base
Group(pl):	Bazowe
Buildroot:	/tmp/%{name}-%{version}-root
Prereq:		setup
Buildarch:	noarch

%description
This package contains the basic directory layout for a Linux system, 
including the proper permissions for the directories. This layout conforms
to the Filesystem Hierarchy Standard (FHS) 2.0.

%description -l de
Dieses Paket enthält die grundlegende Verzeichnisstruktur eines Linux-Systems,
einschließlich der entsprechenden Zugriffsrechte. Diese Struktur entspricht
dem Filesystem Hierarchy Standard (FHS) 2.0.

%description -l fr
Ce package contient l'arborescence type pour système linux
y compris les permissions adéquates pour les répertoires. Cette
arborescence est conforme au standard \"Filesystem Hierarchy Standard\"
(FHS) 2.0.

%description -l pl
Pakiet ten zawiera informacje o podstawowej strukturze katalogów systemu i
praw dostêpu do nich.
 
%description -l tr
Bu paket GNU makro iþleme dilini içerir. Mantýksal olarak ayrýþtýrýlabilen
metin dosyalarý yazýmý için yararlýdýr.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{bin,boot,home/users,opt} \
	$RPM_BUILD_ROOT/etc/{X11/wmconfig,profile.d,security,opt} \
	$RPM_BUILD_ROOT/lib/{modules,security} \
	$RPM_BUILD_ROOT/{mnt/{floppy,cdrom},proc,root,sbin,tmp} \
	$RPM_BUILD_ROOT/usr/{bin,etc,games,include,sbin,share} \
	$RPM_BUILD_ROOT/usr/share/{dict,doc,info,man,misc,games,fonts} \
	$RPM_BUILD_ROOT/usr/{games,lib/games} \
	$RPM_BUILD_ROOT/usr/local/{bin,games,share/{info,man,doc},lib,sbin,src} \
	$RPM_BUILD_ROOT/var/{local,lock/subsys,log,run,preserve,mail,spool} \
	$RPM_BUILD_ROOT/var/{games,state,tmp,db,opt}

ln -sf share/man 	$RPM_BUILD_ROOT%{_mandir}
ln -sf share/man 	$RPM_BUILD_ROOT/usr/local/man
ln -sf share/info 	$RPM_BUILD_ROOT%{_infodir}
ln -sf state		$RPM_BUILD_ROOT/var/lib
ln -sf share/doc 	$RPM_BUILD_ROOT/usr/doc
ln -sf share/doc 	$RPM_BUILD_ROOT/usr/local/doc
ln -sf share/dict 	$RPM_BUILD_ROOT/usr/dict

%pre
if [ -e %{_mandir} ] && [ ! -L /usr/man ]; then 
	mkdir -p %{_mandir}
	cp -a %{_mandir}/* %{_mandir} || :
	rm -rf %{_mandir}
fi 
if [ -e /usr/local/man ] && [ ! -L /usr/local/man ]; then 
	mkdir -p /usr/local/share/man
	cp -a /usr/local/man/* /usr/local/share/man || :
	rm -rf /usr/local/man
fi 
if [ -e %{_infodir} ] && [ ! -L /usr/info ]; then 
	mkdir -p %{_infodir}
	cp -a %{_infodir}/* %{_infodir} || :
	rm -rf %{_infodir}
	ln -sf ../../../etc/info-dir %{_infodir}/dir
fi 
if [ -e /usr/doc ] && [ ! -L /usr/doc ]; then 
	mkdir -p %{_defaultdocdir}
	cp -a /usr/doc/* %{_defaultdocdir} || :
	rm -rf /usr/doc
fi 
if [ -e /usr/local/doc ] && [ ! -L /usr/local/doc ]; then 
	mkdir -p /usr/local/share/doc
	cp -a /usr/local/doc/* /usr/local/share/doc
	rm -rf /usr/local/doc
fi 
if [ -e /usr/dict ] && [ ! -L /usr/dict ]; then 
	mkdir -p /usr/share/dict
	cp -a /usr/dict/* /usr/share/dict || :
	rm -rf /usr/dict
fi 
if [ -e /var/lib ] && [ ! -L /var/lib ]; then 
	mkdir -p /var/state
	cp -a /var/lib/* /var/state
	rm -rf /var/lib
fi 

%post
if [ -L /var/tmp ]; then
	rm -rf /var/tmp
	mkdir -p /var/tmp
	chmod 1777 /var/tmp
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root,755)
%dir /bin
%attr(700,root,root) /boot
%dir /etc
%attr(751,root,root) %dir /etc/security
%dir /etc/profile.d
%dir /etc/opt
%dir /etc/X11
%dir /etc/X11/wmconfig
/home
/lib
/mnt
%attr(555,root,root) /proc
%attr(700,root,root) /root
%dir /sbin
%attr(1777,root,root) /tmp
/usr
%dir /var
%dir /var/db
%dir /var/lib
%dir /var/local
%dir /var/lock
%attr(751,root,root) /var/log
%dir /var/run
%dir /var/preserve
%dir /var/spool
%dir /var/state
%attr(1777,root,root) %dir /var/tmp

%changelog
* Thu May  6 1999 Artur Frysiak <wiget@pld.org.pl>
  [1.5-1]
- modyfications for FHS 2.0.

* Tue Apr 20 1999 Piotr Czerwiñski <pius@pld.org.pl>
  [1.4-8]
- recompiled on rpm 3.

* Wed Mar 31 1999 Piotr Czerwiñski <pius@pld.org.pl>
  [1.4-7]
- added /etc/X11/wmconfig.

* Thu Feb 23 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-6]
- added /etc/X11.

* Sun Feb 21 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-5]
- removed /usr/tmp (not neccessary),
- added /usr/src,
- removed many directories which must belongs to other packages
  (webserwer, ftpdaemon, smtpdaemon, gopher serwer, petidomo),
- simplification in %files,
- changed GUID on man directorirs to root.

* Wed Dec 30 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.4-3d]
- changed permissions of /boot to 711  
  (System.map must be readable by new ps),
- added /var/spool/{news,lpd,uucp},
- added /var/qmail,
- all symlinks are now as %ghost,
- added /var/lock/subsys,
- added /usr/X11R6/man/* & %{_mandir}/man/*,
- fixed permission of /var/spool/mail,
- added /etc/mail && /home/ftp,
- added /usr/lib/gopher-data && /usr/lib/games.

* Mon Aug 10 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.4-1d]
- changed relase to 1d (PLD-devel),
- added /opt for commercial software,
- /var/tmp as symlink to /tmp,
- /var/adm as symlink to /var/log.

* Mon Aug  10 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-1]
- Buildroot changed to /tmp/%{name}-%%{version}-root,
- directory skeleton is builded directly in %install instead unpacking 
  from cpio archive,
- translation modified for pl,
- removed /usr/etc,
- added /home/users - default base directory for users home
  directories,
- changed permission on /var/lib/rpm to 700,
- changed perrmission on /root and /boot to 700,
- changed permission on /var/log to 711,
- changed permission on /var/spool/mail to 751,
- removed /usr/lib/X11,
- removed /var/nis.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Wed Jul 09 1997 Erik Troan <ewt@redhat.com>
- added /

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Changed /proc to 555
- Removed /var/spool/mqueue (which is owned by sendmail)
