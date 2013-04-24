# The libraries and binaries produced by this compiler are not compatible
# with coreutils strip (yet).

%global debug_package %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
  /usr/lib/rpm/brp-compress

Name:		go
Version:	1.0.3
Release:	2%{?dist}
Summary:	Go compiler and tools (gc)
Group:		Development/Languages
License:	BSD
URL:		http://golang.org/

# This is built from upstream mercurial:

# hg clone -u release https://go.googlecode.com/hg/go
# tar -cjf go-1.0.3.tar.bz2 go
Source0:	http://go.googlecode.com/files/%{name}%{version}.src.tar.gz
Source1:	golang-crosscompile.tar.gz
# Patch away the need for environment variables:
Patch0:		go-goos.c-no-envvars.diff
Patch1:		cgo.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	ed
BuildRequires:	bison

ExclusiveArch: %ix86 x86_64


%package	vim
Summary:	go syntax files for vim
Group:		Applications/Editors
Requires:	vim-common
Requires:	%{name} = %{version}-%{release}

%description	vim
Go syntax for vim.


%package	emacs
Summary:	go syntax files for emacs
Group:		Applications/Editors
Requires:	emacs-common
Requires:	%{name} = %{version}-%{release}

%description	emacs
Go syntax for emacs.


%description
Go is a systems programming language that aims to be both fast and convenient.


%prep
%setup -q -n "go"
#%patch0
%patch1
%setup -T -D -a 1 -n "go"
%ifarch %ix86
	%global GOARCH 386
%endif
%ifarch	x86_64
	%global GOARCH amd64
%endif
#sed -i -e "s|__GOROOT__|%{_libdir}/go|g" \
#       -e "s|__GOARCH__|%{GOARCH}|g" \
#       src/lib9/goos.c

echo >README.Fedora <<EOM
#This is a go package for Fedora. It notably differs from the standard
#go set of binaries in that it ignores the environmental variables,
#except for GOROOT. It uses GOROOT to allow the newly-built 6g to find
#newly-built packages for other package imports during the build
#process.
EOM


%build
export GOARCH GOROOT GOOS GOBIN

GOROOT="`pwd`"
GOOS=linux
GOBIN="$GOROOT/bin"
GOARCH="%{GOARCH}"

mkdir -p "$GOBIN"
cd src

#sed -i -e 's|^\. \./env\.bash$||' ./make.bash

export MAKE=make
LC_ALL=C PATH="$PATH:$GOBIN" ./make.bash

cd ..
PATH=$PATH:$GOBIN
/bin/bash -c '. golang-crosscompile/crosscompile.bash; go-crosscompile-build windows/386'
/bin/bash -c '. golang-crosscompile/crosscompile.bash; go-crosscompile-build linux/amd64'

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/go/crosscompiler
cp golang-crosscompile/* %{buildroot}%{_datadir}/go/crosscompiler
export GOARCH GOROOT GOOS GOBIN

GOROOT="%{buildroot}%{_libdir}/go"
GOOS=linux
GOBIN="$GOROOT/bin"
GOARCH="%{GOARCH}"

install -Dm644 misc/bash/go %{buildroot}%{_sysconfdir}/bash_completion.d/go
install -Dm644 misc/emacs/go-mode-load.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode-load.el
install -Dm644 misc/emacs/go-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode.el
install -Dm644 misc/vim/indent/go.vim %{buildroot}%{_datadir}/vim/vimfiles/indent/go.vim
install -Dm644 misc/vim/syntax/go.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/go.vim

mkdir -p $GOROOT/{misc,lib}

mkdir -p %{buildroot}%{_bindir}/
cp -a bin/* %{buildroot}%{_bindir}/
cp -r pkg $GOROOT
#rm $GOROOT/pkg/~place-holder~

cp -r lib/godoc $GOROOT/lib
#New go is stupid
#find src/{pkg,cmd} -name \*.go -exec install -Dm644 '{}' "$GOROOT/{}" \;
find src/{pkg,cmd} -exec install -Dm644 '{}' "$GOROOT/{}" \;
#install -Dm644 {,$GOROOT/}src/pkg/container/vector/Makefile
install -Dm644 {,$GOROOT/}favicon.ico
cp -r misc/cgo $GOROOT/misc

#cp src/Make.ccmd src/Make.clib src/Make.cmd src/Make.common src/Make.inc src/Make.pkg $GOROOT/src
cp src/pkg/runtime/{cgocall,runtime}.h $GOROOT/src/pkg/runtime

rm -f %{buildroot}/%{_bindir}/{hgpatch,quietgcc}

find %{buildroot}/%{_libdir}/go/pkg/linux_amd64 -name '*.a' | xargs chmod 0666


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTORS LICENSE README doc/* README.Fedora
%{_libdir}/go
%ifarch %ix86
%{_bindir}/8*
%endif
%{_bindir}/go*
%{_bindir}/windows_386
%{_sysconfdir}/bash_completion.d/go
%{_datadir}/go/crosscompiler


%files vim
%defattr(-,root,root,-)
%{_datadir}/vim/vimfiles/syntax/go.vim
%{_datadir}/vim/vimfiles/indent/go.vim


%files emacs
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/go-mode*.el


%changelog
* Tue Jan 17 2012 Kevin Fox <Kevin.Fox@pnnl.gov> - 0-0.20120117
- Update to newest tip

* Fri May 14 2010 Conrad Meyer <konrad@tylerc.org> - 0-0.20100504
- Fix the patch to allow GOROOT overrides during the build process

* Thu Apr 29 2010 Conrad Meyer <konrad@tylerc.org> - 0-0.20100427
- Initial Go hg release spec template.
