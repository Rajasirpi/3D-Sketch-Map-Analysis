import json
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import itertools
import Rhino.Geometry as rg

def generate_result():
    
    def find_connections(layer_name):
        # Get all objects on the specified layer
        objects = rs.ObjectsByLayer(layer_name)
    
        # Initialize dictionaries to store points
        coor = {}
    
        # Iterate over each object
        for obj in objects:
            # Check if the object has a user text 'ID'
            if rs.GetUserText(obj, 'ID'):
                # Get the ID value
                object_id = rs.GetUserText(obj, 'ID')
                
                # Get the object's geometry as a RhinoCommon object
                geometry = rs.coercegeometry(obj)
    
                # Check if the geometry is an extrusion
                if isinstance(geometry, Rhino.Geometry.Extrusion) or isinstance(geometry, Rhino.Geometry.Brep):
                    # Get the eight corner points
                    if isinstance(geometry, Rhino.Geometry.Extrusion):
                        corner_points = geometry.GetBoundingBox(True).GetCorners()
                    else:  # Handle polysurfaces
                        brep = Rhino.Geometry.Brep.TryConvertBrep(geometry)
                        if brep:
                            corner_points = brep.GetBoundingBox(True).GetCorners()
                        else:
                            continue 
 
                    # Convert the points to a list of coordinates
                    corner_points = [[round(point.X, 6), round(point.Y, 6), round(point.Z, 6)] for point in corner_points]
                    
                    # Store the corner points in the dictionary
                    coor[object_id] = corner_points
                    
                # Check if the geometry is a surface using rs.IsSurface()
                elif rs.IsSurface(obj):
                    # Get the surface points
                    surface_pts = rs.SurfacePoints(obj)
    
                    if surface_pts:
                        # Convert the points to a list of coordinates
                        surface_pts = [[round(point.X, 6), round(point.Y, 6), round(point.Z, 6)] for point in surface_pts]
                        
                        # Store the surface points in the dictionary
                        coor[object_id] = surface_pts
    
        # Create a dictionary to store the final result
        result = {
            "coordinates": coor
        }
    
        # Convert the result to JSON format
        data = json.dumps(result, indent=4)
    
        #Parse the JSON data into a dictionary
        data_dict = json.loads(data)
    
        # Extract the extrusion points from the data dictionary
        points = data_dict["coordinates"]

        #Get the IDs of the extrusion points
        ids = list(points.keys())
    
        connections = [] 
        
        for original_id in ids:
            target_connections = []
            
            for target_id in ids:
                if original_id != target_id:  # Skip comparing with the same ID
                    num_matching_points = sum(1 for x, y in itertools.product(points[original_id], points[target_id]) if x == y)
                    
                    if num_matching_points == 4:
                        target_connections.append({
                            "id": target_id,
                            "Connection Type": "surface"
                        })
                    elif num_matching_points == 2:
                        target_connections.append({
                            "id": target_id,
                            "Connection Type": "edge or partial surface"
                        })
                    elif num_matching_points == 1:
                        target_connections.append({
                            "id": target_id,
                            "Connection Type": "point"
                        })
                        
            if target_connections:  # Check if any target IDs found
                connections.append({
                    "Original id": original_id,
                    "Target ids": target_connections
                })
                
        return connections

    def find_point_intersection(layer_name):
        objects = rs.ObjectsByLayer(layer_name)
    
        # Get the IDs of point objects in the layer
        point_ids = [obj for obj in objects if rs.IsPoint(obj)]
    
        # Create dictionaries to store extrusion information
        extrusion_ids = {}
        extrusion_types = {}
    
        # Find extrusions associated with the points and retrieve ID and type values
        for point_id in point_ids:
            point_coords = rs.PointCoordinates(point_id)
            extrusions = []
            for obj in objects:
                if rs.ObjectType(obj) == rs.filter.extrusion or rs.ObjectType(obj) == rs.filter.polysurface:
                    if rs.IsPolysurface(obj):
                        extrusion = rs.coercebrep(obj)
                        is_inside = extrusion.IsPointInside(point_coords, rs.UnitAbsoluteTolerance(), False)
                        if is_inside:
                            extrusions.append(obj)
                    else:
                        extrusion = rs.coercegeometry(obj)
                        brep = extrusion.ToBrep()
                        is_inside = brep.IsPointInside(point_coords, rs.UnitAbsoluteTolerance(), False)
                        if is_inside:
                            extrusions.append(obj)
                    
    
            if extrusions:
                # Get the ID from the user attribute text of the point
                point_id_attr = rs.GetUserText(point_id, 'ID')
                if point_id_attr:
                    extrusion_ids[point_id_attr] = extrusions
    
                    # Get the 'type' attribute value
                    extrusion_type = rs.GetUserText(point_id, 'type')
                    if extrusion_type:
                        extrusion_types[point_id_attr] = extrusion_type
    
        # Create a result dictionary
        result_dict = {}
        for point_id, extrusions in extrusion_ids.items():
            extrusion_data = []
            for extrusion in extrusions:
                extrusion_id = rs.GetUserText(extrusion, 'ID')
                extrusion_type = extrusion_types.get(point_id, "No type available")
                extrusion_data.append({"Extrusion ID": extrusion_id, "Type": extrusion_type})
            result_dict[point_id] = extrusion_data
    
        return result_dict
    
    def is_surface_inside_polysurface(layer_name):
        # Get all objects on the specified layer
        objects = rs.ObjectsByLayer(layer_name)
        
        # Get all surface objects in the model
        surface_objects = rs.ObjectsByType(rs.filter.surface)
        
        # Initialize dictionaries to store surface and polysurface IDs
        surface_ids = {}
        polysurface_ids = {}
    
        # Find surface and polysurface IDs based on user attribute text
        for obj in objects:
            # Check if the object has a user attribute text 'ID'
            if rs.GetUserText(obj, 'ID'):
                # Get the ID value
                object_id = rs.GetUserText(obj, 'ID')
    
                # Check if the object is a surface and in the surface_objects list
                if obj in surface_objects:
                    surface_ids[object_id] = obj
    
                # Check if the object is a polysurface using rs.IsObjectSolid()
                if rs.IsPolysurface(obj):
                    polysurface_ids[object_id] = obj
    
    #     Create a dictionary to store the connections
        connections = {}
    
        def find_inside_relationship(surface_id, polysurface_id):
            if surface_id not in connections:
                connections[surface_id] = {"Connection": []}
    
            connections[surface_id]["Connection"].append("ID {} is inside ID {}".format(surface_id, polysurface_id))
    
            if polysurface_id in surface_inside_polysurface:
                new_polysurface_id = surface_inside_polysurface[polysurface_id]
                find_inside_relationship(surface_id, new_polysurface_id)
                
    
        # Iterate over each surface and check if it is inside any of the polysurfaces
        surface_inside_polysurface = {}
        
        for surface_id, surface_obj in surface_ids.items():
            surface = rs.coercesurface(surface_obj)
            inside_polysurfaces = []
    
            for polysurface_id, polysurface_obj in polysurface_ids.items():
                polysurface = rs.coercebrep(polysurface_obj)
    
                # Create a Brep from the surface
                brep = rg.Brep.CreateFromSurface(surface)
    
                # Check if any of the BrepFaces are inside the polysurface
                for face in brep.Faces:
                    mid_u = face.Domain(0).Mid
                    mid_v = face.Domain(1).Mid
                    point = face.PointAt(mid_u, mid_v)
    
                    result = polysurface.IsPointInside(point, sc.doc.ModelAbsoluteTolerance, False)
                    if result:
                        inside_polysurfaces.append(polysurface_id)
                        break
    
            if inside_polysurfaces:
                surface_inside_polysurface[surface_id] = inside_polysurfaces
    
        # Find all hierarchical relationships using the recursive function
        for surface_id, polysurface_ids_list in surface_inside_polysurface.items():
            for polysurface_id in polysurface_ids_list:
                find_inside_relationship(surface_id, polysurface_id)
                
        stair_connections = {}
        for surface_id, connection_data in connections.items():
            stair_connections[surface_id] = {"Connection": connection_data["Connection"]}
    
        return stair_connections
    
    def check_surface_connection(layer_name):
        layer_id = rs.LayerName(layer_name)
        if layer_id is None:
            return {"Connection": "Layer not found."}
    
        objects = rs.ObjectsByLayer(layer_id)
        surface_ids = []
        for obj in objects:
            if rs.ObjectType(obj) == 8:  # Check if object type is not extrusion (8).
                surface_ids.append(obj)
    
        if len(surface_ids) < 2:
            return {"Connection": "Not enough surfaces in the layer."}
    
        connection_info = {"Connection": []}
    
        # Find connected surfaces based on proximity of corner points
        for i in range(len(surface_ids)):
            surface_id_1 = surface_ids[i]
            surface_1_corners = rs.SurfaceEditPoints(surface_id_1)
    
            for j in range(i + 1, len(surface_ids)):
                surface_id_2 = surface_ids[j]
                surface_2_corners = rs.SurfaceEditPoints(surface_id_2)
    
                # Check if any corner points of surface 1 are within a distance threshold to any corner points of surface 2
                connection_found = False
                for corner_1 in surface_1_corners:
                    for corner_2 in surface_2_corners:
                        if corner_1.DistanceTo(corner_2) < rs.UnitAbsoluteTolerance():
                            connection_found = True
                            break
                    if connection_found:
                        break
    
                if connection_found:
                    attr_id_1 = rs.GetUserText(surface_id_1, "ID")
                    attr_id_2 = rs.GetUserText(surface_id_2, "ID")
                    connection_info["Connection"].append("ID {} is connected to ID {}".format(attr_id_1, attr_id_2))
    
        if not connection_info["Connection"]:
            connection_info["Connection"].append("No connections found between surfaces in the layer.")
    
        return connection_info
  
    def check_cubevscube_connection(layer_name):
        def are_corners_inside(cube, big_cube):
            tol = rs.UnitAbsoluteTolerance()
            cube_corners = cube.GetBoundingBox(True).GetCorners()
            for corner in cube_corners:
                if not big_cube.IsPointInside(corner, tol, False):
                    return False
            return True
    
        layer_id = rs.LayerName(layer_name)
        if layer_id is None:
            return {"Connection": "Layer not found."}
    
        objects = rs.ObjectsByLayer(layer_id)
        polysurface_ids = {}
    
        # Find surface and polysurface IDs based on user attribute text
        for obj in objects:
            # Check if the object has a user attribute text 'ID'
            if rs.GetUserText(obj, 'ID'):
                # Get the ID value
                object_id = rs.GetUserText(obj, 'ID')
    
                # Check if the object is a polysurface using rs.IsObjectSolid()
                if rs.IsPolysurface(obj) or rs.ObjectType(obj) == 1073741824:
                    polysurface_ids[object_id] = obj

        if len(polysurface_ids) < 2:
            return {"Connection": "Not enough polysurfaces in the layer."}
    
        connection_info = []
        checked_connections = set()
    
        for id1, obj1 in polysurface_ids.items():
            for id2, obj2 in polysurface_ids.items():
                if id1 != id2 and (id1, id2) not in checked_connections and (id2, id1) not in checked_connections:
                    # Coerce the Brep objects
                    cube1 = rs.coercebrep(obj1)
                    cube2 = rs.coercebrep(obj2)
    
                    # Check if cube1 is inside cube2 or vice versa
                    if are_corners_inside(cube1, cube2):
                        connection = {
                            "Inside ID": id1,
                            "Connection Type": "inside",
                            "Outside ID": id2,
                            "Description": "ID {} is inside ID {}".format(id1, id2)
                        }
                        connection_info.append(connection)
                        checked_connections.add((id1, id2))
                    elif are_corners_inside(cube2, cube1):
                        connection = {
                            "Inside ID": id2,
                            "Connection Type": "inside",
                            "Outside ID": id1,
                            "Description": "ID {} is inside ID {}".format(id2, id1)
                        }
                        connection_info.append(connection)
                        checked_connections.add((id2, id1))
    
        if not connection_info:
            return {"Connection": "No connection found between polysurfaces."}
    
        return {"inside_connections": connection_info}
    
    # Example usage:
    layer_name = rs.GetString("Enter layer name")
    connections_types = find_connections(layer_name)
    point_connections = find_point_intersection(layer_name)
    stair_connections = is_surface_inside_polysurface(layer_name)
    surface_connections = check_surface_connection(layer_name)
    inside_connections = check_cubevscube_connection(layer_name)
    # Create a dictionary to combine the results
    combined_result = {
        "connections_types": connections_types,
        "point_connections": point_connections,
        "stair_connections": stair_connections,
        "surface_connections": surface_connections,
        "inside_connections": inside_connections
    }
    
    # Convert the combined result to JSON format
    json_result = json.dumps(combined_result, indent=4)
    
    # Print or return the JSON result
    print(json_result)
    
    
    # Save the JSON data to a file
    output_file = "{}.json".format(layer_name)
    with open(output_file, 'w') as file:
        file.write(json_result)
    
generate_result()