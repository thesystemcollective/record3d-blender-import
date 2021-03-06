import zipfile
import os, json
import bpy, mathutils

def importJson(fileName):
  dir = os.path.dirname(bpy.data.filepath)

  fileName = os.path.join(dir,fileName)

  # make sure the provided file exists
  if not os.path.exists(fileName):
    print('this file does not exist.')
    return

  with zipfile.ZipFile(fileName) as archive:
    with archive.open('metadata') as metadata:
      jsonData = json.load(metadata)

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
    qx, qy, qz, qw, px, py, pz = json[i]

    (px, py, pz) = (px, pz, -py)
    (qx, qy, qz) = (qx, qz, -qy)

    wxyz = mathutils.Vector([qw, qx, qy, qz])

    # apply rotation to quaternion animation
    quat = mathutils.Quaternion(wxyz)

    pos = mathutils.Vector([px, py, pz])

#    print('set keyframe pos', i, 'to', pos)

#    realI = i + 1

    obj.location = pos
    obj.keyframe_insert(data_path='location', frame=i, index=0)
    obj.keyframe_insert(data_path='location', frame=i, index=1)
    obj.keyframe_insert(data_path='location', frame=i, index=2)

    obj.rotation_quaternion = quat
    obj.keyframe_insert(data_path='rotation_quaternion', frame=i, index=0)
    obj.keyframe_insert(data_path='rotation_quaternion', frame=i, index=1)
    obj.keyframe_insert(data_path='rotation_quaternion', frame=i, index=2)
    obj.keyframe_insert(data_path='rotation_quaternion', frame=i, index=3)
#    print('set keyframe rot', i, 'to', obj.rotation_quaternion)

  obj.location = old_pos
  obj.rotation_euler = old_rot

  print('finished creating keyframes')

json = importJson('data.r3d')
removeActions()
recreateActions(json)
