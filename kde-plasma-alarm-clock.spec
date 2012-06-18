Name: kde-plasma-alarm-clock
Version: 1.0
Release: 1%{?dist}
Summary: Simple AlarmClock plasmoid.
Summary(ru): Простой плазмоид-Будильник.
Group: Applications/Date and Time
License: GPL
Source0: http://cloud.github.com/downloads/F1ash/kde-plasma-alarm-clock/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://github.com/F1ash/plasmaGreatAdvice
BuildArch: noarch

Requires: python, PyQt4, PyKDE4

%description
kde-plasma-alarm-clock
Simple AlarmClock plasmoid. Support list of alarms,
custom sounds for each alarm.

%description -l ru
kde-plasma-alarm-clock
Простой плазмоид-Будильник. Может будить по назначенному списку,
для каждого сигнала можно задать свой звук.

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

* Mon Jun 18 2012 Fl@sh <kaperang07@gmail.com> - 1.0-1
- Initial build
