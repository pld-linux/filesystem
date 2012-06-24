Summary:	Common directories
Summary(pl):	Wsp�lne katalogi
Name:		filesystem
Version:	3.0
Release:	1
License:	GPL
Group:		Base
URL:		http://www.pathname.com/fhs/
Requires:	FHS >= 2.3-14.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains common directories for packages that extend
some programs functionality, but don't require them themselves.

%description -l pl
Ten pakiet zawiera wsp�lne katalogi dla pakiet�w rozszerzaj�cych
funkcjonalno�� program�w, ale nie wymagaj�cych ich.

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig,xdg} \
	$RPM_BUILD_ROOT/usr/share/{sounds,pixmaps,icons,wm-properties,xsessions,wallpapers,themes/Default}


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
%dir /usr/share/icons
%dir /usr/share/pixmaps
%dir /usr/share/sounds
%dir /usr/share/themes
%dir /usr/share/themes/Default
%dir /usr/share/wallpapers
%dir /usr/share/wm-properties
%dir /usr/share/xsessions
