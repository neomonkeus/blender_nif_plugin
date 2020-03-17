#!/bin/bash

function help() {
  echo "Please use \`make_docs <target>\` where <target> is one of"
  echo "    clean      to clean your build directory"
  echo "    html       to make standalone HTML files"
  echo "    htmlclean  to clean your build directory and make standalone HTML files"
  echo "    dirhtml    to make HTML files named index.html in directories"
  echo "    singlehtml to make a single large HTML file"
  echo "    pickle     to make pickle files"
  echo "    json       to make JSON files"
  echo "    htmlhelp   to make HTML files and a HTML help project"
  echo "    qthelp     to make HTML files and a qthelp project"
  echo "    devhelp    to make HTML files and a Devhelp project"
  echo "    epub       to make an epub"
  echo "    latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
  echo "    text       to make text files"
  echo "    man        to make manual pages"
  echo "    texinfo    to make Texinfo files"
  echo "    gettext    to make PO message catalogs"
  echo "    changes    to make an overview over all changed/added/deprecated items"
  echo "    linkcheck  to check all external links for integrity"
  echo "    doctest    to run all doctests embedded in the documentation if enabled"
}

help

## Command file for Sphinx documentation
if [[ "${1}" == "" ]]; then
  help
  exit
fi

if [[ -z "${BLENDER_HOME}" ]]; then
  echo "Please set BLENDER_HOME to the blender executable folder"
  exit
fi

export SPHINX_BUILD="${BLENDER_HOME}/blender --background --factory-startup --python blender-sphinx-build.py -- "
export SPHINX_API_BUILD="${BLENDER_HOME}/blender --background --factory-startup --python blender-sphinx-api-build.py -- "
export BUILD_DIR="_build"

export CODE_API="../io_scene_nif/"
export CODE_DIR="development/api/submodules"
export CODE_OPTS="${CODE_DIR} ${CODE_API}"

export TEST_API="../testframework/"
export TEST_DIR="development/testframework/api/submodules"
export TEST_OPTS="${TEST_DIR} ${TEST_API}"

export ALL_API_OPTS="${TEST_OPTS} ${CODE_DIR}"
export ALL_SPHINX_OPTS=-"d ${BUILD_DIR}/doctrees ${SPHINXOPTS} ."
export I18N_SPHINX_OPTS="${SPHINXOPTS} ."

if [[ -z "${PAPER}" ]]; then
  export ALL_SPHINX_OPTS="-D latex_paper_size=${PAPER} ${ALL_SPHINX_OPTS}"
  export I18N_SPHINX_OPTS="-D latex_paper_size=${PAPER} ${I18N_SPHINX_OPTS}"
fi

if [[ "${1}" == "htmlfull" ]]; then
  . make_docs.sh clean
  . make_docs.sh gencodeapi
  . make_docs.sh gentestapi
  . make_docs.sh html
fi

#if [[ "${1}" == "clean" ]]; then
#    for /d %%i in (${BUILD_DIR}\*) do rmdir /q /s %%i
#    rmdir /q /s ${BUILD_DIR}\*
#    rmdir /q /s "%CODE_DIR%\*"
#    rmdir /q /s "%TEST_DIR%\*"
#    exit
#fi

if [[ "${1}" == "html" ]]; then
  echo "Generating auto-docs for plugin source api"
  echo
  $(${SPHINX_BUILD} -b html ${ALL_SPHINX_OPTS} ${BUILD_DIR}/html) || exit 1
  echo
  echo "Build finished. The HTML pages are in ${BUILD_DIR}/html."
  exit
fi

if [[ "${1}" == "gencodeapi" ]]; then
  echo "Generating auto-docs for plugin source api"
  echo
  $(${PHINX_API_BUILD} -o ${CODE_OPTS}) || exit 1
  echo "Generated auto-docs"
  exit
fi

if [[ "${1}" == "gentestapi" ]]; then
  echo "Generating auto-docs for testframework api"
  echo
  $(${SPHINX_API_BUILD} -o ${TEST_OPTS}) || exit 1
  echo "Generated auto-docs for testframework"
  exit
fi

if [[ "${1}" == "dirhtml" ]]; then
  $(${SPHINX_BUILD} -b dirhtml ${ALL_SPHINX_OPTS} ${BUILD_DIR}/dirhtml) || exit 1
  echo
  echo "Build finished. The HTML pages are in ${BUILD_DIR}/dirhtml."
  exit
fi

if [[ "${1}" == "singlehtml" ]]; then
  $(${SPHINX_BUILD} -b singlehtml ${ALL_SPHINX_OPTS} ${BUILD_DIR}/singlehtml) || exit 1
  echo
  echo "Build finished. The HTML pages are in ${BUILD_DIR}/singlehtml."
  exit
