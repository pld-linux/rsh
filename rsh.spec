Summary: Clients and servers for remote access commands (rsh, rlogin, rcp).
Name: rsh
Version: 0.10
Release: 25
Copyright: BSD
Group: Applications/Internet
Source: ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rsh-0.10.tar.gz
Source1: rexec.pam
Source2: rlogin.pam
Source3: rsh.pam
Source4: rexec-1.4.tar.gz
Patch0: netkit-rsh-0.10-misc.patch
Patch1: netkit-rsh-0.10-newpam.patch
Patch2: netkit-rsh-0.10-sectty.patch
Patch3: netkit-rsh-0.10-rexec.patch
Requires: inetd, pam >= 0.59
Buildroot: /var/tmp/%{name}-root

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
%patch0 -p1 -b .misc
%patch1 -p1 -b .newpam
%patch2 -p1 -b .sectty
%patch3 -p1 -b .rexec

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

make -C rexec-1.4

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man5
mkdir -p $RPM_BUILD_ROOT/usr/man/man8
make INSTALLROOT=$RPM_BUILD_ROOT install

make INSTALLROOT=$RPM_BUILD_ROOT install -C rexec-1.4
strip $RPM_BUILD_ROOT/usr/bin/rexec

install -m 644 $RPM_SOURCE_DIR/rexec.pam $RPM_BUILD_ROOT/etc/pam.d/rexec
install -m 644 $RPM_SOURCE_DIR/rlogin.pam $RPM_BUILD_ROOT/etc/pam.d/rlogin
install -m 644 $RPM_SOURCE_DIR/rsh.pam $RPM_BUILD_ROOT/etc/pam.d/rsh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/pam.d/rsh
/etc/pam.d/rlogin
/etc/pam.d/rexec
/usr/bin/rcp
/usr/bin/rexec
/usr/bin/rlogin
/usr/bin/rsh
/usr/man/man1/rcp.1
/usr/man/man1/rexec.1
/usr/man/man1/rlogin.1
/usr/man/man1/rsh.1
/usr/man/man8/in.rexecd.8
/usr/man/man8/in.rlogind.8
/usr/man/man8/in.rshd.8
/usr/man/man8/rexecd.8
/usr/man/man8/rlogind.8
/usr/man/man8/rshd.8
/usr/sbin/in.rexecd
/usr/sbin/in.rlogind
/usr/sbin/in.rshd
