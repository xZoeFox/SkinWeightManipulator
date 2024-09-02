import maya.cmds as cmds
import re
import time

def loadVertexWeightsFromFile(file_path):
    joint_list = []
    vertex_weights_data = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    joint_list_section = False
    skin_weight_section = False
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line == "# Joint list":
            joint_list_section = True
            i += 1
            continue
        elif line == "# Joint list ends":
            joint_list_section = False
            i += 1
            continue
        elif line == "# skin weight begins":
            skin_weight_section = True
            i += 1
            continue
        elif line == "# skin weight ends":
            skin_weight_section = False
            i += 1
            continue

        if joint_list_section:
            joint_list.extend(line.split())
        elif skin_weight_section:
            match = re.match(r'\[(\d+)\]', line)
            if match:
                vertex_index = match.group(1)
                i += 1
                if i < len(lines):
                    joints_line = lines[i].strip()
                i += 1
                if i < len(lines):
                    weights_line = lines[i].strip()
                
                joints = joints_line.split()
                weights = list(map(float, weights_line.split()))
                
                # Normalize weights if their sum exceeds 1.0
                total_weight = sum(weights)
                if total_weight > 1.0:
                    weights = [w / total_weight for w in weights]

                vertex_weights_data[vertex_index] = dict(zip(joints, weights))

        i += 1

    return joint_list, vertex_weights_data

def resetSkinWeights(obj):
    # Find the skinCluster of the selected object
    skin_clusters = cmds.ls(cmds.listHistory(obj), type='skinCluster')
    if not skin_clusters:
        print("The selected object is not skinned with a skinCluster.")
        return
    
    skin_cluster = skin_clusters[0]
    
    # Get all vertices
    vertices = cmds.ls(cmds.polyListComponentConversion(obj, toVertex=True), flatten=True)

    # Reset weights for each vertex to zero
    for vertex in vertices:
        cmds.skinPercent(skin_cluster, vertex, transformValue=[(joint, 0.0) for joint in cmds.skinCluster(skin_cluster, query=True, influence=True)])

def applyVertexWeights(file_path):
    joint_list, vertex_weights_data = loadVertexWeightsFromFile(file_path)
    print("Starting to apply vertex weights")
    start_time = time.time()
    
    # Check if an object is selected
    selected_objects = cmds.ls(selection=True, long=True)
    if not selected_objects:
        print("No object selected.")
        return
    obj = selected_objects[0]
    # Reset skin weights
    #resetSkinWeights(obj)
    
    # Find the skinCluster of the selected object
    skin_clusters = cmds.ls(cmds.listHistory(obj), type='skinCluster')
    if not skin_clusters:
        print("The selected object is not skinned with a skinCluster.")
        return
    
    skin_cluster = skin_clusters[0]
    cmds.skinCluster(skin_cluster, e=True, nw=2)
    joints_in_skin_cluster = cmds.skinCluster(skin_cluster, query=True, influence=True)
    if set(joint_list) != set(joints_in_skin_cluster):
        print("Joint list does not match the joints in the skinCluster.")
        return
    
    # Apply the weights
    for vertex_index, weights in vertex_weights_data.items():
        vertex = "{}.vtx[{}]".format(obj, vertex_index)
        weight_values = [weights.get(joint, 0.0) for joint in joints_in_skin_cluster]
        
        # Normalize weights if their sum exceeds 1.0
        total_weight = sum(weight_values)
        if total_weight > 1.0:
            weight_values = [w / total_weight for w in weight_values]
        
        # Apply the weights to the vertex
        cmds.skinPercent(skin_cluster, vertex, transformValue=list(zip(joints_in_skin_cluster, weight_values)))

    cmds.skinCluster(skin_cluster, e=True, nw=1)

    end_time = time.time()
    print("Vertex weights applied successfully in {:.2f} seconds".format(end_time - start_time))

def applyWeightsToSelectedVertices(file_path):
    joint_list, vertex_weights_data = loadVertexWeightsFromFile(file_path)
    print("Starting to apply vertex weights to selected vertices")
    start_time = time.time()
    
    # Check if an object is selected
    selected_objects = cmds.ls(selection=True, long=True)
    if not selected_objects:
        print("No object selected.")
        return
    
    obj = selected_objects[0]
    
    # Check if vertices are selected
    selected_vertices = cmds.ls(selection=True, fl=True)
    if not selected_vertices:
        print("No vertices selected.")
        return
    
    # Find the skinCluster of the selected object
    skin_clusters = cmds.ls(cmds.listHistory(obj), type='skinCluster')
    if not skin_clusters:
        print("The selected object is not skinned with a skinCluster.")
        return
    
    skin_cluster = skin_clusters[0]
    cmds.skinCluster(skin_cluster, e=True, nw=2)
    joints_in_skin_cluster = cmds.skinCluster(skin_cluster, query=True, influence=True)
    if set(joint_list) != set(joints_in_skin_cluster):
        print("Joint list does not match the joints in the skinCluster.")
        return
    
    # Apply the weights only to selected vertices
    for vertex in selected_vertices:
        vertex_index = vertex.split('[')[1].split(']')[0]
        if vertex_index in vertex_weights_data:
            weights = vertex_weights_data[vertex_index]
            weight_values = [weights.get(joint, 0.0) for joint in joints_in_skin_cluster]
            
            # Normalize weights if their sum exceeds 1.0
            total_weight = sum(weight_values)
            if total_weight > 1.0:
                weight_values = [w / total_weight for w in weight_values]
            
            # Apply the weights to the vertex
            cmds.skinPercent(skin_cluster, vertex, transformValue=list(zip(joints_in_skin_cluster, weight_values)))

    cmds.skinCluster(skin_cluster, e=True, nw=1)

    end_time = time.time()
    print("Vertex weights applied to selected vertices successfully in {:.2f} seconds".format(end_time - start_time))

def loadJointListFromFile(file_path):
    joint_list = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    joint_list_section = False
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line == "# Joint list":
            joint_list_section = True
            i += 1
            continue
        elif line == "# Joint list ends":
            joint_list_section = False
            i += 1
            continue

        if joint_list_section:
            joint_list.extend(line.split())

        i += 1

    return joint_list

def selectJointsFromFile(file_path):
    joint_list = loadJointListFromFile(file_path)
    
    if not joint_list:
        print("No joints found in the file.")
        return

    # Deselect all objects
    cmds.select(clear=True)

    # Select joints
    for joint in joint_list:
        if cmds.objExists(joint):
            cmds.select(joint, add=True)
        else:
            print("Joint {} does not exist in the scene.".format(joint))

    if cmds.ls(selection=True):
        print("Joints selected successfully.")
    else:
        print("No joints selected.")
