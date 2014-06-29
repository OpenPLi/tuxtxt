AC_INIT(tuxtxt,0.0.1)
AM_INIT_AUTOMAKE(tuxtxt,0.0.1)

AC_PROG_CC
AC_PROG_CXX
AC_DISABLE_STATIC
AC_PROG_LIBTOOL
AM_PATH_PYTHON

TUXBOX_APPS
TUXBOX_APPS_DIRECTORY
TUXBOX_APPS_DVB
TUXBOX_BOXTYPE

PKG_CHECK_MODULES(FREETYPE, [freetype2])
PKG_CHECK_MODULES(TUXTXT, tuxbox-tuxtxt)

AC_ARG_WITH(textlcd,
        AC_HELP_STRING([--with-textlcd], [use ascii based lcd, yes or no]),
        [[withtextlcd=$withval]],
        [[withtextlcd=no]]
)
if test x"$withtextlcd" != xno ; then
        AC_DEFINE(HAVE_TEXTLCD, 1,[Define when using an ascii based lcd device])
fi
AM_CONDITIONAL(HAVE_TEXTLCD, test x"$withtextlcd" != xno)

AC_OUTPUT([
Makefile
font/Makefile
data/Makefile
plugin/Makefile
])
