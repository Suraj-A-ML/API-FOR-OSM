Name: osmapi
Version: 1.0
Release: 1%{?dist}
Summary: The api program for osm
License: None
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
Requires: python3-systemd

%description
This package contains a Python program and service file.

%prep
%setup -c -n %{name}-%{version}

%install
mkdir -p %{buildroot}/usr/bin
cp main.py %{buildroot}/usr/bin/
mkdir -p %{buildroot}/etc/systemd/system
cp python-program.service %{buildroot}/etc/systemd/system/

%post
systemctl daemon-reload
systemctl enable python-program.service
systemctl start python-program.service

%files
%defattr(-,root,root,-)
/usr/bin/main.py
/etc/systemd/system/python-program.service

%changelog

