#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "bondcpp::bondcpp" for configuration ""
set_property(TARGET bondcpp::bondcpp APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(bondcpp::bondcpp PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libbondcpp.so"
  IMPORTED_SONAME_NOCONFIG "libbondcpp.so"
  )

list(APPEND _cmake_import_check_targets bondcpp::bondcpp )
list(APPEND _cmake_import_check_files_for_bondcpp::bondcpp "${_IMPORT_PREFIX}/lib/libbondcpp.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
