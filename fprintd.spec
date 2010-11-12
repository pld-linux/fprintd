Summary:	Daemon to offer libfprint functionality over D-Bus
Summary(pl.UTF-8):	Demon oferujący funkcjonalność libfprint poprzez D-Bus
Name:		fprintd
Version:	0.2.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.bz2
# Source0-md5:	d6f023e6560d5647eadf668cdbcee57a
URL:		http://www.reactivated.net/fprint/wiki/Fprintd
BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libfprint-devel >= 0.1.0
BuildRequires:	libxslt-progs
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.91
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Daemon to offer libfprint functionality over D-Bus.

%description -l pl.UTF-8
Demon oferujący funkcjonalność libfprint poprzez D-Bus.

%package -n pam-pam_fprintd
Summary:	PAM module for fingerprint authentication
Summary(pl.UTF-8):	Moduł PAM do uwierzytelniania odciskiem palca
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_fprintd
PAM module for fingerprint authentication.

%description -n pam-pam_fprintd -l pl.UTF-8
Moduł PAM do uwierzytelniania odciskiem palca.

%prep
%setup -q

%build
%configure \
	--disable-static

%{__make} \
	pammoddir=/%{_lib}/security

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pammoddir=/%{_lib}/security

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_fprintd.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO doc/html/*
%attr(755,root,root) %{_bindir}/fprintd-delete
%attr(755,root,root) %{_bindir}/fprintd-enroll
%attr(755,root,root) %{_bindir}/fprintd-list
%attr(755,root,root) %{_bindir}/fprintd-verify
%attr(755,root,root) %{_libdir}/fprintd
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.*.xml
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fprintd.conf
/etc/dbus-1/system.d/net.reactivated.Fprint.conf
%{_mandir}/man1/fprintd.1*

%files -n pam-pam_fprintd
%defattr(644,root,root,755)
%doc pam/README
%attr(755,root,root) /%{_lib}/security/pam_fprintd.so
