Summary:	Clients and servers for remote access commands (rsh, rlogin, rcp).
Name:		rsh
Version:	0.16.1
Release:	1
Copyright:	BSD
Group:		Applications/Internet
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-%{name}-0.16.tar.gz
Source1:	rexec.pamd
Source2:	rlogin.pamd
Source3:	rsh.pamd
Source4:	rexec-1.5.tar.gz
Patch0:		netkit-rsh-0.16-patch1.gz
Patch1:		netkit-rsh-sectty.patch
Patch2:		netkit-rsh-rexec.patch
Patch3:		netkit-rsh-stdarg.patch
Patch4:		netkit-rsh-install.patch
Patch5:		netkit-rsh-pamfix.patch
Patch6:		netkit-rsh-jbj2.patch
Patch7:		netkit-rsh-jbj3.patch
Patch8:		netkit-rsh-pam-link.patch
Patch9:		netkit-rsh-prompt.patch
Patch10:	netkit-rsh-rlogin=rsh.patch
Requires:	inetd, pam >= 0.59
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -n netkit-rsh-0.16 -a4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# No, I don't know what this is doing in the tarball.
rm -f rexec/rexec

%build
./configure
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/pam.d,%{_bindir},%{_sbindir},%{_mandir}/man{1,8}}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/rexec
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/rlogin
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/rsh

mv -f $RPM_BUILD_ROOT%{_mandir}/rexec* $RPM_BUILD_ROOT%{_mandir}/man1/

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/{rexec,rlogin,rsh}d.8

echo ".so in.rexecd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rexecd.8
echo ".so in.rlogind.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rlogind.8
echo ".so in.rshd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rshd.8

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* || :

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/rsh
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/rlogin
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/rexec
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
