RPMOPTIONS=

all: download

download:
	if [ ! -f go1.0.3.src.tar.gz ]; then \
	  bash download.sh; \
	fi

rpm: rpms

rpms: download
	rpmbuild --define '_sourcedir '`pwd` --define '_rpmdir '`pwd`'/packages/bin' --define '_srcrpmdir '`pwd`'/packages/src' $(RPMOPTIONS) -ba go.spec

MOCKOPTIONS=
MOCKDIST=fedora-18-x86_64
MOCK=/usr/bin/mock

mock: download
	mkdir -p packages/"$(MOCKDIST)"/srpms
	mkdir -p packages/"$(MOCKDIST)"/bin
	$(MOCK) -r "$(MOCKDIST)" $(MOCKOPTIONS) --buildsrpm --spec go.spec --sources "`pwd`"
	mv "/var/lib/mock/$(MOCKDIST)/result/"*.src.rpm packages/"$(MOCKDIST)"/srpms/
	$(MOCK) $(MOCKOPTIONS) -r "$(MOCKDIST)" --result "$(CURDIR)"/packages/"$(MOCKDIST)"/bin "$(CURDIR)"/packages/"$(MOCKDIST)"/srpms/*.src.rpm; \
	res=$$?; \
	if [ $$res -ne 0 ]; then \
		cat "$(CURDIR)"/packages/"$(MOCKDIST)"/bin/build.log; \
		exit $$res; \
	fi
