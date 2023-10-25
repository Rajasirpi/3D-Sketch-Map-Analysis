
import rhinoscriptsyntax as rs
import time

def delete_objects_with_attribute_value(attribute_name, attribute_value):
    # Get all objects in the document
    all_objects = rs.AllObjects()

    # Iterate through each object
    for obj_id in all_objects:
        # Check if the object has the specified attribute name and value
        if rs.GetUserText(obj_id, attribute_name) == attribute_value:
            # Highlight the object
            rs.SelectObject(obj_id)
            rs.Redraw()

            # Wait for 5 seconds
            time.sleep(2)

            # Delete the object
            rs.DeleteObject(obj_id)
            rs.Redraw()

# Specify the attribute name and value to filter by
attribute_name = "ID"
attribute_value = "10"

# Call the function
delete_objects_with_attribute_value(attribute_name, attribute_value)
