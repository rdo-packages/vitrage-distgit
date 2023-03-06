%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
Source13:         %{name}-ml.service
Source14:         %{name}-persistor.service
Source15:         %{name}-snmp-parsing.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:    openstack-macros
BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    systemd
BuildRequires:    python3-pbr
BuildRequires:    python3-sphinx
BuildRequires:    python3-oslo-messaging
BuildRequires:    python3-oslo-config
BuildRequires:    python3-oslo-upgradecheck
BuildRequires:    python3-keystoneauth1
BuildRequires:    python3-keystoneclient
BuildRequires:    python3-keystonemiddleware
BuildRequires:    python3-oslo-db
BuildRequires:    python3-oslo-policy
BuildRequires:    python3-osprofiler
BuildRequires:    python3-tenacity
BuildRequires:    python3-voluptuous
BuildRequires:    git-core

BuildRequires:    python3-sympy
BuildRequires:    python3-networkx


%description
Vitrage is the OpenStack RCA (Root Cause Analysis) Engine
for organizing, analyzing and expanding OpenStack alarms & events,


%package -n       python3-vitrage
Summary:          OpenStack vitrage python libraries
%{?python_provide:%python_provide python3-vitrage}

Requires:         python3-alembic >= 0.9.8
Requires:         python3-sqlalchemy >= 1.2.5
Requires:         python3-oslo-db >= 4.44.0
Requires:         python3-oslo-config >= 2:6.8.0
Requires:         python3-oslo-i18n >= 3.20.0
Requires:         python3-oslo-log >= 3.44.0
Requires:         python3-oslo-policy >= 3.6.0
Requires:         python3-oslo-messaging >= 5.36.0
Requires:         python3-oslo-service >= 1.24.0
Requires:         python3-oslo-upgradecheck >= 1.3.0
Requires:         python3-oslo-utils >= 3.33.0
Requires:         python3-keystonemiddleware >= 4.21.0
Requires:         python3-pbr >= 3.1.1
Requires:         python3-pecan >= 1.2.1
Requires:         python3-stevedore >= 1.28.0
Requires:         python3-werkzeug >= 0.14.1
Requires:         python3-keystoneclient >= 1:3.15.0
Requires:         python3-neutronclient >= 6.7.0
Requires:         python3-novaclient >= 1:10.1.0
Requires:         python3-voluptuous >= 0.11.1
Requires:         python3-dateutil >= 2.7.0
Requires:         python3-keystoneauth1 >= 3.6.2
Requires:         python3-heatclient >= 1.14.0
Requires:         python3-osprofiler >= 2.0.0
Requires:         python3-aodhclient >= 1.0.0
Requires:         python3-debtcollector >= 1.19.0
Requires:         python3-eventlet >= 0.20.0
Requires:         python3-oslo-context >= 2.22.0
Requires:         python3-oslo-middleware >= 3.35.0
Requires:         python3-oslo-serialization >= 2.25.0
Requires:         python3-pysnmp >= 4.4.4
Requires:         python3-requests >= 2.20.0
Requires:         python3-webob >= 1.7.4
Requires:         python3-cotyledon >= 1.6.8
Requires:         python3-gnocchiclient >= 3.3.1
Requires:         python3-mistralclient >= 3.3.0
Requires:         python3-openstackclient >= 3.12.0
Requires:         python3-jsonschema >= 3.2.0
Requires:         python3-zaqarclient >= 1.2.0
Requires:         python3-pytz >= 2018.3
Requires:         python3-psutil >= 5.4.3
Requires:         python3-tenacity >= 4.12.0
# python2-pyzabbix is required by vitrage but is not available in repo yet
#Requires:         python3-pyzabbix

Requires:         python3-sympy >= 1.1.1
Requires:         python3-lxml >= 4.5.2
Requires:         python3-paste-deploy >= 1.5.2
Requires:         python3-networkx >= 2.4
Requires:         python3-jwt >= 1.6.0
Requires:         python3-pysnmp
Requires:         python3-PyMySQL >= 0.8.0
Requires:         python3-yaml >= 5.1
Requires:         python3-tooz >= 1.58.0
Requires:         python3-psutil >= 5.4.3
Requires:         python3-cryptography >= 2.7
Requires:         python3-cachetools >= 2.0.1


%description -n   python3-vitrage
%{common_desc}

This package contains the vitrage python library.

%package        common
Summary:        Components common to all OpenStack vitrage services

Requires:       python3-vitrage = %{version}-%{release}

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
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
Obsoletes:      %{name}-collector < %{version}-%{release}

%description graph
%{common_desc}

This package contains the vitrage graph service.

%package        notifier

Summary:        OpenStack vitrage notifier

Requires:       %{name}-common = %{version}-%{release}

%description notifier
%{common_desc}

This package contains the vitrage notifier service.

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

%package -n python3-vitrage-tests
Summary:        Vitrage tests
%{?python_provide:%python_provide python3-vitrage-tests}
Requires:       python3-vitrage = %{version}-%{release}
Requires:       python3-tempest >= 12.0.0

%description -n python3-vitrage-tests
%{common_desc}

This package contains the Vitrage test files.

%package doc
Summary:    Documentation for OpenStack vitrage

BuildRequires: python3-openstackdocstheme

%description doc
%{common_desc}

This package contains documentation files for vitrage.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find vitrage -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%py_req_cleanup


%build
# generate html docs
sphinx-build -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}

%{py3_build}

# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=etc/vitrage/vitrage-config-generator.conf
%{py3_build}

%install
%{py3_install}

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
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-ml.service
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/%{name}-persistor.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/%{name}-snmp-parsing.service

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

%files -n python3-vitrage
%license LICENSE
%{python3_sitelib}/vitrage
%{python3_sitelib}/vitrage-*.egg-info
%exclude %{python3_sitelib}/vitrage/tests

%files -n python3-vitrage-tests
%license LICENSE
%{python3_sitelib}/vitrage/tests

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
%{_bindir}/vitrage-dbsync-revision
%{_bindir}/vitrage-dbsync-stamp
%{_bindir}/vitrage-purge-data
%{_bindir}/vitrage-status

%defattr(-, vitrage, vitrage, -)
%dir %{_sharedstatedir}/vitrage
%dir %{_sharedstatedir}/vitrage/tmp

%files api
%{_bindir}/vitrage-api
%{_unitdir}/%{name}-api.service

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
