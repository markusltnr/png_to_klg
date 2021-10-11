#!/usr/bin/python
import rospy
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from associate import read_file_list, associate
import os
import subprocess
from png_to_klg.srv import PngToKlg

def read_file_list(filename):
    """
    Reads a trajectory from a text file. 
    
    File format:
    The file format is "stamp d1 d2 d3 ...", where stamp denotes the time stamp (to be matched)
    and "d1 d2 d3.." is arbitary data (e.g., a 3D position and 3D orientation) associated to this timestamp. 
    
    Input:
    filename -- File name
    
    Output:
    dict -- dictionary of (stamp,data) tuples
    
    """
    file = open(filename)
    data = file.read()
    lines = data.replace(","," ").replace("\t"," ").split("\n") 
    list = [[v.strip() for v in line.split(" ") if v.strip()!=""] for line in lines if len(line)>0 and line[0]!="#"]
    list = [(float(l[0]),l[1:]) for l in list if len(l)>1]
    file.close()
    rospy.sleep(0.5)
    return dict(list)

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
    cmd_pngtoklg = ['/home/v4r/catkin_ws/src/png_to_klg/build/pngtoklg', '-w', folder, '-o' ,'plane_'+str(plane)+'.klg', '-s', '1000', '-t']
    
    process = subprocess.Popen(cmd_pngtoklg,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print('Finished request')
    return True

def png_to_klg_service():
    rospy.init_node('png_to_klg_service')
    s = rospy.Service('png_to_klg', PngToKlg, execute)
    print("PNGtoKLG service is ready.")
    rospy.spin()

if __name__ == "__main__":
    png_to_klg_service()