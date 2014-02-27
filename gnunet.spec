%define gnunetuser gnunetd
%define gnunethome /var/lib/gnunet

%define major 0
%define util_major 5
%define arm_major 1
%define datastore_major 1
%define libname %mklibname %{name} %{major}
%define libutil %mklibname %{name}util %{util_major}
%define libarm %mklibname %{name}arm %{arm_major}
%define libdatastore %mklibname %{name}datastore %{datastore_major}
%define devname %mklibname -d %{name}

Summary:	Secure and anonymous peer-to-peer file sharing
Name:		gnunet
Version:	0.10.0
Release:	1
License:	GPLv2+
Group:		Networking/File transfer
Url:		http://gnunet.org/
Source0:	ftp://ftp.gnu.org/gnu/gnunet/%{name}-%{version}.tar.gz
Source1:	gnunetd.conf
Source2:	init_gnunetd
BuildRequires:	gettext-devel
BuildRequires:	gmp-devel
BuildRequires:	libltdl-devel
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libextractor)
BuildRequires:	pkgconfig(libgcrypt) >= 1.6.0
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)
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

%pre
%_pre_useradd %{gnunetuser} %{gnunethome} /bin/false

%post
%_post_service %{name}d

%preun
%_preun_service %{name}d

%postun
%_postun_userdel %{gnunetuser}


#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Libraries for GNUnet
Group:		System/Libraries

%description -n %{libname}
Libraries for GNUnet.

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libutil}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libutil}
Library for GNUnet.

%files -n %{libutil}
%{_libdir}/lib%{name}util.so.%{util_major}*

#----------------------------------------------------------------------------

%package -n %{libarm}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libarm}
Library for GNUnet.

%files -n %{libarm}
%{_libdir}/lib%{name}arm.so.%{arm_major}*

#----------------------------------------------------------------------------

%package -n %{libdatastore}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libdatastore}
Library for GNUnet.

%files -n %{libdatastore}
%{_libdir}/lib%{name}datastore.so.%{datastore_major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{libname}
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libutil} = %{EVRD}
Requires:	%{libarm} = %{EVRD}
Requires:	%{libdatastore} = %{EVRD}

%description -n %{devname}
Development files for %{libname}.

%files -n %{devname}
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
mv AUTHORS AUTHORS.old
iconv -f ISO_8859-1 -t UTF-8 AUTHORS.old -o AUTHORS

%build
%configure2_5x
# makefile doesn't support running multiple jobs simultaneously
make

%install
%makeinstall_std
mkdir -p %{buildroot}%{gnunethome}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_initrddir}
install -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
ln -s %{_datadir}/%{name}/config.d %{buildroot}%{_sysconfdir}/gnunet.d

%find_lang %{name}

