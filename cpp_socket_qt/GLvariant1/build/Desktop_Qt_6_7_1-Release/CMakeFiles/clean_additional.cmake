# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Release")
  file(REMOVE_RECURSE
  "CMakeFiles/appsocket_qml_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/appsocket_qml_autogen.dir/ParseCache.txt"
  "appsocket_qml_autogen"
  )
endif()
