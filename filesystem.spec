Summary:     Basic filesystem layout
Summary(de): Grundlegende Dateisystemstruktur
Summary(fr): Arborescence de base du système de fichiers
Summary(pl): Podstawa struktóra katalogów systemu
Summary(tr): Temel dosya sistemi yapýsý
Name:        filesystem
Version:     1.4
Release:     2
Copyright:   Public Domain
Group:       Base
Buildroot:   /tmp/%{name}-%{version}-root
Prereq:      setup
BuildArchitectures: noarch

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
Pakiet ten zawiera informacje o podstawowowej struktórze katalogów systemu i
praw dostêpu do nich.
 
%description -l tr
Bu paket GNU makro iþleme dilini içerir. Mantýksal olarak ayrýþtýrýlabilen
metin dosyalarý yazýmý için yararlýdýr.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{bin,boot,etc/X11,home/users,lib/modules}
install -d $RPM_BUILD_ROOT/{mnt/floppy,proc,root,sbin,tmp}
install -d $RPM_BUILD_ROOT/usr/{X11R6/{bin,include,lib,man},bin,dict}
install -d $RPM_BUILD_ROOT/usr/{bin,dict,doc,etc,games,include,info,sbin,share}
ln -sf ../X11R6/bin $RPM_BUILD_ROOT/usr/bin/X11
ln -sf ../var/tmp $RPM_BUILD_ROOT/usr/tmp

install -d $RPM_BUILD_ROOT/usr/man/man{1,2,3,4,5,6,7,8,9,n}

install -d $RPM_BUILD_ROOT/usr/X11R6/{bin,include,lib,man/man{1,3,4,5,6}}
install -d $RPM_BUILD_ROOT/usr/lib/{games,gcc-lib}

install -d $RPM_BUILD_ROOT/usr/local/{bin,etc,doc,games,info,lib,man/man{1,2,3,4,5,6,7,8,9,n},sbin,src}

install -d $RPM_BUILD_ROOT/var/{lib,local,lock/subsys,log,run,preserve,spool}
install -d $RPM_BUILD_ROOT/var/{lib/{games,rpm},tmp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, 755)
%dir /bin
%dir %attr(0700, root, root) /boot
/etc
%dir /home
%dir %attr(0755, root, users) /home/users
/lib
/mnt
%dir %attr(0555, root, root) /proc
%dir %attr(0700, root, root) /root
%dir /sbin
%dir %attr(1777, root, root) /tmp
%dir /usr
%dir /usr/X11R6
%dir /usr/X11R6/bin
%dir /usr/X11R6/include
%dir /usr/X11R6/lib
/usr/X11R6/man
%dir /usr/bin
/usr/bin/X11
%dir /usr/dict
%dir /usr/doc
%dir /usr/include
%dir /usr/info
/usr/man
/usr/local
%dir /usr/sbin
%dir /usr/share
/usr/tmp
%dir /var
%dir /var/lib
%dir /var/lib/games
%dir %attr(700, root, root) /var/lib/rpm
%dir /var/local
/var/lock
%attr(711, root, root) %dir /var/log
%dir /var/run
%dir /var/preserve
%dir /var/spool
%dir %attr(1777, root, root) /var/tmp

%changelog
* Thu Sep 24  1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-2]
- removed /var/spool/mail. This maust belongs to MTA packages.

* Mon Aug  10 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-1]
- Buildroot changed to /tmp/%%{name}-%%{version}-root,
- directory skeleton is builded directly in %install instead unpacking 
  from cpio archive,
- added pl translation,
- removed /usr/etc,
- added /home/users - default base directory for users home
  directories,
- changed perrmisson on /var/lib/rpm to 700,
- changed perrmisson on /root and /boot to 700,
- changed permissoin on /var/log to 711,
- changed permissoin on /var/spool/mail to 751,
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
