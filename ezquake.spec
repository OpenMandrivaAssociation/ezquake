%undefine _debugsource_packages

Name:           ezquake
Version:        3.6.8
Release:        1
Summary:        A modern QuakeWorld client
License:        GPL-2.0-or-later
Group:          Amusements/Games/3D/Shoot
URL:            https://www.ezquake.com/
Source0:        https://github.com/QW-Group/ezquake-source/releases/download/%{version}/ezquake-source-%{version}.tar.gz
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jansson)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(zlib)

%description
ezQuake is a modern QuakeWorld engine. It adds many useful features like
modern graphics, QuakeTV support, multi-monitor support, a built-in
server browser, and many features serving the nedes of competitive Quake
gamers.

QuakeWorld itelf is a variant of the Quake engine designed specifically
for online gameplay.

Game data must be placed in ~/.ezquake/id1 .

%prep
%autosetup -n %{name}-source-%{version} -p1
sed -i 's|Exec=ezquake.sh|Exec=ezquake|g' dist/linux/io.github.ezQuake.desktop

%build
%cmake
%make_build
strip ezquake-linux-*

%install
install -Dm 0755 build/ezquake-linux-* %{buildroot}%{_libexecdir}/ezquake/ezquake
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/ezquake << EOF
#!/bin/sh
gamedir="\$HOME"/.ezquake
test -d "\$gamedir" || mkdir -p "\$gamedir"
test -L "\$gamedir"/ezquake || ln -s %{_libexecdir}/ezquake/ezquake "\$gamedir"/ezquake

%{_libexecdir}/ezquake/ezquake -basedir "\$gamedir" "\$@"
EOF
chmod 755 %{buildroot}%{_bindir}/ezquake

for res in 128 64 48; do
  mkdir -p "%{buildroot}%{_datadir}/icons/hicolor/$res"x"$res/apps/"
  install dist/linux/io.github.ezQuake."$res".png "%{buildroot}%{_datadir}/icons/hicolor/$res"x"$res/apps/io.github.ezQuake.png"
done
install -Dm 0644 dist/linux/io.github.ezQuake.desktop %{buildroot}%{_datadir}/applications/io.github.ezQuake.desktop
install -Dm 0644 dist/linux/io.github.ezQuake.appdata.xml %{buildroot}%{_datadir}/metainfo/io.github.ezQuake.appdata.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/ezquake
%{_libexecdir}/ezquake
%{_datadir}/applications/io.github.ezQuake.desktop
%{_datadir}/icons/hicolor/*/apps/io.github.ezQuake.png
%{_datadir}/metainfo/io.github.ezQuake.appdata.xml
