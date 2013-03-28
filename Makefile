RPMOPTIONS=

all:
	echo nothing to build

rpm: rpms

rpms:
	rpmbuild --define '_sourcedir '`pwd` --define '_rpmdir '`pwd`'/packages/bin' --define '_srcrpmdir '`pwd`'/packages/src' $(RPMOPTIONS) -ba go.spec

MOCKOPTIONS=
MOCKDIST=fedora-18-x86_64
MOCK=/usr/bin/mock

mock:
	mkdir -p packages/"$(MOCKDIST)"/srpms
	mkdir -p packages/"$(MOCKDIST)"/bin
	$(MOCK) -r "$(MOCKDIST)" $(MOCKOPTIONS) --buildsrpm --spec go.spec --sources "`pwd`"
	mv "/var/lib/mock/$(MOCKDIST)/result/"*.src.rpm packages/"$(MOCKDIST)"/srpms/
	$(MOCK) $(MOCKOPTIONS) -r "$(MOCKDIST)" --result "$(CURDIR)"/packages/"$(MOCKDIST)"/bin "$(CURDIR)"/packages/"$(MOCKDIST)"/srpms/*.src.rpm