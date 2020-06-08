import maya.cmds as cmds
import pymel.core as pm


# Welcome!
# This is a quadruped auto rig created by Daniel Akbari

# def BlendInnerFeatherAverage(startDriver, endDriver, blendedTarget, index):
#     # averages the rotation of two objects and connects this value to a third object using a parent constraint
#     # usage: select two blend sources, then target object, and execute script
#     constr1 = cmds.parentConstraint(mo=True,w=1,startDriver,endDriver,blendedTarget)



def CreatePyramidRigCtrl(nameOfCtrl, adjustJnt, startJnt):
    adjustCtrl = cmds.curve(d=1, p=[(0.5, -0.5, 1.940946), (0, 0, 0), (0.5, 0.5, 1.940946), (0.5, -0.5, 1.940946),(-0.5, -0.5, 1.940946), (-0.5, 0.5, 1.940946), (0.5, 0.5, 1.940946), (0, 0, 0),(-0.5, 0.5, 1.940946), (-0.5, -0.5, 1.940946), (0, 0, 0), (0.5, -0.5, 1.940946)],k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], n = nameOfCtrl)
    pyramid2 = cmds.curve(d=1, p=[(0.5, -0.5, 1.940946), (0, 0, 0), (0.5, 0.5, 1.940946), (0.5, -0.5, 1.940946),(-0.5, -0.5, 1.940946), (-0.5, 0.5, 1.940946), (0.5, 0.5, 1.940946), (0, 0, 0),(-0.5, 0.5, 1.940946), (-0.5, -0.5, 1.940946), (0, 0, 0), (0.5, -0.5, 1.940946)],k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

    cmds.setAttr(pyramid2 + '.ry', 180)

    # always freeze transform before combining shapes
    cmds.makeIdentity(adjustCtrl, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.makeIdentity(pyramid2, apply=True, t=1, r=1, s=1, n=0, pn=1)

    # select the shape 2
    shapeSelected2 = cmds.listRelatives(pyramid2, s=True)
    shapeTransform2 = cmds.listRelatives(shapeSelected2, p=True)

    cmds.select(d=True)

    # parent all other shapes to the transform of tranform1
    cmds.parent(shapeSelected2, adjustCtrl, r=True, s=True)

    # delete all parents (transforms) of the shapes that have been merged
    cmds.delete(shapeTransform2)

    # rotate so that centered in z axis
    cmds.setAttr(adjustCtrl + '.rotateX', 90)
    cmds.delete(ch=True)  # delete history
    cmds.makeIdentity(adjustCtrl, apply=True, t=1, r=1, s=1, n=0, pn=1)


    # group and move the ctrl to the corresponding feather adjust jnt
    adjustCtrlGrp = cmds.group(adjustCtrl, n=nameOfCtrl+'_GRP')

    constr = cmds.parentConstraint(adjustJnt, adjustCtrlGrp)
    cmds.delete(constr)

    cmds.parentConstraint(adjustCtrl,adjustJnt,mo=True)
    cmds.parentConstraint(startJnt,adjustCtrlGrp,mo=True)
    return adjustCtrlGrp #returning the ctrl so we can color it after the function is called

def BlendInnerFeather(startDriver, endDriver, blendedFeather, index):
    #endDriver is jnt[3]
    #startDriver is jnt[18]
    # parent constraint inbetween feather to the startDriver and endDriver.
    # print('-------------------------------')
    # print ('OUR INDEX IS = '+str(index))


    if index == 5:
        defVal = 0.2

    if index == 6:
        defVal = 0.4

    if index == 7:
        defVal = 0.5

    if index == 8:
        defVal = 0.6

    if index == 9:
        defVal = 0.65

    if index == 10:
        defVal = 0.7

    if index == 11:
        defVal = 0.75

    if index == 12:
        defVal = 0.8

    if index == 13:
        defVal = 0.85

    if index == 14:
        defVal = .9




    #add a blend ctrl attr on the driven feather
    cmds.select(blendedFeather)
    cmds.addAttr(blendedFeather, longName='source1', at='double', min=0, max=1, k=True)
    cmds.addAttr(blendedFeather, longName='source2', at='double', min=0, max=1, k=True)

    constrRef = cmds.parentConstraint(startDriver, endDriver, blendedFeather, w=1,mo=True, n='wingParentConstraint'+str(index))


    startName = cmds.ls(startDriver)
    startNameW0 = startName[0]+'W0'

    endName = cmds.ls(endDriver)
    endNameW1 = endName[0]+'W1'

    pcName = cmds.ls(constrRef)
    pcName = pcName[0]

    blendFeatherName = cmds.ls(blendedFeather)


    # connectAttr -f l_feather_4_start__JNT.source1 wingParentConstraint1.l_feather_18_start__JNTW0;
    #connected added attributes to corresponding constraint
    cmds.connectAttr(blendedFeather+'.source1', pcName +'.'+startNameW0)
    cmds.connectAttr(blendedFeather+'.source2', pcName +'.'+endNameW1)


    # print("printing expression: ")
    expression = blendFeatherName[0]+".source2 = 1 - " + blendFeatherName[0]+".source1"
    cmds.expression(s=expression, ae=True)


    #lets set our default blend value now that it has been connected to ctrler
    cmds.setAttr(blendedFeather + '.source1', defVal)
    # print('this is our feather blend name:')
    # print (blendFeatherName)
    # print ('this is the defValue given:')
    # print (str(defVal))
    # print('-------------------------------')


def BlendOuterFeather(featherEndStartJnt, featherMidStartJnt, featherJointBlend,nodeNumber,LorR):

    pm.select(featherEndStartJnt)
    pm.shadingNode('blendColors', asShader=True, n=LorR + 'blendColorsNode' + str(nodeNumber))
    name1 = pm.ls(featherEndStartJnt)
    name2 = pm.ls(featherMidStartJnt)
    name3 = pm.ls(featherJointBlend)

    defVal2 = .5
    if nodeNumber == 1:
        defVal2 = 0.8

    if nodeNumber == 2:
        defVal2 = 0.6

    if nodeNumber == 3:
        defVal2 = 0.4

    if nodeNumber == 4:
        defVal2 = 0.3

    if nodeNumber == 5:
        defVal2 = 0.2

    if nodeNumber == 6:
        defVal2 = 0.1



    #lets create an attr 'blender' on our joint and connect it to the 'blender' output of our colorNode
    cmds.select(featherJointBlend)
    cmds.addAttr(featherJointBlend, longName='blend', at='double', dv=defVal2, min=0, max=1, k=True)
    pm.connectAttr(featherJointBlend + '.blend', LorR + 'blendColorsNode' + str(nodeNumber) + '.blender')


    # INPUT
    # connect cube1 to color1
    pm.connectAttr(name1[0]+'.rotateX', LorR + 'blendColorsNode' + str(nodeNumber)+'.color1R')
    pm.connectAttr(name1[0]+'.rotateY', LorR + 'blendColorsNode' + str(nodeNumber)+'.color1G')
    pm.connectAttr(name1[0]+'.rotateZ', LorR + 'blendColorsNode' + str(nodeNumber)+'.color1B')
    # connect cube2 to color2
    pm.connectAttr(name2[0]+'.rotateX', LorR + 'blendColorsNode' + str(nodeNumber)+'.color2R')
    pm.connectAttr(name2[0]+'.rotateY', LorR + 'blendColorsNode' + str(nodeNumber)+'.color2G')
    pm.connectAttr(name2[0]+'.rotateZ', LorR + 'blendColorsNode' + str(nodeNumber)+'.color2B')
    # OUTPUT
    # connect output to drive cube3
    pm.connectAttr(LorR + 'blendColorsNode' + str(nodeNumber)+'.output.outputR', name3[0]+'.rotateX')
    pm.connectAttr(LorR + 'blendColorsNode' + str(nodeNumber)+'.output.outputG', name3[0]+'.rotateY')
    pm.connectAttr(LorR + 'blendColorsNode' + str(nodeNumber)+'.output.outputB', name3[0]+'.rotateZ')

def OrientSelectedJoints(joints):
    pm.select(joints)
    pm.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    pm.select(d=True)

def CreateFeatherSquareRigCtrl(featherStart, featherEnd,ctrlName):
    #THIS FUNCTION CREATES A CUBE CTRL
    square1 = cmds.curve(d=1, p=[(0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5),
                                 (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5),
                                 (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5),
                                 (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                                 (0.5, 0.5, -0.5)],
                         k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], n=ctrlName)



    #lets get the size of our 3 main fk feathers before making the square ctrl for them
    dist = cmds.createNode('distanceDimShape', n='deleteWhenDone')
    featherStart = cmds.xform(featherStart, q=True, ws=True,rp=True)  # (objectToQuery, query, worldSpace,rotationPivotPoint )
    featherEnd = cmds.xform(featherEnd, q=True, ws=True,rp=True)  # (objectToQuery, query, worldSpace,rotationPivotPoint )
    cmds.setAttr(dist + '.endPoint', *(featherEnd))
    cmds.setAttr(dist + '.startPoint', *(featherStart))
    featherLength = cmds.getAttr(dist + '.distance')  # get the total distance traveled by dist  node
    cmds.delete(cmds.listRelatives(dist,p=True))  # we want to grab the parent of the dist node and delete the parent so we don't get an empty group after delete
    # print ("feather length is : "+str(featherLength))

    bbox = cmds.exactWorldBoundingBox(square1)
    bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
    cmds.xform(square1, piv=bottom, ws=True)

    cmds.setAttr(square1 + '.translateY', .5)
    cmds.setAttr(square1 + '.rotateZ', -90)
    cmds.setAttr(square1 + '.scaleX', 4)
    cmds.setAttr(square1 + '.scaleY', featherLength)
    cmds.setAttr(square1 + '.scaleZ', 4)
    cmds.makeIdentity(square1, apply=True, t=1, r=1, s=1, n=0, pn=1)

    return square1

def CreateSphereRigCtrl(ctrlName):
    #THIS FUNCTION CREATES A SPHERE CTRL
    circle1 = cmds.circle(name=ctrlName)

    circle2 = cmds.circle()
    cmds.setAttr(circle2[0] + '.rotateX', 45)

    circle3 = cmds.circle()
    cmds.setAttr(circle3[0] + '.rotateX', 90)

    circle4 = cmds.circle()
    cmds.setAttr(circle4[0] + '.rotateX', 135)

    circle5 = cmds.circle()
    cmds.setAttr(circle5[0] + '.rotateY', 90)

    # always freeze transform before combining shapes
    cmds.makeIdentity(circle1, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.makeIdentity(circle2, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.makeIdentity(circle3, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.makeIdentity(circle4, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.makeIdentity(circle5, apply=True, t=1, r=1, s=1, n=0, pn=1)

    # select the shape of circle2
    shapeSelected2 = cmds.listRelatives(circle2, s=True)
    shapeTransform2 = cmds.listRelatives(shapeSelected2, p=True)

    shapeSelected3 = cmds.listRelatives(circle3, s=True)
    shapeTransform3 = cmds.listRelatives(shapeSelected3, p=True)

    shapeSelected4 = cmds.listRelatives(circle4, s=True)
    shapeTransform4 = cmds.listRelatives(shapeSelected4, p=True)

    shapeSelected5 = cmds.listRelatives(circle5, s=True)
    shapeTransform5 = cmds.listRelatives(shapeSelected5, p=True)

    # parent all other shapes to the transform of circle 1
    cmds.parent(shapeSelected2, shapeSelected3, shapeSelected4,shapeSelected5, circle1[0], r=True, s=True)

    # delete all parents (transforms) of the shapes that have been merged into circle1
    cmds.delete(shapeTransform2)
    cmds.delete(shapeTransform3)
    cmds.delete(shapeTransform4)
    cmds.delete(shapeTransform5)

    #rotate so that centered in z axis
    cmds.setAttr(circle1[0] + '.rotateY', 90)
    cmds.delete(ch=True)#delete history
    cmds.makeIdentity(circle1, apply=True, t=1, r=1, s=1, n=0, pn=1)


    return circle1


def blueColor(s):
    cmds.setAttr(s + '.overrideEnabled', 1);
    cmds.setAttr(s + '.overrideColor', 15);


def yellowColor(s):
    cmds.setAttr(s + '.overrideEnabled', 1);
    cmds.setAttr(s + '.overrideColor', 17);


def redColor(s):
    cmds.setAttr(s + '.overrideEnabled', 1);
    cmds.setAttr(s + '.overrideColor', 13);


def BlendJointsRotation(ikJoints, fkJoints, skinJoints, master):
    #this function moves our skinJoints by blending betweek the ik and fk joints
    count = 0
    for e in skinJoints:
        blender1 = cmds.shadingNode('blendColors', asUtility=True, n='l_IKFK_Switch_rotate_Blend_l')

        cmds.connectAttr(ikJoints[count] + '.rx', blender1 + '.color2R')
        cmds.connectAttr(ikJoints[count] + '.ry', blender1 + '.color2G')
        cmds.connectAttr(ikJoints[count] + '.rz', blender1 + '.color2B')

        cmds.connectAttr(fkJoints[count] + '.rx', blender1 + '.color1R')
        cmds.connectAttr(fkJoints[count] + '.ry', blender1 + '.color1G')
        cmds.connectAttr(fkJoints[count] + '.rz', blender1 + '.color1B')

        cmds.connectAttr(blender1 + '.output.outputR', skinJoints[count] + '.rx')
        cmds.connectAttr(blender1 + '.output.outputG', skinJoints[count] + '.ry')
        cmds.connectAttr(blender1 + '.output.outputB', skinJoints[count] + '.rz')
        # we have now linked both color sets output to our skinJoints[e]

        cmds.connectAttr(master, blender1+'.blender')
        # we have now linked the master to the node's blender attribute

        count+=1


def BlendJointsTranslate(ikJoints,fkJoints,skinJoints,master):
    count =0
    for e in skinJoints:
        #blend has 2 sets of colors each having RGB channel that I can use to blend between fk and ik
        blendr1=cmds.shadingNode('blendColors',asUtility=True,n='L_IKFK_switch_translate_l')
        cmds.connectAttr(ikJoints[count] + '.tx', blendr1 + '.color2R')
        cmds.connectAttr(ikJoints[count] + '.ty', blendr1 + '.color2G')
        cmds.connectAttr(ikJoints[count] + '.tz', blendr1 + '.color2B')
        cmds.connectAttr(fkJoints[count] + '.tx', blendr1 + '.color1R')
        cmds.connectAttr(fkJoints[count] + '.ty', blendr1 + '.color1G')
        cmds.connectAttr(fkJoints[count] + '.tz', blendr1 + '.color1B')

        #blending (driver -> driven)
        #blend both color channels (ik/fk) and passing that to our skinjoints
        cmds.connectAttr(blendr1 + '.output.outputR', skinJoints[count] + '.tx')
        cmds.connectAttr(blendr1 + '.output.outputG', skinJoints[count] + '.ty')
        cmds.connectAttr(blendr1 + '.output.outputB', skinJoints[count] + '.tz')

        #linking master float number to our blender node attribute
        cmds.connectAttr(master, blendr1+'.blender')
        count+=1


def lockTranslate(s):
    cmds.setAttr(s + '.tx', k=False, l=True)  # k=keyable l=locked
    cmds.setAttr(s + '.ty', k=False, l=True)
    cmds.setAttr(s + '.tz', k=False, l=True)


def lockScale(s):
    cmds.setAttr(s + '.sx', k=False, l=True)  # k=keyable l=locked
    cmds.setAttr(s + '.sy', k=False, l=True)
    cmds.setAttr(s + '.sz', k=False, l=True)


def lockRotate(s):
    cmds.setAttr(s + '.rx', k=False, l=True)  # k=keyable l=locked
    cmds.setAttr(s + '.ry', k=False, l=True)
    cmds.setAttr(s + '.rz', k=False, l=True)


def createLeftSideLocators():
    global backToeLoc
    global backBallLoc
    global backAnkleLoc
    global backLowerLoc
    global backUpperLoc
    global backPelvisLoc
    global backLocGrp
    global frontToeLoc
    global frontBallLoc
    global frontAnkleLoc
    global frontLowerLoc
    global frontUpperLoc
    global frontPelvisLoc
    global frontLocGrp

    ''' back leg locator placement '''
    backToeLoc = cmds.spaceLocator(n='l_backToe_LOC')
    cmds.setAttr(backToeLoc[0] + '.translateX', 6.317)
    cmds.setAttr(backToeLoc[0] + '.translateZ', -13.744)

    backBallLoc = cmds.spaceLocator(n='l_backAnkle _LOC')
    cmds.setAttr(backBallLoc[0] + '.translateX', 6.317)
    cmds.setAttr(backBallLoc[0] + '.translateY', 6.303)
    cmds.setAttr(backBallLoc[0] + '.translateZ', -20.488)

    backAnkleLoc = cmds.spaceLocator(n='l_backKnee_LOC')
    cmds.setAttr(backAnkleLoc[0] + '.translateX', 6.317)
    cmds.setAttr(backAnkleLoc[0] + '.translateY', 23.643)
    cmds.setAttr(backAnkleLoc[0] + '.translateZ', -22.658)

    backLowerLoc = cmds.spaceLocator(n='l_backLower_LOC')
    cmds.setAttr(backLowerLoc[0] + '.translateX', 6.317)
    cmds.setAttr(backLowerLoc[0] + '.translateY', 34.916)
    cmds.setAttr(backLowerLoc[0] + '.translateZ', -16.444)

    backUpperLoc = cmds.spaceLocator(n='l_backUpper_LOC')
    cmds.setAttr(backUpperLoc[0] + '.translateX', 6.317)
    cmds.setAttr(backUpperLoc[0] + '.translateY', 47.061)
    cmds.setAttr(backUpperLoc[0] + '.translateZ', -19.792)

    backPelvisLoc = cmds.spaceLocator(n='l_backPelvis_LOC')
    cmds.setAttr(backPelvisLoc[0] + '.translateX', 0)
    cmds.setAttr(backPelvisLoc[0] + '.translateY', 53.116)
    cmds.setAttr(backPelvisLoc[0] + '.translateZ', -21.376)

    backLocGrp = cmds.group(backToeLoc, backBallLoc, backAnkleLoc, backLowerLoc, backUpperLoc, backPelvisLoc, n='backPlacement_GRP')

    ''' front leg locator placement '''

    frontToeLoc = cmds.spaceLocator(n='l_frontToe_LOC')
    cmds.setAttr(frontToeLoc[0] + '.translateX', 6.317)
    cmds.setAttr(frontToeLoc[0] + '.translateZ', 20.155)

    frontBallLoc = cmds.spaceLocator(n='l_frontAnkle_LOC')
    cmds.setAttr(frontBallLoc[0] + '.translateX', 6.317)
    cmds.setAttr(frontBallLoc[0] + '.translateY', 6.058)
    cmds.setAttr(frontBallLoc[0] + '.translateZ', 12.682)

    frontAnkleLoc = cmds.spaceLocator(n='l_frontKnee_LOC')
    cmds.setAttr(frontAnkleLoc[0] + '.translateX', 6.317)
    cmds.setAttr(frontAnkleLoc[0] + '.translateY', 20.3)
    cmds.setAttr(frontAnkleLoc[0] + '.translateZ', 14.6)

    frontLowerLoc = cmds.spaceLocator(n='l_frontUpperKnee_LOC')
    cmds.setAttr(frontLowerLoc[0] + '.translateX', 6.317)
    cmds.setAttr(frontLowerLoc[0] + '.translateY', 34.978)
    cmds.setAttr(frontLowerLoc[0] + '.translateZ', 12)

    frontUpperLoc = cmds.spaceLocator(n='l_frontUpper_LOC')
    cmds.setAttr(frontUpperLoc[0] + '.translateX', 6.317)
    cmds.setAttr(frontUpperLoc[0] + '.translateY', 43.986)
    cmds.setAttr(frontUpperLoc[0] + '.translateZ', 14.482)

    frontPelvisLoc = cmds.spaceLocator(n='l_frontPelvis_LOC')
    cmds.setAttr(frontPelvisLoc[0] + '.translateX', 0)
    cmds.setAttr(frontPelvisLoc[0] + '.translateY', 54.006)
    cmds.setAttr(frontPelvisLoc[0] + '.translateZ', 14.763)


    frontLocGrp = cmds.group(frontToeLoc, frontBallLoc, frontAnkleLoc, frontLowerLoc, frontUpperLoc, frontPelvisLoc, n='frontPlacement_GRP')


def createCenterLocators():
    global neckRootLoc
    global neckEndLoc
    global neckLocGrp
    global tailStartLoc
    global tailEndLoc
    global tailLocGrp
    global headLoc
    '''neck locator placement'''
    neckRootLoc = cmds.spaceLocator(n='neckRoot_LOC')
    cmds.setAttr(neckRootLoc[0] + '.translateX', 0)
    cmds.setAttr(neckRootLoc[0] + '.translateY', 54.15)
    cmds.setAttr(neckRootLoc[0] + '.translateZ', 22.752)

    neckEndLoc = cmds.spaceLocator(n='neckEnd_LOC')
    cmds.setAttr(neckEndLoc[0] + '.translateX', 0)
    cmds.setAttr(neckEndLoc[0] + '.translateY', 68.474)
    cmds.setAttr(neckEndLoc[0] + '.translateZ', 32.578)

    headLoc = cmds.spaceLocator(n='head_LOC')
    cmds.setAttr(headLoc[0] + '.translateX', 0)
    cmds.setAttr(headLoc[0] + '.translateY', 68.474)
    cmds.setAttr(headLoc[0] + '.translateZ', 46.664)


    neckLocGrp = cmds.group(neckRootLoc, neckEndLoc,headLoc, n='neckPlacement_GRP')

    ''' tail locator placement '''
    tailStartLoc = cmds.spaceLocator(n='tailRoot_LOC')
    cmds.setAttr(tailStartLoc[0] + '.translateX', 0)
    cmds.setAttr(tailStartLoc[0] + '.translateY', 51.684)
    cmds.setAttr(tailStartLoc[0] + '.translateZ', -29.856)


    tailEndLoc = cmds.spaceLocator(n='tailEnd_LOC')
    cmds.setAttr(tailEndLoc[0] + '.translateX', 0)
    cmds.setAttr(tailEndLoc[0] + '.translateY', 49.891)
    cmds.setAttr(tailEndLoc[0] + '.translateZ', -42.864)


    tailLocGrp = cmds.group(tailStartLoc, tailEndLoc, n='tailPlacement_GRP')


def createWorldController():
    global subworld
    global worldCtrl
    ''' worldController '''
    worldCtrl = cmds.curve(d=1, p=[(0.382683, 0, 0.92388), (-0.382683, 0, 0.923879), (-0.923879, 0, 0.382683),(-0.923879, 0, -0.382683), (-0.382683, 0, -0.923879), (0.382683, 0, -0.923879),(0.92388, 0, -0.382683), (0.92388, 0, 0.382683), (0.382683, 0, 0.92388)],k=[0, 1, 2, 3, 4, 5, 6, 7, 8], n='c_World_Ctrl')
    subworld = cmds.curve(d=1, p=[(0.382683, 0, 0.92388), (-0.382683, 0, 0.923879), (-0.923879, 0, 0.382683),(-0.923879, 0, -0.382683), (-0.382683, 0, -0.923879), (0.382683, 0, -0.923879),(0.92388, 0, -0.382683), (0.92388, 0, 0.382683), (0.382683, 0, 0.92388)],k=[0, 1, 2, 3, 4, 5, 6, 7, 8], n='s_World_Ctrl')
    cmds.scale(.7, .7, .7, subworld + '.cv[0:8]')

    # create temp curves we will use to draw out our global ctrl pieces
    forward = cmds.curve(d=1, p=[(0.382683, 0, 0.92388), (-0.382683, 0, 0.92388), (0, 0, 1.7), (0.382683, 0, 0.92388)],k=[0, 1, 2, 3], n='forward');
    backward = cmds.curve(d=1, p=[(0.382683, 0, -0.92388), (0, 0, -1.5), (-0.382683, 0, -0.92388), (0.382683, 0, -0.92388)], k=[0, 1, 2, 3], n='backward');
    worldleft = cmds.curve(d=1,p=[(0.92388, 0, -0.382683), (1.5, 0, 0), (0.92388, 0, 0.382683), (0.92388, 0, -0.382683)],k=[0, 1, 2, 3], n='worldleft');
    worldright = cmds.curve(d=1, p=[(-0.92388, 0, -0.382683), (-1.5, 0, 0), (-0.92388, 0, 0.382683),(-0.92388, 0, -0.382683)], k=[0, 1, 2, 3], n='worldright');



    # create new ref curves from the previouse temp curves we drew
    mainshape = cmds.listRelatives(worldCtrl, s=True)
    mainshape = cmds.rename(mainshape, 'worldShape')

    subshape = cmds.listRelatives(worldCtrl, s=True)
    subshape = cmds.rename(subshape, 'subWorldShape')

    forwardshape = cmds.listRelatives(forward, s=True)
    forwardshape = cmds.rename(forwardshape, 'worldForwardShape')

    backwardshape = cmds.listRelatives(backward, s=True)
    backwardshape = cmds.rename(backwardshape, 'worldBackwardShape')

    worldleftshape = cmds.listRelatives(worldleft, s=True)
    worldleftshape = cmds.rename(worldleftshape, 'worldLeftShape')

    worldrightshape = cmds.listRelatives(worldright, s=True)
    worldrightshape = cmds.rename(worldrightshape, 'worldRightShape')

    # set color (our shapes history retains the curve seperations and we can use these stored shapes to color)
    yellowColor(worldCtrl)
    blueColor(worldleftshape)
    redColor(worldrightshape)

    # combine the curve references we created into 1 object and then delete the temp curves
    cmds.parent(forwardshape, worldCtrl, s=True, r=True)
    cmds.parent(worldleftshape, worldCtrl, s=True, r=True)
    cmds.parent(worldrightshape, worldCtrl, s=True, r=True)
    cmds.parent(backwardshape, worldCtrl, s=True, r=True)
    cmds.delete(forward, backward, worldleft, worldright)

    # parent sub curve into our worldCtrl curve
    cmds.parent(subworld, worldCtrl)

    #adjusting scale of parent and child worldCtrl/subworld
    cmds.select(worldCtrl)
    cmds.scale(40,40,40)
    cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)





def createBackLegJoints():
    global backPelvisJnt
    global L_backUpperJnt
    global L_backLowerJnt
    global L_backAnkleJnt
    global L_backBallJnt
    global L_backToeJnt
    global L_backToeEndJnt
    global R_backUpperJnt
    global R_backLowerJnt
    global R_backAnkleJnt
    global R_backBallJnt
    global R_backToeJnt
    global R_backToeEndJnt

    # create back leg joints
    backPelvisJnt = cmds.joint(n='c_backPelvis_JNT')
    constr = cmds.pointConstraint(backPelvisLoc, backPelvisJnt)
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backUpperJnt = cmds.joint(n='l_backUpperLeg_JNT')
    constr = cmds.pointConstraint(backUpperLoc,
                                  L_backUpperJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backAnkleJnt = cmds.joint(n='l_backAnkle_JNT')
    constr = cmds.pointConstraint(backAnkleLoc,
                                  L_backAnkleJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backLowerJnt = cmds.joint(n='l_backLowerLeg_JNT')
    constr = cmds.pointConstraint(backLowerLoc,
                                  L_backLowerJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backBallJnt = cmds.joint(n='l_backBall_JNT')
    constr = cmds.pointConstraint(backBallLoc,
                                  L_backBallJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backToeJnt = cmds.joint(n='l_backToe_JNT')
    constr = cmds.pointConstraint(backToeLoc,
                                  L_backToeJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    # mirror L back joints to other side....

    R_backUpperJnt = cmds.duplicate(L_backUpperJnt, n='r_backUpperLeg_JNT')
    R_backUpperJnt = R_backUpperJnt[0] #pass list element to variable so we don't have to use [0] to refer to duplicate

    xPos = cmds.getAttr(L_backUpperJnt + '.tx')
    cmds.setAttr(R_backUpperJnt + '.tx', -xPos)

    R_backAnkleJnt = cmds.duplicate(L_backAnkleJnt, n='r_backAnkle_JNT')
    R_backAnkleJnt = R_backAnkleJnt[0] #pass list element to variable so we don't have to use [0] to refer to duplicate
    xPos = cmds.getAttr(L_backAnkleJnt + '.tx')
    cmds.setAttr(R_backAnkleJnt + '.tx', -xPos)

    R_backLowerJnt = cmds.duplicate(L_backLowerJnt, n='r_backLowerKnee_JNT')
    R_backLowerJnt = R_backLowerJnt[0] # convert list element to variable
    xPos = cmds.getAttr(L_backLowerJnt + '.tx')
    cmds.setAttr(R_backLowerJnt + '.tx', -xPos)

    R_backBallJnt = cmds.duplicate(L_backBallJnt, n='r_backBall_JNT')
    R_backBallJnt = R_backBallJnt[0]
    xPos = cmds.getAttr(L_backBallJnt + '.tx')
    cmds.setAttr(R_backBallJnt + '.tx', -xPos)

    R_backToeJnt = cmds.duplicate(L_backToeJnt, n='r_backToe_JNT')
    R_backToeJnt =  R_backToeJnt[0]
    xPos = cmds.getAttr(L_backToeJnt + '.tx')
    cmds.setAttr(R_backToeJnt + '.tx', -xPos)

    # end back joints for mayaSkinning
    L_backToeEndJnt = cmds.joint(n='l_backToeEnd_Jnt')
    constr = cmds.pointConstraint(L_backToeJnt, L_backToeEndJnt)
    cmds.delete(constr)
    cmds.parent(L_backToeEndJnt, L_backToeJnt)
    cmds.setAttr(L_backToeEndJnt + '.tz',.04)  # we don't want the end of the toe to overlap another joint due to skinning issues with overlapping joints mirroring
    cmds.setAttr(L_backToeEndJnt + '.visibility', 0)
    cmds.select(d=True)

    R_backToeEndJnt = cmds.joint(n='r_backToeEnd_Jnt')
    constr = cmds.pointConstraint(R_backToeJnt, R_backToeEndJnt)
    cmds.delete(constr)
    cmds.parent(R_backToeEndJnt, R_backToeJnt)
    cmds.setAttr(R_backToeEndJnt + '.tz',.04)  # we don't want the end of the toe to overlap another joint due to skinning issues with overlapping joints mirroring
    cmds.setAttr(R_backToeEndJnt + '.visibility', 0)
    cmds.select(d=True)

    # parent back leg joints...
    cmds.parent(L_backToeJnt, L_backBallJnt)
    cmds.parent(L_backBallJnt, L_backAnkleJnt)
    cmds.parent(L_backAnkleJnt, L_backLowerJnt)
    cmds.parent(L_backLowerJnt, L_backUpperJnt)
    cmds.parent(L_backUpperJnt, backPelvisJnt)

    cmds.parent(R_backToeJnt, R_backBallJnt)
    cmds.parent(R_backBallJnt, R_backAnkleJnt)
    cmds.parent(R_backAnkleJnt, R_backLowerJnt)
    cmds.parent(R_backLowerJnt, R_backUpperJnt)
    cmds.parent(R_backUpperJnt, backPelvisJnt)

    # orient joints
    cmds.select(L_backUpperJnt)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(R_backUpperJnt)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(d=True)


def createBackLegIKJoints():
    global L_backUpperJntIK
    global L_backLowerJntIK
    global L_backAnkleIkJnt
    global L_backBallJntIK
    global L_backToeJntIK
    global R_backUpperJntIK
    global R_backLowerJntIK
    global R_backAnkleJntIK
    global R_backBallJntIK
    global R_backToeJntIK

    '''L IK back Legs'''

    # create L back IK joints....
    L_backUpperJntIK = cmds.joint(n='l_backUpperLegIK_JNT')
    constr = cmds.pointConstraint(backUpperLoc, L_backUpperJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backLowerJntIK = cmds.joint(n='l_backLowerLegIK_JNT')
    constr = cmds.pointConstraint(backLowerLoc, L_backLowerJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backAnkleIkJnt = cmds.joint(n='l_backAnkleIK_JNT')
    constr = cmds.pointConstraint(backAnkleLoc, L_backAnkleIkJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backBallJntIK = cmds.joint(n='l_backBallIK_JNT')
    constr = cmds.pointConstraint(backBallLoc, L_backBallJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backToeJntIK = cmds.joint(n='l_backToeIK_JNT')
    constr = cmds.pointConstraint(backToeLoc, L_backToeJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    # mirror L back IK joints to other side....

    R_backUpperJntIK = cmds.duplicate(L_backUpperJntIK, n='r_backUpperLegIK_JNT')
    R_backUpperJntIK = R_backUpperJntIK[0]
    xPos = cmds.getAttr(L_backUpperJntIK + '.tx')
    cmds.setAttr(R_backUpperJntIK + '.tx', -xPos)

    R_backAnkleJntIK = cmds.duplicate(L_backAnkleIkJnt, n='r_backAnkleIK_JNT')
    R_backAnkleJntIK = R_backAnkleJntIK[0]
    xPos = cmds.getAttr(L_backAnkleIkJnt + '.tx')
    cmds.setAttr(R_backAnkleJntIK + '.tx', -xPos)

    R_backLowerJntIK = cmds.duplicate(L_backLowerJntIK, n='r_backLowerKneeIK_JNT')
    R_backLowerJntIK = R_backLowerJntIK[0]
    xPos = cmds.getAttr(L_backLowerJntIK + '.tx')
    cmds.setAttr(R_backLowerJntIK + '.tx', -xPos)

    R_backBallJntIK = cmds.duplicate(L_backBallJntIK, n='r_backBallIK_JNT')
    R_backBallJntIK = R_backBallJntIK[0]
    xPos = cmds.getAttr(L_backBallJntIK + '.tx')
    cmds.setAttr(R_backBallJntIK + '.tx', -xPos)

    R_backToeJntIK = cmds.duplicate(L_backToeJntIK, n='r_backToeIK_JNT')
    R_backToeJntIK = R_backToeJntIK[0]
    xPos = cmds.getAttr(L_backToeJntIK + '.tx')
    cmds.setAttr(R_backToeJntIK + '.tx', -xPos)

    # parent back IK leg joints...
    cmds.parent(L_backToeJntIK, L_backBallJntIK)
    cmds.parent(L_backBallJntIK, L_backAnkleIkJnt)
    cmds.parent(L_backAnkleIkJnt, L_backLowerJntIK)
    cmds.parent(L_backLowerJntIK, L_backUpperJntIK)
    cmds.parent(L_backUpperJntIK, backPelvisJnt)

    cmds.parent(R_backToeJntIK, R_backBallJntIK)
    cmds.parent(R_backBallJntIK, R_backAnkleJntIK)
    cmds.parent(R_backAnkleJntIK, R_backLowerJntIK)
    cmds.parent(R_backLowerJntIK, R_backUpperJntIK)
    cmds.parent(R_backUpperJntIK, backPelvisJnt)

    # orient back IK joints
    cmds.select(L_backUpperJntIK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(R_backUpperJntIK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(d=True)


def createBackLegFKJoints():
    global L_backUpperJntFK
    global L_backLowerJntFK
    global L_backAnkleJntFK
    global L_backBallJntFK
    global L_backToeJntFK
    global R_backUpperJntFK
    global R_backLowerJntFK
    global R_backAnkleJntFK
    global R_backBallJntFK
    global R_backToeJntFK

    # create FK back joints on left side....
    L_backUpperJntFK = cmds.joint(n='l_backUpperLegFK_JNT')
    constr = cmds.pointConstraint(backUpperLoc,
                                  L_backUpperJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backLowerJntFK = cmds.joint(n='l_backLowerLegFK_JNT')
    constr = cmds.pointConstraint(backLowerLoc,
                                  L_backLowerJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backAnkleJntFK = cmds.joint(n='l_backAnkleFK_JNT')
    constr = cmds.pointConstraint(backAnkleLoc,
                                  L_backAnkleJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backBallJntFK = cmds.joint(n='l_backBallFK_JNT')
    constr = cmds.pointConstraint(backBallLoc,
                                  L_backBallJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_backToeJntFK = cmds.joint(n='l_backToeFK_JNT')
    constr = cmds.pointConstraint(backToeLoc,
                                  L_backToeJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    # mirror L back FK joints to other side....

    R_backUpperJntFK = cmds.duplicate(L_backUpperJntFK, n='r_backUpperLegFK_JNT')
    R_backUpperJntFK = R_backUpperJntFK[0]
    xPos = cmds.getAttr(L_backUpperJntFK + '.tx')
    cmds.setAttr(R_backUpperJntFK + '.tx', -xPos)

    R_backAnkleJntFK = cmds.duplicate(L_backAnkleJntFK, n='r_backAnkleFK_JNT')
    R_backAnkleJntFK = R_backAnkleJntFK[0]
    xPos = cmds.getAttr(L_backAnkleJntFK + '.tx')
    cmds.setAttr(R_backAnkleJntFK + '.tx', -xPos)

    R_backLowerJntFK = cmds.duplicate(L_backLowerJntFK, n='r_backLowerKneeFK_JNT')
    R_backLowerJntFK = R_backLowerJntFK[0]
    xPos = cmds.getAttr(L_backLowerJntFK + '.tx')
    cmds.setAttr(R_backLowerJntFK + '.tx', -xPos)

    R_backBallJntFK = cmds.duplicate(L_backBallJntFK, n='r_backBallFK_JNT')
    R_backBallJntFK = R_backBallJntFK[0]
    xPos = cmds.getAttr(L_backBallJntFK + '.tx')
    cmds.setAttr(R_backBallJntFK + '.tx', -xPos)

    R_backToeJntFK = cmds.duplicate(L_backToeJntFK, n='r_backToeFK_JNT')
    R_backToeJntFK = R_backToeJntFK[0]
    xPos = cmds.getAttr(L_backToeJntFK + '.tx')
    cmds.setAttr(R_backToeJntFK + '.tx', -xPos)

    # parent back FK leg joints...
    cmds.parent(L_backToeJntFK, L_backBallJntFK)
    cmds.parent(L_backBallJntFK, L_backAnkleJntFK)
    cmds.parent(L_backAnkleJntFK, L_backLowerJntFK)
    cmds.parent(L_backLowerJntFK, L_backUpperJntFK)
    cmds.parent(L_backUpperJntFK, backPelvisJnt)

    cmds.parent(R_backToeJntFK, R_backBallJntFK)
    cmds.parent(R_backBallJntFK, R_backAnkleJntFK)
    cmds.parent(R_backAnkleJntFK, R_backLowerJntFK)
    cmds.parent(R_backLowerJntFK, R_backUpperJntFK)
    cmds.parent(R_backUpperJntFK, backPelvisJnt)

    # orient FK joints
    cmds.select(L_backUpperJntFK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(R_backUpperJntFK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(d=True)


def createFrontLegJoints():
    global frontPelvisJnt
    global L_frontUpperJnt
    global L_frontLowerJnt
    global L_frontAnkleJnt
    global L_frontBallJnt
    global L_frontToeJnt
    global L_frontToeEndJnt
    global R_frontUpperJnt
    global R_frontLowerJnt
    global R_frontAnkleJnt
    global R_frontBallJnt
    global R_frontToeJnt
    global R_frontToeEndJnt
    ''' front legs '''
    # create L front joints
    frontPelvisJnt = cmds.joint(n='c_frontPelvis_JNT')
    constr = cmds.pointConstraint(frontPelvisLoc, frontPelvisJnt)
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontUpperJnt = cmds.joint(n='l_frontUpperLeg_JNT')
    constr = cmds.pointConstraint(frontUpperLoc,
                                  L_frontUpperJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontAnkleJnt = cmds.joint(n='l_frontAnkle_JNT')
    constr = cmds.pointConstraint(frontAnkleLoc,L_frontAnkleJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontLowerJnt = cmds.joint(n='l_frontLowerLeg_JNT')
    constr = cmds.pointConstraint(frontLowerLoc,
                                  L_frontLowerJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontBallJnt = cmds.joint(n='l_frontBall_JNT')
    constr = cmds.pointConstraint(frontBallLoc,
                                  L_frontBallJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontToeJnt = cmds.joint(n='l_frontToe_JNT')
    constr = cmds.pointConstraint(frontToeLoc,
                                  L_frontToeJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    # mirror L front joints to other side....
    R_frontUpperJnt = cmds.duplicate(L_frontUpperJnt, n='r_frontUpperLeg_JNT')
    R_frontUpperJnt = R_frontUpperJnt[0]
    xPos = cmds.getAttr(L_frontUpperJnt + '.tx')
    cmds.setAttr(R_frontUpperJnt + '.tx', -xPos)

    R_frontAnkleJnt = cmds.duplicate(L_frontAnkleJnt, n='r_frontAnkle_JNT')
    R_frontAnkleJnt = R_frontAnkleJnt[0]
    xPos = cmds.getAttr(L_frontAnkleJnt + '.tx')
    cmds.setAttr(R_frontAnkleJnt + '.tx', -xPos)

    R_frontLowerJnt = cmds.duplicate(L_frontLowerJnt, n='r_frontLowerKnee_JNT')
    R_frontLowerJnt = R_frontLowerJnt[0]
    xPos = cmds.getAttr(L_frontLowerJnt + '.tx')
    cmds.setAttr(R_frontLowerJnt + '.tx', -xPos)

    R_frontBallJnt = cmds.duplicate(L_frontBallJnt, n='r_frontBall_JNT')
    R_frontBallJnt = R_frontBallJnt[0]
    xPos = cmds.getAttr(L_frontBallJnt + '.tx')
    cmds.setAttr(R_frontBallJnt + '.tx', -xPos)

    R_frontToeJnt = cmds.duplicate(L_frontToeJnt, n='r_frontToe_JNT')
    R_frontToeJnt = R_frontToeJnt[0]
    xPos = cmds.getAttr(L_frontToeJnt + '.tx')
    cmds.setAttr(R_frontToeJnt + '.tx', -xPos)

    # end joints for mayaSkinning
    L_frontToeEndJnt = cmds.joint(n='l_frontToeEnd_Jnt')
    constr = cmds.pointConstraint(L_frontToeJnt, L_frontToeEndJnt)
    cmds.delete(constr)
    cmds.parent(L_frontToeEndJnt, L_frontToeJnt)
    cmds.setAttr(L_frontToeEndJnt + '.tz',
                 .04)  # we don't want the end of the toe to overlap another joint due to skinning issues with overlapping joints mirroring
    cmds.setAttr(L_frontToeEndJnt + '.visibility', 0)
    cmds.select(d=True)

    R_frontToeEndJnt = cmds.joint(n='r_frontToeEnd_Jnt')
    constr = cmds.pointConstraint(R_frontToeJnt, R_frontToeEndJnt)
    cmds.delete(constr)
    cmds.parent(R_frontToeEndJnt, R_frontToeJnt)
    cmds.setAttr(R_frontToeEndJnt + '.tz',
                 .04)  # we don't want the end of the toe to overlap another joint due to skinning issues with overlapping joints mirroring
    cmds.setAttr(R_frontToeEndJnt + '.visibility', 0)
    cmds.select(d=True)

    # parent front leg joints...
    cmds.parent(L_frontToeJnt, L_frontBallJnt)
    cmds.parent(L_frontBallJnt, L_frontAnkleJnt)
    cmds.parent(L_frontAnkleJnt, L_frontLowerJnt)
    cmds.parent(L_frontLowerJnt, L_frontUpperJnt)
    cmds.parent(L_frontUpperJnt, frontPelvisJnt)

    cmds.parent(R_frontToeJnt, R_frontBallJnt)
    cmds.parent(R_frontBallJnt, R_frontAnkleJnt)
    cmds.parent(R_frontAnkleJnt, R_frontLowerJnt)
    cmds.parent(R_frontLowerJnt, R_frontUpperJnt)
    cmds.parent(R_frontUpperJnt, frontPelvisJnt)

    # orient joints
    cmds.select(L_frontUpperJnt)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(R_frontUpperJnt)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(d=True)


def createFrontLegIKJoints():
    global L_frontUpperJntIK
    global L_frontLowerJntIK
    global L_frontAnkleJntIK
    global L_frontBallJntIK
    global L_frontToeJntIK
    global R_frontUpperJntIK
    global R_frontLowerJntIK
    global R_frontAnkleJntIK
    global R_frontBallJntIK
    global R_frontToeJntIK

    '''L IK front Legs'''

    # create L IK joints....
    L_frontUpperJntIK = cmds.joint(n='l_frontUpperLegIK_JNT')
    constr = cmds.pointConstraint(frontUpperLoc,
                                  L_frontUpperJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontLowerJntIK = cmds.joint(n='l_frontLowerLegIK_JNT')
    constr = cmds.pointConstraint(frontLowerLoc,
                                  L_frontLowerJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontAnkleJntIK = cmds.joint(n='l_frontAnkleIK_JNT')
    constr = cmds.pointConstraint(frontAnkleLoc,
                                  L_frontAnkleJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontBallJntIK = cmds.joint(n='l_frontBallIK_JNT')
    constr = cmds.pointConstraint(frontBallLoc,
                                  L_frontBallJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontToeJntIK = cmds.joint(n='l_frontToeIK_JNT')
    constr = cmds.pointConstraint(frontToeLoc,
                                  L_frontToeJntIK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    # mirror L IK joints to other side....

    R_frontUpperJntIK = cmds.duplicate(L_frontUpperJntIK, n='r_frontUpperLegIK_JNT')
    R_frontUpperJntIK = R_frontUpperJntIK[0]
    xPos = cmds.getAttr(L_frontUpperJntIK + '.tx')
    cmds.setAttr(R_frontUpperJntIK + '.tx', -xPos)

    R_frontAnkleJntIK = cmds.duplicate(L_frontAnkleJntIK, n='r_frontAnkleIK_JNT')
    R_frontAnkleJntIK = R_frontAnkleJntIK[0]
    xPos = cmds.getAttr(L_frontAnkleJntIK + '.tx')
    cmds.setAttr(R_frontAnkleJntIK + '.tx', -xPos)

    R_frontLowerJntIK = cmds.duplicate(L_frontLowerJntIK, n='r_frontLowerKneeIK_JNT')
    R_frontLowerJntIK = R_frontLowerJntIK[0]
    xPos = cmds.getAttr(L_frontLowerJntIK + '.tx')
    cmds.setAttr(R_frontLowerJntIK + '.tx', -xPos)

    R_frontBallJntIK = cmds.duplicate(L_frontBallJntIK, n='r_frontBallIK_JNT')
    R_frontBallJntIK = R_frontBallJntIK[0]
    xPos = cmds.getAttr(L_frontBallJntIK + '.tx')
    cmds.setAttr(R_frontBallJntIK + '.tx', -xPos)

    R_frontToeJntIK = cmds.duplicate(L_frontToeJntIK, n='r_frontToeIK_JNT')
    R_frontToeJntIK = R_frontToeJntIK[0]
    xPos = cmds.getAttr(L_frontToeJntIK + '.tx')
    cmds.setAttr(R_frontToeJntIK + '.tx', -xPos)

    # parent front IK leg joints...
    cmds.parent(L_frontToeJntIK, L_frontBallJntIK)
    cmds.parent(L_frontBallJntIK, L_frontAnkleJntIK)
    cmds.parent(L_frontAnkleJntIK, L_frontLowerJntIK)
    cmds.parent(L_frontLowerJntIK, L_frontUpperJntIK)
    cmds.parent(L_frontUpperJntIK, frontPelvisJnt)

    cmds.parent(R_frontToeJntIK, R_frontBallJntIK)
    cmds.parent(R_frontBallJntIK, R_frontAnkleJntIK)
    cmds.parent(R_frontAnkleJntIK, R_frontLowerJntIK)
    cmds.parent(R_frontLowerJntIK, R_frontUpperJntIK)
    cmds.parent(R_frontUpperJntIK, frontPelvisJnt)

    # orient IK joints
    cmds.select(L_frontUpperJntIK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(R_frontUpperJntIK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(d=True)


def createFrontLegFKJoints():
    global L_frontUpperJntFK
    global L_frontLowerJntFK
    global L_frontAnkleJntFK
    global L_frontBallJntFK
    global L_frontToeJntFK
    global R_frontUpperJntFK
    global R_frontLowerJntFK
    global R_frontAnkleJntFK
    global R_frontBallJntFK
    global R_frontToeJntFK
    '''L FK front Legs'''
    # create FK joints on left side....
    L_frontUpperJntFK = cmds.joint(n='l_frontUpperLegFK_JNT')
    constr = cmds.pointConstraint(frontUpperLoc,
                                  L_frontUpperJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontLowerJntFK = cmds.joint(n='l_frontLowerLegFK_JNT')
    constr = cmds.pointConstraint(frontLowerLoc,
                                  L_frontLowerJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontAnkleJntFK = cmds.joint(n='l_frontAnkleFK_JNT')
    constr = cmds.pointConstraint(frontAnkleLoc,
                                  L_frontAnkleJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontBallJntFK = cmds.joint(n='l_frontBallFK_JNT')
    constr = cmds.pointConstraint(frontBallLoc,
                                  L_frontBallJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    L_frontToeJntFK = cmds.joint(n='l_frontToeFK_JNT')
    constr = cmds.pointConstraint(frontToeLoc,
                                  L_frontToeJntFK)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.select(d=True)  # deselect the jnt

    # mirror L FK joints to other side....
    R_frontUpperJntFK = cmds.duplicate(L_frontUpperJntFK, n='r_frontUpperLegFK_JNT')
    R_frontUpperJntFK = R_frontUpperJntFK[0]
    xPos = cmds.getAttr(L_frontUpperJntFK + '.tx')
    cmds.setAttr(R_frontUpperJntFK + '.tx', -xPos)

    R_frontAnkleJntFK = cmds.duplicate(L_frontAnkleJntFK, n='r_frontAnkleFK_JNT')
    R_frontAnkleJntFK = R_frontAnkleJntFK[0]
    xPos = cmds.getAttr(L_frontAnkleJntFK + '.tx')
    cmds.setAttr(R_frontAnkleJntFK + '.tx', -xPos)

    R_frontLowerJntFK = cmds.duplicate(L_frontLowerJntFK, n='r_frontLowerKneeFK_JNT')
    R_frontLowerJntFK = R_frontLowerJntFK[0]
    xPos = cmds.getAttr(L_frontLowerJntFK + '.tx')
    cmds.setAttr(R_frontLowerJntFK + '.tx', -xPos)

    R_frontBallJntFK = cmds.duplicate(L_frontBallJntFK, n='r_frontBallFK_JNT')
    R_frontBallJntFK = R_frontBallJntFK[0]
    xPos = cmds.getAttr(L_frontBallJntFK + '.tx')
    cmds.setAttr(R_frontBallJntFK + '.tx', -xPos)

    R_frontToeJntFK = cmds.duplicate(L_frontToeJntFK, n='r_frontToeFK_JNT')
    R_frontToeJntFK = R_frontToeJntFK[0]
    xPos = cmds.getAttr(L_frontToeJntFK + '.tx')
    cmds.setAttr(R_frontToeJntFK + '.tx', -xPos)

    # parent front FK leg joints...
    cmds.parent(L_frontToeJntFK, L_frontBallJntFK)
    cmds.parent(L_frontBallJntFK, L_frontAnkleJntFK)
    cmds.parent(L_frontAnkleJntFK, L_frontLowerJntFK)
    cmds.parent(L_frontLowerJntFK, L_frontUpperJntFK)
    cmds.parent(L_frontUpperJntFK, frontPelvisJnt)

    cmds.parent(R_frontToeJntFK, R_frontBallJntFK)
    cmds.parent(R_frontBallJntFK, R_frontAnkleJntFK)
    cmds.parent(R_frontAnkleJntFK, R_frontLowerJntFK)
    cmds.parent(R_frontLowerJntFK, R_frontUpperJntFK)
    cmds.parent(R_frontUpperJntFK, frontPelvisJnt)

    # orient FK joints
    cmds.select(L_frontUpperJntFK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(R_frontUpperJntFK)
    cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)
    cmds.select(d=True)


def SetupIK():
    global L_frontLegTranslationCtrlGrp
    global R_frontLegTranslationCtrlGrp
    global L_frontLegTranslationCtrl
    global R_frontLegTranslationCtrl
    global distance
    global L_backAnkleIK
    global R_backAnkleIK
    global L_frontAnkleIK
    global R_frontAnkleIK
    global L_backToeIK
    global R_backToeIK
    global L_frontToeIK
    global R_frontToeIK

    global ctrlSize
    global L_backPoleGrp
    global R_backPoleGrp
    global L_backIKCtl
    global R_backIKCtl
    global L_backIKCtlGrp
    global R_backIKCtlGrp

    global L_frontPoleGrp
    global R_frontPoleGrp
    global L_frontIKCtl
    global R_frontIKCtl
    global L_frontIKCtlGrp
    global R_frontIKCtlGrp
    global L_frontAnkleIK
    global R_frontAnkleIK

    global IKCtrlGrp

    ''' ik L back leg '''
    L_backAnkleIK = cmds.ikHandle(sol='ikRPsolver', n='l_backLeg_IK', sj=L_backUpperJntIK, ee=L_backBallJntIK)  # (solver, name, startJoint, endEffector)
    L_backIKCtl = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4], n='l_backIK_CTRL')
    # get distance to get controller with proper scale. distance is based on front ---> back leg toe joint
    dist = cmds.createNode('distanceDimShape', n='deleteWhenDone')
    legStart = cmds.xform(L_backToeJntIK, q=True, ws=True,rp=True)  # (objectToQuery, query, worldSpace,rotationPivotPoint )
    legEnd = cmds.xform(L_frontToeJntIK, q=True, ws=True,rp=True)  # (objectToQuery, query, worldSpace,rotationPivotPoint )
    # L_backToeJntIK ------> L_frontToeJntIK
    # here we use the dist node to draw out a line that gives us the total distance between the front and back Toe Jnts**
    cmds.setAttr(dist + '.endPoint', *(legEnd))
    cmds.setAttr(dist + '.startPoint', *(legStart))
    distance = cmds.getAttr(dist + '.distance')  # get the total distance traveled by dist  node
    cmds.delete(cmds.listRelatives(dist,p=True))  # we want to grab the parent of the dist node and delete the parent so we don't get an empty group after delete
    ctrlSize = distance / 8
    cmds.setAttr(L_backIKCtl + '.sx', ctrlSize)
    cmds.setAttr(L_backIKCtl + '.sy', ctrlSize)
    cmds.setAttr(L_backIKCtl + '.sz', ctrlSize)
    cmds.makeIdentity(L_backIKCtl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    lockScale(L_backIKCtl)
    L_backIKCtlGrp = cmds.group(L_backIKCtl, n='l_backIKCtrl_GRP')
    blueColor(L_backIKCtlGrp)
    constr = cmds.pointConstraint(L_backToeJnt, L_backIKCtlGrp)
    cmds.delete(constr)
    # the L_IK has 2 components in it's list the ikHandle and the effector. we only want the ikHandle so make sure to target it by grabbing [0] in the list
    # DO NOT MOVE THE EFFECTOR
    cmds.parent(L_backAnkleIK[0], L_backIKCtl)
    cmds.setAttr(L_backAnkleIK[0] + '.visibility', 0)
    cmds.aimConstraint(L_backIKCtl, L_backUpperJntIK, n='l_upperLeg_aim_towards_footCtrl', mo=True, wu=[0, 0, 0])


    L_backToeIK = cmds.ikHandle(sol='ikRPsolver', n='l_backToe_IK', sj=L_backBallJntIK, ee=L_backToeJntIK)  # (solver, name, startJoint, endEffector)
    cmds.parent(L_backToeIK[0], L_backIKCtl)
    cmds.setAttr(L_backToeIK[0] + '.visibility', 0)

    ''' ik R back leg '''
    R_backAnkleIK = cmds.ikHandle(sol='ikRPsolver', n='r_backLeg_IK', sj=R_backUpperJntIK, ee=R_backBallJntIK)  # (solver, name, startJoint, endEffector)
    R_backIKCtl = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],n='r_backIK_CTRL')
    # reusing the distance ctrl size we previously calculated on the left side to adjust curve size
    cmds.setAttr(R_backIKCtl + '.sx', ctrlSize)
    cmds.setAttr(R_backIKCtl + '.sy', ctrlSize)
    cmds.setAttr(R_backIKCtl + '.sz', ctrlSize)
    cmds.makeIdentity(R_backIKCtl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    lockScale(R_backIKCtl)
    R_backIKCtlGrp = cmds.group(R_backIKCtl, n='r_footIKCtrl_GRP')
    redColor(R_backIKCtlGrp)
    constr = cmds.pointConstraint(R_backToeJnt, R_backIKCtlGrp)
    cmds.delete(constr)

    # the R_IK has 2 components in it's list the ikHandle and the effector
    # we only want the ikHandle so make sure to target it by grabbing [0] in the list
    # DO NOT MOVE THE EFFECTOR
    cmds.parent(R_backAnkleIK[0], R_backIKCtl)
    cmds.setAttr(R_backAnkleIK[0] + '.visibility', 0)
    # aim constraint
    cmds.aimConstraint(R_backIKCtl, R_backUpperJntIK, n='r_upperLeg_aim_towards_footCtrl', mo=True, wu=[0, 0, 0])
    R_backToeIK = cmds.ikHandle(sol='ikRPsolver', n='r_backToe_IK', sj=R_backBallJntIK, ee=R_backToeJntIK)  # (solver, name, startJoint, endEffector)

    # the R_backToeIK has 2 components in it's list the ikHandle and the effector
    # we only want the ikHandle so make sure to target it by grabbing [0] in the list
    # DO NOT MOVE THE EFFECTOR
    cmds.parent(R_backToeIK[0], R_backIKCtl)
    cmds.setAttr(R_backToeIK[0] + '.visibility', 0)

    ''' ik L front leg '''
    L_frontAnkleIK = cmds.ikHandle(sol='ikRPsolver', n='l_frontLeg_IK', sj=L_frontUpperJntIK, ee=L_frontBallJntIK)  # (solver, name, startJoint, endEffector)
    L_frontToeIK = cmds.ikHandle(sol='ikRPsolver', n='l_frontToe_IK', sj=L_frontBallJntIK, ee=L_frontToeJntIK)

    L_frontIKCtl = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4], n='l_frontIK_CTRL')

    cmds.setAttr(L_frontIKCtl + '.sx', ctrlSize)  # use distance ctrlSize that was calculated previously at top
    cmds.setAttr(L_frontIKCtl + '.sy', ctrlSize)
    cmds.setAttr(L_frontIKCtl + '.sz', ctrlSize)
    cmds.makeIdentity(L_frontIKCtl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    lockScale(L_frontIKCtl)
    L_frontIKCtlGrp = cmds.group(L_frontIKCtl, n='l_footIKCtrl_GRP')
    blueColor(L_frontIKCtlGrp)
    constr = cmds.pointConstraint(L_frontToeJnt, L_frontIKCtlGrp)
    cmds.delete(constr)

    # DO NOT MOVE THE EFFECTOR [0] ensures we only parent ikHandle and not effector
    cmds.parent(L_frontAnkleIK[0], L_frontIKCtl)
    cmds.parent(L_frontToeIK[0], L_frontIKCtl)
    cmds.setAttr(L_frontAnkleIK[0] + '.visibility', 0)
    cmds.setAttr(L_frontToeIK[0] + '.visibility', 0)

    '''l ik front leg rotation ctrl'''
    L_frontLegTranslationCtrl = CreateSphereRigCtrl('l_frontLegTranslation_CTRL')
    L_frontLegTranslationCtrlGrp = cmds.group(L_frontLegTranslationCtrl, n='l_frontLegTranslationCtrl_GRP')
    cmds.scale(ctrlSize*1.5, ctrlSize*1.5, ctrlSize*1.5)
    cmds.makeIdentity(L_frontLegTranslationCtrlGrp, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    constr = cmds.pointConstraint(L_frontUpperJntIK, L_frontLegTranslationCtrlGrp)
    cmds.delete(constr)
    blueColor(L_frontLegTranslationCtrl[0])



    #lets connect this translation curve to our ik upper joint
    cmds.pointConstraint(L_frontLegTranslationCtrl,L_frontUpperJntIK)

    #we also want the clavicle ctrl to move with the pelvis
    cmds.parentConstraint(frontPelvisJnt,L_frontLegTranslationCtrlGrp,mo=True) # (mover/moved)


    ''' ik R front leg '''
    R_frontAnkleIK = cmds.ikHandle(sol='ikRPsolver', n='r_frontLeg_IK', sj=R_frontUpperJntIK, ee=R_frontBallJntIK)  # (solver, name, startJoint, endEffector)
    R_frontToeIK = cmds.ikHandle(sol='ikRPsolver', n='r_frontToe_IK', sj=R_frontBallJntIK, ee=R_frontToeJntIK)

    R_frontIKCtl = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],n='r_frontIK_CTRL')

    cmds.setAttr(R_frontIKCtl + '.sx', ctrlSize)  # use distance ctrlSize that was calculated previously at top
    cmds.setAttr(R_frontIKCtl + '.sy', ctrlSize)
    cmds.setAttr(R_frontIKCtl + '.sz', ctrlSize)
    cmds.makeIdentity(R_frontIKCtl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    lockScale(R_frontIKCtl)
    R_frontIKCtlGrp = cmds.group(R_frontIKCtl, n='r_frontIKCtrl_GRP')
    redColor(R_frontIKCtlGrp)
    constr = cmds.pointConstraint(R_frontToeJnt, R_frontIKCtlGrp)
    cmds.delete(constr)

    # DO NOT MOVE THE EFFECTOR [0] ensures we only parent ikHandle and not effector
    cmds.parent(R_frontAnkleIK[0], R_frontIKCtl)
    cmds.parent(R_frontToeIK[0], R_frontIKCtl)
    cmds.setAttr(R_frontAnkleIK[0] + '.visibility', 0)
    cmds.setAttr(R_frontToeIK[0] + '.visibility', 0)

    '''r ik front leg rotation ctrl'''
    R_frontLegTranslationCtrl = CreateSphereRigCtrl('r_frontLegTranslation_CTRL')
    R_frontLegTranslationCtrlGrp = cmds.group(R_frontLegTranslationCtrl, n='r_frontLegTranslationCtrl_GRP')
    cmds.scale(ctrlSize*1.5, ctrlSize*1.5, ctrlSize*1.5)
    cmds.makeIdentity(R_frontLegTranslationCtrlGrp, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    constr = cmds.parentConstraint(R_frontUpperJntIK, R_frontLegTranslationCtrlGrp)
    cmds.delete(constr)
    redColor(R_frontLegTranslationCtrl[0])



    #lets connect this translation curve to our ik upper joint
    cmds.pointConstraint(R_frontLegTranslationCtrl,R_frontUpperJntIK)

    #we also want the clavicle ctrl to move with the pelvis
    cmds.parentConstraint(frontPelvisJnt,R_frontLegTranslationCtrlGrp,mo=True) # (mover/moved)

    '''create IK polevector'''
    # L back IK polevector
    L_backPoleVectorCtrl = cmds.curve(d=1, p=[(-1, 0, 0.6), (1, 0, 0.6), (0, 0, -1.2), (-1, 0, 0.6)], k=[0, 1, 2, 3],n='L_backPoleVector_CTRL')
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(L_backPoleVectorCtrl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    L_backPoleGrp = cmds.group(L_backPoleVectorCtrl, n='L_backPoleVectorCtrl_GRP')
    constr = cmds.parentConstraint(backAnkleLoc, L_backPoleGrp)
    cmds.delete(constr)
    addDista = cmds.getAttr(L_backPoleGrp + '.tz')  # move control forward away from knee
    cmds.setAttr(L_backPoleGrp + '.tz', addDista * 2)
    blueColor(L_backPoleVectorCtrl)
    cmds.poleVectorConstraint(L_backPoleVectorCtrl, L_backAnkleIK[0])

    # if leg twitsts in a weird way then set the twist to 180 cmds.setAttr(L_backAnkleIK[0]+'.twist',180)
    cmds.setAttr(L_backAnkleIK[0] + '.twist', 180)


    # R back IK polevector
    R_backPoleVectorCtrl = cmds.curve(d=1, p=[(-1, 0, 0.6), (1, 0, 0.6), (0, 0, -1.2), (-1, 0, 0.6)], k=[0, 1, 2, 3],
                                      n='R_backPoleVector_CTRL')
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(R_backPoleVectorCtrl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    R_backPoleGrp = cmds.group(R_backPoleVectorCtrl, n='R_backPoleVectorCtrl_GRP')
    constr = cmds.parentConstraint(backAnkleLoc, R_backPoleGrp)
    cmds.delete(constr)
    addDista = cmds.getAttr(R_backPoleGrp + '.tz')  # move control forward away from knee
    cmds.setAttr(R_backPoleGrp + '.tz', addDista * 2)
    redColor(R_backPoleVectorCtrl)

    # mirror to other side
    mirrorX = cmds.getAttr(R_backPoleGrp + '.tx')
    print('Mirror x value is = ' + str(mirrorX))
    cmds.setAttr(R_backPoleGrp + '.tx', -(mirrorX))

    cmds.poleVectorConstraint(R_backPoleVectorCtrl, R_backAnkleIK[0])

    # if leg twitsts in a weird way then set the twist to 180 cmds.setAttr(R_backAnkleIK[0]+'.twist',180)
    cmds.setAttr(R_backAnkleIK[0] + '.twist', 180)

    # L front IK polevector
    L_frontPoleVectorCtrl = cmds.curve(d=1, p=[(-1, 0, 0.6), (1, 0, 0.6), (0, 0, -1.2), (-1, 0, 0.6)],
                                       k=[0, 1, 2, 3],
                                       n='L_frontPoleVector_CTRL')

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(L_frontPoleVectorCtrl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    L_frontPoleGrp = cmds.group(L_frontPoleVectorCtrl, n='L_frontPoleVectorCtrl_GRP')
    constr = cmds.parentConstraint(frontAnkleLoc, L_frontPoleGrp)
    cmds.delete(constr)
    addDista = cmds.getAttr(L_frontPoleGrp + '.tz')  # move control forward away from knee
    cmds.setAttr(L_frontPoleGrp + '.tz', addDista * .1)
    blueColor(L_frontPoleVectorCtrl)
    cmds.poleVectorConstraint(L_frontPoleVectorCtrl, L_frontAnkleIK[0])

    # if leg twitsts in a weird way then set the twist to 180 cmds.setAttr(L_frontIK[0]+'.twist',180)
    # cmds.setAttr(L_frontAnkleIK[0] + '.twist', 180)

    # R front IK polevector
    R_frontPoleVectorCtrl = cmds.curve(d=1, p=[(-1, 0, 0.6), (1, 0, 0.6), (0, 0, -1.2), (-1, 0, 0.6)],
                                       k=[0, 1, 2, 3],
                                       n='R_frontPoleVector_CTRL')
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(R_frontPoleVectorCtrl, apply=True, t=1, r=1, s=1, n=0)  # freeze transform
    R_frontPoleGrp = cmds.group(R_frontPoleVectorCtrl, n='R_frontPoleVectorCtrl_GRP')
    constr = cmds.parentConstraint(frontAnkleLoc, R_frontPoleGrp)
    cmds.delete(constr)
    addDista = cmds.getAttr(R_frontPoleGrp + '.tz')  # move control forward away from knee
    cmds.setAttr(R_frontPoleGrp + '.tz', addDista * .1)
    redColor(R_frontPoleVectorCtrl)

    # mirror to other side
    mirrorX = cmds.getAttr(R_frontPoleGrp + '.tx')
    cmds.setAttr(R_frontPoleGrp + '.tx', -(mirrorX))

    cmds.poleVectorConstraint(R_frontPoleVectorCtrl, R_frontAnkleIK[0])
    # if leg twists in a weird way then set the twist to 180
    # cmds.setAttr(R_frontAnkleIK[0] + '.twist', 180)

    # group polevector groups
    poleVectorGrp = cmds.group(L_frontPoleGrp, R_frontPoleGrp, L_backPoleGrp, R_backPoleGrp, n='c_poleVector_GRP')

    # group fk groups
    IKCtrlGrp = cmds.group(R_frontLegTranslationCtrlGrp, L_frontLegTranslationCtrlGrp, L_backIKCtlGrp, R_backIKCtlGrp, L_frontIKCtlGrp, R_frontIKCtlGrp, poleVectorGrp, n='c_ikCtrl_GRP')


def SetupFK():
    ''' fk leg setup '''
    global L_backUpperFkCtrl_GRP
    global R_backUpperFkCtrl_GRP
    global L_frontUpperFkCtrl_GRP
    global R_frontUpperFkCtrl_GRP
    global FKCtrlGrp
    # left back fk ctrl
    # left back upper
    L_backUpperFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_backUpperFK_CTRL')
    L_backUpperFkCtrl_GRP = cmds.group(L_backUpperFkCtrl, n='l_backUpperFkCtrl_GRP')
    constr = cmds.pointConstraint(backUpperLoc, L_backUpperFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)


    cmds.parentConstraint(L_backUpperFkCtrl, L_backUpperJntFK, mo=True)
    #now parent the group of upper so that our fk curves/joints follow root

    # this is Daniel's code
    cmds.parentConstraint(backPelvisJnt, L_backUpperFkCtrl_GRP, mo=True, n="c_fkFollowRoot")

    lockScale(L_backUpperFkCtrl[0])
    lockTranslate(L_backUpperFkCtrl[0])

    # left back lower
    L_backLowerFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_backLowerFK_CTRL')
    L_backLowerFkCtrl_GRP = cmds.group(L_backLowerFkCtrl, n='l_backLowerFkCtrl_GRP')
    constr = cmds.pointConstraint(backLowerLoc, L_backLowerFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_backLowerFkCtrl, L_backLowerJntFK, mo=True)
    lockScale(L_backLowerFkCtrl[0])
    lockTranslate(L_backLowerFkCtrl[0])

    # left back ankle
    L_backAnkleFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_backAnkleFK_CTRL')
    L_backAnkleFkCtrl_GRP = cmds.group(L_backAnkleFkCtrl, n='l_backAnkleFkCtrl_GRP')
    constr = cmds.pointConstraint(backAnkleLoc, L_backAnkleFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_backAnkleFkCtrl, L_backAnkleJntFK, mo=True)
    lockScale(L_backAnkleFkCtrl[0])
    lockTranslate(L_backAnkleFkCtrl[0])

    # left back ball
    L_backBallFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_backBallFK_CTRL')
    L_backBallFkCtrl_GRP = cmds.group(L_backBallFkCtrl, n='l_backBallFkCtrl_GRP')
    constr = cmds.pointConstraint(backBallLoc, L_backBallFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_backBallFkCtrl, L_backBallJntFK, mo=True)
    lockScale(L_backBallFkCtrl[0])
    lockTranslate(L_backBallFkCtrl[0])

    # left back toe
    L_backToeFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_backToeFK_CTRL')
    L_backToeFkCtrl_GRP = cmds.group(L_backToeFkCtrl, n='l_backToeFkCtrl_GRP')
    constr = cmds.pointConstraint(backToeLoc, L_backToeFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_backToeFkCtrl, L_backToeJntFK, mo=True)
    lockScale(L_backToeFkCtrl[0])
    lockTranslate(L_backToeFkCtrl[0])

    # parent all back left FK ctrl GRPS
    cmds.parent(L_backLowerFkCtrl_GRP, L_backUpperFkCtrl[0])  # child/parent
    cmds.parent(L_backAnkleFkCtrl_GRP, L_backLowerFkCtrl[0])  # child/parent
    cmds.parent(L_backBallFkCtrl_GRP, L_backAnkleFkCtrl[0])  # child/parent
    cmds.parent(L_backToeFkCtrl_GRP, L_backBallFkCtrl[0])  # child/parent

    # right back fk ctrl
    # right back upper
    R_backUpperFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_backUpperFK_CTRL')
    R_backUpperFkCtrl_GRP = cmds.group(R_backUpperFkCtrl, n='r_backUpperFkCtrl_GRP')
    constr = cmds.pointConstraint(backUpperLoc, R_backUpperFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_backUpperFkCtrl_GRP + '.tx', -(cmds.getAttr(R_backUpperFkCtrl_GRP + '.tx')))

    # set scale
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)


    cmds.parentConstraint(R_backUpperFkCtrl, R_backUpperJntFK, mo=True)
    #now parent the group of upper so that our fk curves/joints follow root

    #this is Daniel's code
    cmds.parentConstraint(backPelvisJnt, R_backUpperFkCtrl_GRP, mo=True, n="c_fkFollowRoot")

    lockScale(R_backUpperFkCtrl[0])
    lockTranslate(R_backUpperFkCtrl[0])

    # right back lower
    R_backLowerFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_backLowerFK_CTRL')
    R_backLowerFkCtrl_GRP = cmds.group(R_backLowerFkCtrl, n='r_backLowerFkCtrl_GRP')
    constr = cmds.pointConstraint(backLowerLoc, R_backLowerFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_backLowerFkCtrl_GRP + '.tx', -(cmds.getAttr(R_backLowerFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_backLowerFkCtrl, R_backLowerJntFK, mo=True)
    lockScale(R_backLowerFkCtrl[0])
    lockTranslate(R_backLowerFkCtrl[0])

    # right back ankle
    R_backAnkleFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_backAnkleFK_CTRL')
    R_backAnkleFkCtrl_GRP = cmds.group(R_backAnkleFkCtrl, n='r_backAnkleFkCtrl_GRP')
    constr = cmds.pointConstraint(backAnkleLoc, R_backAnkleFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_backAnkleFkCtrl_GRP + '.tx', -(cmds.getAttr(R_backAnkleFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_backAnkleFkCtrl, R_backAnkleJntFK, mo=True)
    lockScale(R_backAnkleFkCtrl[0])
    lockTranslate(R_backAnkleFkCtrl[0])

    # right back ball
    R_backBallFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_backBallFK_CTRL')
    R_backBallFkCtrl_GRP = cmds.group(R_backBallFkCtrl, n='r_backBallFkCtrl_GRP')
    constr = cmds.pointConstraint(backBallLoc, R_backBallFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_backBallFkCtrl_GRP + '.tx', -(cmds.getAttr(R_backBallFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_backBallFkCtrl, R_backBallJntFK, mo=True)
    lockScale(R_backBallFkCtrl[0])
    lockTranslate(R_backBallFkCtrl[0])

    # right back toe
    R_backToeFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_backToeFK_CTRL')
    R_backToeFkCtrl_GRP = cmds.group(R_backToeFkCtrl, n='r_backToeFkCtrl_GRP')
    constr = cmds.pointConstraint(backToeLoc, R_backToeFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group x axis  to other side
    cmds.setAttr(R_backToeFkCtrl_GRP + '.tx', -(cmds.getAttr(R_backToeFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_backToeFkCtrl, R_backToeJntFK, mo=True)
    lockScale(R_backToeFkCtrl[0])
    lockTranslate(R_backToeFkCtrl[0])

    # parent all back right FK ctrl GRPS
    cmds.parent(R_backLowerFkCtrl_GRP, R_backUpperFkCtrl[0])  # child/parent
    cmds.parent(R_backAnkleFkCtrl_GRP, R_backLowerFkCtrl[0])  # child/parent
    cmds.parent(R_backBallFkCtrl_GRP, R_backAnkleFkCtrl[0])  # child/parent
    cmds.parent(R_backToeFkCtrl_GRP, R_backBallFkCtrl[0])  # child/parent

    # parent's color applies to all chidlren
    redColor(R_backUpperFkCtrl_GRP)

    # left front fk ctrl
    # left front upper
    L_frontUpperFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_frontUpperFK_CTRL')
    L_frontUpperFkCtrl_GRP = cmds.group(L_frontUpperFkCtrl, n='l_frontUpperFkCtrl_GRP')
    constr = cmds.pointConstraint(frontUpperLoc, L_frontUpperFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    cmds.parentConstraint(L_frontUpperFkCtrl, L_frontUpperJntFK, mo=True,n='testtest')
    #now parent the group of upper so that our fk curves/joints follow root

    #this is Daniel's code
    cmds.parentConstraint(frontPelvisJnt, L_frontUpperFkCtrl_GRP, mo=True, n="c_fkFollowRoot")

    lockScale(L_frontUpperFkCtrl[0])
    lockTranslate(L_frontUpperFkCtrl[0])

    # left front lower
    L_frontLowerFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_frontLowerFK_CTRL')
    L_frontLowerFkCtrl_GRP = cmds.group(L_frontLowerFkCtrl, n='l_frontLowerFkCtrl_GRP')
    constr = cmds.pointConstraint(frontLowerLoc, L_frontLowerFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_frontLowerFkCtrl, L_frontLowerJntFK, mo=True)
    lockScale(L_frontLowerFkCtrl[0])
    lockTranslate(L_frontLowerFkCtrl[0])

    # left front ankle
    L_frontAnkleFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_frontAnkleFK_CTRL')
    L_frontAnkleFkCtrl_GRP = cmds.group(L_frontAnkleFkCtrl, n='l_frontAnkleFkCtrl_GRP')
    constr = cmds.pointConstraint(frontAnkleLoc, L_frontAnkleFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_frontAnkleFkCtrl, L_frontAnkleJntFK, mo=True)
    lockScale(L_frontAnkleFkCtrl[0])
    lockTranslate(L_frontAnkleFkCtrl[0])

    # left front ball
    L_frontBallFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_frontBallFK_CTRL')
    L_frontBallFkCtrl_GRP = cmds.group(L_frontBallFkCtrl, n='l_frontBallFkCtrl_GRP')
    constr = cmds.pointConstraint(frontBallLoc, L_frontBallFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_frontBallFkCtrl, L_frontBallJntFK, mo=True)
    lockScale(L_frontBallFkCtrl[0])
    lockTranslate(L_frontBallFkCtrl[0])

    # left front toe
    L_frontToeFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='l_frontToeFK_CTRL')
    L_frontToeFkCtrl_GRP = cmds.group(L_frontToeFkCtrl, n='l_frontToeFkCtrl_GRP')
    constr = cmds.pointConstraint(frontToeLoc, L_frontToeFkCtrl_GRP)
    cmds.delete(constr)
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(L_frontToeFkCtrl, L_frontToeJntFK, mo=True)
    lockScale(L_frontToeFkCtrl[0])
    lockTranslate(L_frontToeFkCtrl[0])

    # parent all front left FK ctrl GRPS
    cmds.parent(L_frontLowerFkCtrl_GRP, L_frontUpperFkCtrl[0])  # child/parent
    cmds.parent(L_frontAnkleFkCtrl_GRP, L_frontLowerFkCtrl[0])  # child/parent
    cmds.parent(L_frontBallFkCtrl_GRP, L_frontAnkleFkCtrl[0])  # child/parent
    cmds.parent(L_frontToeFkCtrl_GRP, L_frontBallFkCtrl[0])  # child/parent

    # right front fk ctrl
    # right front upper
    R_frontUpperFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_frontUpperFK_CTRL')
    R_frontUpperFkCtrl_GRP = cmds.group(R_frontUpperFkCtrl, n='r_frontUpperFkCtrl_GRP')
    constr = cmds.pointConstraint(frontUpperLoc, R_frontUpperFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_frontUpperFkCtrl_GRP + '.tx', -(cmds.getAttr(R_frontUpperFkCtrl_GRP + '.tx')))

    # set scale
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    cmds.parentConstraint(R_frontUpperFkCtrl, R_frontUpperJntFK, mo=True)

    #now parent the group of upper so that our fk curves/joints follow root
    #this is Daniel's code
    cmds.parentConstraint(frontPelvisJnt, R_frontUpperFkCtrl_GRP, mo=True, n="c_fkFollowRoot")



    lockScale(R_frontUpperFkCtrl[0])
    lockTranslate(R_frontUpperFkCtrl[0])

    # right front lower
    R_frontLowerFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_frontLowerFK_CTRL')
    R_frontLowerFkCtrl_GRP = cmds.group(R_frontLowerFkCtrl, n='r_frontLowerFkCtrl_GRP')
    constr = cmds.pointConstraint(frontLowerLoc, R_frontLowerFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_frontLowerFkCtrl_GRP + '.tx', -(cmds.getAttr(R_frontLowerFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_frontLowerFkCtrl, R_frontLowerJntFK, mo=True)
    lockScale(R_frontLowerFkCtrl[0])
    lockTranslate(R_frontLowerFkCtrl[0])

    # right front ankle
    R_frontAnkleFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_frontAnkleFK_CTRL')
    R_frontAnkleFkCtrl_GRP = cmds.group(R_frontAnkleFkCtrl, n='r_frontAnkleFkCtrl_GRP')
    constr = cmds.pointConstraint(frontAnkleLoc, R_frontAnkleFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_frontAnkleFkCtrl_GRP + '.tx', -(cmds.getAttr(R_frontAnkleFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_frontAnkleFkCtrl, R_frontAnkleJntFK, mo=True)
    lockScale(R_frontAnkleFkCtrl[0])
    lockTranslate(R_frontAnkleFkCtrl[0])

    # right front ball
    R_frontBallFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_frontBallFK_CTRL')
    R_frontBallFkCtrl_GRP = cmds.group(R_frontBallFkCtrl, n='r_frontBallFkCtrl_GRP')
    constr = cmds.pointConstraint(frontBallLoc, R_frontBallFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group to other side
    cmds.setAttr(R_frontBallFkCtrl_GRP + '.tx', -(cmds.getAttr(R_frontBallFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_frontBallFkCtrl, R_frontBallJntFK, mo=True)
    lockScale(R_frontBallFkCtrl[0])
    lockTranslate(R_frontBallFkCtrl[0])

    # right front toe
    R_frontToeFkCtrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), n='r_frontToeFK_CTRL')
    R_frontToeFkCtrl_GRP = cmds.group(R_frontToeFkCtrl, n='r_frontToeFkCtrl_GRP')
    constr = cmds.pointConstraint(frontToeLoc, R_frontToeFkCtrl_GRP)
    cmds.delete(constr)

    # mirror the group x axis  to other side
    cmds.setAttr(R_frontToeFkCtrl_GRP + '.tx', -(cmds.getAttr(R_frontToeFkCtrl_GRP + '.tx')))

    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.parentConstraint(R_frontToeFkCtrl, R_frontToeJntFK, mo=True)
    lockScale(R_frontToeFkCtrl[0])
    lockTranslate(R_frontToeFkCtrl[0])

    # parent all front right FK ctrl GRPS
    cmds.parent(R_frontLowerFkCtrl_GRP, R_frontUpperFkCtrl[0])  # child/parent
    cmds.parent(R_frontAnkleFkCtrl_GRP, R_frontLowerFkCtrl[0])  # child/parent
    cmds.parent(R_frontBallFkCtrl_GRP, R_frontAnkleFkCtrl[0])  # child/parent
    cmds.parent(R_frontToeFkCtrl_GRP, R_frontBallFkCtrl[0])  # child/parent

    # parent's color applies to all chidlren
    redColor(R_frontUpperFkCtrl_GRP)

    # group fk groups
    FKCtrlGrp = cmds.group(R_frontUpperFkCtrl_GRP, L_frontUpperFkCtrl_GRP, R_backUpperFkCtrl_GRP, L_backUpperFkCtrl_GRP,
                           n='c_fkCtrl_GRP')


def IKFKSwitch():
    '''IK FK switch'''
    global IkFkBackReverseNode
    global IkFkFrontReverseNode
    global legSwitchCtrlGrp
    # Back
    # L back leg switch...
    L_backIKFKSwitchCtrl = cmds.curve(d=1, p=[(0, 0, -0.5), (0, -0.5, 0), (0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0),
                                              (0.5, 0, 0), (0, 0, 0.5), (0, -0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                              (-0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                              (0, 0.5, 0), (0.5, 0, 0), (0, 0, 0.5), (0, 0.5, 0), (0.5, 0, 0),
                                              (0, 0, -0.5), (0, 0.5, 0)], n='l_backSwitch_CTRL')
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True)
    lockScale(L_backIKFKSwitchCtrl)
    lockTranslate(L_backIKFKSwitchCtrl)
    lockRotate(L_backIKFKSwitchCtrl)

    # group it so we can move the curve ctrl
    L_backIKFKSwitchCtrlGRP = cmds.group(n='l_backIKFKSwitchCtrl_GRP')
    constr = cmds.pointConstraint(L_backBallJnt, L_backIKFKSwitchCtrlGRP)
    cmds.delete(constr)
    dist = cmds.getAttr(L_backIKFKSwitchCtrlGRP + '.tz')
    cmds.setAttr(L_backIKFKSwitchCtrlGRP + '.tz', dist - ctrlSize)

    # we want our group to follow the joint now that we have it in desired location
    constr = cmds.pointConstraint(L_backBallJnt, L_backIKFKSwitchCtrlGRP, mo=True)
    blueColor(L_backIKFKSwitchCtrl)
    cmds.addAttr(L_backIKFKSwitchCtrl, longName='Leg_functions', at='enum', en='___', k=True)
    cmds.setAttr(L_backIKFKSwitchCtrl + '.Leg_functions', l=True)  # locking attribute we just added
    cmds.addAttr(L_backIKFKSwitchCtrl, longName='IK_FK', at='float', dv=1, min=0, max=1, k=True)

    # R back leg switch...
    R_backIKFKSwitchCtrl = cmds.curve(d=1, p=[(0, 0, -0.5), (0, -0.5, 0), (0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0),
                                              (0.5, 0, 0), (0, 0, 0.5), (0, -0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                              (-0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                              (0, 0.5, 0), (0.5, 0, 0), (0, 0, 0.5), (0, 0.5, 0), (0.5, 0, 0),
                                              (0, 0, -0.5), (0, 0.5, 0)], n='r_backSwitch_CTRL')
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True)
    lockScale(R_backIKFKSwitchCtrl)
    lockTranslate(R_backIKFKSwitchCtrl)
    lockRotate(R_backIKFKSwitchCtrl)

    # group it so we can move the curve ctrl
    R_backIKFKSwitchCtrlGRP = cmds.group(n='r_backIKFKSwitchCtrl_GRP')
    constr = cmds.pointConstraint(R_backBallJnt, R_backIKFKSwitchCtrlGRP)
    cmds.delete(constr)
    dist = cmds.getAttr(R_backIKFKSwitchCtrlGRP + '.tz')
    cmds.setAttr(R_backIKFKSwitchCtrlGRP + '.tz', dist - ctrlSize)

    # we want our group to follow the joint now that we have it in desired location
    constr = cmds.pointConstraint(R_backBallJnt, R_backIKFKSwitchCtrlGRP, mo=True)
    blueColor(R_backIKFKSwitchCtrl)
    cmds.addAttr(R_backIKFKSwitchCtrl, longName='Leg_functions', at='enum', en='___', k=True)
    cmds.setAttr(R_backIKFKSwitchCtrl + '.Leg_functions', l=True)  # locking attribute we just added
    cmds.addAttr(R_backIKFKSwitchCtrl, longName='IK_FK', at='float', dv=1, min=0, max=1, k=True)


    #CONNECT SWITCH CTRLS TO VISIBILITIS
    # left back leg switcher (1 == ON)
    cmds.connectAttr(L_backIKFKSwitchCtrl + '.IK_FK', L_backIKCtlGrp + '.visibility')  # (attribute switcher , attribute switchee)
    cmds.connectAttr(L_backIKFKSwitchCtrl + '.IK_FK', L_backPoleGrp + '.visibility')  # (attribute switcher , attribute switchee)

    # right back leg switcher (1 == ON)
    cmds.connectAttr(R_backIKFKSwitchCtrl + '.IK_FK',R_backIKCtlGrp + '.visibility')  # (attribute switcher , attribute switchee)
    cmds.connectAttr(R_backIKFKSwitchCtrl + '.IK_FK',R_backPoleGrp + '.visibility')  # (attribute switcher , attribute switchee)

    # create our reverse node so we can reverse th on value to turn off fk ctrls
    IkFkBackReverseNode = cmds.createNode('reverse', n='IK_FK_backLeg_REV')

    # switch is now the driver of our reverseNode (driver, driven) if switch is 1 then our node output is 0   :::::::::   "1-input" since our input is 1 then 1-1 is = to 0
    cmds.connectAttr(L_backIKFKSwitchCtrl + '.IK_FK', IkFkBackReverseNode + '.ix')  # i=input :: x controls L side
    cmds.connectAttr(R_backIKFKSwitchCtrl + '.IK_FK', IkFkBackReverseNode + '.iy')  # i=input :: y controls R side

    # connect node output (driver, driven)

    # if switch is 1 then this output is 0
    # we want to connect this 0 to all FK groups
    cmds.connectAttr(IkFkBackReverseNode + '.ox', L_backUpperFkCtrl_GRP + '.visibility')
    cmds.connectAttr(IkFkBackReverseNode + '.oy', R_backUpperFkCtrl_GRP + '.visibility')




    # Front
    # L front leg switch...
    L_frontIKFKSwitchCtrl = cmds.curve(d=1, p=[(0, 0, -0.5), (0, -0.5, 0), (0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0),
                                               (0.5, 0, 0), (0, 0, 0.5), (0, -0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                               (-0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                               (0, 0.5, 0), (0.5, 0, 0), (0, 0, 0.5), (0, 0.5, 0), (0.5, 0, 0),
                                               (0, 0, -0.5), (0, 0.5, 0)], n='l_frontSwitch_CTRL')
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True)
    lockScale(L_frontIKFKSwitchCtrl)
    lockTranslate(L_frontIKFKSwitchCtrl)
    lockRotate(L_frontIKFKSwitchCtrl)
    # group it so we can move the curve ctrl
    L_frontIKFKSwitchCtrlGRP = cmds.group(n='l_frontIKFKSwitchCtrl_GRP')
    constr = cmds.pointConstraint(L_frontBallJnt, L_frontIKFKSwitchCtrlGRP)
    cmds.delete(constr)
    dist = cmds.getAttr(L_frontIKFKSwitchCtrlGRP + '.tz')
    cmds.setAttr(L_frontIKFKSwitchCtrlGRP + '.tz', dist - ctrlSize)
    # we want our group to follow the joint now that we have it in desired location
    constr = cmds.pointConstraint(L_frontBallJnt, L_frontIKFKSwitchCtrlGRP, mo=True)
    blueColor(L_frontIKFKSwitchCtrl)
    cmds.addAttr(L_frontIKFKSwitchCtrl, longName='Leg_functions', at='enum', en='___', k=True)
    cmds.setAttr(L_frontIKFKSwitchCtrl + '.Leg_functions', l=True)  # locking attribute we just added
    cmds.addAttr(L_frontIKFKSwitchCtrl, longName='IK_FK', at='float', dv=1, min=0, max=1, k=True)

    # R front leg switch...
    R_frontIKFKSwitchCtrl = cmds.curve(d=1, p=[(0, 0, -0.5), (0, -0.5, 0), (0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0),
                                               (0.5, 0, 0), (0, 0, 0.5), (0, -0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                               (-0.5, 0, 0), (0, 0, -0.5), (0, 0.5, 0), (-0.5, 0, 0), (0, 0, 0.5),
                                               (0, 0.5, 0), (0.5, 0, 0), (0, 0, 0.5), (0, 0.5, 0), (0.5, 0, 0),
                                               (0, 0, -0.5), (0, 0.5, 0)], n='r_frontSwitch_CTRL')
    cmds.scale(ctrlSize, ctrlSize, ctrlSize)
    cmds.makeIdentity(apply=True)
    lockScale(R_frontIKFKSwitchCtrl)
    lockTranslate(R_frontIKFKSwitchCtrl)
    lockRotate(R_frontIKFKSwitchCtrl)
    # group it so we can move the curve ctrl
    R_frontIKFKSwitchCtrlGRP = cmds.group(n='r_frontIKFKSwitchCtrl_GRP')
    constr = cmds.pointConstraint(R_frontBallJnt, R_frontIKFKSwitchCtrlGRP)
    cmds.delete(constr)
    dist = cmds.getAttr(R_frontIKFKSwitchCtrlGRP + '.tz')
    cmds.setAttr(R_frontIKFKSwitchCtrlGRP + '.tz', dist - ctrlSize)
    # we want our group to follow the joint now that we have it in desired location
    constr = cmds.pointConstraint(R_frontBallJnt, R_frontIKFKSwitchCtrlGRP, mo=True)
    blueColor(R_frontIKFKSwitchCtrl)
    cmds.addAttr(R_frontIKFKSwitchCtrl, longName='Leg_functions', at='enum', en='___', k=True)
    cmds.setAttr(R_frontIKFKSwitchCtrl + '.Leg_functions', l=True)  # locking attribute we just added
    cmds.addAttr(R_frontIKFKSwitchCtrl, longName='IK_FK', at='float', dv=1, min=0, max=1, k=True)

    # visibility of controller...

    # 1st connect swith to group visibility
    # connect ctrl to all ik groups

    # left front leg switcher (1 == ON)
    cmds.connectAttr(L_frontIKFKSwitchCtrl + '.IK_FK',
                     L_frontIKCtlGrp + '.visibility')  # (attribute switcher , attribute switchee)
    cmds.connectAttr(L_frontIKFKSwitchCtrl + '.IK_FK',L_frontPoleGrp + '.visibility')  # (attribute switcher , attribute switchee)

    # right front leg switcher (1 == ON)
    cmds.connectAttr(R_frontIKFKSwitchCtrl + '.IK_FK',
                     R_frontIKCtlGrp + '.visibility')  # (attribute switcher , attribute switchee)
    cmds.connectAttr(R_frontIKFKSwitchCtrl + '.IK_FK',
                     R_frontPoleGrp + '.visibility')  # (attribute switcher , attribute switchee)

    # create our reverse node so we can reverse th on value to turn off fk ctrls
    IkFkFrontReverseNode = cmds.createNode('reverse', n='IK_FK_frontLeg_REV')

    # switch is now the driver of our reverseNode (driver, driven) if switch is 1 then our node output is 0   :::::::::   "1-input" since our input is 1 then 1-1 is = to 0
    cmds.connectAttr(L_frontIKFKSwitchCtrl + '.IK_FK', IkFkFrontReverseNode + '.ix')  # i=input :: x controls L side
    cmds.connectAttr(R_frontIKFKSwitchCtrl + '.IK_FK', IkFkFrontReverseNode + '.iy')  # i=input :: y controls R side

    # connect node output (driver, driven)

    # if switch is 1 then this output is 0
    # we want to connect this 0 to all FK groups
    cmds.connectAttr(IkFkFrontReverseNode + '.ox', L_frontUpperFkCtrl_GRP + '.visibility')
    cmds.connectAttr(IkFkFrontReverseNode + '.oy', R_frontUpperFkCtrl_GRP + '.visibility')

    # lets group all of our switch groups
    legSwitchCtrlGrp =cmds.group(R_frontIKFKSwitchCtrlGRP, R_backIKFKSwitchCtrlGRP, L_frontIKFKSwitchCtrlGRP, L_backIKFKSwitchCtrlGRP,
               n='c_IkFk_SwitchCtrl_GRP')


def BlendIKFKRotation():


    '''blend IK FK joint influence'''
    # we need to define our left back joints lists
    skinJoints_LB = [L_backToeJnt, L_backBallJnt, L_backAnkleJnt, L_backLowerJnt, L_backUpperJnt]
    ikJoints_LB = [L_backToeJntIK, L_backBallJntIK, L_backAnkleIkJnt, L_backLowerJntIK, L_backUpperJntIK]
    fkJoints_LB = [L_backToeJntFK, L_backBallJntFK, L_backAnkleJntFK, L_backLowerJntFK, L_backUpperJntFK]
    master_LB = IkFkBackReverseNode + '.ox'  # x controls our left side and o is the output. output = 1 - input
    BlendJointsRotation(ikJoints_LB, fkJoints_LB, skinJoints_LB, master_LB)

    # we need to define our left front joints lists
    skinJoints_LF = [L_frontToeJnt, L_frontBallJnt, L_frontAnkleJnt, L_frontLowerJnt, L_frontUpperJnt]
    ikJoints_LF = [L_frontToeJntIK, L_frontBallJntIK, L_frontAnkleJntIK, L_frontLowerJntIK, L_frontUpperJntIK]
    fkJoints_LF = [L_frontToeJntFK, L_frontBallJntFK, L_frontAnkleJntFK, L_frontLowerJntFK, L_frontUpperJntFK]
    master_LF = IkFkFrontReverseNode + '.ox'  # x controls our left side and o is the output. output = 1 - input
    BlendJointsRotation(ikJoints_LF, fkJoints_LF, skinJoints_LF, master_LF)

    # we need to define our right back joints lists
    skinJoints_RB = [R_backToeJnt, R_backBallJnt, R_backAnkleJnt, R_backLowerJnt, R_backUpperJnt]
    ikJoints_RB  = [R_backToeJntIK, R_backBallJntIK, R_backAnkleJntIK, R_backLowerJntIK, R_backUpperJntIK]
    fkJoints_RB  = [R_backToeJntFK, R_backBallJntFK, R_backAnkleJntFK, R_backLowerJntFK, R_backUpperJntFK]
    master_RB  = IkFkBackReverseNode + '.oy'  # x controls our right side and o is the output. output = 1 - input
    BlendJointsRotation(ikJoints_RB, fkJoints_RB, skinJoints_RB, master_RB)

    # we need to define our right front joints lists
    skinJoints_RF = [R_frontToeJnt, R_frontBallJnt, R_frontAnkleJnt, R_frontLowerJnt, R_frontUpperJnt]
    ikJoints_RF = [R_frontToeJntIK, R_frontBallJntIK, R_frontAnkleJntIK, R_frontLowerJntIK, R_frontUpperJntIK]
    fkJoints_RF = [R_frontToeJntFK, R_frontBallJntFK, R_frontAnkleJntFK, R_frontLowerJntFK, R_frontUpperJntFK]
    master_RF = IkFkFrontReverseNode + '.oy'  # x controls our right side and o is the output. output = 1 - input
    BlendJointsRotation(ikJoints_RF, fkJoints_RF, skinJoints_RF, master_RF)

    # front upper joint  must be connected to translations...


def BlendIKFKTranslation():
    global skinJoints
    global ikJoints
    global fkJoints
    global master

    skinJoints_TLF = [L_frontUpperJnt]
    ikJoints_TLF = [L_frontUpperJntIK]
    fkJoints_TLF = [L_frontUpperJntFK]
    master_TLF = IkFkFrontReverseNode + '.ox'# x is our left side
    BlendJointsTranslate(ikJoints_TLF, fkJoints_TLF, skinJoints_TLF, master_TLF)

    skinJoints_TRF = [R_frontUpperJnt]
    ikJoints_TRF = [R_frontUpperJntIK]
    fkJoints_TRF = [R_frontUpperJntFK]
    master_TRF = IkFkFrontReverseNode + '.oy'# y is our right side
    BlendJointsTranslate(ikJoints_TRF, fkJoints_TRF, skinJoints_TRF, master_TRF)


def TailSetUp():
    global tailFKCtrl1
    global tailGrp
    global tailRootJnt
    global tailFKCtrl1Grp
    # step 17) create tail spline
    distNode = cmds.createNode('distanceDimShape', n='deleteWhenDone')
    tailStart = cmds.xform(tailStartLoc, q=True, ws=True, rp=True)
    tailEnd = cmds.xform(tailEndLoc, q=True, ws=True, rp=True)
    cmds.setAttr(distNode + '.startPoint', *(tailStart))
    cmds.setAttr(distNode + '.endPoint', *(tailEnd))
    distance = cmds.getAttr(distNode + '.distance')
    cmds.delete(cmds.listRelatives(distNode, p=True))  # select parent and delete grp+node

    # the amount of joints in our tail
    tailJntAmount = 3  # 5 total joints 0,1,2,3,4
    tailRootJnt = cmds.joint(n='c_tail5_JNT')  # using this later to select all joints in heirarchy
    while tailJntAmount > 0:
        tailJnt = cmds.joint(n='c_tail' + str(tailJntAmount) + '_JNT')
        tailJntAmount -= 1
    # select all joints
    cmds.select(tailRootJnt, hi=True)
    tailJointChain = cmds.ls(sl=True)  # select our list of joints

    # reinitialize jnt amount in tail
    tailJntAmount = 3
    distancePerJnt = distance / tailJntAmount

    for e in tailJointChain:
        cmds.setAttr(e + '.tz', -distancePerJnt)

    cmds.rename(tailJointChain[-1], tailJointChain[-1] + 'End')  # (target, name)
    constr = cmds.pointConstraint(tailStartLoc, tailRootJnt)

    # rotate joint to aim for the end of the chain...
    tempcon = cmds.aimConstraint(tailEndLoc, tailRootJnt, aimVector=(0, 0, -1))  # (pointToThis, object)
    rotation = cmds.getAttr(tailRootJnt + '.rx')
    cmds.delete(tempcon)
    cmds.parent(tailJointChain[1], w=True)
    cmds.setAttr(tailRootJnt + '.rx', 0)
    cmds.setAttr(tailRootJnt + '.ry', 0)
    cmds.setAttr(tailRootJnt + '.rz', 0)
    cmds.parent(tailJointChain[1], tailRootJnt)
    cmds.joint(e=True, zso=True, oj='xyz', secondaryAxisOrient='yup', ch=True)

    # create IK solver
    IkTailHandle = cmds.ikHandle(sol='ikSplineSolver', ns=4, n='c_tailSolver_IK', sj=tailRootJnt,
                                 ee=tailJointChain[-1] + 'End')
    IkHandleGrp = cmds.group(IkTailHandle[0], IkTailHandle[2],
                             n='c_IK_TailSystem_GRP')  # do not group effector's of ik handle [0]=ik :: [2]=curve1
    cmds.setAttr(IkHandleGrp + '.inheritsTransform', 0)
    cmds.rename(IkTailHandle[1], 'c_tailSolverEffector')
    cmds.rename(IkTailHandle[2], 'c_tailSolverCurve')

    # create clusters to control the cv points of curve
    cmds.select('c_tailSolverCurve.cv[1:2]')  # select cv 1 and 2
    tail_cluster1 = cmds.cluster(rel=True, n='tail_root_clstr')
    cmds.select('c_tailSolverCurve.cv[3:4]')  # select cv 3 and 4
    tail_cluster2 = cmds.cluster(rel=True, n='tail_mid_clstr')
    cmds.select('c_tailSolverCurve.cv[5:6]')  # select cv 5 and 6
    tail_cluster3 = cmds.cluster(rel=True, n='tail_end_clstr')

    # neutral cluster on the rig is on the root of the tail
    cmds.select('c_tailSolverCurve.cv[0]')  # select root cv
    tail_cluster4 = cmds.cluster(rel=True, n='c_neutral_clstr')

    clusterGrp1 = cmds.group(tail_cluster1, n='c_tail_cluster1_GRP')
    clusterGrp2 = cmds.group(tail_cluster2, n='c_tail_cluster2_GRP')
    clusterGrp3 = cmds.group(tail_cluster3, n='c_tail_cluster3_GRP')
    clusterGrp4 = cmds.group(tail_cluster4, n='c_tail_cluster4_GRP')

    cmds.parent(clusterGrp1, clusterGrp2, clusterGrp3, clusterGrp4, IkHandleGrp)

    # create the controller curves for the tail
    tailCtrl1 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_tailRoot_CTRL')
    tailCtrl1 = tailCtrl1[0]
    cmds.scale(distance / 4, distance / 4, distance / 4)
    cmds.makeIdentity(tailCtrl1, apply=True)
    lockScale(tailCtrl1)
    yellowColor(tailCtrl1)
    tailCtrl1Grp = cmds.group(tailCtrl1, n='c_tailRootCtrl_GRP')

    tailCtrl2 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_tailMid_CTRL')
    tailCtrl2 = tailCtrl2[0]
    cmds.scale(distance / 4, distance / 4, distance / 4)
    cmds.makeIdentity(tailCtrl2, apply=True)
    lockScale(tailCtrl2)
    yellowColor(tailCtrl2)
    tailCtrl2Grp = cmds.group(tailCtrl2, n='c_tailMidCtrl_GRP')

    tailCtrl3 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_tailPoint_CTRL')
    tailCtrl3 = tailCtrl3[0]
    cmds.scale(distance / 4, distance / 4, distance / 4)
    cmds.makeIdentity(tailCtrl3, apply=True)
    lockScale(tailCtrl3)
    yellowColor(tailCtrl3)
    tailCtrl3Grp = cmds.group(tailCtrl3, n='c_tailPointCtrl_GRP')

    # set ctrl grp rotation
    cmds.setAttr(tailCtrl1Grp + '.rx', rotation)
    cmds.setAttr(tailCtrl2Grp + '.rx', rotation)
    cmds.setAttr(tailCtrl3Grp + '.rx', rotation)

    # query pivot info of cluster
    clstrXform = cmds.xform(tail_cluster1[1], piv=True, q=True)
    cmds.setAttr(tailCtrl1Grp + '.tx', clstrXform[0])
    cmds.setAttr(tailCtrl1Grp + '.ty', clstrXform[1])
    cmds.setAttr(tailCtrl1Grp + '.tz', clstrXform[2])

    clstrXform = cmds.xform(tail_cluster2[1], piv=True, q=True)
    cmds.setAttr(tailCtrl2Grp + '.tx', clstrXform[0])
    cmds.setAttr(tailCtrl2Grp + '.ty', clstrXform[1])
    cmds.setAttr(tailCtrl2Grp + '.tz', clstrXform[2])

    clstrXform = cmds.xform(tail_cluster3[1], piv=True, q=True)
    cmds.setAttr(tailCtrl3Grp + '.tx', clstrXform[0])
    cmds.setAttr(tailCtrl3Grp + '.ty', clstrXform[1])
    cmds.setAttr(tailCtrl3Grp + '.tz', clstrXform[2])

    # parent constraint cluster to controller
    cmds.parentConstraint(tailCtrl1, tail_cluster1, mo=True, n='c_tailRoot_controller')  # (driver,driven)
    cmds.parentConstraint(tailCtrl2, tail_cluster2, mo=True, n='c_tailMid_controller')  # (driver,driven)
    cmds.parentConstraint(tailCtrl3, tail_cluster3, mo=True, n='c_tailPoint_controller')  # (driver,driven)
    #Daniel: don't forget to constraint the root cluster to the fk ctrler
    #cmds.parentConstraint(neckFKCtrl1, cluster3, mo=True, n='c_tailPoint_controller')  # (driver,driven)

    # tail FK controllers
    tailFKCtrl1 = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],n='c_tailFK_1_CTRL')
    cmds.scale(distance / 3, distance / 5, distance / 5)
    cmds.makeIdentity(tailFKCtrl1, apply=True)
    lockScale(tailFKCtrl1)
    tailFKCtrl1Grp = cmds.group(tailFKCtrl1, n='c_tailFKCtrl1Grp_GRP')

    tailFKCtrl2 = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],
                             n='c_tailFK_2_CTRL')
    cmds.scale(distance / 3, distance / 5, distance / 5)
    cmds.makeIdentity(tailFKCtrl2, apply=True)
    lockScale(tailFKCtrl2)
    tailFKCtrl2Grp = cmds.group(tailFKCtrl2, n='c_tailFKCtrl2Grp_GRP')

    # make sure this tail fk curve group  matches the correpsonding ik curve group
    rotation = cmds.getAttr(tailCtrl1Grp + '.rx')
    cmds.setAttr(tailFKCtrl1Grp + '.rx', rotation)
    cmds.setAttr(tailFKCtrl2Grp + '.rx', rotation)
    constr = cmds.pointConstraint(tailCtrl1, tailFKCtrl1Grp)
    cmds.delete(constr)
    constr = cmds.pointConstraint(tailCtrl2, tailFKCtrl2Grp)
    cmds.delete(constr)

    # need fk ctrl pivot to align to joints
    # get offset needed by querying the root joint and finding the offset needed
    coordinate = cmds.xform(tailStartLoc, ws=True, t=True, q=True)
    cmds.xform(tailFKCtrl1, piv=(coordinate),ws=True)  # just shifted the pivot out of center and into matching that of our root joint (using locator)

    cmds.parent(tailFKCtrl2Grp, tailFKCtrl1)
    cmds.parent(tailCtrl1Grp, tailFKCtrl1)
    cmds.parent(tailCtrl2Grp, tailFKCtrl2)
    cmds.parent(tailCtrl3Grp, tailFKCtrl2)

    # group the tail elements
    tailGrp = cmds.group(tailRootJnt, IkHandleGrp, tailFKCtrl1Grp, n='c_tailRig_GRP')
    cmds.setAttr(IkHandleGrp + '.visibility', 0)

    #parentConstraint the neutral cluster to allow the tail to follow the parent group and enable scaling
    cmds.parentConstraint(tailFKCtrl1, tail_cluster4, mo=True)

    # adding tail twist from the end ik ctrl
    mult = cmds.shadingNode('multiplyDivide', asUtility=True, n='c_tailTwist_reverseValueRotation_Multiply')
    cmds.setAttr(mult + '.input2X', -1)
    cmds.connectAttr(tailCtrl3 + '.rz', mult + '.input1X')
    cmds.connectAttr(mult + '.outputX', IkTailHandle[0] + '.twist')


def SpineSetUp():
    global spineMasterCtrl
    global spineGrp
    global spineMasterCtrlGrp
    global spineRootJnt
    global spineCtrl1
    global spineFKCtrl1
    global spineJointChain
    global spineCtrl3

    distNode = cmds.createNode('distanceDimShape', n='deleteWhenDone')
    spineStart = cmds.xform(backPelvisLoc, q=True, ws=True, rp=True)
    spineEnd = cmds.xform(frontPelvisLoc, q=True, ws=True, rp=True)
    cmds.setAttr(distNode + '.startPoint', *(spineStart))
    cmds.setAttr(distNode + '.endPoint', *(spineEnd))
    distance = cmds.getAttr(distNode + '.distance')
    cmds.delete(cmds.listRelatives(distNode, p=True))  # select parent and delete grp+node

    # the amount of joints in our spine
    spineJntAmount = 4  # 5 total joints 0,1,2,3,4
    spineRootJnt = cmds.joint(n='c_spine10_JNT')  # using this later to select all joints in heirarchy

    while spineJntAmount > 0:
        spineJnt = cmds.joint(n='c_spine' + str(spineJntAmount) + '_JNT')
        spineJntAmount -= 1

    # select all joints
    cmds.select(spineRootJnt, hi=True)
    spineJointChain = cmds.ls(sl=True)  # select our list of joints

    # reinitialize jnt amount in spine
    spineJntAmount = 4
    distancePerJnt = distance / spineJntAmount

    for e in spineJointChain:
        cmds.setAttr(e + '.tz', -distancePerJnt)

    cmds.rename(spineJointChain[-1], spineJointChain[-1] + 'End')  # (target, name)
    constr = cmds.pointConstraint(frontPelvisLoc, spineJointChain[0])

    # rotate joint to aim for the end of the chain...
    tempcon = cmds.aimConstraint(backPelvisLoc, spineRootJnt, aimVector=(0, 0, -1))  # (pointToThis, object)
    rotation = cmds.getAttr(spineRootJnt + '.rx')
    cmds.delete(tempcon)
    cmds.parent(spineJointChain[1], w=True)
    cmds.setAttr(spineRootJnt + '.rx', 0)
    cmds.setAttr(spineRootJnt + '.ry', 0)
    cmds.setAttr(spineRootJnt + '.rz', 0)
    cmds.parent(spineJointChain[1], spineRootJnt)
    cmds.joint(e=True, zso=True, oj='xyz', secondaryAxisOrient='yup', ch=True)

    # create IK solver
    IkSpineHandle = cmds.ikHandle(sol='ikSplineSolver', ns=4, n='c_spineSolver_IK', sj=spineRootJnt,
                                  ee=spineJointChain[-1] + 'End')
    IkSpineHandleGrp = cmds.group(IkSpineHandle[0], IkSpineHandle[2],
                             n='c_IK_SpineSystem_GRP')  # do not group effector's of ik handle [0]=ik :: [2]=curve1
    cmds.setAttr(IkSpineHandleGrp + '.inheritsTransform', 0)
    cmds.rename(IkSpineHandle[1], 'c_spineSolverEffector')
    cmds.rename(IkSpineHandle[2], 'c_spineSolverCurve')

    # create clusters to control the cv points of curve
    cmds.select('c_spineSolverCurve.cv[1:2]')  # select cv 1 and 2
    cluster1 = cmds.cluster(rel=True, n='spine_root_clstr')
    cmds.select('c_spineSolverCurve.cv[3:4]')  # select cv 3 and 4
    cluster2 = cmds.cluster(rel=True, n='spine_mid_clstr')
    cmds.select('c_spineSolverCurve.cv[5:6]')  # select cv 5 and 6
    cluster3 = cmds.cluster(rel=True, n='spine_end_clstr')

    # neutral cluster on the rig is on the root of the spine
    cmds.select('c_spineSolverCurve.cv[0]')  # select root cv
    cluster4 = cmds.cluster(rel=True, n='c_neutral_clstr')

    clusterGrp1 = cmds.group(cluster1, n='c_cluster1_GRP')
    clusterGrp2 = cmds.group(cluster2, n='c_cluster2_GRP')
    clusterGrp3 = cmds.group(cluster3, n='c_cluster3_GRP')
    clusterGrp4 = cmds.group(cluster4, n='c_cluster4_GRP')

    cmds.parent(clusterGrp1, clusterGrp2, clusterGrp3, clusterGrp4, IkSpineHandleGrp)

    # create the controller curves for the spine
    spineCtrl1 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_spineRoot_CTRL')
    spineCtrl1 = spineCtrl1[0]
    cmds.scale(distance / 4, distance / 4, distance / 4)
    cmds.makeIdentity(spineCtrl1, apply=True)
    lockScale(spineCtrl1)
    yellowColor(spineCtrl1)
    spineCtrl1Grp = cmds.group(spineCtrl1, n='c_spineRootCtrl_GRP')

    spineCtrl2 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_spineMid_CTRL')
    spineCtrl2 = spineCtrl2[0]
    cmds.scale(distance / 4, distance / 4, distance / 4)
    cmds.makeIdentity(spineCtrl2, apply=True)
    lockScale(spineCtrl2)
    yellowColor(spineCtrl2)
    spineCtrl2Grp = cmds.group(spineCtrl2, n='c_spineMidCtrl_GRP')

    spineCtrl3 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_spinePoint_CTRL')
    spineCtrl3 = spineCtrl3[0]
    cmds.scale(distance / 4, distance / 4, distance / 4)
    cmds.makeIdentity(spineCtrl3, apply=True)
    lockScale(spineCtrl3)
    yellowColor(spineCtrl3)
    spineCtrl3Grp = cmds.group(spineCtrl3, n='c_spinePointCtrl_GRP')

    # set ctrl grp rotation
    cmds.setAttr(spineCtrl1Grp + '.rx', rotation)
    cmds.setAttr(spineCtrl2Grp + '.rx', rotation)
    cmds.setAttr(spineCtrl3Grp + '.rx', rotation)

    # query pivot info of cluster
    clstrXform = cmds.xform(cluster1[1], piv=True, q=True)
    cmds.setAttr(spineCtrl1Grp + '.tx', clstrXform[0])
    cmds.setAttr(spineCtrl1Grp + '.ty', clstrXform[1])
    cmds.setAttr(spineCtrl1Grp + '.tz', clstrXform[2])

    clstrXform = cmds.xform(cluster2[1], piv=True, q=True)
    cmds.setAttr(spineCtrl2Grp + '.tx', clstrXform[0])
    cmds.setAttr(spineCtrl2Grp + '.ty', clstrXform[1])
    cmds.setAttr(spineCtrl2Grp + '.tz', clstrXform[2])

    clstrXform = cmds.xform(cluster3[1], piv=True, q=True)
    cmds.setAttr(spineCtrl3Grp + '.tx', clstrXform[0])
    cmds.setAttr(spineCtrl3Grp + '.ty', clstrXform[1])
    cmds.setAttr(spineCtrl3Grp + '.tz', clstrXform[2])

    # parent constraint cluster to controller
    cmds.parentConstraint(spineCtrl1, cluster1, mo=True, n='c_spineRoot_controller')  # (driver,driven)
    cmds.parentConstraint(spineCtrl2, cluster2, mo=True, n='c_spineMid_controller')  # (driver,driven)
    cmds.parentConstraint(spineCtrl3, cluster3, mo=True, n='c_spinePoint_controller')  # (driver,driven)

    # spine FK controllers
    spineFKCtrl1 = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],
                              n='c_spineFK_1_CTRL')
    cmds.scale(distance / 3, distance / 2, distance / 5)
    cmds.makeIdentity(spineFKCtrl1, apply=True)
    lockScale(spineFKCtrl1)
    spineFKCtrl1Grp = cmds.group(spineFKCtrl1, n='c_spineFKCtrl1Grp_GRP')

    spineFKCtrl2 = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],
                              n='c_spineFK_2_CTRL')
    cmds.scale(distance / 3, distance / 2, distance / 5)
    cmds.makeIdentity(spineFKCtrl2, apply=True)
    lockScale(spineFKCtrl2)
    spineFKCtrl2Grp = cmds.group(spineFKCtrl2, n='c_spineFKCtrl2Grp_GRP')

    # make sure this spine fk curve group  matches the correpsonding ik curve group
    rotation = cmds.getAttr(spineCtrl1Grp + '.rx')
    cmds.setAttr(spineFKCtrl1 + '.rx', rotation)
    cmds.setAttr(spineFKCtrl2 + '.rx', rotation)
    constr = cmds.pointConstraint(spineCtrl1, spineFKCtrl1Grp)
    cmds.delete(constr)
    constr = cmds.pointConstraint(spineCtrl2, spineFKCtrl2Grp)
    cmds.delete(constr)

    # connect spine end to back Jnt
    cmds.parentConstraint(spineCtrl1, spineCtrl2Grp, mo=True)
    cmds.parentConstraint(spineCtrl3, spineCtrl2Grp, mo=True)
    cmds.parentConstraint(spineCtrl1, frontPelvisJnt, mo=True)
    cmds.parentConstraint(spineCtrl3, backPelvisJnt, mo=True)
    cmds.parentConstraint(spineCtrl3, tailFKCtrl1Grp, mo=True)

    # create a spine master controller
    spineMasterCtrl = cmds.curve(d=1, p=[(0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5),
                                         (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5),
                                         (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5),
                                         (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                                         (0.5, 0.5, -0.5)],
                                 k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], n='c_spineMaster_CTRL')
    cmds.scale(distance / 4, distance / 4, distance / .8)
    cmds.makeIdentity(apply=True)
    spineMasterCtrlGrp = cmds.group(n='c_spineMasterCtrl_GRP')
    constr = cmds.pointConstraint(spineFKCtrl2, spineMasterCtrlGrp)
    cmds.delete(constr)
    # get the distance the group moved due to constr and multiply that
    dist = cmds.getAttr(spineMasterCtrlGrp + '.ty')
    cmds.setAttr(spineMasterCtrlGrp + '.ty', dist * 1.5)

    # parent the fk ctrls for the spine properly
    cmds.parent(spineFKCtrl2Grp, spineFKCtrl1)
    cmds.parent(spineCtrl1Grp, spineFKCtrl1)
    cmds.parent(spineCtrl2Grp, spineFKCtrl2)
    cmds.parent(spineCtrl3Grp, spineFKCtrl2)
    cmds.parentConstraint(spineCtrl1, cluster4, mo=True)

    cmds.parent(frontPelvisJnt, subworld)
    spineGrp=cmds.group(spineRootJnt,spineMasterCtrlGrp,spineFKCtrl1Grp,IkSpineHandleGrp,n= 'c_spineRig_GRP')


def NeckSetUp():
    global neckGrp
    global neckRootJnt
    global neckFKCtrl1

    global neck_cluster1
    global neck_cluster2
    global neck_cluster3
    global neck_cluster4
    global headCtrl1Grp
    global neckFKCtrl2



    '''creating neck setup'''
    distNode = cmds.createNode('distanceDimShape', n='deleteWhenDone')
    neckStart = cmds.xform(neckRootLoc, q=True, ws=True, rp=True)
    neckEnd = cmds.xform(neckEndLoc, q=True, ws=True, rp=True)
    cmds.setAttr(distNode + '.startPoint', *(neckStart))
    cmds.setAttr(distNode + '.endPoint', *(neckEnd))
    distance = cmds.getAttr(distNode + '.distance')
    cmds.delete(cmds.listRelatives(distNode, p=True))  # select parent and delete grp+node

    # the amount of joints in our neck
    neckJntAmount = 3  # 5 total joints 0,1,2,3,4
    neckRootJnt = cmds.joint(n='c_neck10_JNT')  # using this later to select all joints in heirarchy

    while neckJntAmount > 0:
        neckJnt = cmds.joint(n='c_neck' + str(neckJntAmount) + '_JNT')
        neckJntAmount -= 1

    # select all joints
    cmds.select(neckRootJnt, hi=True)
    neckJointChain = cmds.ls(sl=True)  # select our list of joints

    # reinitialize jnt amount in neck
    neckJntAmount = 3
    distancePerJnt = distance / neckJntAmount

    for e in neckJointChain:
        cmds.setAttr(e + '.tz', distancePerJnt)

    cmds.rename(neckJointChain[-1], neckJointChain[-1] + 'End')  # (target, name)
    constr = cmds.pointConstraint(neckRootLoc, neckJointChain[0])

    # rotate joint to aim for the end of the chain...
    tempcon = cmds.aimConstraint(neckEndLoc, neckRootJnt, aimVector=(0, 0, 1))  # (pointToThis, object)
    rotation = cmds.getAttr(neckRootJnt + '.rx')
    cmds.delete(tempcon)
    cmds.parent(neckJointChain[1], w=True)
    cmds.setAttr(neckRootJnt + '.rx', 0)
    cmds.setAttr(neckRootJnt + '.ry', 0)
    cmds.setAttr(neckRootJnt + '.rz', 0)
    cmds.parent(neckJointChain[1], neckRootJnt)
    cmds.joint(e=True, zso=True, oj='xyz', secondaryAxisOrient='yup', ch=True)

    # create IK solver
    IkNeckHandle = cmds.ikHandle(sol='ikSplineSolver', ns=4, n='c_neckSolver_IK', sj=neckRootJnt,
                                 ee=neckJointChain[-1] + 'End')
    IkNeckHandleGrp = cmds.group(IkNeckHandle[0], IkNeckHandle[2],
                                 n='c_IK_NeckSystem_GRP')  # do not group effector's of ik handle [0]=ik :: [2]=curve1
    cmds.setAttr(IkNeckHandleGrp + '.inheritsTransform', 0)
    cmds.rename(IkNeckHandle[1], 'c_neckSolverEffector')
    cmds.rename(IkNeckHandle[2], 'c_neckSolverCurve')

    # create clusters to control the cv points of curve
    cmds.select('c_neckSolverCurve.cv[1:2]')  # select cv 1 and 2
    neck_cluster1 = cmds.cluster(rel=True, n='neck_root_clstr')
    cmds.select('c_neckSolverCurve.cv[3:4]')  # select cv 3 and 4
    neck_cluster2 = cmds.cluster(rel=True, n='neck_mid_clstr')
    cmds.select('c_neckSolverCurve.cv[5:6]')  # select cv 5 and 6
    neck_cluster3 = cmds.cluster(rel=True, n='neck_end_clstr')

    # neutral cluster on the rig is on the root of the neck
    cmds.select('c_neckSolverCurve.cv[0]')  # select root cv
    neck_cluster4 = cmds.cluster(rel=True, n='c_neutral_clstr')

    clusterGrp1 = cmds.group(neck_cluster1, n='c_neck_cluster1_GRP')
    clusterGrp2 = cmds.group(neck_cluster2, n='c_neck_cluster2_GRP')
    clusterGrp3 = cmds.group(neck_cluster3, n='c_neck_cluster3_GRP')
    clusterGrp4 = cmds.group(neck_cluster4, n='c_neck_cluster4_GRP')

    cmds.parent(clusterGrp1, clusterGrp2, clusterGrp3, clusterGrp4, IkNeckHandleGrp)

    # create the controller curves for the neck
    neckCtrl1 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_neckRoot_CTRL')
    neckCtrl1 = neckCtrl1[0]
    cmds.scale(distance / 1.5, distance / 1.5, distance / 1.5)
    cmds.makeIdentity(neckCtrl1, apply=True)
    lockScale(neckCtrl1)
    yellowColor(neckCtrl1)
    neckCtrl1Grp = cmds.group(neckCtrl1, n='c_neckRootCtrl_GRP')

    neckCtrl2 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_neckMid_CTRL')
    neckCtrl2 = neckCtrl2[0]
    cmds.scale(distance / 2, distance / 2, distance / 2)
    cmds.makeIdentity(neckCtrl2, apply=True)
    lockScale(neckCtrl2)
    yellowColor(neckCtrl2)
    neckCtrl2Grp = cmds.group(neckCtrl2, n='c_neckMidCtrl_GRP')

    neckCtrl3 = cmds.circle(nr=(0, 0, 1), c=(0, 0, 0), n='c_neckPoint_CTRL')
    neckCtrl3 = neckCtrl3[0]
    cmds.scale(distance / 2, distance / 2, distance / 2)
    cmds.makeIdentity(neckCtrl3, apply=True)
    lockScale(neckCtrl3)
    yellowColor(neckCtrl3)
    neckCtrl3Grp = cmds.group(neckCtrl3, n='c_neckPointCtrl_GRP')









    # set ctrl grp rotation
    cmds.setAttr(neckCtrl1Grp + '.rx', rotation)
    cmds.setAttr(neckCtrl2Grp + '.rx', rotation)
    cmds.setAttr(neckCtrl3Grp + '.rx', rotation)

    # query pivot info of cluster
    clstrXform = cmds.xform(neck_cluster1[1], piv=True, q=True)
    cmds.setAttr(neckCtrl1Grp + '.tx', clstrXform[0])
    cmds.setAttr(neckCtrl1Grp + '.ty', clstrXform[1])
    cmds.setAttr(neckCtrl1Grp + '.tz', clstrXform[2])

    clstrXform = cmds.xform(neck_cluster2[1], piv=True, q=True)
    cmds.setAttr(neckCtrl2Grp + '.tx', clstrXform[0])
    cmds.setAttr(neckCtrl2Grp + '.ty', clstrXform[1])
    cmds.setAttr(neckCtrl2Grp + '.tz', clstrXform[2])

    clstrXform = cmds.xform(neck_cluster3[1], piv=True, q=True)
    cmds.setAttr(neckCtrl3Grp + '.tx', clstrXform[0])
    cmds.setAttr(neckCtrl3Grp + '.ty', clstrXform[1])
    cmds.setAttr(neckCtrl3Grp + '.tz', clstrXform[2])

    # parent constraint cluster to controller
    cmds.parentConstraint(neckCtrl1, neck_cluster1, mo=True, n='c_neckRoot_controller')  # (driver,driven)
    cmds.parentConstraint(neckCtrl2, neck_cluster2, mo=True, n='c_neckMid_controller')  # (driver,driven)
    cmds.parentConstraint(neckCtrl3, neck_cluster3, mo=True, n='c_neckPoint_controller')  # (driver,driven)

    # neck FK controllers
    neckFKCtrl1 = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],
                             n='c_neckFK_1_CTRL')
    cmds.scale(distance / 1.5, distance / 4, distance / 5)
    cmds.makeIdentity(neckFKCtrl1, apply=True)
    lockScale(neckFKCtrl1)
    neckFKCtrl1Grp = cmds.group(neckFKCtrl1, n='c_neckFKCtrl1Grp_GRP')

    neckFKCtrl2 = cmds.curve(d=1, p=[(1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)], k=[0, 1, 2, 3, 4],
                             n='c_neckFK_2_CTRL')
    cmds.scale(distance / 1.5, distance / 4, distance / 5)
    cmds.makeIdentity(neckFKCtrl2, apply=True)
    lockScale(neckFKCtrl2)
    neckFKCtrl2Grp = cmds.group(neckFKCtrl2, n='c_neckFKCtrl2Grp_GRP')


    #JNT
    cmds.select(d=True)
    headJnt = cmds.joint(n='head_JNT')
    constr = cmds.pointConstraint(headLoc,headJnt)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)
    cmds.parent(headJnt,'c_neck1_JNTEnd')
    cmds.select(d=True)  # deselect the jnt
    #CTRL
    headCtrl1 = cmds.curve(d=1, p=[(0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5),
                                         (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5),
                                         (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5),
                                         (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
                                         (0.5, 0.5, -0.5)],k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], n='c_head_CTRL')
    cmds.scale(10, 10, 10)
    cmds.makeIdentity(headCtrl1, apply=True)
    yellowColor(headCtrl1)
    headCtrl1Grp = cmds.group(headCtrl1, n='c_headCtrl_GRP')
    #align ctrl to joint
    constr = cmds.pointConstraint('c_neck1_JNTEnd',headCtrl1Grp)  # store a pointer to the contraint we created so that we can easily delete
    cmds.delete(constr)

    #connect ctrl to jnt
    cmds.orientConstraint(headCtrl1,'c_neck1_JNTEnd',mo=True,weight=1)
    cmds.select(d=True)




    # make sure this neck fk curve group  matches the correpsonding ik curve group
    rotation = cmds.getAttr(neckCtrl1Grp + '.rx')
    cmds.setAttr(neckFKCtrl1Grp + '.rx', rotation)
    cmds.setAttr(neckFKCtrl2Grp + '.rx', rotation)
    constr = cmds.pointConstraint(neckCtrl1, neckFKCtrl1Grp)
    cmds.delete(constr)
    constr = cmds.pointConstraint(neckCtrl2, neckFKCtrl2Grp)
    cmds.delete(constr)

    cmds.setAttr(IkNeckHandleGrp + '.visibility', 0)

    #Daniel Daniel: parentConstraint the neutral cluster to allow the tail to follow the parent group and enable scaling
    cmds.pointConstraint(neckFKCtrl1, neck_cluster4) #(driver, driven)

    #lets make sure the neck follows the torso
    cmds.parentConstraint(spineFKCtrl1,neckFKCtrl1Grp, mo=True) #(driver, driven)

    # change root fk ctrl pivot so that it matches our root joint
    coordinate = cmds.xform(neckRootLoc, ws=True, t=True, q=True)
    cmds.xform(neckFKCtrl1, piv=(coordinate),
               ws=True)  # just shifted the pivot out of center and into matching that of our root joint (using locator)

    cmds.parent(neckFKCtrl2Grp, neckFKCtrl1)
    cmds.parent(neckCtrl1Grp, neckFKCtrl1)
    cmds.parent(neckCtrl2Grp, neckFKCtrl2)
    cmds.parent(neckCtrl3Grp, neckFKCtrl2)


    neckGrp = cmds.group(neckRootJnt, IkNeckHandleGrp, neckFKCtrl1Grp, n='c_neckRig_GRP')


def FootRoll():
    global rollJntGrp
    '''creating foot roll setup'''

    # BACK L
    # creating foot roll for L back foot
    lb_AnkleRotateJnt = cmds.joint(n='l_backAnkleRotate_JNT')
    lb_HeelRollJnt = cmds.joint(n='l_backHeelRoll_JNT')
    lb_BallRollJnt = cmds.joint(n='l_backBallRoll_JNT')
    lb_AnkleRollJnt = cmds.joint(n='l_backAnkleRoll_JNT')

    constr = cmds.pointConstraint(L_backBallJnt, lb_AnkleRotateJnt)
    cmds.delete(constr)
    constr = cmds.pointConstraint(L_backToeJnt, lb_HeelRollJnt)
    cmds.delete(constr)
    cmds.setAttr(lb_HeelRollJnt + '.tz', 0)
    constr = cmds.pointConstraint(L_backToeJnt, lb_BallRollJnt)
    cmds.delete(constr)
    constr = cmds.pointConstraint(L_backBallJnt, lb_AnkleRollJnt)
    cmds.delete(constr)

    cmds.parent(L_backAnkleIK[0], lb_BallRollJnt)  # {child / parent}
    cmds.parent(L_backToeIK[0], lb_BallRollJnt)
    cord = cmds.xform(lb_AnkleRotateJnt, ws=True, t=True, q=True)
    cmds.xform(L_backIKCtl, piv=(cord), ws=True)

    lb_HeelCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='l_backHeel_CTRL')
    lb_HeelCtrlGrp = cmds.group(n='l_backHeelCtrl_GRP')
    constr = cmds.pointConstraint(lb_HeelRollJnt, lb_HeelCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    lb_ToeTipCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='l_backToeTip_CTRL')
    lb_ToeTipCtrlGrp = cmds.group(n='l_backToeTipCtrl_GRP')
    constr = cmds.pointConstraint(lb_BallRollJnt, lb_ToeTipCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    cmds.parent(lb_ToeTipCtrlGrp, lb_HeelCtrl[0])
    cmds.parentConstraint(lb_HeelCtrl[0], lb_HeelRollJnt, mo=True)  # (driver,driven)
    cmds.parentConstraint(lb_ToeTipCtrl[0], lb_BallRollJnt, mo=True)  # (driver,driven)
    cmds.parent(lb_HeelCtrlGrp, L_backIKCtl)
    cmds.parentConstraint(L_backIKCtl, lb_AnkleRotateJnt, mo=True)
    cmds.setAttr(lb_AnkleRotateJnt + '.visibility', 0)
    cmds.select(d=True)

    # BACK R
    # creating foot roll for R back foot
    rb_AnkleRotateJnt = cmds.joint(n='r_backAnkleRotate_JNT')
    rb_HeelRollJnt = cmds.joint(n='r_backHeelRolr_JNT')
    rb_BallRollJnt = cmds.joint(n='r_backBallRolr_JNT')
    rb_AnkleRollJnt = cmds.joint(n='r_backAnkleRolr_JNT')

    constr = cmds.pointConstraint(R_backBallJnt, rb_AnkleRotateJnt)
    cmds.delete(constr)

    constr = cmds.pointConstraint(R_backToeJnt, rb_HeelRollJnt)
    cmds.delete(constr)

    cmds.setAttr(rb_HeelRollJnt + '.tz', 0)

    constr = cmds.pointConstraint(R_backToeJnt, rb_BallRollJnt)
    cmds.delete(constr)

    constr = cmds.pointConstraint(R_backBallJnt, rb_AnkleRollJnt)
    cmds.delete(constr)

    cmds.parent(R_backAnkleIK[0], rb_BallRollJnt)  # {child / parent}
    cmds.parent(R_backToeIK[0], rb_BallRollJnt)
    cord = cmds.xform(rb_AnkleRotateJnt, ws=True, t=True, q=True)
    cmds.xform(R_backIKCtl, piv=(cord), ws=True)

    rb_HeelCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='r_backHeer_CTRL')
    rb_HeelCtrlGrp = cmds.group(n='r_backHeelCtrr_GRP')
    constr = cmds.pointConstraint(rb_HeelRollJnt, rb_HeelCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    rb_ToeTipCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='r_backToeTip_CTRL')
    rb_ToeTipCtrlGrp = cmds.group(n='r_backToeTipCtrr_GRP')
    constr = cmds.pointConstraint(rb_BallRollJnt, rb_ToeTipCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    cmds.parent(rb_ToeTipCtrlGrp, rb_HeelCtrl[0])
    cmds.parentConstraint(rb_HeelCtrl[0], rb_HeelRollJnt, mo=True)  # (driver,driven)
    cmds.parentConstraint(rb_ToeTipCtrl[0], rb_BallRollJnt, mo=True)  # (driver,driven)
    cmds.parent(rb_HeelCtrlGrp, R_backIKCtl)
    cmds.parentConstraint(R_backIKCtl, rb_AnkleRotateJnt, mo=True)
    cmds.setAttr(rb_AnkleRotateJnt + '.visibility', 0)
    cmds.select(d=True)

    # FRONT L
    # creating foot roll for L front foot
    lf_AnkleRotateJnt = cmds.joint(n='l_frontAnkleRotate_JNT')
    lf_HeelRollJnt = cmds.joint(n='l_frontHeelRoll_JNT')
    lf_BallRollJnt = cmds.joint(n='l_frontBallRoll_JNT')
    lf_AnkleRollJnt = cmds.joint(n='l_frontAnkleRoll_JNT')

    constr = cmds.pointConstraint(L_frontBallJnt, lf_AnkleRotateJnt)
    cmds.delete(constr)

    constr = cmds.pointConstraint(L_frontToeJnt, lf_HeelRollJnt)
    cmds.delete(constr)

    cmds.setAttr(lf_HeelRollJnt + '.tz', 0)

    constr = cmds.pointConstraint(L_frontToeJnt, lf_BallRollJnt)
    cmds.delete(constr)

    constr = cmds.pointConstraint(L_frontBallJnt, lf_AnkleRollJnt)
    cmds.delete(constr)

    cmds.parent(L_frontAnkleIK[0], lf_BallRollJnt)  # {child / parent}
    cmds.parent(L_frontToeIK[0], lf_BallRollJnt)
    cord = cmds.xform(lf_AnkleRotateJnt, ws=True, t=True, q=True)
    cmds.xform(L_frontIKCtl, piv=(cord), ws=True)

    lf_HeelCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='l_frontHeel_CTRL')
    lf_HeelCtrlGrp = cmds.group(n='l_frontHeelCtrl_GRP')
    constr = cmds.pointConstraint(lf_HeelRollJnt, lf_HeelCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    lf_ToeTipCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='l_frontToeTip_CTRL')
    lf_ToeTipCtrlGrp = cmds.group(n='l_frontToeTipCtrl_GRP')
    constr = cmds.pointConstraint(lf_BallRollJnt, lf_ToeTipCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    cmds.parent(lf_ToeTipCtrlGrp, lf_HeelCtrl[0])
    cmds.parentConstraint(lf_HeelCtrl[0], lf_HeelRollJnt, mo=True)  # (driver,driven)
    cmds.parentConstraint(lf_ToeTipCtrl[0], lf_BallRollJnt, mo=True)  # (driver,driven)
    cmds.parent(lf_HeelCtrlGrp, L_frontIKCtl)
    cmds.parentConstraint(L_frontIKCtl, lf_AnkleRotateJnt, mo=True)
    cmds.setAttr(lf_AnkleRotateJnt + '.visibility', 0)
    cmds.select(d=True)

    # FRONT R
    # creating foot roll for R front foot
    rf_AnkleRotateJnt = cmds.joint(n='r_frontAnkleRotate_JNT')
    rf_HeelRollJnt = cmds.joint(n='r_frontHeelRolr_JNT')
    rf_BallRollJnt = cmds.joint(n='r_frontBallRolr_JNT')
    rf_AnkleRollJnt = cmds.joint(n='r_frontAnkleRolr_JNT')

    constr = cmds.pointConstraint(R_frontBallJnt, rf_AnkleRotateJnt)
    cmds.delete(constr)

    constr = cmds.pointConstraint(R_frontToeJnt, rf_HeelRollJnt)
    cmds.delete(constr)

    cmds.setAttr(rf_HeelRollJnt + '.tz', 0)

    constr = cmds.pointConstraint(R_frontToeJnt, rf_BallRollJnt)
    cmds.delete(constr)

    constr = cmds.pointConstraint(R_frontBallJnt, rf_AnkleRollJnt)
    cmds.delete(constr)

    cmds.parent(R_frontAnkleIK[0], rf_BallRollJnt)  # {child / parent}
    cmds.parent(R_frontToeIK[0], rf_BallRollJnt)
    cord = cmds.xform(rf_AnkleRotateJnt, ws=True, t=True, q=True)
    cmds.xform(R_frontIKCtl, piv=(cord), ws=True)

    rf_HeelCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='r_frontHeer_CTRL')
    rf_HeelCtrlGrp = cmds.group(n='r_frontHeelCtrr_GRP')
    constr = cmds.pointConstraint(rf_HeelRollJnt, rf_HeelCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    rf_ToeTipCtrl = cmds.circle(nr=(1, 0, 0), r=distance / 7, n='r_frontToeTip_CTRL')
    rf_ToeTipCtrlGrp = cmds.group(n='r_frontToeTipCtrr_GRP')
    constr = cmds.pointConstraint(rf_BallRollJnt, rf_ToeTipCtrlGrp)  # (target, moveThis)
    cmds.delete(constr)

    cmds.parent(rf_ToeTipCtrlGrp, rf_HeelCtrl[0])
    cmds.parentConstraint(rf_HeelCtrl[0], rf_HeelRollJnt, mo=True)  # (driver,driven)
    cmds.parentConstraint(rf_ToeTipCtrl[0], rf_BallRollJnt, mo=True)  # (driver,driven)
    cmds.parent(rf_HeelCtrlGrp, R_frontIKCtl)
    cmds.parentConstraint(R_frontIKCtl, rf_AnkleRotateJnt, mo=True)
    cmds.setAttr(rf_AnkleRotateJnt + '.visibility', 0)
    cmds.select(d=True)

    # group all roll joints
    rollJntGrp = cmds.group(lf_AnkleRotateJnt, rf_AnkleRotateJnt, lb_AnkleRotateJnt, rb_AnkleRotateJnt,
                            n='c_footRollJnt_GRP')

    # NOT NEEDED: r_frontLegTranslation_CTRL has been setup differently currently
    # constraint front leg rotation ctrl to ik controller...
    # constrPoint=cmds.parentConstraint(frontPelvisJnt, L_frontLegTranslationCtrlGrp, mo=True)
    # cmds.parentConstraint(L_frontLegTranslationCtrl, L_frontUpperJntIK, mo=True)
    # cmds.parentConstraint(L_frontIKCtl, L_frontLegTranslationCtrlGrp, mo=True)
    # here we are adding different influence to the ik instead of a full 1 value
    # cmds.setAttr(constrPoint[0]+'.l_frontIK_CTRLW1',.3)
    #
    # constrPoint=cmds.parentConstraint(frontPelvisJnt, R_frontLegTranslationCtrlGrp, mo=True)
    # cmds.parentConstraint(R_frontLegTranslationCtrl, R_frontUpperJntIK, mo=True)
    # cmds.parentConstraint(R_frontIKCtl, R_frontLegTranslationCtrlGrp, mo=True)
    # cmds.setAttr(constrPoint[0]+'.r_frontIK_CTRLW1',.3)


def CleanUpRig():
    global rigGrp
    # first unparent our master control
    legCtrlGrp = cmds.group(IKCtrlGrp, FKCtrlGrp, n='c_legCtrl_GRP')
    cmds.parent(spineMasterCtrlGrp, w=True)
    cmds.parent(spineGrp, spineMasterCtrl)

    rigGrp = cmds.group(tailGrp, legCtrlGrp, legSwitchCtrlGrp, spineMasterCtrlGrp, neckGrp, n='c_rig_GRP')
    jntGrp = cmds.group(rollJntGrp, backPelvisJnt, frontPelvisJnt, tailRootJnt, spineRootJnt, neckRootJnt,
                        n='c_jnt_GRP')

    cmds.parent(rigGrp, jntGrp, subworld)
    cmds.setAttr(L_backUpperJntFK + '.visibility', 0)
    cmds.setAttr(R_backUpperJntFK + '.visibility', 0)
    cmds.setAttr(L_frontUpperJntFK + '.visibility', 0)
    cmds.setAttr(R_frontUpperJntFK + '.visibility', 0)

    cmds.setAttr(L_backUpperJntIK + '.visibility', 0)
    cmds.setAttr(R_backUpperJntIK + '.visibility', 0)
    cmds.setAttr(L_frontUpperJntIK + '.visibility', 0)
    cmds.setAttr(R_frontUpperJntIK + '.visibility', 0)

def StretchySpine():
    ''' stretchy spine '''
    baseLoc = cmds.spaceLocator(n='baseSpine_StretchySpine_Loc')
    poseLoc = cmds.spaceLocator(n='poseSpine_StretchySpine_Loc')
    targetLoc = cmds.spaceLocator(n='targetSpine_StretchySpine_Loc')

    # parent baseLoc to the start of the spineJointChain [the joint highest in the joint chain]
    cmds.parent(baseLoc, spineJointChain[0], r=True)
    cmds.parent(targetLoc, backPelvisJnt, r=True)  # locator parented to back pelvis
    cmds.parent(poseLoc, backPelvisJnt, r=True)  # locator parented to back pelvis

    spineStretchGrp = cmds.group(baseLoc, poseLoc, targetLoc, n='c_spineDistanceReader_GRP')

    # constraint ONLY on z axis
    cmds.pointConstraint(spineCtrl3, poseLoc, sk=('x', 'y'), mo=True)  # sk=skip

    distNode1 = cmds.createNode('distanceDimShape', n='distanceMasterSpin')
    cmds.connectAttr(baseLoc[0] + '.worldPosition', distNode1 + '.startPoint')
    cmds.connectAttr(poseLoc[0] + '.worldPosition', distNode1 + '.endPoint')

    distNode2 = cmds.createNode('distanceDimShape', n='distancePoseSpin')
    cmds.connectAttr(baseLoc[0] + '.worldPosition', distNode2 + '.startPoint')
    cmds.connectAttr(targetLoc[0] + '.worldPosition', distNode2 + '.endPoint')

    divide = cmds.shadingNode('multiplyDivide', asUtility=True, n='stretchSpine_divideWithScale')
    cmds.setAttr(divide + '.operation', 2)
    cmds.connectAttr(distNode1 + '.distance',
                     divide + '.input1X')  # distNode1 distance is connect to input1 of divideNode
    cmds.connectAttr(distNode2 + '.distance',
                     divide + '.input2X')  # distNode2 distance is connect to input2 of divideNode
    cmds.addAttr(baseLoc, longName='output_value', at='enum', en=('_____'), max=1, min=0, k=True)
    cmds.setAttr(baseLoc[0] + '.output_value', lock=True)
    cmds.addAttr(baseLoc, longName='distance', at='float', k=True)
    cmds.connectAttr(divide + '.outputX', baseLoc[0] + '.distance')

    nonShape1 = cmds.listRelatives(distNode1, p=True)  # returns parent of dag
    cmds.setAttr(nonShape1[0] + '.visibility', 0)
    nonShape1 = cmds.rename(nonShape1[0], 'distanceMaster_DST')

    nonShape2 = cmds.listRelatives(distNode2, p=True)  # returns parent of dag
    cmds.setAttr(nonShape2[0] + '.visibility', 0)
    nonShape2 = cmds.rename(nonShape2[0], 'distancePose_DST')

    # e=element
    for e in spineJointChain:
        try:  # try means maya will try to excute a command, if it doesn't succeed it will simply move on
            cmds.connectAttr(baseLoc[0] + '.distance', e + '.scaleX')
        except:
            print 'ignoring spine end joint because there is a constraint'

    cmds.parent(nonShape1, nonShape2, spineStretchGrp)
    cmds.parent(spineStretchGrp, spineGrp)
    cmds.select(d=True)


def SetBodyLocatorsButton():
    # step 1) call function to create  left locators
    createLeftSideLocators()
    # step 2) call function to create center locators
    createCenterLocators()


def CreateBodyRigButton():
    # step 3) group all of the locators we just created
    mainLocGrp = cmds.group(backLocGrp, frontLocGrp, neckLocGrp, tailLocGrp, n='mainPlacementLoc_GRP')

    # step 4) create world controller curvs
    createWorldController()

    # step 5)create back leg joints
    createBackLegJoints()

    # step 6)create back leg IK joints
    createBackLegIKJoints()

    # step 7)create back leg FK joints
    createBackLegFKJoints()

    # step 8)create front leg joints
    createFrontLegJoints()

    # step 9)create front leg IK joints
    createFrontLegIKJoints()

    # step 10)create front leg FK joints
    createFrontLegFKJoints()

    # step 11) setup Ik [create ik handles, effectors, curves and aim polevectors
    SetupIK()

    # step 12) setup FK [create fk handles, effectors, curves]
    SetupFK()

    # step 13) setup IK FK switch
    IKFKSwitch()

    # step 14) blend IK FK joints rotation
    BlendIKFKRotation()

    # step 15) blend IK FK joints translation so that our front upper legs follow the rig
    BlendIKFKTranslation()

    # step 16) create a set for the joints we will be using to paint weight map to
    '''skin joint set, this is what we paint skin weights to'''
    skinJntSet = cmds.sets(L_backUpperJnt, L_backLowerJnt, L_backAnkleJnt, L_backBallJnt, L_backToeJnt,
                           R_backUpperJnt, R_backLowerJnt, R_backAnkleJnt, R_backBallJnt, R_backToeJnt,
                           n='LegSkinJnt_SET')

    # step 17) call tail setup
    TailSetUp()

    # step 18) setup spine
    SpineSetUp()

    # step 19) setup neck
    NeckSetUp()

    # step 20) foot roll
    FootRoll()

    # step 21) remove locators
    cmds.delete(
        mainLocGrp)  # delete all 4 loc groups located inside of our main (backPlacement_GRP/frontPlacement_GRP/neckPlacement_GRP/tailPlacment_GRP)

    # step 22) cleanup outliner by grouping
    CleanUpRig()

    # step 23) stretchy spine
    StretchySpine()

    # parent head ctrl Grp to neck fk ctrl
    cmds.parent(headCtrl1Grp, neckFKCtrl2)
    cmds.select(d=True)


def MoveJointToLocator(jnt,target):
    #move joint to target location
    pm.setAttr(jnt.tx, target[0])
    pm.setAttr(jnt.ty, target[1])
    pm.setAttr(jnt.tz, target[2])

def SetRightWingLocatorsButton():
    global R_clavicleLoc, R_wing01_Loc, R_wing02_Loc, R_wing03_Loc
    global R_feather_01_startLoc, R_feather_01_endLoc
    global R_featherStartLocList, R_featherEndLocList
    global R_featherLocGrp

    # creating wing base locators
    R_clavicleLoc = pm.spaceLocator(n='r_clavicle_Loc')
    R_wing01_Loc = pm.spaceLocator(n='r_wing01_Loc')
    R_wing02_Loc = pm.spaceLocator(n='r_wing02_Loc')
    R_wing03_Loc = pm.spaceLocator(n='r_wing03_Loc')

    # initialize position for  base wing locators
    pm.setAttr(R_clavicleLoc.translateX, -7)
    pm.setAttr(R_clavicleLoc.translateY, 45.5)
    pm.setAttr(R_clavicleLoc.translateZ, 19)

    pm.setAttr(R_wing01_Loc.translateX, -11)
    pm.setAttr(R_wing01_Loc.translateY, 54.5)
    pm.setAttr(R_wing01_Loc.translateZ, 10.488)

    pm.setAttr(R_wing02_Loc.translateX, -23.912)
    pm.setAttr(R_wing02_Loc.translateY, 54.5)
    pm.setAttr(R_wing02_Loc.translateZ, 11)

    pm.setAttr(R_wing03_Loc.translateX, -36.988)
    pm.setAttr(R_wing03_Loc.translateY, 54.5)
    pm.setAttr(R_wing03_Loc.translateZ, 13.639)
    cmds.select(d=True)

    # 19 unique feathers
    numberOfFeatherLoc = 19
    R_featherStartLocList = []
    R_featherEndLocList = []
    R_featherLocGrp = cmds.group(em=True, n='R_featherLoc_GRP')
    cmds.parent('r_clavicle_Loc','r_wing01_Loc','r_wing02_Loc','r_wing03_Loc',R_featherLocGrp)

    # create the locators and store them in a list
    for x in range(0, numberOfFeatherLoc):
        featherStartLoc = pm.spaceLocator(n='r_feather_' + str(x + 1) + '_startLoc')
        featherEndLoc = pm.spaceLocator(n='r_feather_' + str(x + 1) + '_endLoc')

        # ADD TO OUR LISTS
        R_featherStartLocList.append(featherStartLoc)
        R_featherEndLocList.append(featherEndLoc)
        cmds.select(d=True)

        cmds.parent('r_feather_' + str(x + 1) + '_startLoc', 'r_feather_' + str(x + 1) + '_endLoc', R_featherLocGrp)

    # lets give the default values for the feathers
    # feather1
    pm.setAttr(R_featherStartLocList[0].translateX, -55.595)
    pm.setAttr(R_featherStartLocList[0].translateY, 53.975)
    pm.setAttr(R_featherStartLocList[0].translateZ, 13.559)
    pm.setAttr(R_featherEndLocList[0].translateX, -84.094)
    pm.setAttr(R_featherEndLocList[0].translateY, 53.975)
    pm.setAttr(R_featherEndLocList[0].translateZ, 4.133)

    # feather2
    pm.setAttr(R_featherStartLocList[1].translateX, -53.551)
    pm.setAttr(R_featherStartLocList[1].translateY, 54.158)
    pm.setAttr(R_featherStartLocList[1].translateZ, 13.213)
    pm.setAttr(R_featherEndLocList[1].translateX, -78.996)
    pm.setAttr(R_featherEndLocList[1].translateY, 54.532)
    pm.setAttr(R_featherEndLocList[1].translateZ, 2.198)

    # feather3
    pm.setAttr(R_featherStartLocList[2].translateX, -51.071)
    pm.setAttr(R_featherStartLocList[2].translateY, 54.06)
    pm.setAttr(R_featherStartLocList[2].translateZ, 12.763)
    pm.setAttr(R_featherEndLocList[2].translateX, -74.181)
    pm.setAttr(R_featherEndLocList[2].translateY, 54.682)
    pm.setAttr(R_featherEndLocList[2].translateZ, -0.628)

    # feather4
    pm.setAttr(R_featherStartLocList[3].translateX, -48.711)
    pm.setAttr(R_featherStartLocList[3].translateY, 54.243)
    pm.setAttr(R_featherStartLocList[3].translateZ, 12.302)
    pm.setAttr(R_featherEndLocList[3].translateX, -68.656)
    pm.setAttr(R_featherEndLocList[3].translateY, 54.57)
    pm.setAttr(R_featherEndLocList[3].translateZ, -1.167)

    # feather5
    pm.setAttr(R_featherStartLocList[4].translateX, -46.143)
    pm.setAttr(R_featherStartLocList[4].translateY, 54.221)
    pm.setAttr(R_featherStartLocList[4].translateZ, 11.68)
    pm.setAttr(R_featherEndLocList[4].translateX, -62.234)
    pm.setAttr(R_featherEndLocList[4].translateY, 54.524)
    pm.setAttr(R_featherEndLocList[4].translateZ, -2.721)

    # feather6
    pm.setAttr(R_featherStartLocList[5].translateX, -43.24)
    pm.setAttr(R_featherStartLocList[5].translateY, 54.215)
    pm.setAttr(R_featherStartLocList[5].translateZ, 11.118)
    pm.setAttr(R_featherEndLocList[5].translateX, -57.991)
    pm.setAttr(R_featherEndLocList[5].translateY, 54.599)
    pm.setAttr(R_featherEndLocList[5].translateZ, -3.291)

    # feather7
    pm.setAttr(R_featherStartLocList[6].translateX, -40.604)
    pm.setAttr(R_featherStartLocList[6].translateY, 54.239)
    pm.setAttr(R_featherStartLocList[6].translateZ, 10.462)
    pm.setAttr(R_featherEndLocList[6].translateX, -52.15)
    pm.setAttr(R_featherEndLocList[6].translateY, 54.653)
    pm.setAttr(R_featherEndLocList[6].translateZ, -4.88)

    # feather8
    pm.setAttr(R_featherStartLocList[7].translateX, -38.392)
    pm.setAttr(R_featherStartLocList[7].translateY, 54.262)
    pm.setAttr(R_featherStartLocList[7].translateZ, 9.819)
    pm.setAttr(R_featherEndLocList[7].translateX, -46.701)
    pm.setAttr(R_featherEndLocList[7].translateY, 54.517)
    pm.setAttr(R_featherEndLocList[7].translateZ, -5.278)

    # feather9
    pm.setAttr(R_featherStartLocList[8].translateX, -36.229)
    pm.setAttr(R_featherStartLocList[8].translateY, 54.262)
    pm.setAttr(R_featherStartLocList[8].translateZ, 9.124)
    pm.setAttr(R_featherEndLocList[8].translateX, -42.713)
    pm.setAttr(R_featherEndLocList[8].translateY, 54.488)
    pm.setAttr(R_featherEndLocList[8].translateZ, -5.679)

    # feather10
    pm.setAttr(R_featherStartLocList[9].translateX, -34.077)
    pm.setAttr(R_featherStartLocList[9].translateY, 54.254)
    pm.setAttr(R_featherStartLocList[9].translateZ, 8.07)
    pm.setAttr(R_featherEndLocList[9].translateX, -39.602)
    pm.setAttr(R_featherEndLocList[9].translateY, 54.55)
    pm.setAttr(R_featherEndLocList[9].translateZ, -7.453)

    # feather11
    pm.setAttr(R_featherStartLocList[10].translateX, -31.695)
    pm.setAttr(R_featherStartLocList[10].translateY, 54.261)
    pm.setAttr(R_featherStartLocList[10].translateZ, 7.369)
    pm.setAttr(R_featherEndLocList[10].translateX, -36.119)
    pm.setAttr(R_featherEndLocList[10].translateY, 54.452)
    pm.setAttr(R_featherEndLocList[10].translateZ, -8.608)

    # feather12
    pm.setAttr(R_featherStartLocList[11].translateX, -29.134)
    pm.setAttr(R_featherStartLocList[11].translateY, 54.256)
    pm.setAttr(R_featherStartLocList[11].translateZ, 6.631)
    pm.setAttr(R_featherEndLocList[11].translateX, -33.766)
    pm.setAttr(R_featherEndLocList[11].translateY, 54.503)
    pm.setAttr(R_featherEndLocList[11].translateZ, -10.582)

    # feather13
    pm.setAttr(R_featherStartLocList[12].translateX, -26.532)
    pm.setAttr(R_featherStartLocList[12].translateY, 54.503)
    pm.setAttr(R_featherStartLocList[12].translateZ, 5.701)
    pm.setAttr(R_featherEndLocList[12].translateX, -30.411)
    pm.setAttr(R_featherEndLocList[12].translateY, 54.483)
    pm.setAttr(R_featherEndLocList[12].translateZ, -11.634)

    # feather14
    pm.setAttr(R_featherStartLocList[13].translateX, -24.079)
    pm.setAttr(R_featherStartLocList[13].translateY, 54.259)
    pm.setAttr(R_featherStartLocList[13].translateZ, 5.174)
    pm.setAttr(R_featherEndLocList[13].translateX, -26.271)
    pm.setAttr(R_featherEndLocList[13].translateY, 54.555)
    pm.setAttr(R_featherEndLocList[13].translateZ, -12.294)

    # feather15
    pm.setAttr(R_featherStartLocList[14].translateX, -22.005)
    pm.setAttr(R_featherStartLocList[14].translateY, 54.28)
    pm.setAttr(R_featherStartLocList[14].translateZ, 5.772)
    pm.setAttr(R_featherEndLocList[14].translateX, -21.727)
    pm.setAttr(R_featherEndLocList[14].translateY, 54.49)
    pm.setAttr(R_featherEndLocList[14].translateZ, -11.616)

    # feather16
    pm.setAttr(R_featherStartLocList[15].translateX, -19.27)
    pm.setAttr(R_featherStartLocList[15].translateY, 54.296)
    pm.setAttr(R_featherStartLocList[15].translateZ, 6.279)
    pm.setAttr(R_featherEndLocList[15].translateX, -18.022)
    pm.setAttr(R_featherEndLocList[15].translateY, 54.515)
    pm.setAttr(R_featherEndLocList[15].translateZ, -9.195)

    # feather17
    pm.setAttr(R_featherStartLocList[16].translateX, -17.035)
    pm.setAttr(R_featherStartLocList[16].translateY, 54.287)
    pm.setAttr(R_featherStartLocList[16].translateZ, 6.378)
    pm.setAttr(R_featherEndLocList[16].translateX, -14.21)
    pm.setAttr(R_featherEndLocList[16].translateY, 54.451)
    pm.setAttr(R_featherEndLocList[16].translateZ, -7.129)

    # feather18
    pm.setAttr(R_featherStartLocList[17].translateX, -15.128)
    pm.setAttr(R_featherStartLocList[17].translateY, 54.291)
    pm.setAttr(R_featherStartLocList[17].translateZ, 6.504)
    pm.setAttr(R_featherEndLocList[17].translateX, -12.082)
    pm.setAttr(R_featherEndLocList[17].translateY, 54.484)
    pm.setAttr(R_featherEndLocList[17].translateZ, -3.796)

    # feather19
    pm.setAttr(R_featherStartLocList[18].translateX, -13.338)
    pm.setAttr(R_featherStartLocList[18].translateY, 54.298)
    pm.setAttr(R_featherStartLocList[18].translateZ, 6.58)
    pm.setAttr(R_featherEndLocList[18].translateX, -10.484)
    pm.setAttr(R_featherEndLocList[18].translateY, 54.429)
    pm.setAttr(R_featherEndLocList[18].translateZ, 0.028)

def SetLeftWingLocatorsButton():
    global L_clavicleLoc, L_wing01_Loc, L_wing02_Loc, L_wing03_Loc
    global L_feather_01_startLoc, L_feather_01_endLoc
    global L_featherStartLocList, L_featherEndLocList
    global L_featherLocGrp

    # creating wing base locators
    L_clavicleLoc = pm.spaceLocator(n='l_clavicle_Loc')
    L_wing01_Loc = pm.spaceLocator(n='l_wing01_Loc')
    L_wing02_Loc = pm.spaceLocator(n='l_wing02_Loc')
    L_wing03_Loc = pm.spaceLocator(n='l_wing03_Loc')

    #initialize position for  base wing locators
    pm.setAttr(L_clavicleLoc.translateX, 7)
    pm.setAttr(L_clavicleLoc.translateY, 45.5)
    pm.setAttr(L_clavicleLoc.translateZ, 19)

    pm.setAttr(L_wing01_Loc.translateX, 11)
    pm.setAttr(L_wing01_Loc.translateY, 54.5)
    pm.setAttr(L_wing01_Loc.translateZ, 10.488)

    pm.setAttr(L_wing02_Loc.translateX, 23.912)
    pm.setAttr(L_wing02_Loc.translateY, 54.5)
    pm.setAttr(L_wing02_Loc.translateZ, 11)

    pm.setAttr(L_wing03_Loc.translateX, 36.988)
    pm.setAttr(L_wing03_Loc.translateY, 54.5)
    pm.setAttr(L_wing03_Loc.translateZ, 13.639)
    cmds.select(d=True)

    # 19 unique feathers
    numberOfFeatherLoc = 19
    L_featherStartLocList = []
    L_featherEndLocList =[]
    L_featherLocGrp = cmds.group(em=True, n='L_featherLoc_GRP')
    cmds.parent('l_clavicle_Loc','l_wing01_Loc','l_wing02_Loc','l_wing03_Loc',L_featherLocGrp)

    #create the locators and store them in a list
    for x in range (0,numberOfFeatherLoc):
        featherStartLoc = pm.spaceLocator(n='l_feather_' + str(x+1) + '_startLoc')
        featherEndLoc = pm.spaceLocator(n='l_feather_' + str(x+1) + '_endLoc')

        #ADD TO OUR LISTS
        L_featherStartLocList.append(featherStartLoc)
        L_featherEndLocList.append(featherEndLoc)
        cmds.select(d=True)

        cmds.parent('l_feather_' + str(x+1) + '_startLoc','l_feather_' + str(x+1) + '_endLoc',L_featherLocGrp)

    # lets give the default values for the feathers
    # feather1
    pm.setAttr(L_featherStartLocList[0].translateX, 55.595)
    pm.setAttr(L_featherStartLocList[0].translateY, 53.975)
    pm.setAttr(L_featherStartLocList[0].translateZ, 13.559)
    pm.setAttr(L_featherEndLocList[0].translateX, 84.094)
    pm.setAttr(L_featherEndLocList[0].translateY, 53.975)
    pm.setAttr(L_featherEndLocList[0].translateZ, 4.133)

    # feather2
    pm.setAttr(L_featherStartLocList[1].translateX, 53.551)
    pm.setAttr(L_featherStartLocList[1].translateY, 54.158)
    pm.setAttr(L_featherStartLocList[1].translateZ, 13.213)
    pm.setAttr(L_featherEndLocList[1].translateX, 78.996)
    pm.setAttr(L_featherEndLocList[1].translateY, 54.532)
    pm.setAttr(L_featherEndLocList[1].translateZ, 2.198)

    # feather3
    pm.setAttr(L_featherStartLocList[2].translateX, 51.071)
    pm.setAttr(L_featherStartLocList[2].translateY, 54.06)
    pm.setAttr(L_featherStartLocList[2].translateZ, 12.763)
    pm.setAttr(L_featherEndLocList[2].translateX, 74.181)
    pm.setAttr(L_featherEndLocList[2].translateY, 54.682)
    pm.setAttr(L_featherEndLocList[2].translateZ, -0.628)

    # feather4
    pm.setAttr(L_featherStartLocList[3].translateX, 48.711)
    pm.setAttr(L_featherStartLocList[3].translateY, 54.243)
    pm.setAttr(L_featherStartLocList[3].translateZ, 12.302)
    pm.setAttr(L_featherEndLocList[3].translateX, 68.656)
    pm.setAttr(L_featherEndLocList[3].translateY, 54.57)
    pm.setAttr(L_featherEndLocList[3].translateZ, -1.167)

    # feather5
    pm.setAttr(L_featherStartLocList[4].translateX, 46.143)
    pm.setAttr(L_featherStartLocList[4].translateY, 54.221)
    pm.setAttr(L_featherStartLocList[4].translateZ, 11.68)
    pm.setAttr(L_featherEndLocList[4].translateX, 62.234)
    pm.setAttr(L_featherEndLocList[4].translateY, 54.524)
    pm.setAttr(L_featherEndLocList[4].translateZ, -2.721)

    # feather6
    pm.setAttr(L_featherStartLocList[5].translateX, 43.24)
    pm.setAttr(L_featherStartLocList[5].translateY, 54.215)
    pm.setAttr(L_featherStartLocList[5].translateZ, 11.118)
    pm.setAttr(L_featherEndLocList[5].translateX, 57.991)
    pm.setAttr(L_featherEndLocList[5].translateY, 54.599)
    pm.setAttr(L_featherEndLocList[5].translateZ, -3.291)

    # feather7
    pm.setAttr(L_featherStartLocList[6].translateX, 40.604)
    pm.setAttr(L_featherStartLocList[6].translateY, 54.239)
    pm.setAttr(L_featherStartLocList[6].translateZ, 10.462)
    pm.setAttr(L_featherEndLocList[6].translateX, 52.15)
    pm.setAttr(L_featherEndLocList[6].translateY, 54.653)
    pm.setAttr(L_featherEndLocList[6].translateZ, -4.88)

    # feather8
    pm.setAttr(L_featherStartLocList[7].translateX, 38.392)
    pm.setAttr(L_featherStartLocList[7].translateY, 54.262)
    pm.setAttr(L_featherStartLocList[7].translateZ, 9.819)
    pm.setAttr(L_featherEndLocList[7].translateX, 46.701)
    pm.setAttr(L_featherEndLocList[7].translateY, 54.517)
    pm.setAttr(L_featherEndLocList[7].translateZ, -5.278)

    # feather9
    pm.setAttr(L_featherStartLocList[8].translateX, 36.229)
    pm.setAttr(L_featherStartLocList[8].translateY, 54.262)
    pm.setAttr(L_featherStartLocList[8].translateZ, 9.124)
    pm.setAttr(L_featherEndLocList[8].translateX, 42.713)
    pm.setAttr(L_featherEndLocList[8].translateY, 54.488)
    pm.setAttr(L_featherEndLocList[8].translateZ, -5.679)

    # feather10
    pm.setAttr(L_featherStartLocList[9].translateX, 34.077)
    pm.setAttr(L_featherStartLocList[9].translateY, 54.254)
    pm.setAttr(L_featherStartLocList[9].translateZ, 8.07)
    pm.setAttr(L_featherEndLocList[9].translateX, 39.602)
    pm.setAttr(L_featherEndLocList[9].translateY, 54.55)
    pm.setAttr(L_featherEndLocList[9].translateZ, -7.453)

    # feather11
    pm.setAttr(L_featherStartLocList[10].translateX, 31.695)
    pm.setAttr(L_featherStartLocList[10].translateY, 54.261)
    pm.setAttr(L_featherStartLocList[10].translateZ, 7.369)
    pm.setAttr(L_featherEndLocList[10].translateX, 36.119)
    pm.setAttr(L_featherEndLocList[10].translateY, 54.452)
    pm.setAttr(L_featherEndLocList[10].translateZ, -8.608)

    # feather12
    pm.setAttr(L_featherStartLocList[11].translateX, 29.134)
    pm.setAttr(L_featherStartLocList[11].translateY, 54.256)
    pm.setAttr(L_featherStartLocList[11].translateZ, 6.631)
    pm.setAttr(L_featherEndLocList[11].translateX, 33.766)
    pm.setAttr(L_featherEndLocList[11].translateY, 54.503)
    pm.setAttr(L_featherEndLocList[11].translateZ, -10.582)

    # feather13
    pm.setAttr(L_featherStartLocList[12].translateX, 26.532)
    pm.setAttr(L_featherStartLocList[12].translateY, 54.503)
    pm.setAttr(L_featherStartLocList[12].translateZ, 5.701)
    pm.setAttr(L_featherEndLocList[12].translateX, 30.411)
    pm.setAttr(L_featherEndLocList[12].translateY, 54.483)
    pm.setAttr(L_featherEndLocList[12].translateZ, -11.634)

    # feather14
    pm.setAttr(L_featherStartLocList[13].translateX, 24.079)
    pm.setAttr(L_featherStartLocList[13].translateY, 54.259)
    pm.setAttr(L_featherStartLocList[13].translateZ, 5.174)
    pm.setAttr(L_featherEndLocList[13].translateX, 26.271)
    pm.setAttr(L_featherEndLocList[13].translateY, 54.555)
    pm.setAttr(L_featherEndLocList[13].translateZ, -12.294)

    # feather15
    pm.setAttr(L_featherStartLocList[14].translateX, 22.005)
    pm.setAttr(L_featherStartLocList[14].translateY, 54.28)
    pm.setAttr(L_featherStartLocList[14].translateZ, 5.772)
    pm.setAttr(L_featherEndLocList[14].translateX, 21.727)
    pm.setAttr(L_featherEndLocList[14].translateY, 54.49)
    pm.setAttr(L_featherEndLocList[14].translateZ, -11.616)

    # feather16
    pm.setAttr(L_featherStartLocList[15].translateX, 19.27)
    pm.setAttr(L_featherStartLocList[15].translateY, 54.296)
    pm.setAttr(L_featherStartLocList[15].translateZ, 6.279)
    pm.setAttr(L_featherEndLocList[15].translateX, 18.022)
    pm.setAttr(L_featherEndLocList[15].translateY, 54.515)
    pm.setAttr(L_featherEndLocList[15].translateZ, -9.195)

    # feather17
    pm.setAttr(L_featherStartLocList[16].translateX, 17.035)
    pm.setAttr(L_featherStartLocList[16].translateY, 54.287)
    pm.setAttr(L_featherStartLocList[16].translateZ, 6.378)
    pm.setAttr(L_featherEndLocList[16].translateX, 14.21)
    pm.setAttr(L_featherEndLocList[16].translateY, 54.451)
    pm.setAttr(L_featherEndLocList[16].translateZ, -7.129)

    # feather18
    pm.setAttr(L_featherStartLocList[17].translateX, 15.128)
    pm.setAttr(L_featherStartLocList[17].translateY, 54.291)
    pm.setAttr(L_featherStartLocList[17].translateZ, 6.504)
    pm.setAttr(L_featherEndLocList[17].translateX, 12.082)
    pm.setAttr(L_featherEndLocList[17].translateY, 54.484)
    pm.setAttr(L_featherEndLocList[17].translateZ, -3.796)

    # feather19
    pm.setAttr(L_featherStartLocList[18].translateX, 13.338)
    pm.setAttr(L_featherStartLocList[18].translateY, 54.298)
    pm.setAttr(L_featherStartLocList[18].translateZ, 6.58)
    pm.setAttr(L_featherEndLocList[18].translateX, 10.484)
    pm.setAttr(L_featherEndLocList[18].translateY, 54.429)
    pm.setAttr(L_featherEndLocList[18].translateZ, 0.028)






def CreateLeftWingJointButton():
    global wingLeftAndRightSystemGrp
    global L_featherShaperCurve

    #This is the definition called from our ui button
    #creatings the base wing joints
    pm.select(d=True)
    L_wing01Jnt = pm.joint(n='l_wing01_JNT')
    cmds.select(d=True)
    L_wing02Jnt = pm.joint(n='l_wing02_JNT')
    pm.select(d=True)
    L_wing03Jnt = pm.joint(n='l_wing03_JNT')
    pm.select(d=True)

    L_claviclePosition = pm.xform(L_clavicleLoc, q=True, ws=True, rp=True)
    L_wing01Position = pm.xform(L_wing01_Loc, q=True, ws=True, rp=True)
    L_wing02Position = pm.xform(L_wing02_Loc, q=True, ws=True, rp=True)
    L_wing03Position = pm.xform(L_wing03_Loc, q=True, ws=True, rp=True)

    MoveJointToLocator(L_wing01Jnt, L_wing01Position)
    MoveJointToLocator(L_wing02Jnt, L_wing02Position)
    MoveJointToLocator(L_wing03Jnt, L_wing03Position)

    #now parent the wing base joints
    pm.parent(L_wing01Jnt, frontPelvisJnt) #dandan
    #pm.parent(L_wing01Jnt,L_clavicleJnt)
    pm.parent(L_wing02Jnt, L_wing01Jnt)
    pm.parent(L_wing03Jnt, L_wing02Jnt)
    pm.select(d=True)

    #19 feathers
    numberOfFeathers2 = 19
    L_featherStartJntList = []
    L_featherEndJntList = []
    for x in range (0,numberOfFeathers2):
        featherLocStart = pm.xform(L_featherStartLocList[x], q=True, ws=True, rp=True)
        pm.select(d=True)
        featherLocEnd = pm.xform(L_featherEndLocList[x], q=True, ws=True, rp=True)
        pm.select(d=True)
        featherName = 'l_feather_'+str(x)

        #creating feather joint
        cmds.select(d=True)
        featherStartJnt = cmds.joint(n=featherName + '_start_JNT')
        cmds.select(d=True)

        featherEndJnt = cmds.joint(n=featherName + '_end_JNT')
        cmds.select(d=True)

        #adding joint created to lists for tracking purposes
        L_featherStartJntList.append(featherStartJnt)
        L_featherEndJntList.append(featherEndJnt)

        cmds.setAttr(L_featherStartJntList[x] + '.tx', featherLocStart[0])
        cmds.setAttr(L_featherStartJntList[x] + '.ty', featherLocStart[1])
        cmds.setAttr(L_featherStartJntList[x] + '.tz', featherLocStart[2])

        cmds.setAttr(L_featherEndJntList[x] + '.tx', featherLocEnd[0])
        cmds.setAttr(L_featherEndJntList[x] + '.ty', featherLocEnd[1])
        cmds.setAttr(L_featherEndJntList[x] + '.tz', featherLocEnd[2])

        #parent the feather 2 joints together (add adj joint later because it's ruining joint orientation)
        cmds.parent(L_featherEndJntList[x], L_featherStartJntList[x])

    cmds.parent(L_featherLocGrp, rigGrp)  # leelee

    # lets parent feather start joints to the wing arm
    # start_1_FeatherJoint (joints 0-3 parent to l_wing03_JNT)

    pm.parent(L_featherStartJntList[14], L_wing01Jnt)
    pm.parent(L_featherStartJntList[15], L_wing01Jnt)
    pm.parent(L_featherStartJntList[16], L_wing01Jnt)
    pm.parent(L_featherStartJntList[17], L_wing01Jnt)
    pm.parent(L_featherStartJntList[18], L_wing01Jnt)

    # mid_2_FeatherJoint (joints 0-3 parent to l_wing03_JNT)

    pm.parent(L_featherStartJntList[8],L_wing02Jnt)
    pm.parent(L_featherStartJntList[9], L_wing02Jnt)
    pm.parent(L_featherStartJntList[10], L_wing02Jnt)
    pm.parent(L_featherStartJntList[11], L_wing02Jnt)
    pm.parent(L_featherStartJntList[12], L_wing02Jnt)
    pm.parent(L_featherStartJntList[13], L_wing02Jnt)


    # end_3_FeatherJoint (joints 0-3 parent to l_wing03_JNT)
    pm.parent(L_featherStartJntList[0],L_wing03Jnt)
    pm.parent(L_featherStartJntList[1], L_wing03Jnt)
    pm.parent(L_featherStartJntList[2], L_wing03Jnt)
    pm.parent(L_featherStartJntList[3], L_wing03Jnt)
    pm.parent(L_featherStartJntList[4],L_wing03Jnt)
    pm.parent(L_featherStartJntList[5], L_wing03Jnt)
    pm.parent(L_featherStartJntList[6], L_wing03Jnt)
    pm.parent(L_featherStartJntList[7], L_wing03Jnt)

    #lets orient the full wing joints
    # orient L arm chain joints
    pm.select(L_wing01Jnt)
    OrientSelectedJoints(L_wing01Jnt)


    #NOW THAT THE START JOINTS ARE ORIENTED WE CAN DUPE IT AND CREATE A SINGLE ADJUST JNT WITH MATCHING PIVOT
    #making sure our adjust joint matches the pivot of our start feather joint (by duplicating)
    L_featherAdjustJntList = []
    L_featherAdjustCtrlList = []
    L_featherAdjustCtrlAllGrps = cmds.group(em=True, n='L_featherAdjustCtrlAll_GRP')
    for x in range (0,19):
        # transForAdjustJnt = pm.xform(featherStartJnt[x], q=True, ws=True, rp=True)
        featherName = 'l_feather_' + str(x)
        cmds.select(L_featherStartJntList[x])
        duped = cmds.duplicate(parentOnly=True, n=featherName + '_adjust_JNT')
        L_featherAdjustJntList.append(duped)
        cmds.parent(L_featherAdjustJntList[x],L_featherStartJntList[x])
        cmds.select(d=True)

        # create ctrl for adjust joint
        #store all ctrl+Grp object in a list

        featherToAdd = CreatePyramidRigCtrl(featherName+'_adjust_jnt_CTRL', L_featherAdjustJntList[x], L_featherStartJntList[x])
        L_featherAdjustCtrlList.append(featherToAdd)
        cmds.parent(L_featherAdjustCtrlList[x],L_featherAdjustCtrlAllGrps)

    #color all our feather adjust ctrl
    blueColor(L_featherAdjustCtrlAllGrps)


    #creating wing ctrl
    L_wing01Ctrl = CreateSphereRigCtrl('l_wing01_CTRL')
    blueColor(L_wing01Ctrl[0])
    L_wing01CtrlGrp = pm.group(L_wing01Ctrl, n='l_wing01_Ctrl_GRP')
    pm.scale(L_wing01CtrlGrp, [4,4,4])
    cnstr = pm.parentConstraint(L_wing01Jnt,L_wing01CtrlGrp) #(moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    L_wing02Ctrl = CreateSphereRigCtrl('l_wing02_CTRL')
    blueColor(L_wing02Ctrl[0])
    L_wing02CtrlGrp = pm.group(L_wing02Ctrl, n='l_wing02_Ctrl_GRP')
    pm.scale(L_wing02CtrlGrp, [4, 4, 4])
    cnstr = pm.parentConstraint(L_wing02Jnt, L_wing02CtrlGrp) #(moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    L_wing03Ctrl = CreateSphereRigCtrl('l_wing03_CTRL')
    blueColor(L_wing03Ctrl[0])
    L_wing03CtrlGrp = pm.group(L_wing03Ctrl, n='l_wing03_Ctrl_GRP')
    pm.scale(L_wing03CtrlGrp, [4, 4, 4])
    cnstr = pm.parentConstraint(L_wing03Jnt, L_wing03CtrlGrp) #(moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)





    #create the sub fk ctrl for the 3 main driver feathers
    L_feather03Ctrl = CreateFeatherSquareRigCtrl(L_featherStartJntList[0], L_featherEndJntList[0],'l_feather03_CTRL')
    blueColor(L_feather03Ctrl)
    pm.select(d=True)
    L_feather03CtrlGrp = pm.group(n='l_feather03_Grp')
    pm.parent(L_feather03Ctrl, L_feather03CtrlGrp)
    cnstr = pm.parentConstraint(L_featherStartJntList[0], L_feather03CtrlGrp) #(moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    L_feather02Ctrl = CreateFeatherSquareRigCtrl(L_featherStartJntList[7], L_featherEndJntList[7],'l_feather02_CTRL')
    blueColor(L_feather02Ctrl)
    pm.select(d=True)
    L_feather02CtrlGrp = pm.group(n='l_feather02_Grp')
    pm.parent(L_feather02Ctrl,L_feather02CtrlGrp)
    cnstr = pm.parentConstraint(L_featherStartJntList[7], L_feather02CtrlGrp) #(moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    L_feather01Ctrl = CreateFeatherSquareRigCtrl(L_featherStartJntList[18], L_featherEndJntList[18],'l_feather01_CTRL')
    blueColor(L_feather01Ctrl)
    pm.select(d=True)
    L_feather01CtrlGrp = pm.group(n='l_feather01_Grp')
    pm.parent(L_feather01Ctrl,L_feather01CtrlGrp)
    cnstr = pm.parentConstraint(L_featherStartJntList[18], L_feather01CtrlGrp) #(moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)


    # parent constraint L arm ctrls
    pm.parentConstraint(L_wing01Ctrl,L_wing01Jnt)
    pm.parentConstraint(L_wing02Ctrl, L_wing02Jnt)
    pm.parentConstraint(L_wing03Ctrl, L_wing03Jnt)

    # parent constraint L feather ctrls
    pm.parentConstraint(L_feather03Ctrl,L_featherStartJntList[0])
    pm.parentConstraint(L_feather02Ctrl, L_featherStartJntList[7])
    pm.parentConstraint(L_feather01Ctrl, L_featherStartJntList[18])

    # parent constraint the L ctrls to one another
    pm.select(d=True)
    pm.parent(L_feather03CtrlGrp, L_wing03Ctrl[0])
    pm.parent(L_feather02CtrlGrp, L_wing03Ctrl[0])
    pm.parent(L_feather01CtrlGrp, L_wing01Ctrl[0])
    pm.parent(L_wing03CtrlGrp, L_wing02Ctrl[0])
    pm.parent(L_wing02CtrlGrp, L_wing01Ctrl[0])
    pm.parent(L_wing01CtrlGrp,spineCtrl1)#dandan



    #blend outer feathers to main feathers
    #(featherBlendMax, featherBlendMin, FeatherBlend, node number)
    #(featherEndStartJnt, featherMidStartJnt, BlendFeatherStartJnt, nodeNumber)
    BlendOuterFeather(L_featherStartJntList[0], L_featherStartJntList[7], L_featherStartJntList[1], 1, 'L_')
    BlendOuterFeather(L_featherStartJntList[0], L_featherStartJntList[7], L_featherStartJntList[2], 2, 'L_')
    BlendOuterFeather(L_featherStartJntList[0], L_featherStartJntList[7], L_featherStartJntList[3], 3, 'L_')
    BlendOuterFeather(L_featherStartJntList[0], L_featherStartJntList[7], L_featherStartJntList[4], 4, 'L_')
    BlendOuterFeather(L_featherStartJntList[0], L_featherStartJntList[7], L_featherStartJntList[5], 5, 'L_')
    BlendOuterFeather(L_featherStartJntList[0], L_featherStartJntList[7], L_featherStartJntList[6], 6, 'L_')





    #blend inner feathers    (start // end // blendThis // cnstraintNumber)

    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[8], 5)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[9], 6)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[10], 7)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[11], 8)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[12], 9)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[13], 10)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[14], 11)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[15], 12)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[16], 13)
    BlendInnerFeather(L_featherStartJntList[18], L_featherStartJntList[7], L_featherStartJntList[17], 14)








    # creating curve that will allow us to sculpt end of feathers of the wing with clusters
    point1 = cmds.xform(L_featherEndJntList[0], q=True, ws=True, rp=True)
    point2 = cmds.xform(L_featherEndJntList[7], q=True, ws=True, rp=True)
    point3 = cmds.xform(L_featherEndJntList[13], q=True, ws=True, rp=True)
    point4 = cmds.xform(L_featherEndJntList[18], q=True, ws=True, rp=True)
    L_featherShaperCurve = cmds.curve(d=3, p=[(point1[0],point1[1],point1[2]),
                       (point2[0],point2[1],point2[2]),
                       (point3[0],point3[1],point3[2]),
                       (point4[0],point4[1],point4[2])], k=(0, 0, 0, 1, 1, 1), n='L_feather_Shaper_curve')


    #lets create an empty group that we will use to grp our clusters
    wingLeftAndRightSystemGrp = cmds.group(em=True, n='c_Wings_GRP')
    L_ClusterCtrlAllGrps = cmds.group(em=True, n='L_ClusterCtrlAll_GRP')
    L_ClusterHandleGrp = cmds.group(em=True, n='L_ClusterHandleGrp_GRP')
    L_WingSystemGrp = cmds.group(em=True, n='L_WingSystem_GRP')

    #create 4 ctrls for the 4 clusters we are about to make
    cmds.select(d=True)
    L_featherCluster1Ctrl = CreateSphereRigCtrl('L_feather_Cluster1_CTRL')
    blueColor(L_featherCluster1Ctrl[0])
    L_featherCluster1CtrlGrp = cmds.group(L_featherCluster1Ctrl,n='L_featherCluster1CtrlGrp')
    constr = cmds.pointConstraint(L_featherEndJntList[18],L_featherCluster1CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(L_featherCluster1CtrlGrp+'.scaleX', 2)
    cmds.setAttr(L_featherCluster1CtrlGrp+'.scaleY', 2)
    cmds.setAttr(L_featherCluster1CtrlGrp+'.scaleZ', 2)

    cmds.select(d=True)
    L_featherCluster2Ctrl = CreateSphereRigCtrl('L_feather_Cluster2_CTRL')
    blueColor(L_featherCluster2Ctrl[0])
    L_featherCluster2CtrlGrp = cmds.group(L_featherCluster2Ctrl,n='L_featherCluster2CtrlGrp')
    constr = cmds.pointConstraint(L_featherEndJntList[13],L_featherCluster2CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(L_featherCluster2CtrlGrp+'.scaleX', 2)
    cmds.setAttr(L_featherCluster2CtrlGrp+'.scaleY', 2)
    cmds.setAttr(L_featherCluster2CtrlGrp+'.scaleZ', 2)

    cmds.select(d=True)
    L_featherCluster3Ctrl = CreateSphereRigCtrl('L_feather_Cluster3_CTRL')
    blueColor(L_featherCluster3Ctrl[0])
    L_featherCluster3CtrlGrp = cmds.group(L_featherCluster3Ctrl,n='L_featherCluster3CtrlGrp')
    constr = cmds.pointConstraint(L_featherEndJntList[7],L_featherCluster3CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(L_featherCluster3CtrlGrp+'.scaleX', 2)
    cmds.setAttr(L_featherCluster3CtrlGrp+'.scaleY', 2)
    cmds.setAttr(L_featherCluster3CtrlGrp+'.scaleZ', 2)

    cmds.select(d=True)
    L_featherCluster4Ctrl = CreateSphereRigCtrl('L_feather_Cluster4_CTRL')
    blueColor(L_featherCluster4Ctrl[0])
    L_featherCluster4CtrlGrp = cmds.group(L_featherCluster4Ctrl,n='L_featherCluster4CtrlGrp')
    constr = cmds.pointConstraint(L_featherEndJntList[0],L_featherCluster4CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(L_featherCluster4CtrlGrp+'.scaleX', 2)
    cmds.setAttr(L_featherCluster4CtrlGrp+'.scaleY', 2)
    cmds.setAttr(L_featherCluster4CtrlGrp+'.scaleZ', 2)



    #create the needed clusters and attach them to our 4 cv points
    # cmds.select(featherShaperCurve+'.controlPoints[0]')
    L_featherCluster1 = cmds.cluster(L_featherShaperCurve+'.controlPoints[3]', n='L_feather_cluster1')
    L_featherCluster1Grp = cmds.group(n='L_feather_cluster1_GRP')
    L_featherCluster2 = cmds.cluster(L_featherShaperCurve+'.controlPoints[2]', n='L_feather_cluster2')
    L_featherCluster2Grp = cmds.group(n='L_feather_cluster2_GRP')
    L_featherCluster3 = cmds.cluster(L_featherShaperCurve+'.controlPoints[1]', n='L_feather_cluster3')
    L_featherCluster3Grp = cmds.group(n='L_feather_cluster3_GRP')
    L_featherCluster4 = cmds.cluster(L_featherShaperCurve+'.controlPoints[0]', n='L_feather_cluster4')
    L_featherCluster4Grp = cmds.group(n='L_feather_cluster4_GRP')


    #parent constraint clusters to our cluster ctrls
    cmds.parentConstraint(L_featherCluster1Ctrl, L_featherCluster1, mo=True)
    cmds.parentConstraint(L_featherCluster2Ctrl, L_featherCluster2, mo=True)
    cmds.parentConstraint(L_featherCluster3Ctrl, L_featherCluster3, mo=True)
    cmds.parentConstraint(L_featherCluster4Ctrl, L_featherCluster4, mo=True)


    #parent constraint the cluster grp to corresponding wing arm ctrler
    cmds.parentConstraint(L_feather03Ctrl, L_featherCluster4CtrlGrp, mo=True)
    cmds.parentConstraint(L_wing03Ctrl, L_featherCluster3CtrlGrp, mo=True)
    cmds.parentConstraint(L_wing02Ctrl, L_featherCluster2CtrlGrp, mo=True)
    cmds.parentConstraint(L_wing01Ctrl, L_featherCluster1CtrlGrp, mo=True)


    cmds.parent(L_featherCluster1CtrlGrp,L_featherCluster2CtrlGrp,L_featherCluster3CtrlGrp,L_featherCluster4CtrlGrp,L_ClusterCtrlAllGrps)
    cmds.parent(L_featherCluster1Grp, L_featherCluster2Grp, L_featherCluster3Grp, L_featherCluster4Grp,L_ClusterHandleGrp)
    cmds.parent(L_ClusterCtrlAllGrps, L_ClusterHandleGrp,L_featherAdjustCtrlAllGrps, L_WingSystemGrp)
    cmds.parent(L_WingSystemGrp,wingLeftAndRightSystemGrp)


def CreateRightWingJointButton():
    global R_featherShaperCurve
    global featherShapersGrp
    # This is the definition called from our ui button
    # creatings the base wing joints
    pm.select(d=True)
    R_wing01Jnt = pm.joint(n='r_wing01_JNT')
    cmds.select(d=True)
    R_wing02Jnt = pm.joint(n='r_wing02_JNT')
    pm.select(d=True)
    R_wing03Jnt = pm.joint(n='r_wing03_JNT')
    pm.select(d=True)

    R_claviclePosition = pm.xform(R_clavicleLoc, q=True, ws=True, rp=True)
    R_wing01Position = pm.xform(R_wing01_Loc, q=True, ws=True, rp=True)
    R_wing02Position = pm.xform(R_wing02_Loc, q=True, ws=True, rp=True)
    R_wing03Position = pm.xform(R_wing03_Loc, q=True, ws=True, rp=True)

    MoveJointToLocator(R_wing01Jnt, R_wing01Position)
    MoveJointToLocator(R_wing02Jnt, R_wing02Position)
    MoveJointToLocator(R_wing03Jnt, R_wing03Position)

    # now parent the wing base joints
    pm.parent(R_wing01Jnt, frontPelvisJnt)# dandan R
    # pm.parent(R_wing01Jnt, R_clavicleJnt)
    pm.parent(R_wing02Jnt, R_wing01Jnt)
    pm.parent(R_wing03Jnt, R_wing02Jnt)
    pm.select(d=True)

    # 19 feathers
    numberOfFeathers2 = 19
    R_featherStartJntList = []
    R_featherEndJntList = []
    for x in range(0, numberOfFeathers2):
        featherLocStart = pm.xform(R_featherStartLocList[x], q=True, ws=True, rp=True)
        pm.select(d=True)
        featherLocEnd = pm.xform(R_featherEndLocList[x], q=True, ws=True, rp=True)
        pm.select(d=True)
        featherName = 'r_feather_' + str(x)

        # creating feather joint
        cmds.select(d=True)
        featherStartJnt = cmds.joint(n=featherName + '_start_JNT')
        cmds.select(d=True)

        featherEndJnt = cmds.joint(n=featherName + '_end_JNT')
        cmds.select(d=True)

        # adding joint created to lists for tracking purposes
        R_featherStartJntList.append(featherStartJnt)
        R_featherEndJntList.append(featherEndJnt)

        cmds.setAttr(R_featherStartJntList[x] + '.tx', featherLocStart[0])
        cmds.setAttr(R_featherStartJntList[x] + '.ty', featherLocStart[1])
        cmds.setAttr(R_featherStartJntList[x] + '.tz', featherLocStart[2])

        cmds.setAttr(R_featherEndJntList[x] + '.tx', featherLocEnd[0])
        cmds.setAttr(R_featherEndJntList[x] + '.ty', featherLocEnd[1])
        cmds.setAttr(R_featherEndJntList[x] + '.tz', featherLocEnd[2])

        # parent the feather 2 joints together (add adj joint later because it's ruining joint orientation)
        cmds.parent(R_featherEndJntList[x], R_featherStartJntList[x])

    cmds.parent(R_featherLocGrp, rigGrp)  # leelee

    # lets parent feather start joints to the wing arm
    # start_1_FeatherJoint (joints 0-3 parent to r_wing03_JNT)

    pm.parent(R_featherStartJntList[14], R_wing01Jnt)
    pm.parent(R_featherStartJntList[15], R_wing01Jnt)
    pm.parent(R_featherStartJntList[16], R_wing01Jnt)
    pm.parent(R_featherStartJntList[17], R_wing01Jnt)
    pm.parent(R_featherStartJntList[18], R_wing01Jnt)

    # mid_2_FeatherJoint (joints 0-3 parent to r_wing03_JNT)

    pm.parent(R_featherStartJntList[8], R_wing02Jnt)
    pm.parent(R_featherStartJntList[9], R_wing02Jnt)
    pm.parent(R_featherStartJntList[10], R_wing02Jnt)
    pm.parent(R_featherStartJntList[11], R_wing02Jnt)
    pm.parent(R_featherStartJntList[12], R_wing02Jnt)
    pm.parent(R_featherStartJntList[13], R_wing02Jnt)

    # end_3_FeatherJoint (joints 0-3 parent to r_wing03_JNT)
    pm.parent(R_featherStartJntList[0], R_wing03Jnt)
    pm.parent(R_featherStartJntList[1], R_wing03Jnt)
    pm.parent(R_featherStartJntList[2], R_wing03Jnt)
    pm.parent(R_featherStartJntList[3], R_wing03Jnt)
    pm.parent(R_featherStartJntList[4], R_wing03Jnt)
    pm.parent(R_featherStartJntList[5], R_wing03Jnt)
    pm.parent(R_featherStartJntList[6], R_wing03Jnt)
    pm.parent(R_featherStartJntList[7], R_wing03Jnt)

    # lets orient the full wing joints
    # orient L arm chain joints
    pm.select(R_wing01Jnt)
    OrientSelectedJoints(R_wing01Jnt)

    # NOW THAT THE START JOINTS ARE ORIENTED WE CAN DUPE IT AND CREATE A SINGLE ADJUST JNT WITH MATCHING PIVOT
    # making sure our adjust joint matches the pivot of our start feather joint (by duplicating)
    R_featherAdjustJntList = []
    R_featherAdjustCtrlList = []
    R_featherAdjustCtrlAllGrps = cmds.group(em=True, n='R_featherAdjustCtrlAll_GRP')

    for x in range(0, 19):
        # transForAdjustJnt = pm.xform(featherStartJnt[x], q=True, ws=True, rp=True)
        featherName = 'r_feather_' + str(x)
        cmds.select(R_featherStartJntList[x])
        duped = cmds.duplicate(parentOnly=True, n=featherName + '_adjust_JNT')
        R_featherAdjustJntList.append(duped)
        cmds.parent(R_featherAdjustJntList[x], R_featherStartJntList[x])
        cmds.select(d=True)

        # create ctrl for adjust joint
        featherToAdd = CreatePyramidRigCtrl(featherName + '_adjust_jnt_CTRL', R_featherAdjustJntList[x], R_featherStartJntList[x])
        R_featherAdjustCtrlList.append(featherToAdd)
        cmds.parent(R_featherAdjustCtrlList[x],R_featherAdjustCtrlAllGrps)


    redColor(R_featherAdjustCtrlAllGrps)
    # #Group all of the feather adjustment ctrl groups into 1 group
    # cmds.select(R_featherAdjustCtrlList, all=True)
    # R_allFeatherAdjustmentCtrlGrps = cmds.group(n='R_featherAdjustCtrlList_GRP')
    # blueColor(R_allFeatherAdjustmentCtrlGrps[x])

    # creating wing ctrl
    R_wing01Ctrl = CreateSphereRigCtrl('r_wing01_CTRL')
    redColor(R_wing01Ctrl[0])
    R_wing01CtrlGrp = pm.group(R_wing01Ctrl, n='r_wing01_Ctrr_GRP')
    pm.scale(R_wing01CtrlGrp, [4, 4, 4])
    cnstr = pm.parentConstraint(R_wing01Jnt, R_wing01CtrlGrp)  # (moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    R_wing02Ctrl = CreateSphereRigCtrl('r_wing02_CTRL')
    redColor(R_wing02Ctrl[0])
    R_wing02CtrlGrp = pm.group(R_wing02Ctrl, n='r_wing02_Ctrr_GRP')
    pm.scale(R_wing02CtrlGrp, [4, 4, 4])
    cnstr = pm.parentConstraint(R_wing02Jnt, R_wing02CtrlGrp)  # (moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    R_wing03Ctrl = CreateSphereRigCtrl('r_wing03_CTRL')
    redColor(R_wing03Ctrl[0])
    R_wing03CtrlGrp = pm.group(R_wing03Ctrl, n='r_wing03_Ctrr_GRP')
    pm.scale(R_wing03CtrlGrp, [4, 4, 4])
    cnstr = pm.parentConstraint(R_wing03Jnt, R_wing03CtrlGrp)  # (moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    # create the sub fk ctrl for the 3 main driver feathers
    R_feather03Ctrl = CreateFeatherSquareRigCtrl(R_featherStartJntList[0], R_featherEndJntList[0], 'r_feather03_CTRL')
    redColor(R_feather03Ctrl)
    pm.select(d=True)
    R_feather03CtrlGrp = pm.group(n='r_feather03_Grp')
    pm.parent(R_feather03Ctrl, R_feather03CtrlGrp)
    cnstr = pm.parentConstraint(R_featherStartJntList[0], R_feather03CtrlGrp)  # (moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    R_feather02Ctrl = CreateFeatherSquareRigCtrl(R_featherStartJntList[7], R_featherEndJntList[7], 'r_feather02_CTRL')
    redColor(R_feather02Ctrl)
    pm.select(d=True)
    R_feather02CtrlGrp = pm.group(n='r_feather02_Grp')
    pm.parent(R_feather02Ctrl, R_feather02CtrlGrp)
    cnstr = pm.parentConstraint(R_featherStartJntList[7], R_feather02CtrlGrp)  # (moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    R_feather01Ctrl = CreateFeatherSquareRigCtrl(R_featherStartJntList[18], R_featherEndJntList[18], 'r_feather01_CTRL')
    redColor(R_feather01Ctrl)
    pm.select(d=True)
    R_feather01CtrlGrp = pm.group(n='r_feather01_Grp')
    pm.parent(R_feather01Ctrl, R_feather01CtrlGrp)
    cnstr = pm.parentConstraint(R_featherStartJntList[18], R_feather01CtrlGrp)  # (moveTo, moveThis)
    pm.delete(cnstr)
    pm.select(d=True)

    # parent constraint L arm ctrls
    pm.parentConstraint(R_wing01Ctrl, R_wing01Jnt)
    pm.parentConstraint(R_wing02Ctrl, R_wing02Jnt)
    pm.parentConstraint(R_wing03Ctrl, R_wing03Jnt)

    # parent constraint L feather ctrls
    pm.parentConstraint(R_feather03Ctrl, R_featherStartJntList[0])
    pm.parentConstraint(R_feather02Ctrl, R_featherStartJntList[7])
    pm.parentConstraint(R_feather01Ctrl, R_featherStartJntList[18])

    # parent constraint the L ctrls to one another
    pm.select(d=True)
    pm.parent(R_feather03CtrlGrp, R_wing03Ctrl[0])
    pm.parent(R_feather02CtrlGrp, R_wing03Ctrl[0])
    pm.parent(R_feather01CtrlGrp, R_wing01Ctrl[0])
    pm.parent(R_wing03CtrlGrp, R_wing02Ctrl[0])
    pm.parent(R_wing02CtrlGrp, R_wing01Ctrl[0])
    pm.parent(R_wing01CtrlGrp, spineCtrl1)#dandan R

    # blend outer feathers to main feathers
    # (featherBlendMax, featherBlendMin, FeatherBlend, node number)
    # (featherEndStartJnt, featherMidStartJnt, BlendFeatherStartJnt, nodeNumber)
    BlendOuterFeather(R_featherStartJntList[0], R_featherStartJntList[7], R_featherStartJntList[1], 1,'R_')
    BlendOuterFeather(R_featherStartJntList[0], R_featherStartJntList[7], R_featherStartJntList[2], 2,'R_')
    BlendOuterFeather(R_featherStartJntList[0], R_featherStartJntList[7], R_featherStartJntList[3], 3,'R_')
    BlendOuterFeather(R_featherStartJntList[0], R_featherStartJntList[7], R_featherStartJntList[4], 4,'R_')
    BlendOuterFeather(R_featherStartJntList[0], R_featherStartJntList[7], R_featherStartJntList[5], 5,'R_')
    BlendOuterFeather(R_featherStartJntList[0], R_featherStartJntList[7], R_featherStartJntList[6], 6,'R_')

    # blend inner feathers    (start // end // blendThis // cnstraintNumber)

    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[8], 5)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[9], 6)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[10], 7)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[11], 8)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[12], 9)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[13], 10)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[14], 11)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[15], 12)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[16], 13)
    BlendInnerFeather(R_featherStartJntList[18], R_featherStartJntList[7], R_featherStartJntList[17], 14)

    # creating curve that will allow us to sculpt end of feathers of the wing with clusters
    point1 = cmds.xform(R_featherEndJntList[0], q=True, ws=True, rp=True)
    point2 = cmds.xform(R_featherEndJntList[7], q=True, ws=True, rp=True)
    point3 = cmds.xform(R_featherEndJntList[13], q=True, ws=True, rp=True)
    point4 = cmds.xform(R_featherEndJntList[18], q=True, ws=True, rp=True)
    R_featherShaperCurve = cmds.curve(d=3, p=[(point1[0], point1[1], point1[2]),
                                            (point2[0], point2[1], point2[2]),
                                            (point3[0], point3[1], point3[2]),
                                            (point4[0], point4[1], point4[2])], k=(0, 0, 0, 1, 1, 1),
                                    n='R_feather_Shaper_curve')

    #group all feather shaper curves (left and right)
    featherShapersGrp = cmds.group(L_featherShaperCurve,R_featherShaperCurve, n='featherShapers_GRP')

    #lets create an empty group that we will use to grp our clusters
    R_ClusterCtrlAllGrps = cmds.group(em=True, n='R_ClusterCtrlAll_GRP')
    R_ClusterHandleGrp = cmds.group(em=True, n='R_ClusterHandleGrp_GRP')
    R_WingSystemGrp = cmds.group(em=True, n='R_WingSystem_GRP')


    # create 4 ctrls for the 4 clusters we are about to make
    cmds.select(d=True)
    R_featherCluster1Ctrl = CreateSphereRigCtrl('R_feather_Cluster1_CTRL')
    redColor(R_featherCluster1Ctrl[0])
    R_featherCluster1CtrlGrp = cmds.group(R_featherCluster1Ctrl, n='R_featherCluster1CtrlGrp')
    constr = cmds.pointConstraint(R_featherEndJntList[18], R_featherCluster1CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(R_featherCluster1CtrlGrp + '.scaleX', 2)
    cmds.setAttr(R_featherCluster1CtrlGrp + '.scaleY', 2)
    cmds.setAttr(R_featherCluster1CtrlGrp + '.scaleZ', 2)

    cmds.select(d=True)
    R_featherCluster2Ctrl = CreateSphereRigCtrl('R_feather_Cluster2_CTRL')
    redColor(R_featherCluster2Ctrl[0])
    R_featherCluster2CtrlGrp = cmds.group(R_featherCluster2Ctrl, n='R_featherCluster2CtrlGrp')
    constr = cmds.pointConstraint(R_featherEndJntList[13], R_featherCluster2CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(R_featherCluster2CtrlGrp + '.scaleX', 2)
    cmds.setAttr(R_featherCluster2CtrlGrp + '.scaleY', 2)
    cmds.setAttr(R_featherCluster2CtrlGrp + '.scaleZ', 2)

    cmds.select(d=True)
    R_featherCluster3Ctrl = CreateSphereRigCtrl('R_feather_Cluster3_CTRL')
    redColor(R_featherCluster3Ctrl[0])
    R_featherCluster3CtrlGrp = cmds.group(R_featherCluster3Ctrl, n='R_featherCluster3CtrlGrp')
    constr = cmds.pointConstraint(R_featherEndJntList[7], R_featherCluster3CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(R_featherCluster3CtrlGrp + '.scaleX', 2)
    cmds.setAttr(R_featherCluster3CtrlGrp + '.scaleY', 2)
    cmds.setAttr(R_featherCluster3CtrlGrp + '.scaleZ', 2)

    cmds.select(d=True)
    R_featherCluster4Ctrl = CreateSphereRigCtrl('R_feather_Cluster4_CTRL')
    redColor(R_featherCluster4Ctrl[0])
    R_featherCluster4CtrlGrp = cmds.group(R_featherCluster4Ctrl, n='R_featherCluster4CtrlGrp')
    constr = cmds.pointConstraint(R_featherEndJntList[0], R_featherCluster4CtrlGrp)
    cmds.delete(constr)
    cmds.setAttr(R_featherCluster4CtrlGrp + '.scaleX', 2)
    cmds.setAttr(R_featherCluster4CtrlGrp + '.scaleY', 2)
    cmds.setAttr(R_featherCluster4CtrlGrp + '.scaleZ', 2)



    # create the needed clusters and attach them to our 4 cv points
    # cmds.select(featherShaperCurve+'.controlPoints[0]')
    R_featherCluster1 = cmds.cluster(R_featherShaperCurve + '.controlPoints[3]', n='R_feather_cluster1')
    R_featherCluster1Grp = cmds.group(n='R_feather_cluster1_GRP')
    R_featherCluster2 = cmds.cluster(R_featherShaperCurve + '.controlPoints[2]', n='R_feather_cluster2')
    R_featherCluster2Grp = cmds.group(n='R_feather_cluster2_GRP')
    R_featherCluster3 = cmds.cluster(R_featherShaperCurve + '.controlPoints[1]', n='R_feather_cluster3')
    R_featherCluster3Grp = cmds.group(n='R_feather_cluster3_GRP')
    R_featherCluster4 = cmds.cluster(R_featherShaperCurve + '.controlPoints[0]', n='R_feather_cluster4')
    R_featherCluster4Grp = cmds.group(n='R_feather_cluster4_GRP')

    # parent constraint clusters to our cluster ctrls
    cmds.parentConstraint(R_featherCluster1Ctrl, R_featherCluster1, mo=True)
    cmds.parentConstraint(R_featherCluster2Ctrl, R_featherCluster2, mo=True)
    cmds.parentConstraint(R_featherCluster3Ctrl, R_featherCluster3, mo=True)
    cmds.parentConstraint(R_featherCluster4Ctrl, R_featherCluster4, mo=True)

    # parent constraint the cluster grp to corresponding wing arm ctrler
    cmds.parentConstraint(R_feather03Ctrl, R_featherCluster4CtrlGrp, mo=True)
    cmds.parentConstraint(R_wing03Ctrl, R_featherCluster3CtrlGrp, mo=True)
    cmds.parentConstraint(R_wing02Ctrl, R_featherCluster2CtrlGrp, mo=True)
    cmds.parentConstraint(R_wing01Ctrl, R_featherCluster1CtrlGrp, mo=True)


    cmds.parent(R_featherCluster1CtrlGrp,R_featherCluster2CtrlGrp,R_featherCluster3CtrlGrp,R_featherCluster4CtrlGrp,R_ClusterCtrlAllGrps)
    cmds.parent(R_featherCluster1Grp, R_featherCluster2Grp, R_featherCluster3Grp, R_featherCluster4Grp,R_ClusterHandleGrp)
    cmds.parent(R_ClusterCtrlAllGrps,R_ClusterHandleGrp,R_featherAdjustCtrlAllGrps,R_WingSystemGrp)
    cmds.parent(R_WingSystemGrp, wingLeftAndRightSystemGrp)
    cmds.parent(wingLeftAndRightSystemGrp, rigGrp)

    #lets group the ctrls and our shapers under a new parent
    cmds.group(featherShapersGrp,worldCtrl, n='deer')



def deleteButton():
    # first delete all objects in scene before creating this rig again
    cmds.select(all=True)
    cmds.delete()



def ui():
    if cmds.window('autoRigWindow', exists=True):
        cmds.deleteUI('autoRigWindow')

    rigWin = cmds.window('autoRigWindow')
    cmds.columnLayout( adjustableColumn=True )

    cmds.button(label='STEP1: BODY LOCATORS', command='SetBodyLocatorsButton()', w=200, h=75)
    cmds.button(label='STEP2: BODY RIG', command='CreateBodyRigButton()', w=200, h=75)
    cmds.button(label='STEP3: WING LOCATORS', command='SetLeftWingLocatorsButton(),SetRightWingLocatorsButton()', w=200, h=75)
    cmds.button(label='STEP4: WING JOINTS', command='CreateLeftWingJointButton(),CreateRightWingJointButton()', w=200, h=75)

    cmds.button(label='DELETE', command='deleteButton()', w=200, h=75)
    cmds.showWindow('autoRigWindow')

ui()


