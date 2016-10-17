# NOTE
# - do not use any other user/group than "root", as then we have to depend on "setup" package.
#   see the gid_xxx macros and post scriptlet
# FIXME: verify shows changed groups of dirs changed this way
Summary:	Common directories
Summary(pl.UTF-8):	Wspólne katalogi
Name:		filesystem
Version:	4.1
Release:	3
License:	GPL
Group:		Base
BuildRequires:	automake
BuildRequires:	mktemp
BuildRequires:	rpm >= 4.4.9-56
Requires:	FHS >= 3.0
Provides:	browser-plugins(%{_target_base_arch})
%ifarch %{x8664}
Provides:	browser-plugins(i386)
%endif
%ifarch ppc64
Provides:	browser-plugins(ppc)
%endif
%ifarch s390x
Provides:	browser-plugins(s390)
%endif
%ifarch sparc64
Provides:	browser-plugins(sparc)
%endif
Provides:	filesystem-debuginfo = %{version}-%{release}
Obsoletes:	filesystem-debuginfo < 3.0-36
%if "%{pld_release}" != "ac"
Conflicts:	X11-libs < 1:7.7
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Adapter: This file does not like to be adapterized!

# disable rpm generated debug package, we handle it differently here
%define		_enable_debug_packages	0

%if "%{_lib}" == "lib64"
%define		with_lib64	1
%endif
%if "%{_lib}" == "libx32"
%define		with_libx32	1
%define		with_lib64	1
%else
%ifarch %{x8664}
# x32 as additional ABI
%define		with_libx32	1
%endif
%endif

# avoid rpm 4.4.9 adding rm -rf buildroot
%define		__spec_clean_body	%{nil}

# directory for "privilege separation" chroot
%define		_privsepdir	/usr/share/empty
# directory for *.idl files (for CORBA implementations)
%define		_idldir		/usr/share/idl

# we have to use numeric uids/groups. see comment beginning of the spec
%define		gid_logs	124
%define		gid_crontab	117

%description
This package contains common directories for packages that extend some
programs functionality, but don't require them themselves.

