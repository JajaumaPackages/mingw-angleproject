%?mingw_package_header

%global snapshot_stamp 20141113
%global snapshot_rev 30d6c255d238c3064980a22f66fecf0ef9bb58d0
%global snapshot_rev_short %(echo %snapshot_rev | cut -c1-6)

Summary:        Almost Native Graphics Layer Engine
Name:           mingw-angleproject
Version:        0
Release:        0.15.git.%{snapshot_rev_short}.%{snapshot_stamp}%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            http://code.google.com/p/angleproject/

# Upstream hasn't done any official releases yet
# To generate snapshot:
# git clone https://chromium.googlesource.com/angle/angle
# tar --exclude-vcs -cjvpf angle-git-$(cd angle; git rev-parse HEAD | cut -c1-6).tar.bz2 angle
Source0:        angle-git-%{snapshot_rev_short}.tar.bz2

# Additional source files taken from Qt5
# https://qt.gitorious.org/qt/qtbase/raw/2302d386c7a1aa1a96658f79c236d6b8a59db7ac:src/3rdparty/angle/src/libGLESv2/libGLESv2_mingw32.def
Source1:        libGLESv2_mingw32.def

# https://qt.gitorious.org/qt/qtbase/raw/2302d386c7a1aa1a96658f79c236d6b8a59db7ac:src/3rdparty/angle/src/libEGL/libEGL_mingw32.def
Source2:        libEGL_mingw32.def

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw64-gcc-c++

BuildRequires:  gyp

BuildArch:      noarch

# Patches taken from Qt5
# https://qt.gitorious.org/qt/qtbase/source/2302d386c7a1aa1a96658f79c236d6b8a59db7ac:src/angle/patches
Patch0:         0000-General-fixes-for-ANGLE-2.1.patch
Patch1:         0004-Make-it-possible-to-link-ANGLE-statically-for-single.patch
Patch2:         0008-ANGLE-Dynamically-load-D3D-compiler-from-a-list-or-t.patch
Patch3:         0009-ANGLE-Support-WinRT.patch
Patch4:         0010-ANGLE-Enable-D3D11-for-feature-level-9-cards.patch
Patch5:         0012-ANGLE-fix-semantic-index-lookup.patch
Patch6:         0013-ANGLE-Add-support-for-querying-platform-device.patch
Patch7:         0014-Let-ANGLE-use-multithreaded-devices-if-necessary.patch
Patch8:         0015-ANGLE-Fix-angle-d3d11-on-MSVC2010.patch
Patch9:         0016-ANGLE-Fix-compilation-with-MinGW-D3D11.patch
Patch10:        0017-ANGLE-Fix-compilation-with-D3D9.patch
Patch11:        0018-ANGLE-Fix-releasing-textures-after-we-kill-D3D11.patch

# Undo a change from 0016-ANGLE-Fix-compilation-with-MinGW-D3D11.patch which
# implements some missing stuff from the mingw.org toolchain, but which already
# exists in the mingw-w64 toolchain (and causes breakage)
Patch100:       angleproject-undo-mingw-org-compatibility.patch

# Same as above but introduced by a change from 0015-ANGLE-Fix-angle-d3d11-on-MSVC2010.patch
Patch101:       angleproject-undo-mingw-org-compatibility2.patch

# Disable some debug code as it depends on the ID3DUserDefinedAnnotation
# interface which isn't available in mingw-w64 yet
# Patch for this is currently pending at http://source.winehq.org/patches/data/108405
Patch102:       angleproject-disable-debug-annotations.patch

# Undo a change from 0000-General-fixes-for-ANGLE-2.1.patch which renames
# some shader references, but which doesn't rename the precompiled shaders
Patch103:       angleproject-undo-shader-renames.patch

# Prevent multiple definition errors during the final link of libGLESv2
Patch104:       angleproject-prevent-multiple-definition-errors.patch

# Revert commit 4de44cb and commit 409078f as qt5-qtwebkit still depends on it
Patch105:       commit-4de44cb
Patch106:       commit-409078f

# Make sure an import library is created and the correct .def file is used during the build
Patch107:       angleproject-include-import-library-and-use-def-file.patch

# WebKit depends on symbols which are used in the static library called translator_hlsl
# This static library is linked into the libGLESv2 shared library
# To allow building WebKit export the required symbols in the libGLESv2 shared library
Patch108:       angleproject-export-shader-symbols.patch

# Use GCC constructors instead of DllMain to avoid conflicts when using the static library
Patch109:       angleproject-use-constructors-instead-of-DllMain.patch

