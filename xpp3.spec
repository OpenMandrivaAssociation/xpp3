%{?_javapackages_macros:%_javapackages_macros}
%define oversion 1.1.4c

Summary:        XML Pull Parser
Name:           xpp3
Version:        1.1.4c
Release:        2
Epoch:          0
License:        ASL 1.1
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Source0:        http://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{oversion}_src.tgz
Source1:        http://maven.ibiblio.org/maven2/xpp3/xpp3/%{version}/xpp3-%{version}.pom
Source2:        http://maven.ibiblio.org/maven2/xpp3/xpp3_xpath/%{version}/xpp3_xpath-%{version}.pom
Source3:        http://maven.ibiblio.org/maven2/xpp3/xpp3_min/%{version}/xpp3_min-%{version}.pom
Patch0:         %{name}-link-docs-locally.patch
Requires:       java
BuildRequires:  jpackage-utils
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  xml-commons-apis
Requires:       junit
Requires:       xml-commons-apis
Requires:       java

BuildArch:      noarch

%description
XML Pull Parser 3rd Edition (XPP3) MXP1 is an XmlPull
parsing engine that is based on ideas from XPP and in
particular XPP2 but completely revised and rewritten to
take best advantage of latest JIT JVMs such as Hotspot in JDK 1.4.

%package minimal
Summary:        Minimal XML Pull Parser
Requires:       junit
Requires:       xml-commons-apis
Requires:       java

%description minimal
Minimal XML pull parser implementation.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{oversion}
# remove all binary libs
find -name \*.jar -delete

# Remove class bundled from Axis (now it's bundled in JRE)
rm -rf src/java/builder/javax

%patch0

# "src/java/addons_tests" does not exist
sed -i 's|depends="junit_main,junit_addons"|depends="junit_main"|' build.xml
# relax javadoc linting
sed -i '/<javadoc/aadditionalparam="-Xdoclint:none"' build.xml

%build
export CLASSPATH=$(build-classpath xml-commons-apis junit)
ant xpp3 junit apidoc

%install
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

# JARs
install -p -m 644 build/%{name}-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{name}.jar
install -p -m 644 build/%{name}_xpath-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{name}-xpath.jar
install -p -m 644 build/%{name}_min-%{oversion}.jar \
    %{buildroot}%{_javadir}/%{name}-minimal.jar

# POMs
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
install -p -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}-xpath.pom
install -p -m 644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/JPP-%{name}-minimal.pom

# XMvn metadata
%add_maven_depmap
%add_maven_depmap JPP-%{name}-xpath.pom %{name}-xpath.jar
%add_maven_depmap JPP-%{name}-minimal.pom %{name}-minimal.jar -f minimal

# Javadocs
cp -pr doc/api/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc README.html LICENSE.txt doc/*

%files minimal -f .mfiles-minimal
%doc LICENSE.txt

%files javadoc
%doc %{_javadocdir}/%{name}
