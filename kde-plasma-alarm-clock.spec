Name: kde-plasma-alarm-clock
Version: 1.5
Release: 1%{?dist}
Summary: Simple AlarmClock plasmoid.
Summary(ru): Простой плазмоид-Будильник.
Group: Applications/Productivity
License: GPLv2+
Source0: http://cloud.github.com/downloads/F1ash/kde-plasma-alarm-clock/%{name}-%{version}.tar.bz2
URL: https://github.com/F1ash/plasmaGreatAdvice
BuildArch: noarch

Requires: python, PyQt4, PyKDE4, sox

%description
kde-plasma-alarm-clock
Simple AlarmClock plasmoid. Support list of alarms,
custom sound, message and command for each alarm node.
Works without Akonadi.

%description -l ru
kde-plasma-alarm-clock
Простой плазмоид-Будильник. Может будить по назначенному списку,
для каждого сигнала можно задать свой звук, сообщение и команду.
Не нуждается в Akonadi.

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

%changelog
* Sun Jun 24 2012 Fl@sh <kaperang07@gmail.com> - 1.5-1
- improved description
- version updated

* Sat Jun 23 2012 Fl@sh <kaperang07@gmail.com> - 1.3-1
- version updated

* Fri Jun 22 2012 Fl@sh <kaperang07@gmail.com> - 1.1-1
- version updated

* Mon Jun 18 2012 Fl@sh <kaperang07@gmail.com> - 1.0-1
- Initial build
