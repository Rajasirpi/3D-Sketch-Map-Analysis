import json
from collections import defaultdict
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

def detect_object(layer_name, obj_id):
    # Get all objects on the specified layer
    objects = rs.ObjectsByLayer(layer_name)
    
    # Iterate over each object
    for obj in objects:
        # Check if the object has a user text 'ID' and if it matches the provided obj_id
        if rs.GetUserText(obj, 'ID') == obj_id:
            int_type = rs.ObjectType(obj)
            if int_type == 1073741824:
                return "Extrusion"
            elif int_type == 16:
                return "Polysurface"
            elif int_type == 8:
                return "Surface"  
            elif int_type == 4:
                return "Curve"
            elif int_type == 2:
                return "PointCloud"
            elif int_type == 1:
                return "Point"
            elif int_type == 0:
                return "Unknown Object"
            elif int_type == 32:
                return "Mesh"
            else:
                return "Unknown Object Type"

    # If the object with the given ID is not found in the specified layer
    return "Object not found in the specified layer"


def highlight_amalgamated_objects(layer_name_base, layer_name_sketch,b_amalgamated_ids,s_amalgamated_ids):
    # Get all objects on the base model layer
    base_objects = rs.ObjectsByLayer(layer_name_base)
    sketch_objects = rs.ObjectsByLayer(layer_name_sketch)

    # Initialize a list to store the highlighted objects
    highlighted_objects = []
    
    # Initialize variables to store extrusion IDs for merging
    extrusion_ids_to_merge = []
    surface_ids_to_merge = []
    
    # Iterate through the base objects
    for obj in base_objects:
        # Check if the object has a user attribute text 'ID'
        if rs.GetUserText(obj, 'ID'):
            base_id = rs.GetUserText(obj, 'ID')
            
            # Check if the base ID is in the amalgamated IDs list
            if base_id in b_amalgamated_ids:
                # Highlight the object in red color
                rs.SelectObjects(obj)
                rs.ObjectColor(obj, (255, 0, 0))  # Set the highlight color
                highlighted_objects.append(obj)
                
                # Check if the object is an extrusion
                if rs.ObjectType(obj) == 1073741824:
                    extrusion_ids_to_merge.append(obj)
                    
                # Check if the object is an extrusion
                if rs.IsSurface(obj):
                    surface_ids_to_merge.append(obj)
    
    # Iterate through the sketch objects
    for obj in sketch_objects:
        # Check if the object has a user attribute text 'ID'
        if rs.GetUserText(obj, 'ID'):
            sketch_id = rs.GetUserText(obj, 'ID')
            
            # Check if the sketch ID is in the amalgamated IDs list
            if sketch_id in s_amalgamated_ids:
                # Highlight the object in red color
                rs.SelectObjects(obj)
                rs.ObjectColor(obj, (255, 0, 0))  # Set the highlight color
                highlighted_objects.append(obj)
                
    # Select and highlight the amalgamated objects
    rs.SelectObjects(highlighted_objects)

    if len(extrusion_ids_to_merge) >= 2:
        # Perform a Boolean Union to merge the extrusions using rs.Command
        boolean_union_command = "BooleanUnion"
        for extrusion_id in extrusion_ids_to_merge:
            boolean_union_command += " SelID " + str(extrusion_id)
        rs.Command(boolean_union_command)
        merged_extrusion_ids = rs.LastCreatedObjects()
         # Add user attribute 'ID' and set value starting with 'A'
        if merged_extrusion_ids:
            # Add user attribute 'ID' and set value starting with 'A'
            new_id = 'A' + str(len(b_amalgamated_ids))
            for merged_id in merged_extrusion_ids:
                rs.SetUserText(merged_id, 'ID', new_id)

    if len(surface_ids_to_merge) >= 2:
        # Join the surfaces using rs.Command
        join_surfaces_command = "MergeSrf"
        for surface_id in surface_ids_to_merge:
            join_surfaces_command += " SelID " + str(surface_id)
        rs.Command(join_surfaces_command + " _Enter")
        # Add user attribute 'ID' and set value starting with 'A'
        merged_surface_ids = rs.LastCreatedObjects()
        if merged_surface_ids:
            # Add user attribute 'ID' and set value starting with 'A'
            new_id = 'A' + str(len(s_amalgamated_ids))
            for merged_id in merged_surface_ids:
                rs.SetUserText(merged_id, 'ID', new_id)

           
