# from tree import Node
from anytree import Node, RenderTree
# [symbol, x, y, w, h, centroid, confidences[i]*100])
small_height = ['-']
relations = ['+', '-', '\\times', '=', '\\to', '/']  # non-scripted
Open_Bracket = ['(', '{', '[']
Close_Bracket = [')', '}', ']']
Root = ['\\sqrt', '\\log']
Frac = ['\\frac']
Variable_Range = ['\\sum', '\\int']
Ascender = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'C', 'F', 'G', 'H', 'L', 'b', 'd', 'f', 'h', 'k', 't', '\\delta', '\\theta', '\\ln']
Descender = ['g', 'p', 'q', 'y', '\\gamma', '\\beta']
tri = ['\\cot', '\\csc', '\\cos', '\\sec', '\\sin', '\\tan', '\\arcsin',
       '\\arccos', '\\arctan', '\\arccot', '\\arccsc', '\\arcsec']
region_label = ['expression', 'above']
limit_lable = ['lim_']
bias = 0
c = 0.5


def symbol_class(snode):  # 給予類別類型
    if snode[0] in small_height:
        return 'small height'
    elif snode[0] in Frac:
        return 'Frac'
    elif snode[0] in relations:
        return 'relations'
    elif snode[0] in Open_Bracket:
        return 'Open_Bracket'
    elif snode[0] in Root:
        return 'Root'
    elif snode[0] in Variable_Range:
        return 'Variable_Range'
    elif snode[0] in Ascender:
        return 'Ascender'
    elif snode[0] in Descender:
        return 'Descender'
    elif snode[0] in tri:
        return 'tri'
    elif snode[0] in Close_Bracket:
        return 'Close_Bracket'
    elif snode[0] in limit_lable:
        return 'limit'
    else:
        return 'centered'


def position_correction(detection_Objects, file_name):

    print(end='\n')
    s_list = x_min_sort(detection_Objects)
    root = exp_Tree(s_list)
    print(RenderTree(root))
    print('\n')
    sorted_list = []
    traversal(root, sorted_list)
    # print(sorted_list)
    for i in sorted_list:
        print(i, end=' ')
    with open(file_name+'.txt', 'w') as file:
        for d_object in sorted_list:
            file.write(d_object)


def x_min_sort(detection_Objects):
    for i in range(len(detection_Objects) - 1):
        for j in range(len(detection_Objects) - i - 1):
            if(detection_Objects[j][1] > detection_Objects[j+1][1]):
                detection_Objects[j], detection_Objects[j +
                                                        1] = detection_Objects[j+1], detection_Objects[j]
    return detection_Objects


def centroidY(snode):
    basic_center = snode[2]+(snode[4] * 0.5)
    adjustment = 0
    symbol = symbol_class(snode)
    if(symbol == 'small height'):
        adjustment = 30
        # H = (2*snode[2] + snode[4])
        # if s == 'Open_Bracket' or s == 'Root' or s == 'Ascender':
        #     return c*H
        # elif s == 'small height':
        #     return H
        # elif s == 'relations' or s == 'Variable_Range' or s == 'centered' or s == 'Close_Bracket':
        #     return 0.5*H
        # else:
        #     return (1 - c)*H
    return basic_center + adjustment


