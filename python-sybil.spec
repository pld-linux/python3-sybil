#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module [built from python3-sybil.spec]

Summary:	Automated testing for the examples in your documentation
Summary(pl.UTF-8):	Automatyczne testowanie dla przykładów w dokumentacji
Name:		python-sybil
# keep 2.x here for python2 support
Version:	2.0.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sybil/
Source0:	https://files.pythonhosted.org/packages/source/s/sybil/sybil-%{version}.tar.gz
# Source0-md5:	8a445db9badbe9cf26e9126075ff6696
URL:		https://pypi.org/project/sybil/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest >= 3.5.0
BuildRequires:	python-pytest-cov
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 3.5.0
BuildRequires:	python3-pytest-cov
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-sybil
Summary:	Automated testing for the examples in your documentation
Summary(pl.UTF-8):	Automatyczne testowanie dla przykładów w dokumentacji
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-sybil
This library provides a way to test examples in your documentation by
parsing them from the documentation source and evaluating the parsed
examples as part of your normal test run. Integration is provided for
the main Python test runners.

%description -n python3-sybil -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# example.py required because of getsourcefile() in integration/pytest.py
%py_postclean -x example.py
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/sybil
%{py_sitescriptdir}/sybil-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-sybil
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/sybil
%{py3_sitescriptdir}/sybil-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
