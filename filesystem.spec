
# disable rpm generated debug package, we handle it differently here
%define		_enable_debug_packages	0

# avoid rpm 4.4.9 adding rm -rf buildroot
%define		__spec_clean_body	%{nil}
Summary:	Common directories
Summary(pl.UTF-8):	Wspólne katalogi
Name:		filesystem
Version:	3.0
Release:	41
License:	GPL
Group:		Base
BuildRequires:	automake
BuildRequires:	mktemp
BuildRequires:	rpm >= 4.4.9-56
Requires:	FHS >= 2.3-15
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Adapter: This file does not like to be adapterized!

# directory for "privilege separation" chroot
%define		_privsepdir	/usr/share/empty
# directory for *.idl files (for CORBA implementations)
%define		_idldir		/usr/share/idl

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
	$RPM_BUILD_ROOT/{initrd,selinux,sys} \
	$RPM_BUILD_ROOT/etc/{pki,X11/xinit/xinitrc.d,certs,default,logrotate.d,security,sysconfig/wmstyle,tmpwatch,xdg/autostart,init,NetworkManager/dispatcher.d} \
	$RPM_BUILD_ROOT/home/{users,services} \
	$RPM_BUILD_ROOT/lib/{firmware,security,udev/rules.d} \
	$RPM_BUILD_ROOT/usr/include/{security,X11} \
	$RPM_BUILD_ROOT/usr/lib/{cgi-bin,browser-plugins,mozilla/extensions,pkgconfig,initrd,ConsoleKit/run-session.d} \
	$RPM_BUILD_ROOT/usr/share/{backgrounds,color/icc,gnome/{help,wm-properties},man/man{n,l},man/pl/mann,pkgconfig,sound{,font}s,themes/Default,vala/vapi,wallpapers,xsessions} \
	$RPM_BUILD_ROOT/usr/src/examples \
	$RPM_BUILD_ROOT/var/lock/subsys \
	$RPM_BUILD_ROOT/var/log/archive \
	$RPM_BUILD_ROOT{%{_aclocaldir},%{_desktopdir}/docklets,%{_iconsdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_fontsdir}/{{100,75}dpi,OTF,Speedo,Type1/{afm,pfm},TTF,cyrillic,local,misc} \
	$RPM_BUILD_ROOT{%{_idldir},%{_privsepdir}}

%if "%{_lib}" == "lib64"
install -d \
	$RPM_BUILD_ROOT/lib64/security \
	$RPM_BUILD_ROOT/usr/lib64/pkgconfig \
	$RPM_BUILD_ROOT/usr/lib64/browser-plugins \
	$RPM_BUILD_ROOT/usr/lib64/mozilla/extensions \
	$RPM_BUILD_ROOT/usr/lib64/initrd
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

%if "%{_lib}" == "lib64"
install -d \
	$RPM_BUILD_ROOT/usr/lib/debug/lib64/security
%endif

# create this for %clean
tar -cf checkfiles.tar -C $RPM_BUILD_ROOT .

%clean
mkdir -p $RPM_BUILD_ROOT
tar -xf checkfiles.tar -C $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

check_filesystem_dirs() {
	RPMFILE=%{_rpmdir}/%{name}-%{version}-%{release}.%{_target_cpu}.rpm
	RPMFILE2=%{?with_debuginfo:%{_rpmdir}/%{name}-debuginfo-%{version}-%{release}.%{_target_cpu}.rpm}
	TMPFILE=$(mktemp)
	# note: we must exclude from check all existing dirs belonging to FHS
	find | sed -e 's|^\.||g' -e 's|^$||g' | LC_ALL=C sort | grep -v $TMPFILE | grep -E -v '^/(etc|etc/X11|home|lib|lib64|usr|usr/include|usr/lib|usr/lib64|usr/share|usr/share/man|usr/share/man/pl|usr/src|var|var/lock|var/log)$' > $TMPFILE

	# find finds also '.', so use option -B for diff
	rpm -qpl $RPMFILE $RPMFILE2 | grep -v '^/$' | LC_ALL=C sort | diff -uB - $TMPFILE || :

	rm -f $TMPFILE
}

check_filesystem_dirs

%if "%{pld_release}" != "ac"
%pretrans -p <lua>
-- this needs to be a dir
if posix.stat("/usr/include/X11", "type") == "link" then
	-- feel free to write in pure lua, but success on first install is not important.
	os.execute("umask 022; mv -f /usr/include/X11{,.rpmsave}; mkdir -m755 -p /usr/include/X11 && mv -f /usr/include/X11.rpmsave/* /usr/include/X11")
end
%endif

%files
%defattr(644,root,root,755)
%dir /etc/X11/xinit
%dir /etc/X11/xinit/xinitrc.d
%attr(751,root,root) %dir /etc/certs
%dir /etc/default
%dir /etc/init
%dir /etc/logrotate.d
%attr(751,root,root) %dir /etc/security
%dir /etc/sysconfig
%dir /etc/sysconfig/wmstyle
%dir /etc/tmpwatch
%dir /etc/pki
%dir /etc/xdg
%dir /etc/xdg/autostart
%dir /etc/NetworkManager
%dir /etc/NetworkManager/dispatcher.d
%dir /home/users
%dir /home/services
%dir /initrd
%dir /lib/firmware
%dir /lib/security
%dir /lib/udev
%dir /lib/udev/rules.d
%dir /selinux
%dir /sys
%if "%{pld_release}" != "ac"
%dir /usr/include/X11
%endif
%dir /usr/include/security
%dir /usr/lib/ConsoleKit
%dir /usr/lib/ConsoleKit/run-session.d
%dir /usr/lib/browser-plugins
%dir /usr/lib/mozilla
%dir /usr/lib/mozilla/extensions
%dir /usr/lib/cgi-bin
%dir /usr/lib/initrd
%dir /usr/lib/pkgconfig
%dir /usr/share/backgrounds
%dir /usr/share/color
%dir /usr/share/color/icc
%dir /usr/share/gnome
%dir /usr/share/gnome/help
%dir /usr/share/gnome/wm-properties
%dir /usr/share/man/man[nl]
%lang(pl) %dir /usr/share/man/pl/mann
%dir /usr/share/pkgconfig
%dir /usr/share/soundfonts
%dir /usr/share/sounds
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/vala
%dir /usr/share/vala/vapi
%dir /usr/share/wallpapers
%dir /usr/share/xsessions
%dir /usr/src/examples
%attr(700,root,root) %dir /var/lock/subsys
%attr(750,root,logs) %dir /var/log/archive
%dir %{_aclocaldir}
%dir %{_desktopdir}
%dir %{_desktopdir}/docklets
%dir %{_iconsdir}
%dir %{_pixmapsdir}
%{_fontsdir}
%dir %{_idldir}
%dir %{_privsepdir}
%if "%{_lib}" == "lib64"
%dir /lib64/security
%dir /usr/lib64/browser-plugins
%dir /usr/lib64/mozilla
%dir /usr/lib64/mozilla/extensions
%dir /usr/lib64/initrd
%dir /usr/lib64/pkgconfig
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