def highlight_incomplete_sketches(json_res, sketch_layer_name):
    # Load JSON data
    result_list = json.loads(json_res)

    # Get all objects on the sketch layer
    objects_sketch = rs.ObjectsByLayer(sketch_layer_name)

    # Iterate through the result list
    for alignment_info in result_list:
        # Get the SketchModel and BaseModel IDs
        sketch_ids = alignment_info["SketchModel"]["id"]
        base_ids = alignment_info["BaseModel"]["id"]

        # Check if the BaseModel IDs are empty or ' '
        if not base_ids or all(id == ' ' for id in base_ids):
            # Iterate through sketch IDs and highlight them in blue
            for sketch_id in sketch_ids:
                for obj_base in objects_sketch:
                    if rs.GetUserText(obj_base, 'ID') == sketch_id or rs.GetUserText(obj_base, 'BaseAlign') is None:
                        rs.SelectObject(obj_base)
                        rs.ObjectColor(obj_base, (0, 0, 255))  # Set the highlight color to blue


def generalization(layer_name_base, layer_name_sketch):
    # Get all objects on the specified layers
    objects_base = rs.ObjectsByLayer(layer_name_base)
    objects_sketch = rs.ObjectsByLayer(layer_name_sketch)
    Align = []
    # Iterate over each object in the base model
    for obj_base in objects_sketch:
        # Check if the object has a user text 'ID'
        if rs.GetUserText(obj_base, 'ID'):
            # Get the ID value
            sketch_id = rs.GetUserText(obj_base, 'ID')
            base_id_str = rs.GetUserText(obj_base, 'BaseAlign')
            Align.append (base_id_str)

    basealign =[]
    for item in Align:
        if item.strip():
            basealign.extend(item.split(','))

    unique_list = list(set(basealign))
    b = len(unique_list)

    Base_Id = []
    # Iterate over each object in the base model
    for obj_base in objects_base:
        # Check if the object has a user text 'ID'
        if rs.GetUserText(obj_base, 'ID'):
            # Get the ID value
            base_id = rs.GetUserText(obj_base, 'ID')
            Base_Id.append(base_id)

    count_gbm= len(Base_Id)
    numberofnonalignedbaseids= count_gbm-b
    
    # Initialize a dictionary to store the alignment information
    alignment_dict = {}
    
    # Create a separate dictionary to store the associations between sketch IDs and their base IDs
    sketch_to_base = defaultdict(set)
    
    # Iterate over each object in the base model
    for obj_base in objects_sketch:
        # Check if the object has a user text 'ID'
        if rs.GetUserText(obj_base, 'ID'):
            # Get the ID value
            sketch_id = rs.GetUserText(obj_base, 'ID')
            base_id_str = rs.GetUserText(obj_base, 'BaseAlign')

            # Initialize base_ids as an empty list
            base_ids = []
            
            # Check if base_id_str is not None
            if base_id_str is not None:
                # Split the base_id_str into individual base IDs
                base_ids = base_id_str.split(',')
            
            # Store the associations in the sketch_to_base dictionary
            for base_id in base_ids:
                sketch_to_base[sketch_id].add(base_id)
                
    
    # Now, construct the final alignment_dict with unique entries
    for sketch_id, base_ids in sketch_to_base.items():
        alignment_info = {
            "SketchModel": {"id": [sketch_id]},
            "BaseModel": {"id": list(base_ids)}
        }
        alignment_dict[sketch_id] = alignment_info

    # Create the final result list
    result_list = []
    for base_id, alignment_info in alignment_dict.items():
        # Remove duplicate sketch IDs
        alignment_info["SketchModel"]["id"] = list(set(alignment_info["SketchModel"]["id"]))
       # Remove duplicate base IDs
        alignment_info["BaseModel"]["id"] = list(set(alignment_info["BaseModel"]["id"]))
        
        # Check object types for base model and sketch model IDs
        base_model_ids = alignment_info["BaseModel"]["id"]
        sketch_model_ids = alignment_info["SketchModel"]["id"]

        base_model_types = [detect_object(layer_name_base, obj_id) for obj_id in base_model_ids]
        sketch_model_types = [detect_object(layer_name_sketch, obj_id) for obj_id in sketch_model_ids]

        # Perform the comparisons and add the "generalization" key
        if base_model_types.count("Extrusion") >= 2 and sketch_model_types.count("Extrusion") == 1:
            generalization = "amalgamation"
            s_amalgamated_ids = alignment_info["SketchModel"]["id"]
            b_amalgamated_ids = alignment_info["BaseModel"]["id"]
        elif "Extrusion" in base_model_types and "Surface" in sketch_model_types:
            generalization = "collapse"
            s_amalgamated_ids = alignment_info["SketchModel"]["id"]
            b_amalgamated_ids = alignment_info["BaseModel"]["id"]
        elif base_model_types.count("Surface") >= 2 and sketch_model_types.count("Surface") == 1:
            generalization = "amalgamation"
            s_amalgamated_ids = alignment_info["SketchModel"]["id"]
            b_amalgamated_ids = alignment_info["BaseModel"]["id"]
        else:
            generalization = "No generalization"
            amalgamated_ids = []
        
        # Add the "generalization" key to the alignment_info dictionary
        alignment_info["generalization"] = generalization
        
        # Append the modified dictionary to the result list
        result_list.append(alignment_info)
        
        if generalization == "amalgamation":
            # Call the function to highlight amalgamated objects
            highlight_amalgamated_objects(layer_name_base, layer_name_sketch,b_amalgamated_ids,s_amalgamated_ids)
            
        if generalization == "collapse":
            # Call the function to highlight amalgamated objects
            highlight_amalgamated_objects(layer_name_base, layer_name_sketch,b_amalgamated_ids,s_amalgamated_ids)
    
    json_res = json.dumps(result_list, indent=4)
    # Load the JSON data
    data = json.loads(json_res)
    for entry in data:
        base_model_ids = entry["BaseModel"]["id"]
        if not any(id.strip() for id in base_model_ids):
            entry["generalization"] = "None"   

    highlight_incomplete_sketches(json_res, layer_name_sketch)
    
    G_objects_on_layer = rs.ObjectsByLayer(layer_name_base)
    
    # Count the number of objects on the layer
    num_objects_on_Gbase = len(G_objects_on_layer)

    # Initialize counters
    no_generalization_count = 0
    other_generalization_count = 0
    non_empty_base_model_count = 0
    base_align_count = 0
    
    # Iterate through the data
    for item in data:
        base_model_ids = item.get("BaseModel", {}).get("id", [])
        if any(base_id.strip() for base_id in base_model_ids):
            non_empty_base_model_count += 1
   
    base_model_occurrences = {}  # Dictionary to store occurrences of base model IDs

    # Iterate through the JSON data
    for item in data:
        base_ids = item.get("BaseModel", {}).get("id", [])
        for base_id in base_ids:
            if base_id.strip():
                if base_id not in base_model_occurrences:
                    base_model_occurrences[base_id] = 1
                else:
                    base_model_occurrences[base_id] += 1
        
    # Filter out base model IDs that have occurred more than once
    repeated_base_ids = {base_id: occurrences for base_id, occurrences in base_model_occurrences.items() if occurrences > 1}
    
    # Count the keys with values other than 1
    count_keys_with_non_one_value = sum(1 for value in base_model_occurrences.values() if value != 1)
    # print("Number of keys with values other than 1:", count_keys_with_non_one_value)
    
    # Calculate the total occurrence only for keys with values other than 1
    total_occurrence = sum(value for key, value in base_model_occurrences.items() if value != 1)
    # print(total_occurrence)

    for base_id, occurrences in repeated_base_ids.items():
        print("Base ID: {}, Occurrences: {}".format(base_id,occurrences))
        
    # Iterate through the data
    for item in data:
        generalization_value = item.get("generalization", "")
        sketch_model_ids = item.get("SketchModel", {}).get("id", [])
        base_model_ids = item.get("BaseModel", {}).get("id", [])
    
        if generalization_value == "No generalization":
            no_generalization_count += 1
        elif generalization_value in ["amalgamation", "collapse"]:
            other_generalization_count += 1
    
    # Add the additional statistics to the result list
    data.append({
        "AdditionalStatistics": {
            "SketchMapLayerName": layer_name_sketch,
            "NumberOfObjectsNotGeneralisedBaseMap":count_gbm,
            "NumberOfObjectsGeneralisedBaseMap": num_objects_on_Gbase,
            "Numberofnonalignedbaseids":numberofnonalignedbaseids,
            "NumberOfAlignedObjects": non_empty_base_model_count,
            "NumberOfNoGeneralisations": no_generalization_count,
            "NumberOfGeneralisations": other_generalization_count,
            "RepeatedAlignIDs":count_keys_with_non_one_value,
            "NoOfInstance": total_occurrence
        }
    })
    
    # Convert the updated data to JSON
    updated_json_res = json.dumps(data, indent=4)
    # print(updated_json_res)

