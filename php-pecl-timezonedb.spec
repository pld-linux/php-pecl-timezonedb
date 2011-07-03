%define		modname	timezonedb
%define		status		stable
Summary:	%{modname} - timezone database to be used with PHP's date and time functions
Summary(pl.UTF-8):	%{modname} - baza stref czasowych do wykorzystania z funkcjami date() oraz time()
Name:		php-pecl-%{modname}
Version:	2011.8
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	60199734243541519aec9e6cb023db43
URL:		http://pecl.php.net/package/timezonedb/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension is a drop-in replacement for the builtin timezone
database that comes with PHP. You should only install this extension
in case you need to get a later version of the timezone database then
the one that ships with PHP.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
To rozszerzenie zastępuje wbudowanę bazę stref czasowych dostarczaną
wraz z PHP. Należy instalować to rozszerzenie tylko jeśli musimy
skorzystać z nowszej wersji bazy stref czasowych niż tej dostarczanej
wraz z archiwum PHP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
