#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Daemon to offer libfprint functionality over D-Bus
Summary(pl.UTF-8):	Demon oferujący funkcjonalność libfprint poprzez D-Bus
Name:		fprintd
Version:	1.90.8
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/libfprint/fprintd/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	94f1760274a6dc95fcd713edc393206b
URL:		https://fprint.freedesktop.org/
BuildRequires:	dbus-glib-devel
%{?with_apidocs:BuildRequires:	docbook-dtd412-xml}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.3}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libfprint-devel >= 1.90.6
%{?with_apidocs:BuildRequires:	libxml2-progs}
%{?with_apidocs:BuildRequires:	libxslt-progs}
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja
BuildRequires:	pam-devel
BuildRequires:	pam_wrapper
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.91
BuildRequires:	python3-dbusmock
BuildRequires:	python3-pypamtest
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	libfprint >= 0.6.0
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
BuildArch:	noarch

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
%setup -q -n %{name}-v%{version}

%build
%meson build \
	-Dgtk_doc=%__true_false apidocs

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/fprint

%meson_install -C build

# to -devel, but we haven't any
%{__rm} $RPM_BUILD_ROOT%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.*.xml

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post fprintd.service

%preun
%systemd_preun fprintd.service

%postun
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fprintd.conf
%attr(755,root,root) %{_bindir}/fprintd-delete
%attr(755,root,root) %{_bindir}/fprintd-enroll
%attr(755,root,root) %{_bindir}/fprintd-list
%attr(755,root,root) %{_bindir}/fprintd-verify
%attr(755,root,root) %{_libexecdir}/fprintd
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/dbus-1/system.d/net.reactivated.Fprint.conf
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{systemdunitdir}/fprintd.service
%{_mandir}/man1/fprintd.1*
%dir %attr(700,root,root) /var/lib/fprint

%files -n pam-pam_fprintd
%defattr(644,root,root,755)
%doc pam/README
%attr(755,root,root) /%{_lib}/security/pam_fprintd.so
%{_mandir}/man8/pam_fprintd.8*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/fprintd
%endif