#    # Save the JSON data to a file
    output_file = "{}.json".format(layer_name_base)
    with open(output_file, 'w') as file:
        file.write(updated_json_res)

# Call the function with the layer names for "SketchModel" and "BaseModel"
layer_name = rs.GetString("Enter Base layer name")
layer_name1 = rs.GetString("Enter Sketch layer name")
generalization(layer_name, layer_name1)




# Function for doing  Manual Alignment
def generate_result():
    result = {}
    highlighted_objects = []
    
    while True:
        selected_objects = []
        object_ids = []

        # Select objects from the original model
        original_objects = rs.GetObjects("Select objects from the Base model")
        if not original_objects:
            break

        selected_objects.extend(original_objects)
        object_ids.extend(rs.GetUserText(obj_guid, "ID") for obj_guid in original_objects)

        # Select objects from the sketch model
        sketch_objects = rs.GetObjects("Select objects from the sketch model")
        if not sketch_objects:
            break

        selected_objects.extend(sketch_objects)
        object_ids.extend(rs.GetUserText(obj_guid, "ID") for obj_guid in sketch_objects)

        pair_result = {"BaseModel": {"id": []}, "SketchModel": {"id": []}}

        for obj_guid, obj_id in zip(selected_objects, object_ids):
            layer_name = rs.ObjectLayer(obj_guid)

            if obj_id not in pair_result[layer_name]["id"]:
                pair_result[layer_name]["id"].append(obj_id)

        # Combine the base_ids into a single string separated by commas
        combined_base_ids = ",".join(pair_result["BaseModel"]["id"])

        # Assign the pair_result to the combined_base_ids key in the result dictionary
        result[combined_base_ids] = pair_result
        
        # Highlight the selected objects
        rs.SelectObjects(selected_objects)
        rs.ObjectColor(selected_objects, (255, 0, 0))  # Set the highlight color
        highlighted_objects.extend(selected_objects)

    # Restore the original state of the highlighted objects
    rs.SelectObjects(highlighted_objects)
    rs.ObjectColor(highlighted_objects, (0, 0, 0))  # Set the original color


    return result

# Call the function
#result = generate_result()



