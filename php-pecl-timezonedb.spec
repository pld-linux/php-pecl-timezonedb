%define		_modname	timezonedb
%define		_status		stable
Summary:	%{_modname} - timezone database to be used with PHP's date and time functions
Summary(pl):	%{_modname} - baza stref czasowych do wykorzystania z funkcjami date() oraz time()
Name:		php-pecl-%{_modname}
Version:	2006.16
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	052ab30554b1f30c64ab8ea46cebe8a5
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

In PECL status of this extension is: %{_status}.

%description -l pl
To rozszerzenie zastêpuje wbudowanê bazê stref czasowych dostarczan±
wraz z PHP. Nale¿y instalowaæ to rozszerzenie tylko je¶li musimy
skorzystaæ z nowszej wersji bazy stref czasowych ni¿ tej dostarczanej
wraz z archiwum PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
