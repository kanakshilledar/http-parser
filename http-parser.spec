%global somajor 1
%global sominor 0
%global git_hash 32c0e11

Name:           http-parser
Version:        %{somajor}.%{sominor}
Release:        1%{?dist}
Summary:        HTTP request/response parser for C

Group:          System Environment/Libraries
License:        MIT
URL:            http://github.com/ry/http-parser
# download from https://github.com/ry/http-parser/tarball/v%%{version}
Source0:        ry-http-parser-v%{version}-0-g%{git_hash}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).


%package devel
Group:          Development/Libraries
Summary:        Development headers and libraries for http-parser
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for http-parser.


%prep
%setup -q -n ry-http-parser-%{git_hash}


%build
make %{?_smp_mflags} CC="%{__cc} %{optflags} -fsigned-char -fPIC" http_parser.o
%{__cc} %{optflags} -Wl,-soname,http_parser.so.%{somajor} \
        -o libhttp_parser.so -shared http_parser.o


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -pm644 http_parser.h $RPM_BUILD_ROOT%{_includedir}
install libhttp_parser.so $RPM_BUILD_ROOT%{_libdir}/libhttp_parser.so.%{somajor}.%{sominor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} $RPM_BUILD_ROOT%{_libdir}/libhttp_parser.so.%{somajor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} $RPM_BUILD_ROOT%{_libdir}/libhttp_parser.so


%check
make %{?_smp_mflags} CC="%{__cc} %{optflags} -fsigned-char -fPIC" test


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libhttp_parser.so.*
%doc CONTRIBUTIONS LICENSE-MIT README.md


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libhttp_parser.so


%changelog
* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0-1
- New upstream release 1.0
- Remove patches, no longer needed for nodejs
- Fix typo in -devel description
- use github tarball instead of checkout

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6.20100911git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.3-5.20100911git
- Add support for methods used by node.js

* Thu Nov  4 2010 Dan HorÃ¡k <dan[at]danny.cz> - 0.3-4.20100911git
- build with -fsigned-char

* Wed Sep 29 2010 jkeating - 0.3-3.20100911git
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.3-2.20100911git
- Call ldconfig (Peter Lemenkov)

* Fri Sep 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.3-1.20100911git
- Initial packaging