SUBDIRS = font data plugin

AM_CPPFLAGS = \
	@FREETYPE_CFLAGS@ \
	@TUXTXT_CFLAGS@

lib_LTLIBRARIES = libtuxtxt32bpp.la

libtuxtxt32bpp_la_LIBADD = -lpthread \
	@FREETYPE_LIBS@ \
	@TUXTXT_LIBS@

libtuxtxt32bpp_la_SOURCES = tuxtxt.c
