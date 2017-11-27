%global service vitrage

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

Name:             openstack-vitrage
Version:          XXX
Release:          XXX
Summary:          OpenStack Root Cause Analysis
License:          ASL 2.0
URL:              https://github.com/openstack/vitrage
BuildArch:        noarch
Source0:          http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source2:          %{service}.logrotate
Source10:         %{name}-api.service
Source11:         %{name}-graph.service
Source12:         %{name}-notifier.service
Source13:         %{name}-collector.service
Source14:         %{name}-ml.service
Source15:         %{name}-persistor.service

BuildRequires:    openstack-macros
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    systemd
BuildRequires:    python-pbr
BuildRequires:    python-sphinx
BuildRequires:    python-oslo-messaging
BuildRequires:    python-oslo-config
BuildRequires:    python-keystoneauth1
BuildRequires:    python-keystoneclient
BuildRequires:    python-keystonemiddleware
BuildRequires:    python-oslo-db
BuildRequires:    python-oslo-policy
BuildRequires:    python-osprofiler
BuildRequires:    git


%description
Vitrage is the OpenStack RCA (Root Cause Analysis) Engine
for organizing, analyzing and expanding OpenStack alarms & events,


%package -n       python-vitrage
Summary:          OpenStack vitrage python libraries


Requires:         python-lxml

Requires:         python-sqlalchemy >= 1.0.10
Requires:         python-oslo-db >= 4.24.0
Requires:         python-oslo-config >= 2:4.0.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-log >= 3.22.0
Requires:         python-oslo-policy >= 1.23.0
Requires:         python-oslo-messaging >= 5.24.2
Requires:         python-oslo-service >= 1.10.0
Requires:         python-oslo-utils >= 3.20.0
Requires:         python-keystonemiddleware >= 4.12.0
Requires:         python-pbr >= 2.0.0
Requires:         python-pecan >= 1.0.0
Requires:         python-stevedore >= 1.20.0
Requires:         python-werkzeug >= 0.7
Requires:         python-paste-deploy >= 1.5.0
Requires:         python-ceilometerclient >= 2.5.0
Requires:         python-keystoneclient >= 1:3.8.0
Requires:         python-cinderclient >= 3.1.0
Requires:         python-neutronclient >= 6.3.0
Requires:         python-novaclient >= 1:9.0.0
Requires:         python-networkx >= 1.10
Requires:         python-voluptuous >= 0.8.9
Requires:         sympy >= 0.7.6
Requires:         python-dateutil >= 2.4.2
Requires:         python-keystoneauth1 >= 2.12.1
Requires:         python-heatclient >= 1.6.1
Requires:         python-osprofiler >= 1.4.0
Requires:         python-jwt
Requires:         pysnmp
# python-pyzabbix is required by vitrage but is not available in repo yet
#Requires:         python-pyzabbix

%description -n   python-vitrage
%{common_desc}

This package contains the vitrage python library.

%package        common
Summary:        Components common to all OpenStack vitrage services

Requires:       python-vitrage = %{version}-%{release}

%{?systemd_requires}
Requires(pre):    shadow-utils


%description    common
%{common_desc}


%package        api

Summary:        OpenStack vitrage api

Requires:       %{name}-common = %{version}-%{release}

%description api
%{common_desc}

This package contains the vitrage API service.


%package        graph

Summary:        OpenStack vitrage graph

Requires:       %{name}-common = %{version}-%{release}

%description graph
%{common_desc}

This package contains the vitrage graph service.

%package        notifier

Summary:        OpenStack vitrage notifier

Requires:       %{name}-common = %{version}-%{release}

%description notifier
%{common_desc}

This package contains the vitrage notifier service.


%package        collector
Summary:        OpenStack vitrage collector
Requires:       %{name}-common = %{version}-%{release}

%description collector
%{common_desc}

This package contains the vitrage collector service.


%package        ml
Summary:        OpenStack vitrage machine learning
Requires:       %{name}-common = %{version}-%{release}

%description ml
%{common_desc}

This package contains the vitrage machine learning service.

%package        persistor
Summary:        OpenStack vitrage persistor
Requires:       %{name}-common = %{version}-%{release}

%description persistor
%{common_desc}

This package contains the vitrage persistor service.

%package -n python-vitrage-tests
Summary:        Vitrage tests
Requires:       python-vitrage = %{version}-%{release}
Requires:       python-tempest >= 12.0.0

%description -n python-vitrage-tests
%{common_desc}

This package contains the Vitrage test files.

%package doc
Summary:    Documentation for OpenStack vitrage

BuildRequires: python-openstackdocstheme

