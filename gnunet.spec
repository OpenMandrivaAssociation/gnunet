%define gnunetuser gnunetd
%define gnunethome /var/lib/gnunet

%define major		0
%define libname %mklibname %{name} %{major}
%define util_major	9
%define libutilname %mklibname %{name}util %{util_major}
%define arm_major	1
%define libarmname %mklibname %{name}arm %{arm_major}
%define datastore_major	1
%define libdatastorename %mklibname %{name}datastore %{datastore_major}
%define	stats_major	4
%define libnamestats	%mklibname %{name}stats %{stats_major}
%define	frag_major	2
%define libnamefrag	%mklibname %{name}fragmentation %{frag_major}
%define	fs_major	2
%define libnamefs	%mklibname %{name}fs %{fs_major}
%define	mesh_major	1
%define libnamemesh	%mklibname %{name}mesh %{mesh_major}
%define	block_major	2
%define libnameblock	%mklibname %{name}meshblock %{block_major}
%define	regex_major	1
%define libnameregex	%mklibname %{name}regex %{regex_major}
%define	stream_major	1
%define libnamestream	%mklibname %{name}stream %{stream_major}
%define	test_major	1
%define libnametest	%mklibname %{name}test %{test_major}
%define	trans_major	2
%define libnametrans	%mklibname %{name}transport %{trans_major}
%define devname %mklibname -d %{name}

Summary:	Secure and anonymous peer-to-peer file sharing
Name:		gnunet
Version:	0.9.5
Release:	1
License:	GPLv2+
Group:		Networking/File transfer
Url:		http://gnunet.org/
Source0:	ftp://ftp.gnu.org/gnu/gnunet/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/gnu/gnunet/%{name}-%{version}.tar.gz.sig
Source2:	gnunetd.conf
Source3:	init_gnunetd

BuildRequires:	gawk
BuildRequires:	gettext-devel
BuildRequires:	gmp-devel
BuildRequires:	libltdl-devel
BuildRequires:	mysql-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libextractor)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)
Requires(pre):	rpm-helper
Suggests:	mysql-client

%description
GNUnet is a framework for secure peer-to-peer networking that does not
use any centralized or otherwise trusted services. A first service
implemented on top of the networking layer allows anonymous censorship-
resistant file-sharing. GNUnet uses a simple, excess-based economic
model to allocate resources. Peers in GNUnet monitor each others behavior
with respect to resource usage; peers that contribute to the network
are rewarded with better service.

%package -n %{libname}
Summary:	Libraries for GNUnet
Group:		System/Libraries

%description -n %{libname}
Libraries for GNUnet.

%package -n %{libutilname}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libutilname}
Library for GNUnet.

%package -n %{libarmname}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libarmname}
Library for GNUnet.

%package -n %{libdatastorename}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libdatastorename}
Library for GNUnet.

%package -n %{libnamestats}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnamestats}
Library for GNUnet.

%package -n %{libnamefrag}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnamefrag}
Library for GNUnet.

%package -n %{libnamefs}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnamefs}
Library for GNUnet.

%package -n %{libnamemesh}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnamemesh}
Library for GNUnet.

%package -n %{libnameblock}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnameblock}
Library for GNUnet.

%package -n %{libnameregex}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnameregex}
Library for GNUnet.

%package -n %{libnamestream}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnamestream}
Library for GNUnet.

%package -n %{libnametest}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnametest}
Library for GNUnet.

%package -n %{libnametrans}
Summary:	Library for GNUnet
Group:		System/Libraries

%description -n %{libnametrans}
Library for GNUnet.

%package -n %{devname}
Summary:	Development files for %{libname}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libutilname} = %{version}-%{release}
Requires:	%{libarmname} = %{version}-%{release}
Requires:	%{libdatastorename} = %{version}-%{release}
Requires:	%{libnamestats} = %{version}-%{release}
Requires:	%{libnamefrag} = %{version}-%{release}
Requires:	%{libnamefs} = %{version}-%{release}
Requires:	%{libnamemesh} = %{version}-%{release}
Requires:	%{libnameblock} = %{version}-%{release}
Requires:	%{libnameregex} = %{version}-%{release}
Requires:	%{libnamestream} = %{version}-%{release}
Requires:	%{libnametest} = %{version}-%{release}
Requires:	%{libnametrans} = %{version}-%{release}

%description -n %{devname}
Development files for %{libname}.

%prep
%setup -q -n %{name}-%{version}
mv AUTHORS AUTHORS.old
iconv -f ISO_8859-1 -t UTF-8 AUTHORS.old -o AUTHORS

%build
%configure2_5x
# makefile doesn't support running multiple jobs simultaneously
make LIBS='-lz -lm'

%install
%makeinstall_std
mkdir -p %{buildroot}%{gnunethome}
mkdir -p %{buildroot}%{_sysconfdir}
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}d.conf
mkdir -p %{buildroot}%{_initrddir}
install -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
ln -s %{_datadir}/%{name}/config.d %{buildroot}%{_sysconfdir}/gnunet.d
rm -f %{buildroot}%{_libdir}/*.la

%find_lang %{name}

%pre
%_pre_useradd %{gnunetuser} %{gnunethome} /bin/false

%post
%_post_service %{name}d

%preun
%_preun_service %{name}d

%postun
%_postun_userdel %gnunetuser

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README
%attr(0700, %{gnunetuser}, %{gnunetuser}) %dir %{gnunethome}
%config %{_sysconfdir}/gnunet.d
%config %{_sysconfdir}/gnunetd.conf
%{_initrddir}/%{name}d
%{_bindir}/*
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}-*
%{_mandir}/man5/gnunet.conf.5*

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}*

%files -n %{libutilname}
%{_libdir}/lib%{name}util.so.%{util_major}*

%files -n %{libarmname}
%{_libdir}/lib%{name}arm.so.%{arm_major}*

%files -n %{libdatastorename}
%{_libdir}/lib%{name}datastore.so.%{datastore_major}*

%files -n %{libnamestats}
%{_libdir}/libgnunetats.so.%{stats_major}*

%files -n %{libnamefrag}
%{_libdir}/libgnunetfragmentation.so.%{frag_major}*

%files -n %{libnamefs}
%{_libdir}/libgnunetfs.so.%{fs_major}*

%files -n %{libnamemesh}
%{_libdir}/libgnunetmesh.so.%{mesh_major}*

%files -n %{libnameblock}
%{_libdir}/libgnunetmeshblock.so.%{block_major}*

%files -n %{libnameregex}
%{_libdir}/libgnunetregex.so.%{regex_major}*

%files -n %{libnamestream}
%{_libdir}/libgnunetstream.so.%{stream_major}*

%files -n %{libnametest}
%{_libdir}/libgnunettesting.so.%{test_major}*

%files -n %{libnametrans}
%{_libdir}/libgnunettransport.so.%{trans_major}*

%files -n %{devname}
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

