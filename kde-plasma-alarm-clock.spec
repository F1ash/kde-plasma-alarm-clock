Name: kde-plasma-alarm-clock
Version: 1.1
Release: 1%{?dist}
Summary: Simple AlarmClock plasmoid.
Summary(ru): Простой плазмоид-Будильник.
Group: Applications/Date and Time
License: GPLv2+
Source0: http://cloud.github.com/downloads/F1ash/kde-plasma-alarm-clock/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://github.com/F1ash/plasmaGreatAdvice
BuildArch: noarch

Requires: python, PyQt4, PyKDE4, sox

%description
kde-plasma-alarm-clock
Simple AlarmClock plasmoid. Support list of alarms,
custom sound and message for each alarm node.

%description -l ru
kde-plasma-alarm-clock
Простой плазмоид-Будильник. Может будить по назначенному списку,
для каждого сигнала можно задать свой звук и сообщение.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT/usr

%files
%defattr(-,root,root)
%{_datadir}/kde4/services/%{name}.desktop
%{_datadir}/kde4/apps/plasma/plasmoids/%{name}/*
%dir %{_datadir}/kde4/apps/plasma/plasmoids/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Fri Jun 22 2012 Fl@sh <kaperang07@gmail.com> - 1.1-1
- version updated

* Mon Jun 18 2012 Fl@sh <kaperang07@gmail.com> - 1.0-1
- Initial build
