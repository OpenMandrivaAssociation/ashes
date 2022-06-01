%define _disable_ld_no_undefined 1
%define oname Ashes
%define git 20220407

Name: ashes
Summary: Drop-in replacement for Vulkan shared library, for older hardware compatibility
Version:	0.%{git}
Release:	1
Group: System/X11
License: MIT
URL: https://dragonjoker.github.io/Ashes/
Source0: https://github.com/DragonJoker/Ashes/archive/refs/heads/Ashes-%{git}.tar.xz
  
BuildRequires:  cmake
BuildRequires:	ninja
BuildRequires:  vulkan-headers
BuildRequires:  pkgconfig(vulkan)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:	pkgconfig(dri)
BuildRequires:	pkgconfig(gl)

BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xxf86vm)

%define libname %mklibname ashes
%define devname %mklibname -d ashes
%define devnamepp %mklibname -d ashespp

%description
Ashes is a drop-in replacement or ICD to Vulkan.
It allows to write Vulkan code, and to select the rendering API that will be used.
It also comes with ashespp, a C++ wrapper for Vulkan.
To build it, you can use CMake.

Renderers available:
Vulkan: Ashes is a passthrough, when using Vulkan rendering API, and it has no additional cost if dynamic loader is used.
OpenGL: From OpenGL 3.3 to OpenGL 4.6 (Core profile), it can be used directly as an ICD.
Direct3D 11: From feature level 11.0.

%package -n %{libname}
Summary: The Ashes Vulkan-on-OpenGL renderer
Group: System/X11

%description -n %{libname}
The Ashes Vulkan-on-OpenGL renderer

%package -n %{devname}
Summary: Development files for the Ashes Vulkan-on-OpenGL library
Group: Development/C and C++
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files for the Ashes Vulkan-on-OpenGL library

%package -n %{devnamepp}
Summary: Development files for the Ashes Vulkan-on-OpenGL library C++ bindings
Group: Development/C and C++
Requires: %{devname} = %{EVRD}

%description -n %{devnamepp}
Development files for the Ashes Vulkan-on-OpenGL library C++ bindings
    
%prep
%autosetup -n %{oname}-%{git} -p1

# Work around insane cmake hardcodes...
%if "%{_lib}" != "lib"
find . -name "*.cmake" -o -name CMakeLists.txt |xargs sed -i -e 's,DESTINATION lib,DESTINATION %{_lib},g'
%endif

%build
%cmake  \
	-DASHES_BUILD_SAMPLES=OFF \
        -DASHES_BUILD_TEMPLATES=OFF \
        -DASHES_BUILD_SW_SAMPLES=OFF \
        -DASHES_BUILD_TESTS=OFF \
        -DPROJECTS_GENERATE_DOC=OFF \
        -DPROJECTS_PROFILING=OFF \
        -DPROJECTS_USE_PRECOMPILED_HEADERS=OFF \
        -DCMAKE_BUILD_TYPE=Release \
	-G Ninja
  
%ninja_build
  
%install
%ninja_install -C build

# Move the ICD file to where the ICD loader will actually see it
# and adjust it to not being in the same directory as the library...
ARCH=%{_target_cpu}
[ "$ARCH" = "znver1" ] && ARCH=x86_64
mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d
sed -i -e 's,\./lib,%{_libdir}/lib,g' %{buildroot}%{_libdir}/ashesGlRenderer_icd.json >%{buildroot}%{_datadir}/vulkan/icd.d/ashesGlRenderer_icd.$ARCH.json
rm %{buildroot}%{_libdir}/ashesGlRenderer_icd.json

%files -n %{devname}
%{_includedir}/ashes
%{_libdir}/cmake/ashes
%{_libdir}/libashesCommon.a
%{_libdir}/libashes.so
%{_libdir}/libashesGlRenderer.so
%{_libdir}/libashesVkRenderer.so

%files -n %{devnamepp}
%{_includedir}/ashespp
%{_libdir}/libashespp.a

%files -n %{libname}
%{_libdir}/libashes.so.*
%{_libdir}/libashesGlRenderer.so.*
%{_libdir}/libashesVkRenderer.so.*
%{_datadir}/vulkan/icd.d/*.json
