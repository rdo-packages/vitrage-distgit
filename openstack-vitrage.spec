# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
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
Source16:         %{name}-snmp-parsing.service

BuildRequires:    openstack-macros
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-devel
BuildRequires:    systemd
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-oslo-messaging
BuildRequires:    python%{pyver}-oslo-config
BuildRequires:    python%{pyver}-keystoneauth1
BuildRequires:    python%{pyver}-keystoneclient
BuildRequires:    python%{pyver}-keystonemiddleware
BuildRequires:    python%{pyver}-oslo-db
BuildRequires:    python%{pyver}-oslo-policy
BuildRequires:    python%{pyver}-osprofiler
BuildRequires:    python%{pyver}-voluptuous
BuildRequires:    git

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    sympy
%else
BuildRequires:    python%{pyver}-sympy
%endif


%description
Vitrage is the OpenStack RCA (Root Cause Analysis) Engine
for organizing, analyzing and expanding OpenStack alarms & events,


%package -n       python%{pyver}-vitrage
Summary:          OpenStack vitrage python libraries
%{?python_provide:%python_provide python%{pyver}-vitrage}



Requires:         python%{pyver}-sqlalchemy >= 1.2.5
Requires:         python%{pyver}-oslo-db >= 4.35.0
Requires:         python%{pyver}-oslo-config >= 2:5.2.0
Requires:         python%{pyver}-oslo-i18n >= 3.20.0
Requires:         python%{pyver}-oslo-log >= 3.37.0
Requires:         python%{pyver}-oslo-policy >= 1.34.0
Requires:         python%{pyver}-oslo-messaging >= 5.36.0
Requires:         python%{pyver}-oslo-service >= 1.24.0
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-keystonemiddleware >= 4.21.0
Requires:         python%{pyver}-pbr >= 3.1.1
Requires:         python%{pyver}-pecan >= 1.2.1
Requires:         python%{pyver}-stevedore >= 1.28.0
Requires:         python%{pyver}-werkzeug >= 0.14.1
Requires:         python%{pyver}-ceilometerclient >= 2.9.0
Requires:         python%{pyver}-keystoneclient >= 1:3.15.0
Requires:         python%{pyver}-cinderclient >= 3.3.0
Requires:         python%{pyver}-neutronclient >= 6.7.0
Requires:         python%{pyver}-novaclient >= 10.1.0
Requires:         python%{pyver}-voluptuous >= 0.8.9
Requires:         python%{pyver}-dateutil >= 2.7.0
Requires:         python%{pyver}-keystoneauth1 >= 3.4.0
Requires:         python%{pyver}-heatclient >= 1.14.0
Requires:         python%{pyver}-osprofiler >= 2.0.0
Requires:         python%{pyver}-aodhclient >= 1.0.0
Requires:         python%{pyver}-babel >= 2.3.4
Requires:         python%{pyver}-debtcollector >= 1.19.0
Requires:         python%{pyver}-eventlet >= 0.20.0
Requires:         python%{pyver}-oslo-context >= 2.20.0
Requires:         python%{pyver}-oslo-middleware >= 3.35.0
Requires:         python%{pyver}-oslo-serialization >= 2.25.0
Requires:         python%{pyver}-pysnmp >= 4.2.3
Requires:         python%{pyver}-requests >= 2.18.4
Requires:         python%{pyver}-six >= 1.11.0
Requires:         python%{pyver}-webob >= 1.7.4
Requires:         python%{pyver}-cotyledon >= 1.6.3
Requires:         python%{pyver}-gnocchiclient >= 3.3.1
Requires:         python%{pyver}-mistralclient >= 3.3.0
Requires:         python%{pyver}-openstackclient >= 3.12.0
Requires:         python%{pyver}-pytz
# python2-pyzabbix is required by vitrage but is not available in repo yet
#Requires:         python%{pyver}-pyzabbix

# Handle python2 exception
%if %{pyver} == 2
Requires:         sympy >= 0.7.6
Requires:         python-lxml
Requires:         python-paste-deploy >= 1.5.2
Requires:         python-networkx >= 1.10
Requires:         python-jwt
Requires:         pysnmp
Requires:         python-PyMySQL >= 0.7.6
Requires:         PyYAML >= 3.10
Requires:         python%{pyver}-futures
%else
Requires:         python%{pyver}-sympy >= 0.7.6
Requires:         python%{pyver}-lxml
Requires:         python%{pyver}-paste-deploy >= 1.5.2
Requires:         python%{pyver}-networkx >= 1.10
Requires:         python%{pyver}-jwt
Requires:         python%{pyver}-pysnmp
Requires:         python%{pyver}-PyMySQL >= 0.7.6
Requires:         python%{pyver}-PyYAML >= 3.10
%endif


%description -n   python%{pyver}-vitrage
%{common_desc}

This package contains the vitrage python library.

%package        common
Summary:        Components common to all OpenStack vitrage services

Requires:       python%{pyver}-vitrage = %{version}-%{release}

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

%package        snmp-parsing
Summary:        OpenStack vitrage SNMP parsing
Requires:       %{name}-common = %{version}-%{release}

%description snmp-parsing
%{common_desc}

This package contains the SNMP parsing service.

%package -n python%{pyver}-vitrage-tests
Summary:        Vitrage tests
%{?python_provide:%python_provide python%{pyver}-vitrage-tests}
Requires:       python%{pyver}-vitrage = %{version}-%{release}
Requires:       python%{pyver}-tempest >= 12.0.0

%description -n python%{pyver}-vitrage-tests
%{common_desc}

This package contains the Vitrage test files.

%package doc
Summary:    Documentation for OpenStack vitrage

BuildRequires: python%{pyver}-openstackdocstheme

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
%{pyver_bin} setup.py build_sphinx

%{pyver_build}

# Generate config file
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=etc/vitrage/vitrage-config-generator.conf
%{pyver_build}

%install
%{pyver_install}

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
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/%{name}-snmp-parsing.service

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

%post -n %{name}-snmp-parsing
%systemd_post %{name}-snmp-parsing.service

%preun -n %{name}-snmp-parsing
%systemd_preun %{name}-snmp-parsing.service

%files -n python%{pyver}-vitrage
%license LICENSE
%{pyver_sitelib}/vitrage
%{pyver_sitelib}/vitrage-*.egg-info
%exclude %{pyver_sitelib}/vitrage/tests

%files -n python%{pyver}-vitrage-tests
%license LICENSE
%{pyver_sitelib}/vitrage/tests

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
%{_bindir}/vitrage-purge-data

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

%files snmp-parsing
%{_bindir}/vitrage-snmp-parsing
%{_unitdir}/%{name}-snmp-parsing.service

%files doc
%license LICENSE
%doc doc/build/html

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/vitrage/commit/?id=ecb4cbade3e20582bbb7d570534ee3e673aaf268
