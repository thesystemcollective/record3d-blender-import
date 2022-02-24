import zipfile
import os, json, math, sys
import bpy, mathutils

def importJson (fileName):
    dir = os.path.dirname(bpy.data.filepath)

    fileName = os.path.join(dir,fileName)

    # make sure the provided file exists
    if not os.path.exists(fileName):
        print('this file does not exist.')
        return

    fin = open(fileName, 'r')
    jsonData = json.load(fin)
    fin.close()

    print('loaded and parsed json file')

    return jsonData['poses']

def removeActions():
    actions = bpy.data.actions

    for actionname in actions.keys():
        if actionname.startswith('record3D'):
            actions.remove(actions[actionname])
            print('removed record3D action')

def recreateActions(json):
    obj = bpy.context.object

    old_pos = obj.location
    old_rot = obj.rotation_euler

    # delete the action if it exists
    obj.animation_data_clear()

    obj.animation_data_create()
    obj.animation_data.action = bpy.data.actions.new(name='record3D')
    print('recreated record3D action')

    fcu_x = obj.animation_data.action.fcurves.new(data_path='location', index=0)
    fcu_y = obj.animation_data.action.fcurves.new(data_path='location', index=1)
    fcu_z = obj.animation_data.action.fcurves.new(data_path='location', index=2)

    for i in range(len(json)):
        rawPos = json[i]

        wxyz = mathutils.Vector([rawPos[0], rawPos[1], rawPos[2], rawPos[3]])

        # apply rotation to quaternion animation
        quat = mathutils.Quaternion(wxyz)

        pos = mathutils.Vector([rawPos[4], rawPos[5], rawPos[6]])

        print('set keyframe pos', i, 'to', pos)

        realI = i + 1

        obj.location = pos
        obj.keyframe_insert(data_path='location', frame=i, index=0)
        obj.keyframe_insert(data_path='location', frame=i, index=1)
        obj.keyframe_insert(data_path='location', frame=i, index=2)

        obj.rotation_euler = quat.to_euler()
        obj.keyframe_insert(data_path='rotation_euler', frame=i, index=0)
        print('set keyframe rot', i, 'to', obj.rotation_euler)

    obj.location = old_pos
    obj.rotation_euler = old_rot

    print('finished creating keyframes')

json = importJson('metadata.json')
removeActions()
recreateActions(json)
