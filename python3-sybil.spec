#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Automated testing for the examples in your documentation
Summary(pl.UTF-8):	Automatyczne testowanie dla przykładów w dokumentacji
Name:		python3-sybil
Version:	10.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sybil/
Source0:	https://files.pythonhosted.org/packages/source/s/sybil/sybil-%{version}.tar.gz
# Source0-md5:	6e78e792cf585deb898f6667e96892ac
URL:		https://pypi.org/project/sybil/
BuildRequires:	python3-build
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.11
%if %{with tests}
BuildRequires:	python3-myst_parser
BuildRequires:	python3-pytest >= 8
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-seedir
BuildRequires:	python3-testfixtures >= 11
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3 >= 8
%endif
Requires:	python3-modules >= 1:3.11
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
%py3_build_pyproject

%if %{with tests} || %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/build-3-test \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3-test \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/sybil
%{py3_sitescriptdir}/sybil-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
