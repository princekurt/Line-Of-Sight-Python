__author__ = 'kurt'
# Created by Kurt Anderson, used to read in a list of obstructions and then return the largest area
# To see that obstruction
# Created 4/3/2015

from xml.etree.ElementTree import *
import sys


def los_calc(h_data, p_data,o_list):
    """
    Used to calculate line of sight.
    :param h_data: house data
    :param p_data: property data
    :param o_list: obstacle list
    :return: distance
    """
    prop_y = p_data[2]
    house_y = h_data[2]

    coord_list = []
    for i in range(len(o_list)):
        obs_y = o_list[i][2]
        if float(obs_y) >= float(house_y) or float(obs_y) <= float(prop_y):
            pass
        else:
            coordinates = get_shadow_area(h_data, p_data,o_list[i])
            if coordinates[0] >= coordinates[1]:
                zero = coordinates[0]
                one = coordinates[1]
                coordinates = (one, zero)
            coord_list.append(coordinates)
    new_list = coord_consol(coord_list)


    dist = distance_finder(p_data, new_list)
    return dist

def distance_finder(p_data, coord_list):
    """
    used to find the distance of line of sight
    :param p_data: property coordinates
    :param coord_list: list of coordinates
    :return:
    """
    p_x1 = float(p_data[0])
    p_x2 = float(p_data[1])
    highest_poss = p_x2 - p_x1
    flag = 0
    flag_1 = 0

    top_numb = 0

    if len(coord_list) == 0:
        return highest_poss
    if len(coord_list) == 1:
        if p_x1 < coord_list[0][0] < p_x2 or p_x1 < coord_list[0][1] < p_x2:
            if coord_list[0][0] < p_x1:
                top_numb = p_x2 - coord_list[0][1]
            elif coord_list[0][1] > p_x2:
                top_numb = coord_list[0][0] - p_x1
            else:
                temp_value_1 = p_x2 - coord_list[0][1]
                temp_value_2 = coord_list[0][0] - p_x1
                if temp_value_1 >= temp_value_2:
                    top_numb = temp_value_1
                else:
                    top_numb = temp_value_2
            flag_1 = 1
    elif len(coord_list) == 2:
        temp_first = 0
        temp_second = 0
        temp_mid = 0
        if p_x1 < coord_list[0][0] < p_x2 or p_x1 < coord_list[0][1] < p_x2:
            if p_x1 < coord_list[0][0] < p_x2 and p_x1 < coord_list[0][1] < p_x2:
                t_1 = coord_list[0][0] - p_x1
                if p_x1 < coord_list[1][0] < p_x2:
                    t_2 = coord_list[1][0] - coord_list[0][1]
                else:
                    t_2 = p_x2 - coord_list[0][1]
                if t_1 >= t_2:
                    temp_first = t_1
                else:
                    temp_first = t_2
            elif p_x1 < coord_list[1][0] < p_x2:
                temp_first = coord_list[1][0] - coord_list[0][1]
            elif coord_list[0][0] < p_x1:
                temp_first = p_x2 - coord_list[0][1]
            elif coord_list[0][1] > p_x2:
                temp_first = coord_list[0][0] - p_x1
            else:
                temp_values_1 = p_x2 - coord_list[0][1]
                temp_values_2 = coord_list[0][0] - p_x1
                if temp_values_1 >= temp_values_2:
                    temp_second = temp_values_1
                else:
                    temp_second = temp_values_2
            flag_1 = 1

        if p_x1 < coord_list[1][0] < p_x2 or p_x1 < coord_list[1][1] < p_x2:
            if coord_list[1][1] < p_x2 and coord_list[1][0] > p_x1:
                t_1 = p_x2 - coord_list[1][1]
                if p_x1 < coord_list[0][1] < p_x2:
                    t_2 = coord_list[1][0] - coord_list[0][1]
                else:
                    t_2 = coord_list[1][0] - p_x1
                if t_1 >= t_2:
                    temp_second = t_1
                else:
                    temp_second = t_2
            elif coord_list[1][1] < p_x2:
                temp_second = p_x2 - coord_list[1][1]
            elif coord_list[1][1] > p_x2 and coord_list[0][1] < p_x1:
                temp_second = coord_list[1][0] - p_x1
            flag_1 = 1
        if temp_mid >= temp_first:
            temp_first = temp_mid
        if temp_first >= temp_second:
            top_numb = temp_first
        else:
            top_numb = temp_second
    else:
        for i in range(len(coord_list) - 1):
            x = i + 1
            checker = False
            checker_2 = False
            if x == len(coord_list) - 1:
                checker = True
            if i == 0:
                checker_2 = True
            if p_x1 < coord_list[i][1] < p_x2 or p_x1 < coord_list[x][0] < p_x2 or \
                    (checker == True and p_x1 < coord_list[x][1] < p_x2) or \
                    (checker_2 == True and p_x1 < coord_list[i][0] < p_x2):
                if coord_list[x][0] > p_x2:
                    temp_value = p_x2 - coord_list[i][1]
                elif coord_list[i][1] < p_x1:
                    temp_value = coord_list[x][0] - p_x1
                else:
                    temp_value = coord_list[x][0] - coord_list[i][1]

                if checker == True:
                    temp_value_2 = 0
                    if p_x1 < coord_list[x][1] < p_x2:
                        if coord_list[x][1] > p_x2 and coord_list[x][0] > p_x2 and coord_list[i][1] < p_x1:
                            temp_value_2 = coord_list[x][0] - p_x1
                        elif coord_list[x][1] < p_x2 and coord_list[x][0] < p_x2:
                            temp_value_2 = p_x2 - coord_list[x][1]
                    if temp_value_2 >= temp_value:
                        temp_value = temp_value_2

                if checker_2 == True:
                    temp_value_3 = 0
                    if p_x1 < coord_list[i][0] < p_x2:
                        temp_value_3 = coord_list[i][0] - p_x1
                    if temp_value_3 >= temp_value:
                        temp_value = temp_value_3


                if temp_value > top_numb:
                    top_numb = temp_value
                flag_1 = 1

    for i in range(len(coord_list)):
        if coord_list[i][0] < p_x1 and coord_list[i][1] > p_x2:
            flag = 1
    if flag == 1:
        return 0
    elif flag_1 == 1:
        if top_numb > highest_poss:
            return highest_poss
        else:
            return top_numb
    else:
        return highest_poss