def exp_Tree(s_list):
    bias = 0
    root = Node('expression', attribute='expression')
    for index, s_node in enumerate(s_list):
        try:
            if index == 0:
                tmp = Node(s_node[0], parent=root, attribute=s_node)
                # 若第一個就是fraction，則亦要建fraction的tree(above and below)
                if s_node[0] == '\\frac':
                    Node('above', parent=tmp)  # [0]
                    Node('below', parent=tmp)  # [1]
            else:
                point = root
                while(point.children):  # 如果有children就繼續執行
                    # print(point.children)
                    point = point.children[-1]  # 去取最新的Node，判斷他是哪一種expression
                    # print(point)
                    segment_block = segment(point.attribute, s_node, bias)
                    # print(segment_block)
                    if point.name == '\\sqrt':
                        # contain means contain in square root.
                        if contain(point.attribute, s_node, bias):
                            print('come in')
                            if not point.children:  # 如果是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                        else:
                            if segment_block == 'hor':
                                Node(
                                    s_node[0], parent=point.parent, attribute=s_node)  # create a sibling node.
                                break
                    # 如果是在水平線上，屬於同一階層(horizone)
                    elif segment_block == 'hor':
                        tmp = Node(
                            s_node[0], parent=point.parent, attribute=s_node)  # create a sibling node.
                        if s_node[0] == '\\frac':  # 遇到fraction後要新建above and below
                            Node('above', parent=tmp)  # [0]
                            Node('below', parent=tmp)  # [1]
                        break
                    elif point.name == '\\frac':  # the last point is fraction.
                        print('fraction point is ', point.attribute[4])
                        if segment(point.attribute, s_node, bias) == 'above':  # 分子
                            point = point.children[0]
                            if not point.children:  # 如果不是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                        else:                                # 分母('below')
                            point = point.children[1]
                            if not point.children:  # 如果不是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                    elif point.name == 'lim_':
                        # print("limit PA:",point.attribute)
                        if segment(point.attribute, s_node, bias) == 'below':
                            if not point.children:  # 如果是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                            # else:
                            #     point = point.children[1]
                            #     if not point.children:# 如果是空的
                            #         Node(s_node[0],parent=point,attribute=s_node)
                            #         break
                    elif segment_block == 'above':  # 次方
                        # point = point.children[0] # superscript
                        if not point.children:
                            super = Node('superscript', parent=point)
                            tmp = Node(
                                s_node[0], parent=super, attribute=s_node)
                            point = point.children[0]  # superscript
                            if s_node[0] == '\\frac':            # 次方上有fraction
                                Node('above', parent=tmp)  # [0]
                                Node('below', parent=tmp)  # [1]
                            break
                        else:
                            point = point.children[0]
        except:
            print("error occur while index = ", index,
                  "which object is ", s_node[0])
    return root


def superscript(treenode, node, bias):
    if(treenode[2] + bias > centroidY(node)):
        return True
    else:
        return False


def Horizon(treenode, node, bias):
    if (treenode[2] <= centroidY(node)) and (centroidY(node) < (treenode[2] + treenode[4])):
        return True
    else:
        return False


# to decide whether the segment is above,hor or below.
def segment(treenode, node, bias):
    if(node[0] == '\\frac'):
        bias = 30
    elif(node[0] == '-'):
        if(treenode[0] != '\\frac'):
            bias = treenode[4] * 0.5
        else:
            bias = 30
    else:
        bias = node[4] * 0.5

    print("segment this time: treenode=", treenode,
          'node = ', node, 'bias = ', bias)
    center_of_left = treenode[2] + (treenode[4] * 0.5)  # 左邊的center
    # center_of_right = node[2]+(node[4] * 0.5)  # 右邊的中心點
    center_of_right = centroidY(node)

    if(center_of_left + bias < center_of_right):
        return 'below'
    elif(center_of_left - bias > center_of_right):
        return 'above'
    else:
        return 'hor'


def contain(treenode, node, bias):  # contain means contain in square root.
    # if (treenode[2] + bias < centroidY(node)) and treenode[1] + treenode[3] > node[1]:
    #     return True
    # else:
    #     return False
    bias = 0
    center_of_left = treenode[2] + (treenode[4] * 0.5)  # 左邊的center
    center_of_right = centroidY(node)
    if(treenode[1] + treenode[3] + bias > node[1]):  # x + w + bias
        return True
    else:
        return False


def traversal(root, sorted_list):

    for child in root.children:
        # print(child.name)
        if(child.name == 'superscript'):
            sorted_list.append('^')
            sorted_list.append('{')
        elif(child.name == 'above'):
            sorted_list.append('{')
        elif(child.name == 'below'):
            sorted_list.append('}')
            sorted_list.append('{')
        elif(child.name == 'lim_'):
            sorted_list.append(child.name+'{')
        elif(child.name == '\\sqrt'):
            sorted_list.append(child.name+'{')
        else:
            sorted_list.append(child.name)

        if len(child.children) != 0:
            traversal(child, sorted_list)

        if(child.name == 'below'):
            sorted_list.append('}')
        elif(child.name == 'superscript'):
            sorted_list.append('}')
        elif(child.name == 'lim_'):
            sorted_list.append('}')
        elif(child.name == '\\sqrt'):
            sorted_list.append('}')
