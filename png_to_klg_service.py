#!/usr/bin/python
import rospy
from associate import read_file_list, associate
import os
import subprocess
from png_to_klg.srv import PngToKlg


def execute(req):
    print('Received request')
    plane = req.id 
    folder = '/home/v4r/data/read_rosbag/plane_'+str(plane)
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
    if len(matches)==0:
        return False

    for a,b in matches:
        associations = associations + ("%f %s %f %s\n"%(a," ".join(first_list[a]),b-offset," ".join(second_list[b])))

    associations_file = open(os.path.join(folder, 'associations.txt'), 'w')
    associations_file.write(associations) 
    cmd_pngtoklg = ['/home/v4r/catkin_ws/devel/lib/png_to_klg/pngtoklg', '-w', folder, '-o' ,'plane_'+str(plane)+'.klg','-s', '1000', '-t']
    subprocess.call(cmd_pngtoklg,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('Finished request')
    return True

def png_to_klg_service():
    rospy.init_node('png_to_klg_service')
    s = rospy.Service('png_to_klg', PngToKlg, execute)
    print("PNGtoKLG service is ready.")
    rospy.spin()

if __name__ == "__main__":
    png_to_klg_service()