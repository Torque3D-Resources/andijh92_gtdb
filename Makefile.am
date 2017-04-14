dist_bin_SCRIPTS = gtdb/gtdb

gtdb_PYTHON = \
	gtdb/Connect.py \
	gtdb/Editor.py \
	gtdb/Notebook.py \
	gtdb/Splash.py \
	gtdb/Tree.py \
	gtdb/Console.py \
	gtdb/Menu.py \
	gtdb/Parameters.py \
	gtdb/ToolBar.py \
	gtdb/Util.py \
	gtdb/App.py \
	gtdb/Config.py \
	gtdb/__init__.py

dist_lexer_DATA = \
	data/lexer/key1.txt \
	data/lexer/key2.txt \
	data/lexer/key3.txt \
	data/lexer/key4.txt \
	data/lexer/key5.txt \
	data/lexer/style.txt

dist_icon_DATA = \
	data/icons/debuggerSplash.png \
	data/icons/Dump.png \
	data/icons/Pause.png \
	data/icons/Play.png \
	data/icons/RunToCursor.png \
	data/icons/Save.png \
	data/icons/StepIn.png \
	data/icons/StepOut.png \
	data/icons/StepOver.png \
	data/icons/Stop.png

dist_poENUS_DATA = \
	data/en_US/LC_MESSAGES/torqueDebug.mo \
	data/en_US/LC_MESSAGES/torqueDebug.po

gtdbdir = $(pythondir)/gtdb
lexerdir = $(datadir)/gtdb/lexer
icondir = $(datadir)/gtdb/icons
poENUSdir = $(datadir)/gtdb/en_US/LC_MESSAGES

do_subst = sed -e 's,[@]datadir[@],$(datadir)/gtdb,g' \
					 		 -e 's,[@]VERSION[@],$(VERSION),g'

install-data-local:
	$(do_subst) < $(srcdir)/gtdb/Config.py.in > $(srcdir)/gtdb/Config.py
