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

%description
Ashes is a drop-in replacement or ICD to Vulkan.
It allows to write Vulkan code, and to select the rendering API that will be used.
It also comes with ashespp, a C++ wrapper for Vulkan.
To build it, you can use CMake.

Renderers available:
Vulkan: Ashes is a passthrough, when using Vulkan rendering API, and it has no additional cost if dynamic loader is used.
OpenGL: From OpenGL 3.3 to OpenGL 4.6 (Core profile), it can be used directly as an ICD.
Direct3D 11: From feature level 11.0.
    
%prep
%autosetup -n %{oname}-%{git} -p1

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
		-DCMAKE_INSTALL_PREFIX="%{_libdir}"
  
%make_build
  
%install
%make_install -C build

%files
