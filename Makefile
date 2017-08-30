help:
	@echo "Use 'make bootstrap' to install dependencies to create a .deb package"
	@echo "Use 'make deb' to create the .deb package"
	@echo "Use 'make source' to create only the .deb source package"
	@echo "Use 'make clean' to clean all temporary files"
	@echo "Use 'make install' to install the .deb package created"

bootstrap:
	@sudo apt-get -y install build-essential debhelper tar gzip python-stdeb devscripts
	@sudo pip install stdeb

deb:
	@python setup.py --command-packages=stdeb.command bdist_deb

source:
	@python setup.py --command-packages=stdeb.command sdist_dsc

clean:
	@rm -rf pyfile.egg-info
	@rm -rf dist
	@rm -rf deb_dist
	@rm -f pyfile*.tar.gz
	@rm -rf build
	@find . -type f -name "*.pyc" -delete

install:
	@sudo dpkg -i deb_dist/*.deb

uninstall:
	@sudo apt purge python-pyfile

tox:
	@docker build -t neriberto/pyfile .
	@docker run --rm neriberto/pyfile