# Fix compilation against GCC 6
Patch110:       angle-gcc6-fix.patch


%description
ANGLE is a conformant implementation of the OpenGL ES 2.0 specification that
is hardware‐accelerated via Direct3D. ANGLE v1.0.772 was certified compliant
by passing the ES 2.0.3 conformance tests in October 2011. ANGLE also provides
an implementation of the EGL 1.4 specification.

ANGLE is used as the default WebGL backend for both Google Chrome and
Mozilla Firefox on Windows platforms. Chrome uses ANGLE for all graphics
rendering on Windows, including the accelerated Canvas2D implementation
and the Native Client sandbox environment.

Portions of the ANGLE shader compiler are used as a shader validator and
translator by WebGL implementations across multiple platforms. It is used
on Mac OS X, Linux, and in mobile variants of the browsers. Having one shader
validator helps to ensure that a consistent set of GLSL ES shaders are
accepted across browsers and platforms. The shader translator can be used
to translate shaders to other shading languages, and to optionally apply
shader modifications to work around bugs or quirks in the native graphics
drivers. The translator targets Desktop GLSL, Direct3D HLSL, and even ESSL
for native GLES2 platforms.


%?mingw_debug_package


# Win32
%package -n mingw32-angleproject
Summary:        Almost Native Graphics Layer Engine for Win32
Group:          Development/Libraries

%description -n mingw32-angleproject
ANGLE is a conformant implementation of the OpenGL ES 2.0 specification that
is hardware‐accelerated via Direct3D. ANGLE v1.0.772 was certified compliant
by passing the ES 2.0.3 conformance tests in October 2011. ANGLE also provides
an implementation of the EGL 1.4 specification.

ANGLE is used as the default WebGL backend for both Google Chrome and
Mozilla Firefox on Windows platforms. Chrome uses ANGLE for all graphics
rendering on Windows, including the accelerated Canvas2D implementation
and the Native Client sandbox environment.

Portions of the ANGLE shader compiler are used as a shader validator and
translator by WebGL implementations across multiple platforms. It is used
on Mac OS X, Linux, and in mobile variants of the browsers. Having one shader
validator helps to ensure that a consistent set of GLSL ES shaders are
accepted across browsers and platforms. The shader translator can be used
to translate shaders to other shading languages, and to optionally apply
shader modifications to work around bugs or quirks in the native graphics
drivers. The translator targets Desktop GLSL, Direct3D HLSL, and even ESSL
for native GLES2 platforms.

%package -n mingw32-angleproject-static
Summary:       Static version of the mingw32-angleproject library
Requires:      mingw32-angleproject = %{version}-%{release}
BuildArch:     noarch

%description -n mingw32-angleproject-static
Static version of the mingw32-angleproject library.

# Win64
%package -n mingw64-angleproject
Summary:        Almost Native Graphics Layer Engine for Win64
Group:          Development/Libraries

%description -n mingw64-angleproject
ANGLE is a conformant implementation of the OpenGL ES 2.0 specification that
is hardware‐accelerated via Direct3D. ANGLE v1.0.772 was certified compliant
by passing the ES 2.0.3 conformance tests in October 2011. ANGLE also provides
an implementation of the EGL 1.4 specification.

ANGLE is used as the default WebGL backend for both Google Chrome and
Mozilla Firefox on Windows platforms. Chrome uses ANGLE for all graphics
rendering on Windows, including the accelerated Canvas2D implementation
and the Native Client sandbox environment.

Portions of the ANGLE shader compiler are used as a shader validator and
translator by WebGL implementations across multiple platforms. It is used
on Mac OS X, Linux, and in mobile variants of the browsers. Having one shader
validator helps to ensure that a consistent set of GLSL ES shaders are
accepted across browsers and platforms. The shader translator can be used
to translate shaders to other shading languages, and to optionally apply
shader modifications to work around bugs or quirks in the native graphics
drivers. The translator targets Desktop GLSL, Direct3D HLSL, and even ESSL
for native GLES2 platforms.

%package -n mingw64-angleproject-static
Summary:       Static version of the mingw32-angleproject library
Requires:      mingw64-angleproject = %{version}-%{release}
BuildArch:     noarch

%description -n mingw64-angleproject-static
Static version of the mingw64-angleproject library.


%prep
%setup -q -n angle

# Install additional .def files
cp %{SOURCE1} src/libGLESv2/
cp %{SOURCE2} src/libEGL/

%patch0 -p4
%patch1 -p4
%patch2 -p4
%patch3 -p4
%patch4 -p4
%patch5 -p4
%patch6 -p4
%patch7 -p4
%patch8 -p4
%patch9 -p4
%patch10 -p4
%patch11 -p4

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1 -R
%patch106 -p1 -R
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1

