import maya.cmds as cmds
import re  
import os 

def saveVertexWeightsToFile(filename='vertex_weights.ma'):
    # Get the list of selected objects
    selected_objects = cmds.ls(selection=True, long=True)
    
    if not selected_objects:
        print("No objects selected.")
        return

    # Initialize data structures
    joint_list = set()
    vertex_weights_data = []

    # Iterate over selected objects
    for obj in selected_objects:
        # Find the skin cluster attached to the object
        skin_clusters = cmds.ls(cmds.listHistory(obj), type='skinCluster')
        
        if not skin_clusters:
            print("Object '{}' is not skinned with a skinCluster.".format(obj))
            continue
        
        # Assume the first skinCluster in the list is the one we're interested in
        skin_cluster = skin_clusters[0]
        
        # Get joints influenced by the skinCluster
        joints = cmds.skinCluster(skin_cluster, query=True, influence=True)
        joint_list.update(joints)
        
        if not joints:
            print("No joints found in skinCluster '{}'.".format(skin_cluster))
            continue
        
        # Get vertex list
        vertices = cmds.ls(cmds.polyListComponentConversion(obj, toVertex=True), flatten=True)
        
        # Iterate over vertices
        for vertex in vertices:
            # Extract vertex index number from the format "head_LOD0_geo.vtx[1914]"
            match = re.search(r'\[([0-9]+)\]', vertex)
            if match:
                vertex_index = match.group(1)
                
                # Get the weights for the vertex
                weights = cmds.skinPercent(skin_cluster, vertex, query=True, value=True)
                
                # Filter out joints with zero weights
                filtered_weights = [w for w in weights if w > 0]
                
                # Collect weights for the vertex if any non-zero weight is present
                if filtered_weights:
                    weight_str = " ".join("{:.4f}".format(w) for w in filtered_weights)  # Format weights to 4 decimal places
                    # Filter the joint list to only include joints with non-zero weights
                    active_joints = [joint for joint, weight in zip(joints, weights) if weight > 0]
                    if active_joints:
                        vertex_weights_data.append((vertex_index, weight_str, active_joints))
    
    # Format joint list as a space-separated string
    joint_list = sorted(joint_list)
    
    # Ensure the directory exists
    directory = os.path.dirname(filename)
    if not os.path.exists(directory) and directory:
        os.makedirs(directory)

    # Write data to file
    with open(filename, 'w') as file:
        # Write joint list
        file.write("#starting of skinWeight data\n")
        file.write("# Joint list\n")
        file.write(" ".join(joint_list) + "\n")
        file.write("# Joint list ends\n")
        
        # Write vertex weights data
        file.write("# skin weight begins\n")
        for vertex_index, weights, active_joints in vertex_weights_data:
            file.write("[{}]\n".format(vertex_index))
            file.write(" ".join(active_joints) + "\n")
            file.write(weights + "\n")
        file.write("#end of skinWeight data\n")

    print("Data saved to {}".format(filename))
