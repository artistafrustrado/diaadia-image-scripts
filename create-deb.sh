#!/bin/bash
#VERSION=$2
#PACK=$1
#PACK=$(echo $PACK | sed -r 's#/##g')

# svn co https://ddreditor.svn.sourceforge.net/svnroot/ddreditor/tools/gimp/ gimp-portal

svn update

PACK="plugins"
STRING=$(svn update)
VERSION=$(echo $STRING | grep 'At revision' | sed -r 's#At revision ([0-9]{1,}).#0.0.\1#g')
echo $VERSION

cp -fr $PACK $PACK-$VERSION
tar -zcvf $PACK-$VERSION.tar.gz $PACK-$VERSION/

cd $PACK-$VERSION
sed -r "s#0.0.1#$VERSION#g" -i debian/changelog
sed -r "s#0.0.1#$VERSION#g" -i debian/files
find . -iname ".svn" -exec rm -fr {} \;


dpkg-buildpackage -rfakeroot

