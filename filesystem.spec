Summary:	Basic filesystem layout
Summary(de):	Grundlegende Dateisystemstruktur
Summary(fr):	Arborescence de base du système de fichiers
Summary(pl):	Podstawa uk³ad katalogów systemu Linux
Summary(tr):	Temel dosya sistemi yapýsý
Name:		filesystem
Version:	1.5
Release:	4
Copyright:	Public Domain
Group:		Base
Group(pl):	Podstawowe
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
	$RPM_BUILD_ROOT/etc/{profile.d,security,opt} \
	$RPM_BUILD_ROOT/lib/{modules,security} \
	$RPM_BUILD_ROOT/{mnt/{floppy,cdrom},proc,root,sbin,tmp} \
	$RPM_BUILD_ROOT/usr/{bin,src,games,lib,include,sbin,share} \
	$RPM_BUILD_ROOT/usr/share/{dict,doc,info,man,misc,games,tmac} \
	$RPM_BUILD_ROOT/usr/local/{bin,games,share/{info,doc,man},lib,sbin,src} \
	$RPM_BUILD_ROOT/var/{lock/subsys,log,mail,run,spool} \
	$RPM_BUILD_ROOT/var/{games,state/misc,tmp,db,opt,crash,cache,account} \
	$RPM_BUILD_ROOT/var/cache/fonts \
	$RPM_BUILD_ROOT/usr/X11R6/share/applnk

ln -sf share/man 	$RPM_BUILD_ROOT/usr/man
ln -sf share/info 	$RPM_BUILD_ROOT/usr/info
ln -sf state		$RPM_BUILD_ROOT/var/lib
ln -sf share/doc 	$RPM_BUILD_ROOT/usr/doc
ln -sf share/doc 	$RPM_BUILD_ROOT/usr/local/doc
ln -sf share/dict 	$RPM_BUILD_ROOT/usr/dict

%pre
if [ -e /usr/man ] && [ ! -L /usr/man ]; then 
	mkdir -p /usr/share/man
	cp -a /usr/man/* /usr/share/man || :
	rm -rf /usr/man
fi 
if [ -e /usr/info ] && [ ! -L /usr/info ]; then 
	mkdir -p /usr/share/info
	cp -a /usr/info/* /usr/share/info || :
	rm -rf /usr/info
	ln -sf ../../../etc/info-dir /usr/share/info/dir
fi 
if [ -e /usr/doc ] && [ ! -L /usr/doc ]; then 
	mkdir -p /usr/share/doc
	cp -a /usr/doc/* /usr/share/doc || :
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
/bin
%attr(700,root,root) /boot
%dir /etc
%attr(750,root,root) %dir /etc/security
%dir /etc/profile.d
%dir /etc/opt
%dir /etc/X11
%dir /usr/X11R6/share/applnk
/home
/lib
/mnt
/opt
%attr(555,root,root) /proc
%attr(700,root,root) /root
%dir /sbin
%attr(1777,root,root) /tmp
/usr
%dir /var
%dir /var/db
%dir /var/account
%dir /var/games
/var/lock
%attr(751,root,root) /var/log
%dir /var/run
%dir /var/crash
/var/cache
%dir /var/state
%dir /var/opt
%attr(1777,root,root) %dir /var/tmp
