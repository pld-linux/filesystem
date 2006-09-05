# TODO
# - move here from FHS.spec all dirs not covered by FHS, update descs
# - cnfl /usr/share/pkgconfig, /usr/lib/pkgconfig
# - cnfl /usr/share/aclocal
# - cnfl /etc/X11/xinit
# - cnfl /usr/share/gnome, /usr/share/gnome/help
# - cnfl /usr/share/applications/docklets
# - cnfl /etc/sysconfig/wmstyle
# - cnfl /usr/share/xsessions ?
#
Summary:	Common directories
Summary(pl):	Wspólne katalogi
Name:		filesystem
Version:	2.0
Release:	0.1
License:	GPL
Group:		Base
Requires:	FHS >= 2.3-14.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xmandir	/usr/X11R6/man

%description
This package contains common directories for packages that extend
some programs functionality, but don't require them themselves.

%description -l pl
Ten pakiet zawiera wspólne katalogi dla pakietów rozszerzaj±cych
funkcjonalno¶æ programów, ale nie wymagaj±cych ich.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig,xdg/autostart} \
	$RPM_BUILD_ROOT%{_prefix}/share/{gnome/help,icons,pixmaps,pkgconfig,sounds,themes/Default,wallpapers,wm-properties,xsessions} \
	$RPM_BUILD_ROOT{%{_aclocaldir},%{_pkgconfigdir}} \
	$RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d \
	$RPM_BUILD_ROOT%{_desktopdir}/docklets \
	$RPM_BUILD_ROOT/etc/sysconfig/wmstyle

%if "%{_lib}" != "lib"
install -d $RPM_BUILD_ROOT/usr/lib/pkgconfig
%endif

# X11
install -d $RPM_BUILD_ROOT/usr/X11R6/share
for manp in man{1,2,3,4,5,6,7,8} ; do
	install -d $RPM_BUILD_ROOT%{_xmandir}/${manp}
	for mloc in it ko pl; do
		install -d $RPM_BUILD_ROOT%{_xmandir}/${mloc}/${manp}
	done
done

%clean
cd $RPM_BUILD_ROOT

# %{_rpmfilename} is not expanded, so use
# %{name}-%{version}-%{release}.%{buildarch}.rpm
RPMFILE=%{name}-%{version}-%{release}.%{_target_cpu}.rpm
TMPFILE=%{name}-%{version}.tmp$$
find . | sed -e 's|^\.||g' -e 's|^$||g' | sort | grep -v $TMPFILE > $TMPFILE

# find finds also '.', so use option -B for diff
rpm -qpl %{_rpmdir}/$RPMFILE | grep -v '^/$' | sort | diff -uB $TMPFILE - || :

rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir /etc/sysconfig
%dir /etc/X11/xinit
%dir /etc/X11/xinit/xinitrc.d
%dir /etc/xdg
%dir /etc/xdg/autostart
%dir %{_pkgconfigdir}
%if "%{_lib}" != "lib"
%dir /usr/lib/pkgconfig
%endif
%dir %{_aclocaldir}
%dir %{_desktopdir}/docklets
%dir /etc/sysconfig/wmstyle
%dir /usr/share/gnome
%dir /usr/share/gnome/help
%dir /usr/share/icons
%dir /usr/share/pixmaps
%dir /usr/share/pkgconfig
%dir /usr/share/sounds
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/wallpapers
%dir /usr/share/wm-properties
%dir /usr/share/xsessions

%dir /usr/X11R6
%dir %{_xmandir}
%{_xmandir}/man*
%lang(it) %{_xmandir}/it
%lang(ko) %{_xmandir}/ko
%lang(pl) %{_xmandir}/pl
%dir /usr/X11R6/share
