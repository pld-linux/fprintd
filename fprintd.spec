# TODO: systemd post/preun
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Daemon to offer libfprint functionality over D-Bus
Summary(pl.UTF-8):	Demon oferujący funkcjonalność libfprint poprzez D-Bus
Name:		fprintd
Version:	0.5.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.bz2
# Source0-md5:	74cff28ed2b6b72453fbc4465761a114
URL:		http://www.reactivated.net/fprint/wiki/Fprintd
BuildRequires:	dbus-glib-devel
%{?with_apidocs:BuildRequires:	docbook-dtd412-xml}
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
%{?with_apidocs:BuildRequires:  gtk-doc >= 1.3}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libfprint-devel >= 0.5.0
%{?with_apidocs:BuildRequires:	libxslt-progs}
BuildRequires:	pam-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.91
BuildRequires:	rpmbuild(macros) >= 1.644
Requires:	libfprint >= 0.5.0
Requires:	systemd-units >= 38
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
Requires:	gtk-doc-common

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

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	%{?with_apidocs:--enable-gtk-doc --with-html-dir=%{_gtkdocdir}}

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
%{__rm} $RPM_BUILD_ROOT%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.*.xml

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{bg_BG,bg}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{fa_IR,fa}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fprintd.conf
%attr(755,root,root) %{_bindir}/fprintd-delete
%attr(755,root,root) %{_bindir}/fprintd-enroll
%attr(755,root,root) %{_bindir}/fprintd-list
%attr(755,root,root) %{_bindir}/fprintd-verify
%attr(755,root,root) %{_libdir}/fprintd
/etc/dbus-1/system.d/net.reactivated.Fprint.conf
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{systemdunitdir}/fprintd.service
%{_mandir}/man1/fprintd.1*
%dir %attr(700,root,root) /var/lib/fprint

%files -n pam-pam_fprintd
%defattr(644,root,root,755)
%doc pam/README
%attr(755,root,root) /%{_lib}/security/pam_fprintd.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/fprintd
%endif
