cmake_minimum_required(VERSION 3.13)

project(monitor-newapi LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

if (NOT TARGET bout++::bout++)
  find_package(bout++ REQUIRED)
endif()

include_directories(SYSTEM
    /work/x01/x01/auser/smartsim/smartredis/install/include
)
add_executable(monitor-newapi monitor.cxx)
add_executable(monitor-smartsim monitor-smartsim.cxx)
target_link_libraries(monitor-newapi
    bout++::bout++ 
)
target_link_libraries(monitor-smartsim
    bout++::bout++ 
    ${sr_lib}
)
