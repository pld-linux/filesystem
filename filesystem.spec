# TODO: move here from FHS.spec all dirs not covered by FHS, update descs
Summary:	Common directories
Summary(pl):	Wspólne katalogi
Name:		filesystem
Version:	3.0
Release:	2
License:	GPL
Group:		Base
Requires:	FHS >= 2.3-14.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains common directories for packages that extend
some programs functionality, but don't require them themselves.

%description -l pl
Ten pakiet zawiera wspólne katalogi dla pakietów rozszerzających
funkcjonalność programów, ale nie wymagających ich.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig,xdg} \
	$RPM_BUILD_ROOT/usr/share/{sounds,pixmaps,icons,wm-properties,xsessions,wallpapers,themes/Default,pkgconfig} \
	$RPM_BUILD_ROOT{%{_aclocaldir},%{_pkgconfigdir}}

%if "%{_lib}" != "lib"
install -d $RPM_BUILD_ROOT/usr/lib/pkgconfig
%endif

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
%dir /etc/xdg
%dir %{_pkgconfigdir}
%if "%{_lib}" != "lib"
%dir /usr/lib/pkgconfig
%endif
%dir %{_aclocaldir}
%dir /usr/share/icons
%dir /usr/share/pixmaps
%dir /usr/share/pkgconfig
%dir /usr/share/sounds
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/wallpapers
%dir /usr/share/wm-properties
%dir /usr/share/xsessions
