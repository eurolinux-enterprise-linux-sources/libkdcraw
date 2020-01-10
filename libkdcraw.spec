Name: libkdcraw
Summary: A C++ interface around LibRaw library
Version: 4.10.5
Release: 7%{?dist}
# libkdcraw is GPLv2+,
# LibRaw(bundled) is LGPLv2
# demosaic-pack GPLv2+ GPLv3+ (addons to libraw)
License: GPLv2+ and LGPLv2 and GPLv3+
URL:  https://projects.kde.org/projects/kde/kdegraphics/libs/libkdcraw
Source0: https://download.kde.org/Attic/4.10.5/src/%{name}-%{version}.tar.xz

# drop bundled libraw and use the system LibRaw
Patch1: libkdcraw-4.10.5-use-system-libraw.patch

# port to build against LibRAW-0.19
patch2: libkdcraw-4.10.5-api-change-in-LibRAW-0.19.patch

# fix libjpeg detection for libjpeg-turbo, hopefully upstreamable
# (the hack to add jpeg_mem_src from RawSpeed to LibRaw might not be though)
Patch50: libkdcraw-4.10.0-libjpeg-turbo.patch

# upstream patches
Patch100: libkdcraw-4.10.5-CVE-2013-2126.patch

BuildRequires: kdelibs4-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(jasper)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: LibRaw-devel

Requires: kdelibs4%{?_isa} >= %{_kde4_version}

# when split occurred
Conflicts: kdegraphics-libs < 7:4.6.95-10

%description
Libkdcraw is a C++ interface around LibRaw library used to decode RAW
picture files. More information about LibRaw can be found at
http://www.libraw.org.

%package devel
Summary:  Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel 

%description devel
%{summary}.


%prep
%setup -q
%patch1 -p1 -b .using-system-libraw
%patch2 -p1 -b .api-change-in-LibRAW-0.19
%patch50 -p1 -b .libjpeg-turbo

# upstream patches
%patch100 -p1 -b .CVE-2013-2126

# drop bundled libraw and use the system LibRaw
rm -rf libraw

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} -DENABLE_LCMS2=ON -DENABLE_RAWSPEED=ON ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
pkg-config --modversion libkdcraw
make -C %{_target_platform}/test


%post
/sbin/ldconfig
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :


%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi


%files
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_kde4_libdir}/libkdcraw.so.22*
%{_kde4_appsdir}/libkdcraw/
%{_kde4_iconsdir}/hicolor/*/*/*

%files devel
%{_kde4_libdir}/libkdcraw.so
%{_kde4_libdir}/pkgconfig/libkdcraw.pc
%{_kde4_includedir}/libkdcraw/


%changelog
* Wed Feb 13 2019 Than Ngo <than@redhat.com> - 4.10.5-7
- Related: #1670708 - rebuilt against rebased LibRaw 0.19.2

* Wed Jan 30 2019 Than Ngo <than@redhat.com> - 4.10.5-6
- Resolves: #1670708 - dependencies issue with rebased LibRaw 0.19.2

* Wed Apr 18 2018 Than Ngo <than@redhat.com> - 4.10.5-5
- Resolves: #1557171, #1557189, #1558954
  use the system LibRaw

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4.10.5-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4.10.5-3
- Mass rebuild 2013-12-27

* Mon Jul 15 2013 Than Ngo <than@redhat.com> - 4.10.5-2
- bz#970713, CVE-2013-2126, double-free flaw when handling
  damaged full-color in Foveon and sRAW files

* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 09 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.10.1-1.1
- make libjpeg support work on Fedora 17

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 08 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.0-3
- Requires: libjpeg-turbo >= 1.2.90

* Wed Feb 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.10.0-2
- BR libjpeg-turbo-devel >= 1.2.90, fix libjpeg detection for libjpeg-turbo

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sat Jan 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Wed Dec 19 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90 (4.10 beta2)

* Tue Nov 20 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.80-1
- 4.9.80

* Thu Nov  8 2012 Alexey Kurov <nucleo@fedoraproject.org> - 4.9.60-1
- libkdcraw update from digikam-3.0.0-beta3

* Wed Oct 24 2012 Alexey Kurov <nucleo@fedoraproject.org> - 4.9.50-3
- rebuild for libjpeg8

* Sat Oct 13 2012 Alexey Kurov <nucleo@fedoraproject.org> - 4.9.50-2
- BR: pkgconfig(jasper) pkgconfig(libxml-2.0)

* Sat Oct 13 2012 Alexey Kurov <nucleo@fedoraproject.org> - 4.9.50-1
- libkdcraw update from digikam-3.0.0-beta2
- enable build against lcms2
- enable RawSpeed libraw codec

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Sat May 26 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80
- bump soname version to 21*

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for c++ ABI breakage

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 4.7.97-1
- 4.7.97

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.90-1
- 4.7.90

* Fri Nov 25 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 07 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Mon Jul 11 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-1
- 4.6.95

* Mon Jul 11 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-5
- License: GPLv2+ and LGPLv2 and GPLv3+
- Provides: bundled(LibRaw)

* Sun Jul 10 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-4
- fix URL
- fix scriptlets

* Sun Jul 10 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-3
- License: GPLv2+
- %%doc: +ChangeLog NEWS
- add %%check section

* Wed Jul 06 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-2
- fix Source0 URL
- Conflicts: kdegraphics < 7:4.6.90-10

* Tue Jul 05 2011 Rex Dieter <rdieter@fedoraproject.org>  4.6.90-1
- first try


