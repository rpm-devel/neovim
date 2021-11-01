%bcond_with jemalloc
%bcond_without luajit

Name:           neovim
Version:        0.3.7.0.git.11455.078f8d716
Release:        1%{?dist}

License:        ASL 2.0
Summary:        Vim-fork focused on extensibility and agility
Url:            http://neovim.io

Source0:        neovim-0.3.7.0.git.11455.078f8d716.tar.gz
Source1:        sysinit.vim
Source2:        spec-template
%if ! %{with luajit}
Patch0:         neovim-0.1.7-bitop.patch
%endif

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gettext
BuildRequires:  gperf
BuildRequires:  gcc
%if %{with luajit}
# luajit implements version 5.1 of the lua language spec, so it needs the
# compat versions of libs.
BuildRequires:  luajit-devel
#BuildRequires:  compat-lua-lpeg
#BuildRequires:  compat-lua-mpack
BuildRequires:  lua-devel
%else
BuildRequires:  lua-devel
BuildRequires:  lua-lpeg
BuildRequires:  lua-mpack
%endif
%if %{with jemalloc}
BuildRequires:  jemalloc-devel
%endif
BuildRequires:  msgpack-devel >= 1.2.0
BuildRequires:  libtermkey-devel
BuildRequires:  libuv-devel
BuildRequires:  libvterm-devel
BuildRequires:  unibilium-devel
%if 0%{?el7}
BuildRequires:  lua-bit32
Requires:       lua-bit32
BuildRequires:  lua-devel
BuildRequires:  lua-lpeg
BuildRequires:  lua-lpeg
Requires: xsel
%else
Suggests:       (python2-neovim if python2)
Suggests:       (python3-neovim if python3)
# XSel provides access to the system clipboard
Recommends:     xsel
%endif

%description
Neovim is a refactor - and sometimes redactor - in the tradition of
Vim, which itself derives from Stevie. It is not a rewrite, but a
continuation and extension of Vim. Many rewrites, clones, emulators
and imitators exist; some are very clever, but none are Vim. Neovim
strives to be a superset of Vim, notwithstanding some intentionally
removed misfeatures; excepting those few and carefully-considered
excisions, Neovim is Vim. It is built for users who want the good
parts of Vim, without compromise, and more.

%prep
%setup -q -n neovim-0.3.7.0.git.11455.078f8d716

%build
mkdir -p build
pushd build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DPREFER_LUA=%{?with_luajit:OFF}%{!?with_luajit:ON} \
       -DLUA_PRG=%{_bindir}/%{?with_luajit:luajit}%{!?with_luajit:lua} \
       -DENABLE_JEMALLOC=%{?with_jemalloc:ON}%{!?with_jemalloc:OFF} \
       ..

%make_build VERBOSE=1
popd

%install
pushd build
%make_install
popd

install -p -m 644 %SOURCE1 %{buildroot}%{_datadir}/nvim/sysinit.vim
install -p -m 644 %SOURCE2 %{buildroot}%{_datadir}/nvim/template.spec

desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    runtime/nvim.desktop
install -d -m0755 %{buildroot}%{_datadir}/pixmaps
install -m0644 runtime/nvim.png %{buildroot}%{_datadir}/pixmaps/nvim.png

%fdupes %{buildroot}%{_datadir}/
%find_lang nvim

%files -f nvim.lang
%license LICENSE
%doc BACKERS.md CONTRIBUTING.md README.md
%{_bindir}/nvim
%{_datadir}/applications/nvim.desktop
%{_datadir}/nvim
%{_datadir}/pixmaps/nvim.png
%{_mandir}/man1/nvim.1*


%changelog
* Wed Jun 05 2019 Aron Griffis <aron@scampersand.com> - 0.3.7.0.git.11455.078f8d716-1
- Nightly build from git master

* Wed Mar 06 2019 Aron Griffis <aron@scampersand.com> - 0.3.4-1
- Update to version 0.3.4 with luajit, rhbz #1685781

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.3-2
- Remove Recommends: xterm

* Sun Jan 06 2019 Andreas Schneider <asn@redhat.com> - 0.3.3-1
- Update to version 0.3.3

* Wed Jan 02 2019 Andreas Schneider <asn@redhat.com> - 0.3.2-1
- Update to version 0.3.2

* Fri Aug 10 2018 Andreas Schneider <asn@redhat.com> - 0.3.1-1
- Update to version 0.3.1

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.3.0-6
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-5
- Rebuild for new binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-4
- Disable jemalloc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Andreas Schneider <asn@redhat.com> - 0.3.0-2
- resolves: #1592474 - Add jemalloc as a requirement

* Mon Jun 11 2018 Andreas Schneider <asn@redhat.com> - 0.3.0-1
- Update to version 0.3.0
- resolves: #1450624 - Set default python_host_prog

* Sat May 26 2018 Andreas Schneider <asn@redhat.com> - 0.2.2-3
- Rebuild against unibilium-2.0.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 23 2017 Andreas Schneider <asn@redhat.com> - 0.2.2-1
- resolves: #1510899 - Update to version 0.2.2

* Wed Nov 08 2017 Andreas Schneider <asn@redhat.com> - 0.2.1-1
- resolves: #1510762 - Update to version 0.2.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Than Ngo <than@redhat.com> 0.2.0-3
- fixed bz#1451143, ppc64/le build failure

* Mon May 15 2017 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.2.0-2
- Adjust spec for building on epel7

* Mon May 08 2017 Andreas Schneider <asn@redhat.com> - 0.2.0-1
- resolves: #1447481 - Update to 0.2.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Filip Szymański <fszymanski at, fedoraproject.org> - 0.1.7-6
- Add RPM spec file template

* Thu Dec 08 2016 Filip Szymański <fszymanski at, fedoraproject.org> - 0.1.7-5
- Add recommends for python2-neovim and xsel
- Remove unused CMake options
- Use %%make_build and %%make_install macros
- Remove unnecessary %%defattr directive

* Mon Dec 05 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-4
- Set license file correctly

* Mon Dec 05 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-3
- Update build requires

* Mon Dec 05 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-2
- Add Recommends for python3-neovim
- Use 'bit32' from lua 5.3

* Mon Nov 28 2016 Andreas Schneider <asn@redhat.com> - 0.1.7-1
- Update to version 0.1.7

* Tue Nov 15 2016 Andreas Schneider <asn@redhat.com> - 0.1.6-2
- Removed Group:
- Removed BuildRoot:

* Thu Nov 10 2016 Andreas Schneider <asn@redhat.com> - 0.1.6-1
- Initial version 0.1.6
