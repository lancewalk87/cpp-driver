%define distnum %(/usr/lib/rpm/redhat/dist.sh --distnum)

Name:    cassandra-cpp-driver
Epoch:   1
Version: %{driver_version}
Release: 1%{?dist}
Summary: DataStax C/C++ Driver for Apache Cassandra

Group: Development/Tools
License: Apache 2.0
URL: https://github.com/datastax/cpp-driver
Source0: %{name}-%{version}.tar.gz
Source1: cassandra.pc.in
Source2: cassandra_static.pc.in

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{distnum} == 5
BuildRequires: buildsys-macros >= 5
%endif
BuildRequires: cmake >= 2.6.4
BuildRequires: libuv-devel >= %{libuv_version}
BuildRequires: openssl-devel >= 0.9.8e

%description
A modern, feature-rich, and highly tunable C/C++ client library for Apache
Cassandra using exclusively Cassandra's native protocol and Cassandra Query
Language.

%package devel
Summary: Development libraries for ${name}
Group: Development/Tools
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: libuv >= %{libuv_version}
Requires: openssl >= 0.9.8e
Requires: pkgconfig

%description devel
Development libraries for %{name}

%prep
%setup -qn %{name}-%{version}

%build
export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
cmake -DCMAKE_BUILD_TYPE=RELEASE -DCASS_BUILD_STATIC=ON -DCASS_INSTALL_PKG_CONFIG=OFF -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir} .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/%{_libdir}/pkgconfig
sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE1 > %{buildroot}/%{_libdir}/pkgconfig/cassandra.pc
sed -e "s#@prefix@#%{_prefix}#g" \
    -e "s#@exec_prefix@#%{_exec_prefix}#g" \
    -e "s#@libdir@#%{_libdir}#g" \
    -e "s#@includedir@#%{_includedir}#g" \
    -e "s#@version@#%{version}#g" \
    %SOURCE2 > %{buildroot}/%{_libdir}/pkgconfig/cassandra_static.pc

%clean
rm -rf %{buildroot}

%check
# make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md LICENSE.txt
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc README.md LICENSE.txt
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Dec 14 2015 Michael Penick <michael.penick@datastax.com> - 2.2.2-1
- patch release
* Fri Nov 20 2015 Michael Penick <michael.penick@datastax.com> - 2.2.1-1
- patch release
* Mon Nov 02 2015 Michael Penick <michael.penick@datastax.com> - 2.2.0-1
- release
* Mon Sep 21 2015 Michael Penick <michael.penick@datastax.com> - 2.2.0beta1-1
- beta release
* Tue Aug 11 2015 Michael Penick <michael.penick@datastax.com> - 2.1.0-1
- release
* Wed Jul 08 2015 Michael Penick <michael.penick@datastax.com> - 2.1.0beta-1
- beta release
* Mon May 18 2015 Michael Penick <michael.penick@datastax.com> - 2.0.1-1
- patch release
* Thu Apr 23 2015 Michael Penick <michael.penick@datastax.com> - 2.0.0-1
- release
* Tue Feb 03 2015 Michael Penick <michael.penick@datastax.com> - 1.0.0-1
- release
* Tue Dec 23 2014 Michael Penick <michael.penick@datastax.com> - 1.0.0rc1-1
- release candidate
* Thu Nov 20 2014 Michael Penick <michael.penick@datastax.com> - 1.0.0beta5-1
- beta release
* Thu Sep 11 2014 Michael Penick <michael.penick@datastax.com> - 1.0.0beta4-1
- beta release
* Wed Aug 13 2014 Michael Penick <michael.penick@datastax.com> - 1.0.0beta3-1
- beta release
* Thu Jul 17 2014 Michael Penick <michael.penick@datastax.com> - 1.0.0beta2-1
- beta release
* Mon Jun 16 2014 Michael Penick <michael.penick@datastax.com> - 1.0.0beta1-1
- beta release
