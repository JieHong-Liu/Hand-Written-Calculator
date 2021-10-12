# from tree import Node
from anytree import Node, RenderTree
# [symbol, x, y, w, h, centroid, confidences[i]*100])
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
    if snode[0] in Frac:
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
    for d_object in detection_Objects:
        # if(float(d_object[5]) > 0):
        #c.append(Node(d_object[0], parent=c[nums]))
        print(d_object[0], end=' ')

    with open(file_name+'.txt', 'w') as file:
        for d_object in detection_Objects:
            if(float(d_object[5]) > 0):
                file.write(d_object[0])


def x_min_sort(detection_Objects):
    for i in range(len(detection_Objects) - 1):
        for j in range(len(detection_Objects) - i - 1):
            if(detection_Objects[j][1] > detection_Objects[j+1][1]):
                detection_Objects[j], detection_Objects[j +
                                                        1] = detection_Objects[j+1], detection_Objects[j]
    return detection_Objects


def centroidY(snode):
    s = symbol_class(snode)
    H = (2*snode[2] + snode[4])
    if s == 'Open_Bracket' or s == 'Root' or s == 'Ascender':
        return c*H
    elif s == 'relations' or s == 'Variable_Range' or s == 'centered' or s == 'Close_Bracket':
        return 0.5*H
    else:
        return (1 - c)*H


def exp_Tree(s_list):

    root = Node('expression', attribute='expression')
    for index, s_node in enumerate(s_list):
        try:
            if index == 0:
                tmp = Node(s_node[0], parent=root, attribute=s_node)
                if s_node[0] == '\\frac': #若第一個就是fraction，則亦要建fraction的tree(above and below)
                    Node('above', parent=tmp)  # [0]
                    Node('below', parent=tmp)  # [1]
                if(s_node[0] in limit_lable):                   
                    bias = s_node[4]/2.5 # determine the next bias.
                else:
                    bias = s_node[4]/2 # determine the previous bias
                # bias = 0
            else:
                point = root
                while(point.children):  # 如果有children就繼續執行
                    # print(point.children)
                    point = point.children[-1] #去取最新的Node，判斷他是哪一種expression
                    if point.name == '\\sqrt':
                        if contain(point.attribute, s_node,bias): # contain means contain in square root.
                            print('come in1')
                            if not point.children:  # 如果是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                    elif segment(point.attribute, s_node,bias) == 'hor':# 如果是在水平線上，屬於同一階層(horizone)
                        print('come in12')
                        tmp = Node(
                            s_node[0], parent=point.parent, attribute=s_node)#create a sibling node.
                        if s_node[0] == '\\frac': #遇到fraction後要新建above and below
                            Node('above', parent=tmp)  # [0]
                            Node('below', parent=tmp)  # [1]
                        break
                    elif point.name == '\\frac': # the last point is fraction.
                        print('fraction point is ', point.attribute[4])
                        bias = point.attribute[4] * 0.5
                        if segment(point.attribute, s_node,bias) == 'above':  # 分子
                            point = point.children[0]
                            if not point.children:  # 如果是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                        else:                                # 分母
                            point = point.children[1]
                            if not point.children:  # 如果是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                    elif point.name == 'lim_':
                        # print("limit PA:",point.attribute)
                        bias = point.attribute[4] * 0.3
                        if segment(point.attribute, s_node,bias) == 'below':
                            if not point.children:  # 如果是空的
                                Node(s_node[0], parent=point, attribute=s_node)
                                break
                            # else:
                            #     point = point.children[1]
                            #     if not point.children:# 如果是空的
                            #         Node(s_node[0],parent=point,attribute=s_node)
                            #         break
                    elif segment(point.attribute, s_node,bias) == 'above':  # 次方
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
            print("error occur while index = ",index,"which object is ",s_node[0])
    return root


def superscript(treenode, node,bias):
    if(treenode[2] + bias > centroidY(node)):
        return True
    else:
        return False


def Horizon(treenode, node,bias):
    if (treenode[2] <= centroidY(node)) and (centroidY(node) < (treenode[2] + treenode[4])):
        return True
    else:
        return False


def segment(treenode, node,bias): # to decide whether the segment is above,hor or below.
    # print("segment this time: treenode=",treenode,'node = ',node,'bias = ',bias)
    if (treenode[2] - bias > centroidY(node)):
        return 'above'
    elif (treenode[2] + treenode[4] + bias < centroidY(node)):
        return 'below'
    else:
        return 'hor'


def contain(treenode, node,bias): # contain means contain in square root.
    if (treenode[2] + bias < centroidY(node)) and treenode[1] + treenode[3] > node[1]:
        return True
    else:
        return False


# root = Node('expression')
# Node('layer2',parent=root)
# #if not root.children:
# print(root.children[-1].name)
# point = root

# while(point.children):# 如果有children就繼續執行
# #for treenode in reversed(treenodes):
#     point = point.children[-1]
#     print('great')