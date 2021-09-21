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

catkin_package(CATKIN_DEPENDS 
    roscpp 
    rospy
    std_msgs
    message_generation
)
include_directories()
