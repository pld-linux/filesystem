Summary:	Basic filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du syst�me de fichiers
Summary(pl):	Podstawa uk�ad katalog�w systemu Linux
Summary(tr):	Temel dosya sistemi yap�s�
Name:		filesystem
Version:	1.4
Release:	6
Copyright:	Public Domain
Group:		Base
Group(pl):	Podstawy
Buildroot:	/tmp/%{name}-%{version}-root
Prereq:		setup
Buildarch:	noarch

%description
This package contains the basic directory layout for a Linux system, 
including the proper permissions for the directories. This layout conforms
to the Linux Filesystem Standard (FSSTND) 1.3.

%description -l de
Dieses Paket enth�lt die grundlegende Verzeichnisstruktur eines Linux-Systems,
einschlie�lich der entsprechenden Zugriffsrechte. Diese Struktur entspricht
dem Linux-Dateisystem-Standard (FSSTND) 1.3.

%description -l fr
Ce package contient l'arborescence type pour syst�me linux
y compris les permissions ad�quates pour les r�pertoires. Cette
arborescence est conforme au standard \"Linux Filesystem Standard\"
(FSSTND) 1.3.

%description -l pl
Pakiet ten zawiera informacje o podstawowej strukturze katalog�w systemu i
praw dost�pu do nich.
 
%description -l tr
Bu paket GNU makro i�leme dilini i�erir. Mant�ksal olarak ayr��t�r�labilen
metin dosyalar� yaz�m� i�in yararl�d�r.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{bin,boot,etc/X11,home/users,lib/modules}
install -d $RPM_BUILD_ROOT/{mnt/{floppy,cdrom},proc,root,sbin,tmp}
install -d $RPM_BUILD_ROOT/usr/{bin,dict,doc,etc,games,include,info,sbin,share}

install -d $RPM_BUILD_ROOT/usr/{games,lib/games,man}

install -d $RPM_BUILD_ROOT/usr/local/{bin,etc,doc,games,info,lib,man,sbin,src}

install -d $RPM_BUILD_ROOT/var/{lib,local,lock/subsys,log,run,preserve,spool/mail}
install -d $RPM_BUILD_ROOT/var/lib/games

ln -sf ../tmp $RPM_BUILD_ROOT/var/tmp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
/bin
%attr(-,root,root,700) /boot
/etc
/home
/lib
/mnt
%attr(-,root,root,555) /proc
%attr(-,root,root,700) /root
/sbin
%attr(-,root,root,1777) /tmp
/usr
%dir /var
/var/lib
/var/local
/var/lock
%attr(-,root,root,711) /var/log
/var/run
/var/preserve
/var/spool
/var/tmp

%changelog
* Thu Feb 23 1999 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-6]
- added /etc/X11.

* Sun Feb 21 1999 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-5]
- removed /usr/tmp (not neccessary),
- added /usr/src,
- removed many directories which must belongs to other packages
  (webserwer, ftpdaemon, smtpdaemon, gopher serwer, petidomo),
- simplification in %files,
- changed GUID on man directorirs to root.

* Wed Dec 30 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.4-3d]
- changed permissions of /boot to 711  
  (System.map must be readable by new ps),
- added /var/spool/{news,lpd,uucp},
- added /var/qmail,
- all symlinks are now as %ghost,
- added /var/lock/subsys,
- added /usr/X11R6/man/* & /usr/man/man/*,
- fixed permission of /var/spool/mail,
- added /etc/mail && /home/ftp,
- added /usr/lib/gopher-data && /usr/lib/games.

* Mon Aug 10 1998 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [1.4-1d]
- changed relase to 1d (PLD-devel),
- added /opt for commercial software,
- /var/tmp as symlink to /tmp,
- /var/adm as symlink to /var/log.

* Mon Aug  10 1998 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
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
