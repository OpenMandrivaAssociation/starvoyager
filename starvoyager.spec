%define name starvoyager
%define version 0.4.4

Summary:	A space combat and exploration game
Name:		%{name}
Version:	%{version}
Release:	%mkrel 8
Source0:	%{name}-%{version}.tar.bz2
%{!?_without_newgfx:Source1: sv_newgfx.tar.bz2}
%{!?_with_startrek:Source2: starvoyager-notrek.tar.bz2}
Source10:	%{name}16.png.bz2
Source11:	%{name}32.png.bz2
Source12:	%{name}48.png.bz2
License:	BSD
Group:		Games/Strategy
URL:		http://starvoyager.bluesky.me.uk/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	SDL-devel SDL_net-devel

%description
Star Voyager is a space combat and exploration game set in 
%{?_with_startrek:the Star Trek universe. It uses SDL for portability.}%{!?_with_startrek:a Trek-like universe. It uses SDL for portability.}

%{!?_without_newgfx:This package also includes the "new graphics" patch.}

%prep
%setup -q -n %{name}
%{!?_without_newgfx:%setup -q -T -D -a 1 -n %{name}/data}
%{!?_with_startrek:%setup -q -T -D -b 2 -n %{name}}
%setup -q -T -D -n %{name}

# Fix typo (the file is referred to everywhere by the proper name)
cp -f LICENCE LICENSE

%build
%make BINDIR=%{_gamesbindir} DATADIR=%{_gamesdatadir}/%{name}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT/%{_prefix}  BINDIR=$RPM_BUILD_ROOT/%{_gamesbindir} DATADIR=$RPM_BUILD_ROOT/%{_gamesdatadir}/%{name}

# Mandrake menu stuff. Icons were created as follows:
#   for size in 16 32 48; do 
#     convert $RPM_BUILD_ROOT/%{_datadir}/%{name}/gfx/43.bmp \
#       -resize ${size}x${size}\! -transparent black \
#       starvoyager$size.png; 
#     bzip2 starvoyager$size.png; 
#   done

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Star Voyager
Comment=Space Exploration Game
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame;
EOF

mkdir -p $RPM_BUILD_ROOT/{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
bzcat %{SOURCE10} > $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
bzcat %{SOURCE11} > $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
bzcat %{SOURCE12} > $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

# Remove the incorrect docdir the installer creates
rm -rf $RPM_BUILD_ROOT/usr/share/doc/%{name}

# Avoid potential problems with Paramount
%{!?_with_startrek:sed -i $RPM_BUILD_ROOT/%{_gamesdatadir}/%{name}/{alliances.svd,equip.svd,ships.svd} -e"s/Starfleet/Human/" -e"s/Klingon/Lobsterman/" -e"s/Borg/Cyborg/" -e"s/Dominion/Shapechanger/" -e"s/Romulan/Pointears/" -e"s/Jem'Hadar/Junky/" -e"s/phaser/laser/" -e"s/Polaron Phaser/Polarized laser/" -e"s/Bird of Prey/Falcon/" -e"s/V'orcha/Beast/" -e"s/Defiant/Speedy/" -e"s/Collective/Cyborg/" -e"s/isruptor/isintegrator/" -e"s/Photon torpedo/Energy-torpedo/" -e"s/isrupter/isintegrator/"}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc FAQ LGPL LICENSE README CHANGES TODO manual.html
%{!?_with_startrek:%doc README.names}
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}/
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
