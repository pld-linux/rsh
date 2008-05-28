Summary:	rsh client and rcp command
Summary(pl.UTF-8):	Klient rsh i polecenie rcp
Name:		rsh
Version:	0.17
Release:	22
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
# Source0-md5:	65f5f28e2fe22d9ad8b17bb9a10df096
Source1:	rexec.pamd
Source2:	rlogin.pamd
Source3:	%{name}.pamd
Source4:	rexec-1.5.tar.gz
# Source4-md5:	17c2b2fa2aed6af7e0b850673d5ef1f9
Source5:	rlogind.inetd
Source6:	%{name}d.inetd
Source7:	rexec.inetd
Patch0:		netkit-%{name}-sectty.patch
Patch1:		netkit-%{name}-rexec.patch
Patch2:		netkit-%{name}-stdarg.patch
Patch3:		netkit-%{name}-install.patch
Patch4:		netkit-%{name}-jbj2.patch
Patch5:		netkit-%{name}-pam-link.patch
Patch6:		netkit-%{name}-prompt.patch
Patch7:		netkit-%{name}-rlogin=rsh.patch
Patch8:		netkit-%{name}-nokrb.patch
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	pam >= 0.79.0
Obsoletes:	heimdal-rsh
Obsoletes:	krb5-rsh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rsh package contains programs which allow users to run commmands
on remote machines (rsh) and copy files between machines (rcp).

%description -l pl.UTF-8
Pakiet rsh zawiera program pozwalający użytkownikom na uruchamianie
poleceń na zdalnych maszynach (rsh) i kopiowanie plików między
maszynami (rcp).

%package -n rshd
Summary:	Servers for rsh
Summary(pl.UTF-8):	Serwery dla rsh
Group:		Applications/Networking
Requires:	pam >= 0.77.3
Requires:	rc-inetd
Obsoletes:	heimdal-rshd
Obsoletes:	krb5-kshd
Obsoletes:	rsh-server

%description -n rshd
The rshd package contains a server which allow users to run commmands
from remote machines (rsh) and copy files between machines (rcp).

%description -n rshd -l pl.UTF-8
Pakiet rshd zawiera serwer pozwalający użytkownikom uruchamiać
polecenia ze zdalnych maszyn (rsh) oraz kopiować pliki między
maszynami (rcp).

%package -n rlogin
Summary:	rlogin client
Summary(pl.UTF-8):	Klient rlogin
Group:		Applications/Networking
Obsoletes:	heimdal-rlogin
Obsoletes:	krb5-rlogin

%description -n rlogin
The rlogin package contains a program which allow users to login on
remote machines (rlogin).

%description -n rlogin -l pl.UTF-8
Pakiet rlogin zawiera program pozwalający użytkownikom na logowanie
się na zdalne maszyny (rlogin).

%package -n rlogind
Summary:	Servers for rlogin
Summary(pl.UTF-8):	Serwer rlogin
Group:		Applications/Networking
Requires:	login
Requires:	pam >= 0.77.3
Requires:	rc-inetd
Obsoletes:	heimdal-rlogin
Obsoletes:	krb5-klogind
Obsoletes:	rsh-server

%description -n rlogind
The rlogind package contains a server which allow users to login from
remote machines.

%description -n rlogind -l pl.UTF-8
Pakiet rlogind zawiera serwer pozwalający użytkownikom logować się ze
zdalnych maszyn.

%package -n rexec
Summary:	rexec client
Summary(pl.UTF-8):	Klient rexec
Group:		Applications/Networking
Obsoletes:	rsh-server

%description -n rexec
The rexec package contains a program which allow users to execute
programs on remote machines (rexec).

%description -n rexec -l pl.UTF-8
Pakiet rexec zawiera program pozwalający użytkownikom uruchamiać
programy na zdalnych maszynach (rexec).

%package -n rexecd
Summary:	Servers for rexec
Summary(pl.UTF-8):	Serwer rexec
Group:		Applications/Networking
Requires:	pam >= 0.77.3
Requires:	rc-inetd

%description -n rexecd
The rexecd package contains a server which allow users to execute
programs from remote machines (rexec).

%description -n rexecd -l pl.UTF-8
Pakiet rexecd zawiera serwer pozwalający użytkownikom na uruchamianie
programów ze zdalnych maszyn (rexec).

%prep
%setup -q -n netkit-%{name}-%{version} -a4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# No, I don't know what this is doing in the tarball.
rm -f rexec/rexec

%build
./configure \
	--with-c-compiler="%{__cc}"
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/pam.d,%{_bindir},%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/rexec
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/rlogin
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/rsh
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/rlogind
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/rshd
install %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/rexec

mv -f $RPM_BUILD_ROOT%{_mandir}/rexec* $RPM_BUILD_ROOT%{_mandir}/man1/

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/{rexec,rlogin,rsh}d.8

echo ".so in.rexecd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rexecd.8
echo ".so in.rlogind.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rlogind.8
echo ".so in.rshd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rshd.8

%clean
rm -rf $RPM_BUILD_ROOT

%post -n rshd
%service -q rc-inetd reload

%postun -n rshd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post -n rlogind
%service -q rc-inetd reload

%postun -n rlogind
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post -n rexecd
%service -q rc-inetd reload

%postun -n rexecd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/rsh
%attr(4755,root,root) %{_bindir}/rcp
%{_mandir}/man1/rsh.1*
%{_mandir}/man1/rcp.1*

%files -n rshd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/rsh
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/rshd
%attr(755,root,root) %{_sbindir}/in.rshd
%{_mandir}/man8/in.rshd.8*
%{_mandir}/man8/rshd.8*

%files -n rlogin
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/rlogin
%{_mandir}/man1/rlogin.1*

%files -n rlogind
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/rlogin
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/rlogind
%attr(755,root,root) %{_sbindir}/in.rlogind
%{_mandir}/man8/in.rlogind.8*
%{_mandir}/man8/rlogind.8*

%files -n rexec
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rexec
%{_mandir}/man1/rexec.1*

%files -n rexecd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/rexec
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/rexec
%attr(755,root,root) %{_sbindir}/in.rexecd
%{_mandir}/man8/in.rexecd.8*
%{_mandir}/man8/rexecd.8*
