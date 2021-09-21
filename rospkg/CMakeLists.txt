cmake_minimum_required(VERSION 2.6.0)
project(png_to_klg)

find_package(catkin REQUIRED
  genmsg
  message_generation
  message_runtime
  rospy
  std_msgs
)

add_service_files(
  DIRECTORY srv
  FILES
  PngToKlg.srv
)

generate_messages()

set(OpenCV_DIR $ENV{OpenCV_DIR249})
INCLUDE_DIRECTORIES($ENV{OpenCV_DIR249}/include)
set(OpenCV_INCLUDE_DIRS $ENV{OpenCV_DIR249}/include)
set(OpenCV_LIBS $ENV{OpenCV_DIR249}/lib)


find_package(ZLIB REQUIRED)
find_package(OpenCV REQUIRED)
find_package(Boost COMPONENTS date_time REQUIRED)

INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
INCLUDE_DIRECTORIES(${ZLIB_INCLUDE_DIR})

set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_STATIC_RUNTIME OFF)
set(BOOST_ALL_DYN_LINK ON) #force dynamic linking for all libraries

add_executable(pngtoklg
               main.cpp)

target_link_libraries(pngtoklg
                      ${ZLIB_LIBRARY}
                      ${OpenCV_LIBS})
                      
catkin_package(CATKIN_DEPENDS 
    roscpp 
    rospy
    std_msgs
    message_generation
)
include_directories()
