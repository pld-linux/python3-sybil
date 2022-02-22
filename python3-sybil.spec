#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Automated testing for the examples in your documentation
Summary(pl.UTF-8):	Automatyczne testowanie dla przykładów w dokumentacji
Name:		python3-sybil
Version:	3.0.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sybil/
Source0:	https://files.pythonhosted.org/packages/source/s/sybil/sybil-%{version}.tar.gz
# Source0-md5:	fd8e33c2691eb042a16dfc179687592b
URL:		https://pypi.org/project/sybil/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 6.2.0
BuildRequires:	python3-pytest-cov
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides a way to test examples in your documentation by
parsing them from the documentation source and evaluating the parsed
examples as part of your normal test run. Integration is provided for
the main Python test runners.

%description -l pl.UTF-8
Ta biblioteka pozwala na testowanie przykładów w dokumentacji poprzez
ich analizę ze źródeł dokumentacji i wykonywanie jako części
normalnego uruchamiania testów. Zapewniona jest integracja z głównymi
sposobami uruchamiania testów w Pythonie.

%package apidocs
Summary:	API documentation for Python sybil module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sybil
Group:		Documentation

%description apidocs
API documentation for Python sybil module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sybil.

%prep
%setup -q -n sybil-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/sybil
%{py3_sitescriptdir}/sybil-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