%description -l pl.UTF-8
Ten pakiet zawiera wspólne katalogi dla pakietów rozszerzających
funkcjonalność programów, ale nie wymagających ich.

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/{initrd,selinux} \
	$RPM_BUILD_ROOT/etc/{NetworkManager/dispatcher.d,X11/xinit/{xinput,xinitrc}.d,certs,cron.d,default,logrotate.d,fonts/conf.d,modprobe.d,pki/{CA,tls},security,skel,sysconfig,tmpwatch,xdg/{autostart,colors,menus}} \
	$RPM_BUILD_ROOT/home/{users,services} \
	$RPM_BUILD_ROOT/lib/{firmware,security,udev/{hwdb.d,rules.d},systemd/system} \
	$RPM_BUILD_ROOT/usr/include/{security,X11} \
	$RPM_BUILD_ROOT/usr/lib/{ConsoleKit/run-session.d,browser-plugins,cgi-bin,cmake,mozilla/extensions,pkcs11,pkgconfig,initrd,tmpfiles.d,binfmt.d} \
	$RPM_BUILD_ROOT/usr/share/{appdata,augeas/lenses/tests,backgrounds,cmake/Modules,defaults,factory/etc/pam.d,fontconfig/conf.avail,gnome/help,mate/help,man/man{n,l},man/pl/mann,pkgconfig,soundfonts,sounds,themes/Default,thumbnailers,vala/vapi,wallpapers,wayland-sessions,xdg-desktop-portal/portals,xsessions} \
	$RPM_BUILD_ROOT/usr/src/examples \
	$RPM_BUILD_ROOT/var/lock/subsys \
	$RPM_BUILD_ROOT/var/log/archive \
	$RPM_BUILD_ROOT{%{_aclocaldir},%{_desktopdir}/{docklets,screensavers},%{_iconsdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_fontsdir}/{{100,75}dpi,OTF,Speedo,Type1/{afm,pfm},TTF,cyrillic,local,misc} \
	$RPM_BUILD_ROOT{%{_idldir},%{_privsepdir}} \
	$RPM_BUILD_ROOT/boot/efi/EFI \
	$RPM_BUILD_ROOT/etc/OpenCL/vendors

> %{name}.lang
install -d $RPM_BUILD_ROOT/usr/share/help/C

for lang in ar as ast bg bn_IN ca cs da de el en_GB es eu fa fi fr gl gu he hi hr hu id it ja ko kn lt lv mk ml mr nb nds nl oc pa pl ps pt pt_BR ro ru sk sl sr sr@latin sv ta te th tr uk vi zh_CN zh_HK zh_TW; do
	install -d $RPM_BUILD_ROOT/usr/share/help/${lang}
	echo "%%lang($lang) %dir /usr/share/help/${lang}" >> %{name}.lang
done

%if %{with lib64}
install -d \
	$RPM_BUILD_ROOT/lib64/security \
	$RPM_BUILD_ROOT/usr/lib64/{browser-plugins,cmake,initrd,mozilla/extensions,pkcs11,pkgconfig} \
	$RPM_BUILD_ROOT/usr/lib/debug/lib64/security
%endif
%if %{with libx32}
install -d \
	$RPM_BUILD_ROOT/libx32/security \
	$RPM_BUILD_ROOT/usr/libx32/{browser-plugins,cmake,initrd,mozilla/extensions,pkcs11,pkgconfig} \
	$RPM_BUILD_ROOT/usr/lib/debug/libx32/security
%endif

%if "%{pld_release}" == "ac"
rmdir $RPM_BUILD_ROOT/usr/include/X11
# X11
install -d $RPM_BUILD_ROOT/usr/X11R6/share
for manp in man{1,2,3,4,5,6,7,8} ; do
	install -d $RPM_BUILD_ROOT/usr/X11R6/man/$manp
	for mloc in it ko pl; do
		install -d $RPM_BUILD_ROOT/usr/X11R6/man/$mloc/$manp
	done
done
install -d $RPM_BUILD_ROOT/usr/share/wm-properties
%endif

install -d \
	$RPM_BUILD_ROOT/usr/lib/debug/%{_lib} \
	$RPM_BUILD_ROOT/usr/lib/debug%{_libdir} \
	$RPM_BUILD_ROOT/usr/lib/debug/{bin,sbin} \
	$RPM_BUILD_ROOT/usr/lib/debug/usr/{bin,sbin} \
	$RPM_BUILD_ROOT/usr/lib/debug/lib/security \
	$RPM_BUILD_ROOT/usr/src/debug

%clean
cd $RPM_BUILD_ROOT

check_filesystem_dirs() {
	RPMFILE=%{_rpmdir}/%{name}-%{version}-%{release}.%{_target_cpu}.rpm
	TMPFILE=$(mktemp)
	# note: we must exclude from check all existing dirs belonging to FHS
	find | sed -e 's|^\.||g' -e '/^$/d' | LC_ALL=C sort | grep -v $TMPFILE | \
	grep -E -v '^/(boot|etc|etc/X11|home|lib|lib64|libx32|usr|usr/include|usr/lib|usr/lib64|usr/libx32|usr/share|usr/share/man|usr/share/man/pl|usr/src|var|var/lib|var/lock|var/log)$' > $TMPFILE

	if rpm -qpl $RPMFILE | grep -v '^/$' | LC_ALL=C sort | diff -u $TMPFILE - ; then
		rm -rf $RPM_BUILD_ROOT
	else
		echo -e "\nNot so good, some directories are not included in package\n"
		exit 1
	fi
	rm -f $TMPFILE
}

check_filesystem_dirs

%if "%{pld_release}" != "ac"
%pretrans -p <lua>
-- this needs to be a dir
if posix.stat("/usr/include/X11", "type") == "link" then
	posix.umask("0755");
	os.rename("/usr/include/X11", "/usr/include/X11.rpmsave")
	posix.mkdir("/usr")
	posix.mkdir("/usr/include")
	posix.mkdir("/usr/include/X11")
	oldpwd = posix.getcwd()
	posix.chdir("/usr/include/X11.rpmsave")
	for i,j in pairs(posix.glob("*")) do
		os.rename(j, "/usr/include/X11/" .. j)
	end
	posix.chdir(oldpwd)
end
%endif

%post -p <lua>
posix.chown("/var/log/archive", 0, %{gid_logs})
posix.chown("/etc/cron.d", 0, %{gid_crontab})

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir /boot/efi
%dir /boot/efi/EFI
%dir /etc/X11/xinit
%dir /etc/X11/xinit/xinitrc.d
%dir /etc/X11/xinit/xinput.d
%dir /etc/OpenCL
%dir /etc/OpenCL/vendors
%attr(751,root,root) %dir /etc/certs
%dir /etc/cron.d
%dir /etc/default
%dir /etc/fonts
%dir /etc/fonts/conf.d
%dir /etc/logrotate.d
%dir /etc/modprobe.d
%dir /etc/pki
%dir /etc/pki/CA
%dir /etc/pki/tls
%attr(751,root,root) %dir /etc/security
%dir /etc/skel
%dir /etc/sysconfig
%dir /etc/tmpwatch
%dir /etc/xdg
%dir /etc/xdg/autostart
%dir /etc/xdg/colors
%dir /etc/xdg/menus
%dir /etc/NetworkManager
%dir /etc/NetworkManager/dispatcher.d
%dir /home/users
%dir /home/services
%dir /initrd
%dir /lib/firmware
%dir /lib/security
%dir /lib/systemd
%dir /lib/systemd/system
# for library packages or other software with optional udev support not to pull udev
%dir /lib/udev
%dir /lib/udev/hwdb.d
%dir /lib/udev/rules.d
%dir /selinux
%if "%{pld_release}" != "ac"
%dir /usr/include/X11
%endif
%dir /usr/include/security
%dir /usr/lib/ConsoleKit
%dir /usr/lib/ConsoleKit/run-session.d
%dir /usr/lib/binfmt.d
%dir /usr/lib/browser-plugins
%dir /usr/lib/cgi-bin
%dir /usr/lib/cmake
%dir /usr/lib/initrd
%dir /usr/lib/mozilla
%dir /usr/lib/mozilla/extensions
%dir /usr/lib/pkcs11
%dir /usr/lib/pkgconfig
%dir /usr/lib/tmpfiles.d
%dir /usr/share/appdata
%dir /usr/share/augeas
%dir /usr/share/augeas/lenses
%dir /usr/share/augeas/lenses/tests
%dir /usr/share/backgrounds
%dir /usr/share/cmake
%dir /usr/share/cmake/Modules
%dir /usr/share/defaults
%dir /usr/share/factory
%dir /usr/share/factory/etc
%dir /usr/share/factory/etc/pam.d
%dir /usr/share/fontconfig
%dir /usr/share/fontconfig/conf.avail
%dir /usr/share/gnome
%dir /usr/share/gnome/help
%dir /usr/share/mate
%dir /usr/share/mate/help
%dir /usr/share/help
%dir /usr/share/help/C
%dir /usr/share/man/man[nl]
%lang(pl) %dir /usr/share/man/pl/mann
%dir /usr/share/pkgconfig
%dir /usr/share/soundfonts
%dir /usr/share/sounds
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/thumbnailers
%dir /usr/share/vala
%dir /usr/share/vala/vapi
%dir /usr/share/wallpapers
%dir /usr/share/wayland-sessions
%dir /usr/share/xdg-desktop-portal
%dir /usr/share/xdg-desktop-portal/portals
%dir /usr/share/xsessions
%dir /usr/src/examples
%attr(700,root,root) %dir /var/lock/subsys
%attr(751,root,root) %dir /var/log/archive
%dir %{_aclocaldir}
%dir %{_desktopdir}
%dir %{_desktopdir}/docklets
%dir %{_desktopdir}/screensavers
%dir %{_iconsdir}
%dir %{_pixmapsdir}
%{_fontsdir}
%dir %{_idldir}
%dir %{_privsepdir}
%if %{with lib64}
%dir /lib64/security
%dir /usr/lib64/browser-plugins
%dir /usr/lib64/cmake
%dir /usr/lib64/initrd
%dir /usr/lib64/mozilla
%dir /usr/lib64/mozilla/extensions
%dir /usr/lib64/pkcs11
%dir /usr/lib64/pkgconfig
%endif
%if %{with libx32}
%dir /libx32/security
%dir /usr/libx32/browser-plugins
%dir /usr/libx32/cmake
%dir /usr/libx32/initrd
%dir /usr/libx32/mozilla
%dir /usr/libx32/mozilla/extensions
%dir /usr/libx32/pkcs11
%dir /usr/libx32/pkgconfig
%endif

%if "%{pld_release}" == "ac"
%dir /usr/X11R6
%dir /usr/X11R6/man
/usr/X11R6/man/man*
%lang(it) /usr/X11R6/man/it
%lang(ko) /usr/X11R6/man/ko
%lang(pl) /usr/X11R6/man/pl
%dir /usr/X11R6/share

%dir /usr/share/wm-properties
%endif

# debuginfo
%dir /usr/lib/debug
/usr/lib/debug/*

%dir /usr/src/debug
