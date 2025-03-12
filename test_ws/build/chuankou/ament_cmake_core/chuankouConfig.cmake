# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_chuankou_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED chuankou_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(chuankou_FOUND FALSE)
  elseif(NOT chuankou_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(chuankou_FOUND FALSE)
  endif()
  return()
endif()
set(_chuankou_CONFIG_INCLUDED TRUE)

# output package information
if(NOT chuankou_FIND_QUIETLY)
  message(STATUS "Found chuankou: 0.0.0 (${chuankou_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'chuankou' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${chuankou_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(chuankou_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${chuankou_DIR}/${_extra}")
endforeach()
