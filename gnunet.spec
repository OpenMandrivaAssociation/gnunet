%define name gnunet

%define gnunetuser gnunetd
%define gnunethome /var/lib/gnunet

%define major	0
%define util_major 5
%define arm_major 1
%define datastore_major 1
%define libname %mklibname %{name} %{major}
%define libutilname %mklibname %{name}util %{util_major}
%define libarmname %mklibname %{name}arm %{arm_major}
%define libdatastorename %mklibname %{name}datastore %{datastore_major}
%define devname %mklibname -d %{name}

Name:		%{name}
Version:	0.9.1
Release:	3
License:	GPLv2+
Summary:	Secure and anonymous peer-to-peer file sharing
URL:		http://gnunet.org/
Source0:	ftp://ftp.gnu.org/gnu/gnunet/%{name}-%{version}.tar.gz
Source1:	gnunetd.conf
Source2:	init_gnunetd
Group:		Networking/File transfer
BuildRequires:	pkgconfig(libextractor)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	curl-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	gawk
BuildRequires:	gmp-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	gettext-devel
BuildRequires:	sqlite3-devel
BuildRequires:	mysql-devel
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	libltdl-devel
Suggests:	mysql-client
Requires(pre):	rpm-helper

%description
GNUnet is a framework for secure peer-to-peer networking that does not
use any centralized or otherwise trusted services. A first service
implemented on top of the networking layer allows anonymous censorship-
resistant file-sharing. GNUnet uses a simple, excess-based economic
model to allocate resources. Peers in GNUnet monitor each others behavior
with respect to resource usage; peers that contribute to the network
are rewarded with better service.

%package -n %libname
Summary:	Libraries for GNUnet
Group:		System/Libraries

%description -n %libname
Libraries for GNUnet.

%package -n %libutilname
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %libutilname
Library for GNUnet.

%package -n %libarmname
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %libarmname
Library for GNUnet.

%package -n %libdatastorename
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %libdatastorename
Library for GNUnet.

%package -n %devname
Summary:	Development files for %{libname}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libutilname} = %{version}-%{release}
Requires:	%{libarmname} = %{version}-%{release}
Requires:	%{libdatastorename} = %{version}-%{release}

%description -n %devname
Development files for %{libname}.

%prep
%setup -q -n %{name}-%{version}
mv AUTHORS AUTHORS.old
iconv -f ISO_8859-1 -t UTF-8 AUTHORS.old -o AUTHORS

%build
%configure2_5x
# makefile doesn't support running multiple jobs simultaneously
%{__make}

%install
%{__rm} -rf %{buildroot}
%makeinstall_std
%{__mkdir_p} %{buildroot}%{gnunethome}
%{__mkdir_p} %{buildroot}%{_sysconfdir}
#{__install} -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}d.conf
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
%{__ln_s} %{_datadir}/%{name}/config.d %{buildroot}%{_sysconfdir}/gnunet.d
%{__rm} -f %{buildroot}%{_libdir}/*.la

%find_lang %{name}

%pre
%_pre_useradd %{gnunetuser} %{gnunethome} /bin/false

%post
%_post_service %{name}d

%preun
%_preun_service %{name}d

%postun
%_postun_userdel %gnunetuser

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README
%attr(0700, %{gnunetuser}, %{gnunetuser}) %dir %{gnunethome}
%config %{_sysconfdir}/gnunet.d
%{_initrddir}/%{name}d
%{_bindir}/*
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}-*

%files -n %libname
%{_libdir}/lib%{name}*.so.%{major}*

%files -n %libutilname
%{_libdir}/lib%{name}util.so.%{util_major}*

%files -n %libarmname
%{_libdir}/lib%{name}arm.so.%{arm_major}*

%files -n %libdatastorename
%{_libdir}/lib%{name}datastore.so.%{datastore_major}*

%files -n %devname
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/*.pc
#%{_libdir}/lib%{name}*.la
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*



%changelog
* Mon Jan 16 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.9.1-2mdv2012.0
+ Revision: 761718
- spec cleanup
- unused pathes removed

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - get rid of %%pre variable that's not really in use and that breaks %%pre script

* Mon Jan 09 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.9.1-1
+ Revision: 759222
- new version 0.9.1

* Thu Aug 11 2011 Andrey Bondrov <abondrov@mandriva.org> 0.9.0-0.pre2.1
+ Revision: 693952
- Update patch1
- imported package gnunet


* Thu Aug 11 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 0.9.0-0.pre2.1mdv2011.0
- Port to 2011
- New version
- Major spec rewrite

* Wed Apr 02 2008 Anssi Hannula <anssi@zarb.org> 0.7.3-1plf2008.1
- add to PLF
- ensure major correctness
- do not package COPYING, it is GPLv2+
- provide gnunet-devel
- fix library groups
- split library package due to different majors
- fix plugin loading on lib64 systems
- do not use daemonize

* Fri Mar 21 2008 Nicolas Vigier <boklm@mars-attacks.org> 0.7.3-1mdv2008.1
- first version