# Executing .bat scripts on Linux is a no-go so make this a no-op
echo "" > src/copy_compiler_dll.bat
chmod +x src/copy_compiler_dll.bat


%build
# This project uses the gyp build system and various
# hacks are required to get this project built.
# Therefore the regular Fedora MinGW RPM macros
# can't be used for this package

# The gyp build system always uses the environment variable RPM_OPT_FLAGS when it's set
# For MinGW we don't want this, so unset this environment variable
unset RPM_OPT_FLAGS

for target in win32 win64 ; do
    mkdir build_$target
    pushd build_$target
        if [ "$target" = "win32" ] ; then
            export CXX=%{mingw32_cxx}
            export AR=%{mingw32_ar}
        else
            export CXX=%{mingw64_cxx}
            export AR=%{mingw64_ar}
        fi

        gyp -D OS=win -D TARGET=$target -D MSVS_VERSION="" --depth . -I ../build/common.gypi ../src/angle.gyp

        # Make sure the correct libraries are linked in
        sed -i s@'^LIBS :='@'LIBS := -ld3d9 -ldxguid'@ ../src/libGLESv2.target.mk
        sed -i s@'^LIBS :='@'LIBS := -ld3d9 -ldxguid -L. -lGLESv2'@ ../src/libEGL.target.mk

        make %{?_smp_mflags} V=1 CXXFLAGS="-std=c++11 -msse2 -DUNICODE -D_UNICODE -g"

        # Also build static libraries (which are needed by the static Qt build)
        ${AR} rcs libGLESv2.a \
            out/Debug/obj.target/src/common/*.o \
            out/Debug/obj.target/src/common/win32/*.o \
            out/Debug/obj.target/src/compiler/translator/*.o \
            out/Debug/obj.target/src/compiler/translator/depgraph/*.o \
            out/Debug/obj.target/src/compiler/translator/timing/*.o \
            out/Debug/obj.target/src/compiler/preprocessor/*.o \
            out/Debug/obj.target/src/third_party/compiler/*.o \
            out/Debug/obj.target/src/third_party/murmurhash/*.o \
            out/Debug/obj.target/src/third_party/systeminfo/*.o \
            out/Debug/obj.target/src/libGLESv2/*.o \
            out/Debug/obj.target/src/libGLESv2/renderer/*.o \
            out/Debug/obj.target/src/libGLESv2/renderer/d3d/*.o \
            out/Debug/obj.target/src/libGLESv2/renderer/d3d/d3d9/*.o \
            out/Debug/obj.target/src/libGLESv2/renderer/d3d/d3d11/*.o

        ${AR} rcs libEGL.a \
            out/Debug/obj.target/libEGL/../src/common/RefCountObject.o \
            out/Debug/obj.target/libEGL/../src/common/angleutils.o \
            out/Debug/obj.target/libEGL/../src/common/debug.o \
            out/Debug/obj.target/libEGL/../src/common/event_tracer.o \
            out/Debug/obj.target/libEGL/../src/common/mathutil.o \
            out/Debug/obj.target/libEGL/../src/common/tls.o \
            out/Debug/obj.target/libEGL/../src/common/utilities.o \
            out/Debug/obj.target/libEGL/../src/libEGL/AttributeMap.o \
            out/Debug/obj.target/libEGL/../src/libEGL/Config.o \
            out/Debug/obj.target/libEGL/../src/libEGL/Display.o \
            out/Debug/obj.target/libEGL/../src/libEGL/Error.o \
            out/Debug/obj.target/libEGL/../src/libEGL/Surface.o \
            out/Debug/obj.target/libEGL/../src/libEGL/libEGL.o \
            out/Debug/obj.target/libEGL/../src/libEGL/main.o \
            out/Debug/obj.target/libEGL/../src/common/win32/NativeWindow.o
    popd
done


%install
# The gyp build system doesn't know how to install files
# and gives libraries invalid filenames.. *sigh*
mkdir -p $RPM_BUILD_ROOT%{mingw32_bindir} $RPM_BUILD_ROOT%{mingw32_libdir} $RPM_BUILD_ROOT%{mingw32_includedir}
mkdir -p $RPM_BUILD_ROOT%{mingw64_bindir} $RPM_BUILD_ROOT%{mingw64_libdir} $RPM_BUILD_ROOT%{mingw64_includedir}

install build_win32/out/Debug/src/libGLESv2.so $RPM_BUILD_ROOT%{mingw32_bindir}/libGLESv2.dll
install build_win64/out/Debug/src/libGLESv2.so $RPM_BUILD_ROOT%{mingw64_bindir}/libGLESv2.dll

install build_win32/out/Debug/src/libEGL.so $RPM_BUILD_ROOT%{mingw32_bindir}/libEGL.dll
install build_win64/out/Debug/src/libEGL.so $RPM_BUILD_ROOT%{mingw64_bindir}/libEGL.dll

install -m0644 build_win32/libGLESv2.dll.a build_win32/libGLESv2.a $RPM_BUILD_ROOT%{mingw32_libdir}
install -m0644 build_win64/libGLESv2.dll.a build_win64/libGLESv2.a $RPM_BUILD_ROOT%{mingw64_libdir}

install -m0644 build_win32/libEGL.dll.a build_win32/libEGL.a $RPM_BUILD_ROOT%{mingw32_libdir}
install -m0644 build_win64/libEGL.dll.a build_win64/libEGL.a $RPM_BUILD_ROOT%{mingw64_libdir}

cp -Rv include/* $RPM_BUILD_ROOT%{mingw32_includedir}
cp -Rv include/* $RPM_BUILD_ROOT%{mingw64_includedir}


%files -n mingw32-angleproject
%doc LICENSE
%{mingw32_bindir}/libEGL.dll
%{mingw32_bindir}/libGLESv2.dll
%{mingw32_includedir}/EGL
%{mingw32_includedir}/GLES2
%{mingw32_includedir}/GLES3
%{mingw32_includedir}/GLSLANG
%{mingw32_includedir}/KHR
%{mingw32_includedir}/angle_gl.h
%{mingw32_includedir}/angle_windowsstore.h
%{mingw32_libdir}/libEGL.dll.a
%{mingw32_libdir}/libGLESv2.dll.a

%files -n mingw32-angleproject-static
%{mingw32_libdir}/libEGL.a
%{mingw32_libdir}/libGLESv2.a

%files -n mingw64-angleproject
%doc LICENSE
%{mingw64_bindir}/libEGL.dll
%{mingw64_bindir}/libGLESv2.dll
%{mingw64_includedir}/EGL
%{mingw64_includedir}/GLES2
%{mingw64_includedir}/GLES3
%{mingw64_includedir}/GLSLANG
%{mingw64_includedir}/KHR
%{mingw64_includedir}/angle_gl.h
%{mingw64_includedir}/angle_windowsstore.h
%{mingw64_libdir}/libEGL.dll.a
%{mingw64_libdir}/libGLESv2.dll.a

%files -n mingw64-angleproject-static
%{mingw64_libdir}/libEGL.a
%{mingw64_libdir}/libGLESv2.a


%changelog
* Sat May 07 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.15.git.30d6c2.20141113
- Fix FTBFS against GCC 6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14.git.30d6c2.20141113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.13.git.30d6c2.20141113
- Use GCC constructors instead of DllMain to avoid conflicts in the static library (RHBZ #1257630)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.12.git.30d6c2.20141113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.11.git.30d6c2.20141113
- Update to 20141113 snapshot (git revision 30d6c2)
- Include all patches which were used by the Qt5 fork
- Reverted some recent commits as they break mingw-qt5-qtwebkit 5.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.10.svn2215.20130517
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb  4 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.9.svn2215.20130517
- Automatically LoadLibrary("d3dcompiler_43.dll") when no other D3D compiler is
  already loaded yet. Fixes RHBZ #1057983
- Make sure the libraries are built with debugging symbols
- Rebuild against latest mingw-w64 (fixes Windows XP compatibility, RHBZ #1054481)

* Fri Jan 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.8.svn2215.20130517
- Rebuilt against latest mingw-w64 to fix Windows XP compatibility (RHBZ #1054481)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.7.svn2215.20130517
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 18 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.6.svn2215.20130517
- Export various symbols from the hlsl translator static library in the
  libGLESv2.dll shared library as they are needed by mingw-qt5-qtwebkit.
  The symbols in question are marked as NONAME (hidden)

* Fri May 17 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.5.svn2215.20130517
- Update to 20130517 snapshot (r2215)

* Thu Apr  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.4.svn1561.20121214
- Added another workaround due to the fact that the gyp
  build system doesn't properly support cross-compilation
  Fixes FTBFS against latest gyp

* Fri Jan 25 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.3.svn1561.20121214
- Added license
- Resolved various rpmlint warnings
- Prefix the release tag with '0.'

* Mon Dec 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.2.svn1561.20121214
- Added -static subpackages

* Fri Dec 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.1.svn1561.20121214
- Initial release

