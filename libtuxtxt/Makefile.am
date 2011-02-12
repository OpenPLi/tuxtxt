lib_LTLIBRARIES = libtuxtxt.la

pkgincludedir = ${includedir}
pkginclude_HEADERS = tuxtxt_def.h tuxtxt_common.h

libtuxtxt_la_SOURCES = libtuxtxt.c

AM_CPPFLAGS = \
	@FREETYPE_CFLAGS@ \
	@ZLIB_CFLAGS@

libtuxtxt_la_LIBADD = \
	@FREETYPE_LIBS@ \
	@ZLIB_LIBS@

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = tuxbox-tuxtxt.pc
