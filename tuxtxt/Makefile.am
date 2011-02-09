SUBDIRS = font 

AM_CPPFLAGS = \
	@FREETYPE_CFLAGS@ \
	@TUXTXT_CFLAGS@

bin_PROGRAMS = tuxtxt

tuxtxt_LDADD = -lpthread -lz \
	@FREETYPE_LIBS@ \
	@TUXTXT_LIBS@

tuxtxt_SOURCES = tuxtxt.c

install_DATA = tuxtxt.conf
