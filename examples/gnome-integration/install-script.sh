#!/bin/bash
#	Get script directory path.
scriptdir="`dirname ${0}`"
DESTDIR="${DESTDIR:-}"

install_program()   # arg1=bindir, arg2=datadir, arg3=pkglibdir,
        #	arg4=pkgdatadir, arg5=pkgdocdir.
{
    echo ${DESTDIR}

    # Install binary data - /usr/local/bin/helloworld
    install -m 755 -d "${DESTDIR}${1}"
    install -m 755 "${scriptdir}/helloworld.py" "${DESTDIR}${1}/helloworld"

    # Install package library - /usr/local/lib/helloworld
    install -m 755 -d "${DESTDIR}${3}"
    install "${scriptdir}"/helloworld_*.py "${DESTDIR}${3}/"

    # Install package data /usr/local/share/helloworld
    install -m 755 -d "${DESTDIR}${4}"
    install -m 644 "${scriptdir}/helloworld.png" "${DESTDIR}${4}/"

    # Install data directory - /usr/local/share/pixmaps
    install -m 755 -d "${DESTDIR}${2}/pixmaps"
    install -m 644 "${scriptdir}/helloworld.png" "${DESTDIR}${2}/pixmaps/"

    # /usr/local/share/applications
    install -m 755 -d "${DESTDIR}${2}/applications"
    install -m 644 "${scriptdir}/helloworld.desktop" \
					    "${DESTDIR}${2}/applications/"


    echo "Finished Install"
}

uninstall_program()	# arg1=bindir, arg2=datadir, arg3=pkglibdir,
			#	arg4=pkgdatadir, arg5=pkgdocdir.
{
	rm -f "${DESTDIR}${1}/helloworld"
	rm -f "${DESTDIR}${1}/helloworld.py"
	rm -rf "${DESTDIR}${3}"
	rm -rf "${DESTDIR}${4}"
	rm -rf "${DESTDIR}${5}"
	rm -f "${DESTDIR}${2}/pixmaps/helloworld.png"
	rm -f "${DESTDIR}${2}/applications/helloworld.desktop"
	echo "Finished Uninstall"
}

# First arg to the script
action=$1

if test "$action" = --install
then
    echo "install selected"
    install_program	"/usr/local/bin" \
        "/usr/local/share" \
        "/usr/local/lib/helloworld" \
        "/usr/local/share/helloworld" \
        "/usr/local/share/doc/helloworld"
elif test "$action" = --uninstall
then
    echo "uninstall selected"
    uninstall_program    "/usr/local/bin" \
    "/usr/local/share" \
    "/usr/local/lib/helloworld" \
    "/usr/local/share/helloworld" \
    "/usr/local/share/doc/helloworld"
else
    echo ""
    echo "Usage:"
    echo "    --install - Use this argument to install"
    echo "    --uninstall - Use this argument to uninstall"
    echo ""
fi


