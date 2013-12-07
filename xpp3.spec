# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define oversion 1.1.3_8

Summary:        XML Pull Parser
Name:           xpp3
Version:        1.1.3.8
Release:        10
License:        ASL 1.1
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Group:          Development/Java
Source0:        http://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{oversion}_src.tgz
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/xpp3/xpp3/1.1.3.4.O/xpp3-1.1.3.4.O.pom
Source2:        http://mirrors.ibiblio.org/pub/mirrors/maven2/xpp3/xpp3_xpath/1.1.3.4.O/xpp3_xpath-1.1.3.4.O.pom
Source3:        http://mirrors.ibiblio.org/pub/mirrors/maven2/xpp3/xpp3_min/1.1.3.4.O/xpp3_min-1.1.3.4.O.pom
Patch0:         %{name}-link-docs-locally.patch
Requires:       jpackage-utils >= 0:1.6
Requires:       java >= 0:1.4.2
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit
BuildRequires:  xml-commons-apis
BuildRequires:  /usr/bin/perl
Requires:       jpackage-utils
Requires:       junit
Requires:       xml-commons-apis
Requires:       java
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

BuildArch:      noarch

%description
Xml Pull Parser 3rd Edition (XPP3) MXP1 is a new XmlPull
parsing engine that is based on ideas from XPP and in
particular XPP2 but completely revised and rewritten to
take best advantage of latest JIT JVMs such as Hotspot in JDK 1.4.

%package minimal
Summary:        Minimal XML Pull Parser
Group:          Development/Java
Requires:       jpackage-utils
Requires:       junit
Requires:       xml-commons-apis
Requires:       java
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

%description minimal
Minimal XML pull parser implementation.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{oversion}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0

%build
export CLASSPATH=$(build-classpath xml-commons-apis junit)
ant xpp3 junit apidoc

%install

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}-%{oversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
cp -p build/%{name}_min-%{oversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-minimal.jar
cp -p build/%{name}_xpath-%{oversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-xpath.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

rm -rf doc/{build.txt,api}

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE3} \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}-minimal.pom
%add_to_maven_depmap %{name} %{name}_min %{version} JPP %{name}-minimal

mv %{buildroot}%{_mavendepmapfragdir}/%{name} %{buildroot}%{_mavendepmapfragdir}/%{name}-minimal
install -pm 644 %{SOURCE1} \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

install -pm 644 %{SOURCE2} \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}-xpath.pom
%add_to_maven_depmap %{name} %{name}_xpath %{version} JPP %{name}-xpath


%post
%update_maven_depmap

%postun
%update_maven_depmap

%post minimal
%update_maven_depmap

%postun minimal
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc README.html LICENSE.txt doc/*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-xpath.jar
%{_mavenpomdir}/JPP-%{name}-xpath.pom
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files minimal
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_mavendepmapfragdir}/%{name}-minimal
%{_mavenpomdir}/JPP-%{name}-minimal.pom
%{_javadir}/%{name}-minimal.jar

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*



%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 1.1.3.8-7
+ Revision: 734312
- rebuild
- imported package xpp3

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.3.8-1.7
+ Revision: 608232
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.3.8-1.6mdv2010.1
+ Revision: 524462
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.1.3.8-1.5mdv2009.1
+ Revision: 350812
- rebuild

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 0:1.1.3.8-1.4mdv2009.0
+ Revision: 136618
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1.3.8-1.4mdv2008.1
+ Revision: 121062
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1.3.8-1.3mdv2008.0
+ Revision: 87313
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

  + Thierry Vignaud <tv@mandriva.org>
    - kill file require on perl-base

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1.3.8-1.2mdv2008.0
+ Revision: 53226
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)

* Tue Jul 03 2007 David Walluck <walluck@mandriva.org> 0:1.1.3.8-1.1mdv2008.0
+ Revision: 47362
- fix gcj support
- gcj support
- BuildRequires: java-devel
- remove Requires: java
- Import xpp3



* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp.1
- Import
- Fix per Fedora spec

* Mon Feb 12 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.8-1jpp
- Upgrade to 1.1.3.8
- Remove vendor and distribution tags

* Mon Feb 27 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.1.3.4-1.o.2jpp
- First JPP 1.7 build

* Tue Dec 20 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.o.1jpp
- Upgrade to 1.1.3.4-O
- Now includes xpath support

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.2jpp
- Build with ant-1.6.2

* Tue Jun 01 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3.4-1.d.1jpp
- Update to 1.1.3.4

* Mon May  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.3jpp
- Fix non-versioned javadoc symlinking.

* Mon Apr 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.2jpp
- Include non-versioned javadoc symlink.

* Tue Apr  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-1.a.1jpp
- First JPackage release.
