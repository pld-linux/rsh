Summary:	rsh client and rcp command
Name:		rsh
Version:	0.17
Release:	5
License:	BSD
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Source0:	ftp://ftp.linux.uk.org/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	rexec.pamd
Source2:	rlogin.pamd
Source3:	%{name}.pamd
Source4:	rexec-1.5.tar.gz
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	heimdal-rsh

%description
The rsh package a program which allow users to run commmands on remote
machines, login to other machines and copy files between machines.
Package also contains rcp command

%package -n rshd
Summary:	Servers for rsh
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Prereq:		rc-inetd
Obsoletes:	heimdal-rshd
Obsoletes:	rsh-server

%description -n rshd
The rshd package contains a program which allow users to run commmands
on remote machines, login to other machines and copy files between
machines (rsh).

%package -n rlogin
Summary:	rlogin client
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Obsoletes:	heimdal-rlogin

%description -n rlogin
The rlogin package contains a program which allow users to login
on remote machines (rlogin).

%package -n rlogind
Summary:	Servers for rlogin
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Prereq:		rc-inetd
Obsoletes:	heimdal-rlogin
Requires:	login
Obsoletes:	rsh-server

%description -n rlogind
The rlogind package contains a program which allow users to login
on remote machines.

%package -n rexec
Summary:	rexec client
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Obsoletes:	heimdal-rexec
Obsoletes:	rsh-server

%description -n rexec
The rexec package contains a program which allow users to execute
commnad on remote machines (rexec).

%package -n rexecd
Summary:	Servers for rexec
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Prereq:		rc-inetd
Obsoletes:	heimdal-rexecd

%description -n rexecd
The rexecd package contains a server which allow users to execute
commnad on remote machines (rexec).

%prep
%setup -q -n netkit-rsh-0.17 -a4
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
./configure --with-c-compiler=%{__cc}
%{__make} CFLAGS="%{rpmcflags}"

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

%post -n rshd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun -n rshd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post -n rlogind
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun -n rlogind
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post -n rexecd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun -n rexecd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rsh
%attr(755,root,root) %{_bindir}/rcp
%{_mandir}/man1/rsh.1*
%{_mandir}/man1/rcp.1*

%files -n rshd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/rsh
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/rshd
%attr(755,root,root) %{_sbindir}/in.rshd
%{_mandir}/man8/in.rshd.8*
%{_mandir}/man8/rshd.8*

%files -n rlogin
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rlogin
%{_mandir}/man1/rlogin.1*

%files -n rlogind
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/rlogin
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/rlogind
%attr(755,root,root) %{_sbindir}/in.rlogind
%{_mandir}/man8/in.rlogind.8*
%{_mandir}/man8/rlogind.8*

%files -n rexec
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rexec
%{_mandir}/man1/rexec.1*

%files -n rexecd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/rexec
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/rexec
%attr(755,root,root) %{_sbindir}/in.rexecd
%{_mandir}/man8/in.rexecd.8*
%{_mandir}/man8/rexecd.8*
