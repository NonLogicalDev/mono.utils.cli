install:
	cd ./nld.dotter && pip install --upgrade .
	cd ./nld.fsearch && pip install --upgrade .
	cd ./forks/gbf.taskwarrior && make init clean build install
	cd ./forks/gbf.timewarrior && make init clean build install
