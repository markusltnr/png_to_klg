#!/usr/bin/python
import rospy
from associate import read_file_list, associate
from std_srvs.srv import Trigger, TriggerResponse
from roscpp.srv import SetLoggerLevel
import os
import subprocess


def execute(req):
    print('Received request')
    plane = req.logger 
    folder = '/home/v4r/data/read_rosbag/plane_'+plane
    print(folder)
    first_file = os.path.join(folder, 'planes/depth.txt')
    second_file = os.path.join(folder, 'planes/rgb.txt')
    offset = 0
    max_difference = 0.03
    print(first_file)
    first_list = read_file_list(first_file)
    second_list = read_file_list(second_file)

    matches = associate(first_list, second_list,offset,max_difference)    
    associations = ""
    for a,b in matches:
        associations = associations + ("%f %s %f %s\n"%(a," ".join(first_list[a]),b-offset," ".join(second_list[b])))

    associations_file = open(os.path.join(folder, 'associations.txt'), 'w')
    associations_file.write(associations) 
    cmd_pngtoklg = ['/pngtoklg/png_to_klg/build/pngtoklg', '-w', folder, '-o' ,'plane_'+plane+'.klg','-s', '1000', '-t']
    subprocess.call(cmd_pngtoklg,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('Finished request')
    return None

def png_to_klg_service():
    rospy.init_node('png_to_klg_service')
    s = rospy.Service('png_to_klg', SetLoggerLevel, execute)
    print("PNGtoKLG service is ready.")
    rospy.spin()

if __name__ == "__main__":
    png_to_klg_service()