def get_shadow_area(h_data, p_data, o_list):
    """
    Used to get the shadow area of an obstacle
    :param h_data: house data
    :param p_data: property data
    :param o_list: obstacle data
    :return:
    """
    prop_y = p_data[2]

    house_x1 = h_data[0]
    house_x2 = h_data[1]
    house_y = float(h_data[2]) # - float(prop_y)

    obs_x1 = o_list[0]
    obs_x2 = o_list[1]
    obs_y = float(o_list[2]) # - float(prop_y)

    left_x = find_x(float(house_y),float(house_x2),float(obs_y),float(obs_x1),float(prop_y))
    right_x = find_x(float(house_y),float(house_x1),float(obs_y),float(obs_x2),float(prop_y))
    # print("[" + str(left_x) + "," + str(right_x) + "]")
    coordinate_list = (left_x, right_x)
    return coordinate_list


def find_x(house_y,house_x,obs_y,obs_x,prop_y):
    # Find Slope First, The plug that in for y
    """
    Used to find one x position
    :param house_y: y of house
    :param house_x: x of house
    :param obs_y: y of obs
    :param obs_x: x of obstacle
    :param prop_y: y of prop
    :return: value of these put into a tuple
    """
    try:
        # slope = house_y/(house_x - obs_x)
        # y_intercept = obs_y - (slope * obs_x)
        # value =  (0 - y_intercept)/slope
        value = (((prop_y - obs_y) * (house_x - obs_x)) / (house_y - obs_y)) + obs_x
    except ZeroDivisionError:
        value = house_x
    return value

def coord_consol(coordinate_list):
    """
    consolidates the coordinates
    :param coordinate_list: a list of coordinates
    :return:
    """
    coordinate_list.sort(key=lambda tup: tup[0])
    # print(coordinate_list)
    new_list = []
    i = 0
    x = 0

    while i < len(coordinate_list):
        new_bound = coordinate_list[i][1]
        if i == len(coordinate_list) - 1:
            new_list.append(coordinate_list[i])
            i += 1
        else:
            x = i + 1
            while x < len(coordinate_list):
                if new_bound >= coordinate_list[x][0]:
                    if coordinate_list[x][1] > new_bound:
                        new_bound = coordinate_list[x][1]
                    x +=1
                else:
                    break

            new_tuple = (coordinate_list[i][0], new_bound)
            new_list.append(new_tuple)
            i = x



    # print(new_list)
    return new_list


def main():
    """
    Used to implement the program by taking in a specific xml document
    :return: nothin
    """
    tree = ElementTree()
    tree.parse(sys.argv[1])

    root = tree.getroot()
    results_list = []

    output_root = Element('TestResults')
    output_tree = ElementTree(output_root)
	
    for child in root:
        # print(child.tag, child.attrib)
        temp_object_list = []
        house_list = []
        property_list = []
        for object in child:
            if object.tag == "House":
                house_x1 = object.find("From").text
                house_x2 = object.find("To").text
                house_y = object.find("At").text
                house_list = [house_x1, house_x2, house_y]

            elif object.tag == "PropertyLine":
                pLine_x1 = object.find("From").text
                pLine_x2 = object.find("To").text
                pLine_y = object.find("At").text
                property_list = [pLine_x1, pLine_x2, pLine_y]

            else:
                temp_x1 = object.find("From").text
                temp_x2 = object.find("To").text
                temp_y = object.find("At").text
                a = (temp_x1, temp_x2, temp_y)
                temp_object_list.append(a)

        distance = los_calc(house_list,property_list,temp_object_list)


        if distance > 0:
            distance = round(distance, 5)
            distance = round(distance, 2)
            results_list.append("%.2f" % distance)
        else:
            results_list.append("No View")
    i = 0
    for child in root:
        name = Element(child.tag)
        output_root.append(name)
        name.text = str(results_list[i])
        name.attrib = child.attrib
        i += 1

    output_tree.write(sys.argv[2])


if __name__ == '__main__':
    main()