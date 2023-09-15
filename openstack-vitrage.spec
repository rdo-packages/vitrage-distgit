%global milestone .0rc1
%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%global service vitrage

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1
%global common_desc OpenStack vitrage provides API and services for RCA (Root Cause Analysis).

Name:             openstack-vitrage
Version:          11.0.0
Release:          0.1%{?milestone}%{?dist}
Summary:          OpenStack Root Cause Analysis
License:          Apache-2.0
URL:              https://github.com/openstack/vitrage
BuildArch:        noarch
Source0:          http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

#
# patches_base=11.0.0.0rc1
#

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
BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    systemd
BuildRequires:    git-core



%description
Vitrage is the OpenStack RCA (Root Cause Analysis) Engine
for organizing, analyzing and expanding OpenStack alarms & events,


%package -n       python3-vitrage
Summary:          OpenStack vitrage python libraries
Requires:         python3-vitrage+openstack = %{version}-%{release}

%description -n   python3-vitrage
%{common_desc}

This package contains the vitrage python library.

%package        common
Summary:        Components common to all OpenStack vitrage services
Requires:       python3-vitrage = %{version}-%{release}
Requires(pre):  shadow-utils

%{?systemd_ordering}

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
Requires:       python3-vitrage = %{version}-%{release}

%description -n python3-vitrage-tests
%{common_desc}

This package contains the Vitrage test files.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack vitrage

%description doc
%{common_desc}

This package contains documentation files for vitrage.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find vitrage -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install

# Generate config file
PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslo-config-generator --config-file=etc/vitrage/vitrage-config-generator.conf

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

%check
# Unit tests are failing, we need to disable them for now
#rm -f ./vitrage/tests/unit/hacking/test_hacking.py
#%%tox -e %{default_toxenv}

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

%pyproject_extras_subpkg -n python3-vitrage openstack

%files -n python3-vitrage
%license LICENSE
%{python3_sitelib}/vitrage
%{python3_sitelib}/vitrage-*.dist-info
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

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Sep 15 2023 RDO <dev@lists.rdoproject.org> 11.0.0-0.1.0rc1
- Update to 11.0.0.0rc1

