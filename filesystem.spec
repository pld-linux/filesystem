Summary:	Basic filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du système de fichiers
Summary(pl):	Podstawa uk³ad katalogów systemu Linux
Summary(tr):	Temel dosya sistemi yapýsý
Name:		filesystem
Version:	1.4
Release:	4d
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
Dieses Paket enthält die grundlegende Verzeichnisstruktur eines Linux-Systems,
einschließlich der entsprechenden Zugriffsrechte. Diese Struktur entspricht
dem Linux-Dateisystem-Standard (FSSTND) 1.3.

%description -l fr
Ce package contient l'arborescence type pour système linux
y compris les permissions adéquates pour les répertoires. Cette
arborescence est conforme au standard \"Linux Filesystem Standard\"
(FSSTND) 1.3.

%description -l pl
Pakiet ten zawiera informacje o podstawowej strukturze katalogów systemu i
praw dostêpu do nich.
 
%description -l tr
Bu paket GNU makro iþleme dilini içerir. Mantýksal olarak ayrýþtýrýlabilen
metin dosyalarý yazýmý için yararlýdýr.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{bin,boot,etc/X11,home/users,lib/modules}
install -d $RPM_BUILD_ROOT/{mnt/{floppy,cdrom},proc,root,sbin,tmp}
install -d $RPM_BUILD_ROOT/usr/{X11R6/{bin,include,lib,man},bin,dict}
install -d $RPM_BUILD_ROOT/usr/{bin,dict,doc,etc,games,include,info,sbin,share}

ln -sf ../X11R6/bin $RPM_BUILD_ROOT/usr/bin/X11
ln -sf ../tmp $RPM_BUILD_ROOT/usr/tmp

install -d $RPM_BUILD_ROOT/usr/man/man{1,2,3,4,5,6,7,8,9,n}

install -d $RPM_BUILD_ROOT/usr/X11R6/{bin,include,lib,man/man{1,3,4,5,6}}
install -d $RPM_BUILD_ROOT/usr/{games,lib/{games,gopher-data}}

install -d $RPM_BUILD_ROOT/usr/local/{bin,etc,doc,games,info,lib,man/man{1,2,3,4,5,6,7,8,9,n},sbin,src}

install -d $RPM_BUILD_ROOT/var/{lib,local,lock/subsys,log,run,preserve,spool/mail}
install -d $RPM_BUILD_ROOT/var/lib/games

ln -sf ../tmp $RPM_BUILD_ROOT/var/tmp
ln -sf ../var/log $RPM_BUILD_ROOT/var/adm

install -d $RPM_BUILD_ROOT/{opt,etc/mail}
install -d $RPM_BUILD_ROOT/home/{httpd,petidomo,ftp}
install -d $RPM_BUILD_ROOT/var/{qmail/alias,/spool/{lpd,news,uucp}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%dir /bin
%attr(711,root,root) %dir /boot
%dir /etc
%attr(750,root,mail) %dir /etc/mail
%dir /home
%dir /home/users
%dir /home/httpd
%dir /home/ftp
%attr(751,petidomo,petidomo) %dir /home/petidomo

%dir /lib
%dir /lib/modules

%dir /mnt
%dir /mnt/cdrom
%dir /mnt/floppy
%attr(555,root,root) %dir /proc
%dir /sbin
%dir %attr(1777,root,root) /tmp

%dir /usr
%dir /usr/X11R6
%dir /usr/X11R6/bin
%dir /usr/X11R6/include
%dir /usr/X11R6/lib

%attr(755,root,man) %dir /usr/X11R6/man
%attr(755,root,man) /usr/X11R6/man/*

%dir /usr/bin
%ghost /usr/bin/X11
%dir /usr/dict
%dir /usr/doc
%dir /usr/games
%dir /usr/include
%dir /usr/info

%attr(755,root,man) %dir /usr/man
%attr(755,root,man) /usr/man/*

%dir /usr/lib
%attr(755,root,root,755) /usr/lib/*

%dir /usr/local
%attr(755,root,root,755) /usr/local/*

%dir /usr/sbin
%dir /usr/share
/usr/tmp

%dir /var
/var/adm
%dir /var/lib
%dir /var/lib/games
%dir /var/local
%dir /var/lock
%dir /var/lock/subsys
%attr(711,root,root) %dir /var/log
%dir /var/run
%dir /var/preserve

%dir /var/spool
%attr(775, root, mail) %dir /var/spool/mail
%attr(775,root,daemon) %dir /var/spool/lpd
%attr(775, news, news) %dir /var/spool/news
%attr(755, uucp, root) %dir /var/spool/uucp
/var/tmp
%attr(0755,root, qmail) %dir /var/qmail
%attr(2755,alias,qmail) %dir /var/qmail/alias
%dir /opt

%changelog
* Wed Dec 30 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
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
