Summary:	Clients and servers for remote access commands (rsh, rlogin, rcp).
Name:		rsh
Version:	0.10
Release:	26
Copyright:	BSD
Group:		Applications/Internet
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-%{name}-%{version}.tar.gz
Source1:	rexec.pamd
Source2:	rlogin.pamd
Source3:	rsh.pamd
Source4:	rexec-1.4.tar.gz
Patch0:		netkit-rsh-0.10-misc.patch
Patch1:		netkit-rsh-0.10-newpam.patch
Patch2:		netkit-rsh-0.10-sectty.patch
Patch3:		netkit-rsh-0.10-rexec.patch
Patch4:		netkit-rsh-install.patch
Requires:	inetd, pam >= 0.59
Buildroot:	/tmp/%{name}-%{version}-root

%description
The rsh package contains a set of programs which allow users to run
commmands on remote machines, login to other machines and copy files
between machines (rsh, rlogin and rcp).  All three of these commands
use rhosts style authentication.  This package contains the clients
and servers needed for all of these services.  It also contains a
server for rexec, an alternate method of executing remote commands.
All of these servers are run by inetd and configured using
/etc/inetd.conf and PAM.  The rexecd server is disabled by default,
but the other servers are enabled.

The rsh package should be installed to enable remote access to other
machines.

%prep
%setup -q -n netkit-rsh-0.10 -a 4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

make -C rexec-1.4

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/pam.d,%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}
make INSTALLROOT=$RPM_BUILD_ROOT install

make INSTALLROOT=$RPM_BUILD_ROOT install -C rexec-1.4

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/rexec
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/rlogin
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/rsh

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* || :

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
/etc/pam.d/rsh
/etc/pam.d/rlogin
/etc/pam.d/rexec
%attr(755,root,root) %{_bindir}/rcp
%attr(755,root,root) %{_bindir}/rexec
%attr(755,root,root) %{_bindir}/rlogin
%attr(755,root,root) %{_bindir}/rsh
%attr(755,root,root) %{_sbindir}/in.rexecd
%attr(755,root,root) %{_sbindir}/in.rlogind
%attr(755,root,root) %{_sbindir}/in.rshd
%{_mandir}/man1/rcp.1*
%{_mandir}/man1/rexec.1*
%{_mandir}/man1/rlogin.1*
%{_mandir}/man1/rsh.1*
%{_mandir}/man8/in.rexecd.8*
%{_mandir}/man8/in.rlogind.8*
%{_mandir}/man8/in.rshd.8*
%{_mandir}/man8/rexecd.8*
%{_mandir}/man8/rlogind.8*
%{_mandir}/man8/rshd.8*
