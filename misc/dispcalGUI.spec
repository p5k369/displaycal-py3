%define numpy_version 1.0
%define py_minversion ${PY_MINVERSION}
%define py_maxversion ${PY_MAXVERSION}
%define wx_minversion ${WX_MINVERSION}
Summary: ${SUMMARY}
Name: ${PACKAGE}
Version: ${VERSION}
Release: 1
License: GPL
Source: http://%{name}.hoech.net/%{name}-%version.tar.gz
URL: http://dispcalgui.hoech.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
%if 0%{?mandriva_version} > 0
Group: Graphics
%ifarch x86_64
BuildRequires: udev, gcc, python >= %{py_minversion}, python <= %{py_maxversion}, libpython-devel, lib64xorg-x11-devel
%else
BuildRequires: udev, gcc, python >= %{py_minversion}, python <= %{py_maxversion}, libpython-devel, libxorg-x11-devel
%endif
Requires: python >= %{py_minversion}, python <= %{py_maxversion}, wxPythonGTK >= %{wx_minversion}, python-numpy >= %{numpy_version}
%else
%if 0%{?suse_version} > 0
Group: Productivity/Graphics/Other
BuildRequires: udev, update-desktop-files, gcc, python >= %{py_minversion}, python <= %{py_maxversion}, python-devel, xorg-x11-devel
Requires: python >= %{py_minversion}, python <= %{py_maxversion}, python-wxGTK >= %{wx_minversion}, python-numpy >= %{numpy_version}
%else
%if 0%{?fedora_version} > 0
Group: Applications/Multimedia
BuildRequires: udev, gcc, python >= %{py_minversion}, python <= %{py_maxversion}, python-devel, libX11-devel, libXinerama-devel, libXrandr-devel, libXxf86vm-devel
Requires: python >= %{py_minversion}, python <= %{py_maxversion}, wxPython >= %{wx_minversion}, numpy >= %{numpy_version}
%endif
%endif
%endif

%description
${DESC}

%prep
%setup
export python_version=`python -c "import sys;print sys.version[:3]"`
# Make files executable
chmod +x "scripts/%{name}"
chmod +x "misc/Argyll"
# Convert line endings in LICENSE.txt
python -c "f = open('LICENSE.txt', 'rb')
d = f.read().replace('\r\n', '\n').replace('\r', '\n')
f.close()
f = open('LICENSE.txt', 'wb')
f.write(d)
f.close()"

%build
python${python_version} setup.py build --use-distutils

%install
%if 0%{?fedora_version} > 0
OPTIMIZE=1
%endif
install_lib=`python -c "from distutils.sysconfig import get_python_lib;print get_python_lib(True)"`
python${python_version} setup.py install --no-compile --use-distutils \
	--prefix=$RPM_BUILD_ROOT%_prefix \
	--exec-prefix=$RPM_BUILD_ROOT%_exec_prefix \
	--install-data=$RPM_BUILD_ROOT%_datadir \
    --install-lib=$RPM_BUILD_ROOT${install_lib} \
	--skip-instrument-configuration-files --record=INSTALLED_FILES
# Byte-compile *.py files and remove traces of RPM_BUILD_ROOT
python -c "import glob
import os
from distutils.sysconfig import get_python_lib
from distutils.util import byte_compile, change_root
py = glob.glob(os.path.join(change_root('$RPM_BUILD_ROOT', get_python_lib(True)), 
			   '%{name}', '*.py'))
byte_compile(py, optimize=0, force=1, prefix='$RPM_BUILD_ROOT')
if 0${OPTIMIZE} > 0:
	byte_compile(py, optimize=1, force=1, prefix='$RPM_BUILD_ROOT')"
# Remove doc directory
if [ -e "${RPM_BUILD_ROOT}%_datadir/doc/%{name}-%{version}" ]; then
	rm -rf "${RPM_BUILD_ROOT}%_datadir/doc/%{name}-%{version}"
fi
# udev/hotplug
mkdir -p "${RPM_BUILD_ROOT}/usr/share/dispcalGUI/usb"
# USB and serial instruments using udev, where udev already creates /dev/bus/usb/00X/00X devices
cp -f "misc/92-Argyll.rules" "${RPM_BUILD_ROOT}/usr/share/dispcalGUI/usb/92-Argyll.rules"
echo "/usr/share/dispcalGUI/usb/92-Argyll.rules">>INSTALLED_FILES
# USB using udev, where there are NOT /dev/bus/usb/00X/00X devices
cp -f  "misc/45-Argyll.rules" "${RPM_BUILD_ROOT}/usr/share/dispcalGUI/usb/45-Argyll.rules"
echo "/usr/share/dispcalGUI/usb/45-Argyll.rules">>INSTALLED_FILES
# USB using hotplug and Serial using udev (older versions of Linux)
cp -f "misc/Argyll" "${RPM_BUILD_ROOT}/usr/share/dispcalGUI/usb/Argyll"
echo "/usr/share/dispcalGUI/usb/Argyll">>INSTALLED_FILES
cp -f "misc/Argyll.usermap" "${RPM_BUILD_ROOT}/usr/share/dispcalGUI/usb/Argyll.usermap"
echo "/usr/share/dispcalGUI/usb/Argyll.usermap">>INSTALLED_FILES
%if 0%{?suse_version} > 0
# Update categories to prevent buildservice from complaining
%suse_update_desktop_file %{name} 2DGraphics
%endif
# Remove unused files from list of installed files and add directories
python -c "import os
f = open('INSTALLED_FILES')
paths = [path.replace('$RPM_BUILD_ROOT', '').strip() for path in 
		 filter(lambda path: not '/doc/' in path, f.readlines())]
f.close()
for path in list(paths):
	if path.endswith('.py'):
		paths.append(path + 'c')
		if 0${OPTIMIZE} > 0:
			paths.append(path + 'o')
	while True:
		path = os.path.dirname(path)
		if os.path.isdir(path):
			break
		else:
			directory = '%dir ' + path
			if not directory in paths:
				paths.append(directory)
f = open('INSTALLED_FILES', 'w')
f.write('\n'.join(paths))
f.close()"

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc LICENSE.txt
%doc README.html
%doc screenshots
%doc theme

%post
${POST}

%postun
${POSTUN}

%changelog
* ${DATE} ${MAINTAINER} <${MAINTAINER_EMAIL}>
- Version ${VERSION}
