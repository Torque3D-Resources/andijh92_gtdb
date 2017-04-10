AC_INIT([gtdb],  m4_esyscmd([build-aux/git-version-gen .tarball-version]))

AM_INIT_AUTOMAKE([foreign])

AM_PATH_PYTHON([2.7])

AX_PYTHON_MODULE([wx], [fatal])

AC_CONFIG_FILES([Makefile])
AC_CONFIG_FILES([env], [chmod +x env])
AC_CONFIG_FILES([gtdb/Config.py])

AC_OUTPUT
