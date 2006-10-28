
%define		_enable_debug_packages	0

Summary:	Common directories
Summary(pl):	Wspólne katalogi
Name:		filesystem
Version:	3.0
Release:	11
License:	GPL
Group:		Base
BuildRequires:	automake
Requires:	FHS >= 2.3-15
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# directory for "privilege separation" chroot
%define		_privsepdir	/usr/share/empty
# directory for *.idl files (for CORBA implementations)
%define		_idldir		/usr/share/idl

%description
This package contains common directories for packages that extend
some programs functionality, but don't require them themselves.

%description -l pl
Ten pakiet zawiera wspólne katalogi dla pakietów rozszerzaj±cych
funkcjonalno¶æ programów, ale nie wymagaj±cych ich.

%package debuginfo
Summary:	Common directories for debug information
Summary(pl):	Wspólne katalogi dla plików z informacjami dla debuggera
Group:		Development/Debug
Requires:	%{name} = %{version}-%{release}

%description debuginfo
This package provides common directories for debug information.

%description debuginfo -l pl
Ten pakiet udostêpnia wspólne katalogi dla plików z informacjami dla
debuggera.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT/{initrd,selinux,sys} \
	$RPM_BUILD_ROOT/etc/{X11/xinit/xinitrc.d,certs,security,sysconfig/wmstyle,xdg/autostart} \
	$RPM_BUILD_ROOT/home/{users,services} \
	$RPM_BUILD_ROOT/lib/{firmware,security} \
	$RPM_BUILD_ROOT/usr/include/security \
	$RPM_BUILD_ROOT/usr/lib/{cgi-bin,debug,pkgconfig} \
	$RPM_BUILD_ROOT/usr/share/{gnome/help,man/man{n,l},man/pl/mann,pkgconfig,sounds,themes/Default,wallpapers,wm-properties,xsessions} \
	$RPM_BUILD_ROOT/usr/src/{debug,examples} \
	$RPM_BUILD_ROOT/var/lock/subsys \
	$RPM_BUILD_ROOT{%{_aclocaldir},%{_desktopdir}/docklets,%{_iconsdir},%{_pixmapsdir}} \
	$RPM_BUILD_ROOT%{_fontsdir}/{{100,75}dpi,OTF,Speedo,Type1/{afm,pfm},TTF,cyrillic,local,misc} \
	$RPM_BUILD_ROOT{%{_idldir},%{_privsepdir}}

%if "%{_lib}" == "lib64"
install -d \
	$RPM_BUILD_ROOT/lib64/security \
	$RPM_BUILD_ROOT/usr/lib64/pkgconfig
%endif

%clean
cd $RPM_BUILD_ROOT

# %{_rpmfilename} is not expanded, so use
# %{name}-%{version}-%{release}.%{buildarch}.rpm
RPMFILE=%{name}-%{version}-%{release}.%{_target_cpu}.rpm
RPMFILE2=%{name}-debuginfo-%{version}-%{release}.%{_target_cpu}.rpm
TMPFILE=%{name}-%{version}.tmp$$
# note: we must exclude from check all existing dirs belonging to FHS
find . | sed -e 's|^\.||g' -e 's|^$||g' | sort | grep -v $TMPFILE | grep -E -v '^/(etc|etc/X11|home|lib|lib64|usr|usr/include|usr/lib|usr/lib64|usr/share|usr/share/man|usr/share/man/pl|usr/src|var|var/lock)$' > $TMPFILE

# find finds also '.', so use option -B for diff
rpm -qpl %{_rpmdir}/$RPMFILE %{_rpmdir}/$RPMFILE2 | grep -v '^/$' | sort | diff -uB $TMPFILE - || :

rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir /etc/X11/xinit
%dir /etc/X11/xinit/xinitrc.d
%attr(751,root,root) %dir /etc/certs
%attr(751,root,root) %dir /etc/security
%dir /etc/sysconfig
%dir /etc/sysconfig/wmstyle
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
%dir /usr/lib/cgi-bin
%dir /usr/lib/pkgconfig
%dir /usr/share/gnome
%dir /usr/share/gnome/help
%dir /usr/share/man/man[nl]
%lang(pl) %dir /usr/share/man/pl/mann
%dir /usr/share/pkgconfig
%dir /usr/share/sounds
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/wallpapers
%dir /usr/share/wm-properties
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
%endif

%files debuginfo
%defattr(644,root,root,755)
%dir /usr/lib/debug
%dir /usr/src/debug
