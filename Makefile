default:
	@echo "No default."

install.dotter: 
	cd ./nld.cli.dotter && pip install --upgrade . && python setup.py install

install.fsearch: 
	cd ./nld.cli.fsearch && python setup.py install

install.taskwarrior:
	cd ./gbf.taskwarrior && make init clean build install

install.timewarrior:
	cd ./gbf.timewarrior && make init clean build install
