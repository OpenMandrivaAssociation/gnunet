%define gnunetuser gnunetd
%define gnunethome /var/lib/gnunet

%define libs arm ats block blockgroup cadet consensus conversation core curl datacache datastore dht did dns fragmentation friends fs gns gnsrecord gnsrecordjson hello identity json messenger microphone namecache namestore natauto natnew nse nt peerinfo peerstore pq reclaim regex regexblock rest revocation scalarproduct secretsharing set seti setu speaker sq statistics testbed testbedlogger testing testingdhtu transport transportapplication transportcommunicator transportcore transportmonitor transporttesting transporttesting2 util vpn
%define devname %mklibname -d %{name}

Summary:	Secure and anonymous peer-to-peer file sharing
Name:		gnunet
Version:	0.19.4
Release:	1
License:	GPLv2+
Group:		Networking/File transfer
Url:		http://gnunet.org/
Source0:	ftp://ftp.gnu.org/gnu/gnunet/%{name}-%{version}.tar.gz
Source1:	gnunetd.conf
Source2:	init_gnunetd
Patch0:		gnunet-0.19.4-no-Lusrlib.patch
BuildRequires:	gettext-devel
BuildRequires:	gmp-devel
BuildRequires:	libltdl-devel
BuildRequires:	mysql-devel
BuildRequires:	locales-extra-charsets
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libcurl-gnutls)
BuildRequires:	pkgconfig(libextractor)
BuildRequires:	pkgconfig(libgcrypt) >= 1.6.0
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(libsodium)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libunistring)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	doxygen
Suggests:	mysql-client
# Just so the path can be detected
BuildRequires:	openssh-clients
BuildRequires:	iptables
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
%doc %{_docdir}/gnunet
%attr(0700, %{gnunetuser}, %{gnunetuser}) %dir %{gnunethome}
%config %{_sysconfdir}/gnunet.d
%{_initrddir}/%{name}d
%{_bindir}/*
%{_libdir}/%{name}
%{_libdir}/libnss_gns*.so.*
%{_libdir}/libgnunetmy.so.*
%{_libdir}/libgnunetmysql.so.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/gnunet-uri.desktop
%{_mandir}/man1/%{name}-*
%{_infodir}/gnunet.info*
%{_mandir}/man5/gnunet.conf.5*

%pre
%_pre_useradd %{gnunetuser} %{gnunethome} /bin/false

%post
%_post_service %{name}d

%preun
%_preun_service %{name}d

%postun
%_postun_userdel %{gnunetuser}


#----------------------------------------------------------------------------
%(for i in %{libs}; do
	cat <<EOF
%package -n %{_lib}%{name}$i
Summary:	$i libraries for GNUnet
Group:		System/Libraries

%description -n %{_lib}%{name}$i
$i libraries for GNUnet

%files -n %{_lib}%{name}$i
%{_libdir}/lib%{name}$i.so.*
EOF
done)

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{libname}
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
%(for i in %{libs}; do
	echo "Requires: %{_lib}%{name}$i = %{EVRD}"
done
)

%description -n %{devname}
Development files for %{libname}.

%files -n %{devname}
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_datadir}/aclocal/gnunet.m4

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%configure
echo "===== config.log ====="
cat config.log
echo "======================"
# makefile doesn't support running multiple jobs simultaneously
make

%install
%make_install
mkdir -p %{buildroot}%{gnunethome}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_initrddir}
install -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
ln -s %{_datadir}/%{name}/config.d %{buildroot}%{_sysconfdir}/gnunet.d

%find_lang %{name}

