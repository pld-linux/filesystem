#
# Conditional build:
%bcond_without	debuginfo	# build without debuginfo package

# disable rpm generated debug package, we handle it differently here
%define		_enable_debug_packages	0

# avoid rpm 4.4.9 adding rm -rf buildroot
%define		__spec_clean_body	%{nil}
Summary:	Common directories
Summary(pl.UTF-8):	Wspólne katalogi
Name:		filesystem
Version:	3.0
Release:	21
License:	GPL
Group:		Base
BuildRequires:	automake
BuildRequires:	mktemp
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package debuginfo
Summary:	Common directories for debug information
Summary(pl.UTF-8):	Wspólne katalogi dla plików z informacjami dla debuggera
Group:		Development/Debug
Requires:	%{name} = %{version}-%{release}

%description debuginfo
This package provides common directories for debug information.

%description debuginfo -l pl.UTF-8
Ten pakiet udostępnia wspólne katalogi dla plików z informacjami dla
debuggera.

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/{initrd,selinux,sys} \
	$RPM_BUILD_ROOT/etc/{pki,X11/xinit/xinitrc.d,certs,default,security,sysconfig/wmstyle,tmpwatch,xdg/autostart} \
	$RPM_BUILD_ROOT/home/{users,services} \
	$RPM_BUILD_ROOT/lib/{firmware,security} \
	$RPM_BUILD_ROOT/usr/include/security \
	$RPM_BUILD_ROOT/usr/lib/{cgi-bin,browser-plugins,pkgconfig} \
	$RPM_BUILD_ROOT/usr/share/{gnome/{help,wm-properties},man/man{n,l},man/pl/mann,pkgconfig,sounds,themes/Default,wallpapers,xsessions} \
	$RPM_BUILD_ROOT/usr/src/examples \
	$RPM_BUILD_ROOT/var/lock/subsys \
	$RPM_BUILD_ROOT{%{_aclocaldir},%{_desktopdir}/docklets,%{_iconsdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_fontsdir}/{{100,75}dpi,OTF,Speedo,Type1/{afm,pfm},TTF,cyrillic,local,misc} \
	$RPM_BUILD_ROOT{%{_idldir},%{_privsepdir}}

%if "%{_lib}" == "lib64"
install -d \
	$RPM_BUILD_ROOT/lib64/security \
	$RPM_BUILD_ROOT/usr/lib64/pkgconfig \
	$RPM_BUILD_ROOT/usr/lib64/browser-plugins
%endif

%if %{with debuginfo}
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

find $RPM_BUILD_ROOT/usr/lib/debug -type d | while read line; do
	echo ${line#$RPM_BUILD_ROOT}
done > $RPM_BUILD_ROOT/usr/src/debug/%{name}-debuginfo.files
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
	find | sed -e 's|^\.||g' -e 's|^$||g' | LC_ALL=C sort | grep -v $TMPFILE | grep -E -v '^/(etc|etc/X11|home|lib|lib64|usr|usr/include|usr/lib|usr/lib64|usr/share|usr/share/man|usr/share/man/pl|usr/src|var|var/lock)$' > $TMPFILE

	# find finds also '.', so use option -B for diff
	rpm -qpl $RPMFILE $RPMFILE2 | grep -v '^/$' | LC_ALL=C sort | diff -uB $TMPFILE - || :

	rm -f $TMPFILE
}

check_filesystem_dirs

%files
%defattr(644,root,root,755)
%dir /etc/X11/xinit
%dir /etc/X11/xinit/xinitrc.d
%attr(751,root,root) %dir /etc/certs
%dir /etc/default
%attr(751,root,root) %dir /etc/security
%dir /etc/sysconfig
%dir /etc/sysconfig/wmstyle
%dir /etc/tmpwatch
%dir /etc/pki
%dir /etc/xdg
%dir /etc/xdg/autostart
%dir /home/users
%attr(751,root,adm) %dir /home/services
%dir /initrd
%dir /lib/firmware
%dir /lib/security
%dir /selinux
%dir /sys
%dir /usr/include/security
%dir /usr/lib/browser-plugins
%dir /usr/lib/cgi-bin
%dir /usr/lib/pkgconfig
%dir /usr/share/gnome
%dir /usr/share/gnome/help
%dir /usr/share/gnome/wm-properties
%dir /usr/share/man/man[nl]
%lang(pl) %dir /usr/share/man/pl/mann
%dir /usr/share/pkgconfig
%dir /usr/share/sounds
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/wallpapers
%dir /usr/share/xsessions
%dir /usr/src/examples
%attr(700,root,root) %dir /var/lock/subsys
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
%dir /usr/lib64/pkgconfig
%dir /usr/lib64/browser-plugins
%endif

%if %{with debuginfo}
%files debuginfo
%defattr(644,root,root,755)
%dir /usr/lib/debug
/usr/lib/debug/*

%dir /usr/src/debug
/usr/src/debug/filesystem-debuginfo.files
%endif
