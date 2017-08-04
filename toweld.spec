Name: toweld
Summary: NethServer toweld daemon
Version: 0.0.0
Release: 1%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name}

BuildRequires: nethserver-devtools
Requires: pygobject2
Requires: dbus-python

%description
toweld is a daemon that does something for NethServer.

%prep
%setup

%build
%{__install} -d root%{python_sitelib} 
cp -av lib/python/nethserver root%{python_sitelib}

%install
(cd root ; find . -depth -not -name '*.orig' -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > filelist

%files -f filelist
%defattr(-,root,root)
%doc COPYING

%changelog
* Fri Aug 04 2017 Davide Principi <davide.principi@nethesis.it> - 0.0.0-1
- Initial prototype
