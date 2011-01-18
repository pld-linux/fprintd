#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Daemon to offer libfprint functionality over D-Bus
Summary(pl.UTF-8):	Demon oferujący funkcjonalność libfprint poprzez D-Bus
Name:		fprintd
Version:	0.2.0
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.bz2
# Source0-md5:	d6f023e6560d5647eadf668cdbcee57a
Patch0:		dont-ever-unload.patch
URL:		http://www.reactivated.net/fprint/wiki/Fprintd
BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel >= 2.0.0
%{?with_apidocs:BuildRequires:  gtk-doc}
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

%package apidocs
Summary:	fprintd API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki fprintd
License:	GFDL v1.1+
Group:		Documentation
Requires:	gtk-doc

%description apidocs
API and internal documentation for fprintd library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki fprintd.

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
%patch0 -p1

%build
%configure \
	%{?with_apidocs:--enable-gtk-doc} \
	--disable-static

%{__make} \
	pammoddir=/%{_lib}/security

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/fprint
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pammoddir=/%{_lib}/security

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_fprintd.la

# to -devel, but we haven't any
rm $RPM_BUILD_ROOT%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.*.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fprintd.conf
%attr(755,root,root) %{_bindir}/fprintd-delete
%attr(755,root,root) %{_bindir}/fprintd-enroll
%attr(755,root,root) %{_bindir}/fprintd-list
%attr(755,root,root) %{_bindir}/fprintd-verify
%attr(755,root,root) %{_libdir}/fprintd
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
/etc/dbus-1/system.d/net.reactivated.Fprint.conf
%{_mandir}/man1/fprintd.1*
%dir %attr(700,root,root) /var/lib/fprint

%files -n pam-pam_fprintd
%defattr(644,root,root,755)
%doc pam/README
%attr(755,root,root) /%{_lib}/security/pam_fprintd.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_datadir}/gtk-doc/html/fprintd
%endif
