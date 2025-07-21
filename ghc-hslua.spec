#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hslua
Summary:	A Lua language interpreter embedding in Haskell
Summary(pl.UTF-8):	Osadzanie interpretera języka Lua w Haskellu
Name:		ghc-%{pkgname}
Version:	1.1.0
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/hslua
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	765647d6f5788fa12f5d82557e73786c
URL:		http://hackage.haskell.org/package/hslua
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.8
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.10.2
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-containers >= 0.5
BuildRequires:	ghc-containers < 0.7
BuildRequires:	ghc-exceptions >= 0.8
BuildRequires:	ghc-exceptions < 0.11
BuildRequires:	ghc-mtl >= 2.2
BuildRequires:	ghc-mtl < 2.3
BuildRequires:	ghc-text >= 1.0
BuildRequires:	ghc-text < 1.3
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.8
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.10.2
BuildRequires:	ghc-containers-prof >= 0.5
BuildRequires:	ghc-exceptions-prof >= 0.8
BuildRequires:	ghc-mtl-prof >= 2.1
BuildRequires:	ghc-text-prof >= 1.0
%endif
BuildRequires:	lua53-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.608
BuildRequires:	sed >= 4.0
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.8
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.10.2
Requires:	ghc-containers >= 0.5
Requires:	ghc-exceptions >= 0.8
Requires:	ghc-mtl >= 2.1
Requires:	ghc-text >= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The Foreign.Lua module is a wrapper of Lua language interpreter as
described in <https://www.lua.org/>.

%description -l pl.UTF-8
Moduł Foreign.Lua to obudowanie interpretera języka Lua, opisanego
na <https://www.lua.org/>.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof >= 6.12.3
Requires:	ghc-base-prof >= 4.8
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.10.2
Requires:	ghc-containers-prof >= 0.5
Requires:	ghc-exceptions-prof >= 0.8
Requires:	ghc-mtl-prof >= 2.1
Requires:	ghc-text-prof >= 1.0

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--flags=pkg-config \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version} \

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShslua-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShslua-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShslua-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Core
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Core/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Core/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Types
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Types/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Types/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShslua-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Core/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Types/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
