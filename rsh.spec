Summary:	Clients and servers for remote access commands (rsh, rlogin, rcp).
Name:		rsh
Version:	0.17
Release:	0
Copyright:	BSD
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Source0:	ftp://ftp.linux.uk.org/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	rexec.pamd
Source2:	rlogin.pamd
Source3:	rsh.pamd
Source4:	rexec-1.5.tar.gz
Source5:	rlogind.inetd
Source6:	rshd.inetd
Patch0:		netkit-rsh-sectty.patch
Patch1:		netkit-rsh-rexec.patch
Patch2:		netkit-rsh-stdarg.patch
Patch3:		netkit-rsh-install.patch
Patch4:		netkit-rsh-pamfix.patch
Patch5:		netkit-rsh-jbj2.patch
Patch6:		netkit-rsh-jbj3.patch
Patch7:		netkit-rsh-pam-link.patch
Patch8:		netkit-rsh-prompt.patch
Patch9:		netkit-rsh-rlogin=rsh.patch
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
%setup -q -n netkit-rsh-0.17 -a4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Should be removed (?)
# %patch4 -p1
%patch5 -p1
# Should be removed (?)
# %patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# No, I don't know what this is doing in the tarball.
rm -f rexec/rexec

%build
./configure
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/pam.d,%{_bindir},%{_sbindir},%{_mandir}/man{1,8}}
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/rexec
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/rlogin
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/rsh
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/rlogind
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/rshd

mv -f $RPM_BUILD_ROOT%{_mandir}/rexec* $RPM_BUILD_ROOT%{_mandir}/man1/

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/{rexec,rlogin,rsh}d.8

echo ".so in.rexecd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rexecd.8
echo ".so in.rlogind.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rlogind.8
echo ".so in.rshd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/rshd.8

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* || :

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/rsh
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/rlogin
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/rexec
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/rlogind
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/rshd
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