fi

if [[ "${1}" == "pickle" ]]; then
  $(${SPHINX_BUILD} -b pickle ${ALL_SPHINX_OPTS} ${BUILD_DIR}/pickle) || exit 1
  echo
  echo "Build finished; now you can process the pickle files."
  exit
fi

if [[ "${1}" == "json" ]]; then
  $(${SPHINX_BUILD} -b json ${ALL_SPHINX_OPTS} ${BUILD_DIR}/json) || exit 1
  echo
  echo "Build finished; now you can process the JSON files."
  exit
fi

if [[ "${1}" == "htmlhelp" ]]; then
  $(${SPHINX_BUILD} -b htmlhelp ${ALL_SPHINX_OPTS} ${BUILD_DIR}/htmlhelp) || exit 1
  echo
  echo "Build finished; now you can run HTML Help Workshop with the .hhp project file in ${BUILD_DIR}/htmlhelp."
  exit
fi

if [[ "${1}" == "qthelp" ]]; then
  $(${SPHINX_BUILD} -b qthelp ${ALL_SPHINX_OPTS} ${BUILD_DIR}/qthelp) || exit 1
  echo
  echo "Build finished; now you can run \"qcollectiongenerator\" with the .qhcp project file in ${BUILD_DIR}/qthelp, like this:"
  echo "^> qcollectiongenerator ${BUILD_DIR}\qthelp\BlenderNIFScripts.qhcp"
  echo "To view the help file:"
  echo "^> assistant -collectionFile ${BUILD_DIR}\qthelp\BlenderNIFScripts.ghc"
  exit
fi

if [[ "${1}" == "devhelp" ]]; then
  $(${SPHINX_BUILD} -b devhelp ${ALL_SPHINX_OPTS} ${BUILD_DIR}/devhelp) || exit 1
  echo
  echo "Build finished."
  exit
fi

if [[ "${1}" == "epub" ]]; then
  $(${SPHINX_BUILD} -b epub ${ALL_SPHINX_OPTS} ${BUILD_DIR}/epub) || exit 1
  echo
  echo "Build finished. The epub file is in ${BUILD_DIR}/epub."
  exit
fi

if [[ "${1}" == "latex" ]]; then
  $(${SPHINX_BUILD} -b latex ${ALL_SPHINX_OPTS} ${BUILD_DIR}/latex) || exit 1
  echo
  echo "Build finished; the LaTeX files are in ${BUILD_DIR}/latex."
  exit
fi

if [[ "${1}" == "text" ]]; then
  $(${SPHINX_BUILD} -b text ${ALL_SPHINX_OPTS} ${BUILD_DIR}/text) || exit 1
  echo
  echo "Build finished. The text files are in ${BUILD_DIR}/text."
  exit
fi

if [[ "${1}" == "man" ]]; then
  $(${SPHINX_BUILD} -b man ${ALL_SPHINX_OPTS} ${BUILD_DIR}/man) || exit 1
  echo
  echo "Build finished. The manual pages are in ${BUILD_DIR}/man."
  exit
fi

if [[ "${1}" == "texinfo" ]]; then
  $(${SPHINX_BUILD} -b texinfo ${ALL_SPHINX_OPTS} ${BUILD_DIR}/texinfo) || exit 1
  echo
  echo "Build finished. The Texinfo files are in ${BUILD_DIR}/texinfo."
  exit
fi

if [[ "${1}" == "gettext" ]]; then
  $(${SPHINX_BUILD} -b gettext ${I18N_SPHINX_OPTS} ${BUILD_DIR}/locale) || exit 1
  echo
  echo "Build finished. The message catalogs are in ${BUILD_DIR}/locale."
  exit
fi

if [[ "${1}" == "changes" ]]; then
  $(${SPHINX_BUILD} -b changes ${ALL_SPHINX_OPTS} ${BUILD_DIR}/changes) || exit 1
  echo
  echo "The overview file is in ${BUILD_DIR}/changes."
  exit
fi

if [[ "${1}" == "linkcheck" ]]; then
  $(${SPHINX_BUILD} -b linkcheck ${ALL_SPHINX_OPTS} ${BUILD_DIR}/linkcheck) || exit 1
  echo
  echo "Link check complete; look for any errors in the above output or in ${BUILD_DIR}/linkcheck/output.txt.?"
  exit
fi

if [[ "${1}" == "doctest" ]]; then
  $(${SPHINX_BUILD} -b doctest ${ALL_SPHINX_OPTS} ${BUILD_DIR}/doctest) || exit 1
  echo
  echo "Testing of doctests in the sources finished, look at the results in ${BUILD_DIR}/doctest/output.txt."
  exit
fi