%description doc
%{common_desc}

This package contains documentation files for vitrage.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find vitrage -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%py_req_cleanup


%build
# generate html docs
%{__python2} setup.py build_sphinx

# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=etc/vitrage/vitrage-config-generator.conf
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Create fake egg-info for the tempest plugin
%py2_entrypoint %{service} %{service}

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/vitrage/datasources_values
install -p -D -m 640 etc/vitrage/vitrage.conf %{buildroot}%{_sysconfdir}/vitrage/vitrage.conf
install -p -D -m 640 etc/vitrage/api-paste.ini %{buildroot}%{_sysconfdir}/vitrage/api-paste.ini
install -p -D -m 640 etc/vitrage/datasources_values/*.yaml %{buildroot}%{_sysconfdir}/vitrage/datasources_values/

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/vitrage
install -d -m 755 %{buildroot}%{_sharedstatedir}/vitrage/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/vitrage
install -d -m 755 %{buildroot}%{_sysconfdir}/vitrage/static_datasources
install -d -m 755 %{buildroot}%{_sysconfdir}/vitrage/templates

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install systemd unit services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-graph.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-notifier.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-collector.service
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/%{name}-ml.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/%{name}-persistor.service

# Remove unused files
rm -f %{buildroot}/usr/etc/vitrage/*

%pre common
getent group vitrage >/dev/null || groupadd -r vitrage
if ! getent passwd vitrage >/dev/null; then
  useradd -r -g vitrage -G vitrage -d %{_sharedstatedir}/vitrage -s /sbin/nologin -c "OpenStack vitrage Daemons" vitrage
fi
exit 0

%post -n %{name}-api
%systemd_post %{name}-api.service

%preun -n %{name}-api
%systemd_preun %{name}-api.service

%post -n %{name}-graph
%systemd_post %{name}-graph.service

%preun -n %{name}-graph
%systemd_preun %{name}-graph.service

%post -n %{name}-notifier
%systemd_post %{name}-notifier.service

%preun -n %{name}-notifier
%systemd_preun %{name}-notifier.service

%post -n %{name}-collector
%systemd_post %{name}-collector.service

%preun -n %{name}-collector
%systemd_preun %{name}-collector.service

%post -n %{name}-ml
%systemd_post %{name}-ml.service

%preun -n %{name}-ml
%systemd_preun %{name}-ml.service

%post -n %{name}-persistor
%systemd_post %{name}-persistor.service

%preun -n %{name}-persistor
%systemd_preun %{name}-persistor.service

%files -n python-vitrage
%license LICENSE
%{python2_sitelib}/vitrage
%{python2_sitelib}/vitrage-*.egg-info
%exclude %{python2_sitelib}/vitrage_tempest_tests
%exclude %{python2_sitelib}/vitrage/tests

%files -n python-vitrage-tests
%license LICENSE
%{python2_sitelib}/vitrage_tempest_tests
%{python2_sitelib}/vitrage/tests
%{python2_sitelib}/%{service}_tests.egg-info

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/vitrage
%dir %{_sysconfdir}/vitrage/datasources_values
%config(noreplace) %attr(-, root, vitrage) %{_sysconfdir}/vitrage/vitrage.conf
%config(noreplace) %attr(-, root, vitrage) %{_sysconfdir}/vitrage/api-paste.ini
%config(noreplace) %attr(-, root, vitrage) %{_sysconfdir}/vitrage/datasources_values/*.yaml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0755, vitrage, root)  %{_localstatedir}/log/vitrage
%dir %attr(0755, vitrage, root)  %{_sysconfdir}/vitrage/static_datasources
%dir %attr(0755, vitrage, root)  %{_sysconfdir}/vitrage/templates
%{_bindir}/vitrage-dbsync

%defattr(-, vitrage, vitrage, -)
%dir %{_sharedstatedir}/vitrage
%dir %{_sharedstatedir}/vitrage/tmp

%files api
%{_bindir}/vitrage-api
%{_unitdir}/%{name}-api.service

%files collector
%{_bindir}/vitrage-collector
%{_unitdir}/%{name}-collector.service

%files graph
%{_bindir}/vitrage-graph
%{_unitdir}/%{name}-graph.service

%files notifier
%{_bindir}/vitrage-notifier
%{_unitdir}/%{name}-notifier.service

%files ml
%{_bindir}/vitrage-ml
%{_unitdir}/%{name}-ml.service

%files persistor
%{_bindir}/vitrage-persistor
%{_unitdir}/%{name}-persistor.service


%files doc
%license LICENSE
%doc doc/build/html

%changelog
