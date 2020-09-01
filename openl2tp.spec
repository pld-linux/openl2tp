Summary:	An L2TP client/server, designed for VPN use
Summary(pl.UTF-8):	Klient/serwer L2TP, zaprojektowany pod kątem VPN
Name:		openl2tp
Version:	1.8
Release:	7
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net//openl2tp/%{name}-%{version}.tar.gz
# Source0-md5:	e3d08dedfb9e6a9a1e24f6766f6dadd0
Source1:	%{name}d.init
Source2:	%{name}d.sysconfig
Source3:	%{name}.tmpfiles
Patch0:		%{name}-no_Werror.patch
Patch1:		%{name}-setkey.patch
Patch2:		no-hardcoded-libdir.patch
Patch3:		%{name}-tirpc.patch
URL:		http://www.openl2tp.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtirpc-devel
BuildRequires:	linux-libc-headers >= 2.6.23
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpcsvc-proto
BuildRequires:	rpmbuild(macros) >= 1.644
Requires:	ppp >= 2.4.5
Requires:	readline >= 4.2
Requires:	rpcbind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenL2TP is a complete implementation of RFC2661 - Layer Two Tunneling
Protocol Version 2, able to operate as both a server and a client. It
is ideal for use as an enterprise L2TP VPN server, supporting more
than 100 simultaneous connected users. It may also be used as a client
on a home PC or roadwarrior laptop.

OpenL2TP has been designed and implemented specifically for Linux. It
consists of:
- a daemon, openl2tpd, handling the L2TP control protocol exchanges
  for all tunnels and sessions
- a plugin for pppd to allow its PPP connections to run over L2TP
  sessions
- a Linux kernel driver for efficient datapath (integrated into the
  standard kernel from 2.6.23).
- a command line application, l2tpconfig, for management.

%description -l pl.UTF-8
OpenL2TP to kompletna implementacja RFC2661 - Layer Two Tunneling
Protocol (protokołu tunelowania warstwy drugiej) w wersji 2, będąca w
stanie działać zarówno jako serwer, jak i klient. Nadaje się do użycia
jako serwer VPN L2TP, obsługujący ponad 100 jednocześnie podłączonych
użytkowników. Może być także używana jako klient na domowym komputerze
lub podróżnym laptopie.

OpenL2TP został zaprojektowany i zaimplementowany dla Linuksa. Składa
się z:
- demona openl2tpd, obsługującego protokół sterujący L2TP dla
  wszystkich tuneli i sesji
- wtyczki pppd, pozwalającej na uruchamianie połączeń PPP po sesjach
  L2TP
- serwownika jądra Linuksa umożliwiającego wydajne przesyłanie danych
  (zintegrowanego do jądra od wersji 2.6.23)
- aplikacji linii poleceń l2tpconfig do zarządzania.

%package devel
Summary:	OpenL2TP support files for plugin development
Summary(pl.UTF-8):	Pliki OpenL2TP do tworzenia wtyczek
Group:		Development/Libraries

%description devel
This package contains support files for building plugins for OpenL2TP,
or applications that use the OpenL2TP APIs.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki wspomagające budowanie wtyczek OpenL2TP oraz
aplikacji wykorzystujących API OpenL2TP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS.optimize="%{rpmcflags} %{rpmcppflags} $(pkg-config --cflags libtirpc)" \
	SYS_LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/var/run/%{name}} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	SYS_LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openl2tpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/openl2tpd
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/openl2tpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README
%dir %{_libdir}/openl2tp
%attr(755,root,root) %{_bindir}/l2tpconfig
%attr(755,root,root) %{_sbindir}/openl2tpd
%attr(755,root,root) %{_libdir}/openl2tp/ppp_null.so
%attr(755,root,root) %{_libdir}/openl2tp/ppp_unix.so
%attr(755,root,root) %{_libdir}/openl2tp/ipsec.so
%attr(755,root,root) %{_libdir}/openl2tp/event_sock.so
%{_mandir}/man1/l2tpconfig.1*
%{_mandir}/man5/openl2tpd.conf.5*
%{_mandir}/man7/openl2tp.7*
%{_mandir}/man8/openl2tpd.8*
%attr(754,root,root) /etc/rc.d/init.d/openl2tpd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/openl2tpd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openl2tpd.conf
%dir /var/run/%{name}
%{systemdtmpfilesdir}/%{name}.conf

%files devel
%defattr(644,root,root,755)
%doc plugins/README doc/README.event_sock
%{_libdir}/openl2tp/l2tp_rpc.x
%{_libdir}/openl2tp/l2tp_event.h
%{_libdir}/openl2tp/event_sock.h
%{_mandir}/man4/openl2tp_rpc.4*
