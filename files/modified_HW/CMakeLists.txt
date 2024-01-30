cmake_minimum_required(VERSION 3.13)

project(hasegawa-wakatani LANGUAGES CXX)

set(SMARTREDIS_INSTALL_PATH /path/to/SmartRedis/install)
find_library(SMARTREDIS_LIBRARY smartredis
             PATHS ${SMARTREDIS_INSTALL_PATH}/lib
             NO_DEFAULT_PATH REQUIRED
)

if (NOT TARGET bout++::bout++)
  find_package(bout++ REQUIRED)
endif()

include_directories(SYSTEM
    ${SMARTREDIS_INSTALL_PATH}/include
)

add_executable(hasegawa-wakatani hw.cxx)
target_link_libraries(hasegawa-wakatani
    bout++::bout++
    ${SMARTREDIS_LIBRARY}
)
