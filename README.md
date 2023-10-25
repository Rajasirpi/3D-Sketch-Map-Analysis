# 3D-Sketch-Map-Analysis

  ## Background
  As a part of my master's program in Geoinformatics and Spatial Data Science  at the University of Münster, I started my internship within a collaborative project between **IFGI and ETH Zurich** research institute at Switzerland, spanning from 1st April 2023 to 30th September 2023. This internship revolved around the **“3D Sketch Maps”** project.

  ## SketchMap Creation
  To enhance the assessment of the sketch maps, we expanded upon an existing approach for analyzing 2D sketch maps and integrated it with the formalized technique of portraying buildings as a collection of convex spaces, as established in the architectural framework of Space Syntax. Our method involved two primary steps. Initially, we redrew both the sketch map and the ground-truth building model within Rhino using a standardized set of geometric shapes: cuboids to represent rooms and planes to represent staircases. Subsequently, we manually linked/aligned each cuboid and plane in the ground truth to a corresponding object in the sketch map.

  ![Manual Alignment](Alignment.png)


  ## Spatial Analysis
  After acquiring the annotated maps, I have proceeded to examine various spatial relationships within these sketch maps. Initially, focused on extracting connectivity information, specifically between each cuboid-cuboid, cuboid-plane, and plane-plane pairs. To achieve this, a few custom function has been developed and seamlessly integrated into the Rhino software using Python. These custom function served the purpose of retrieving connectivity information, such as identifying the types of connections between cuboids and planes. It determined whether they shared an edge, surface, or point.  Additionally, the function will also gathered topological information, discerning relationships like "inside" and "outside." For instance, it determined which plane, such as a staircase, was positioned inside or outside a particular cuboid, such as a room. In this manner, my script **'Connection_info.py'** systematically collected comprehensive information from each cuboid and plane featured in the annotated sketch maps. 

  ## Completeness and Generalization:
  We systematically identified and quantified specific scenarios during which a participant exhibited the following behaviors:

  - Failure to depict an object from the ground truth in the sketch map, which represents a case of incompleteness.
  - Depiction of multiple objects (e.g., several rooms or cuboids) as a single object (cuboid) in the sketch map, illustrating a common instance of generalization in sketch map drawing. 

  When you run the script **'Generalization.py'** it will produce results with genralization and completeness informations.

  ## Workflow 

  The workflow for our analysis involved the development and implementation of a custom Python function within the Rhino software environment. This function was designed to systematically process the annotated 3D sketch maps, extracting valuable insights and spatial information. The steps can be outlined as follows:

  1) Development of a custom Python function within Rhino. 
  2) Examination of the annotated 3D sketch maps. 
  3) Generation of results in JSON file format. 
  4) Computation of generalization and completeness metrics. 
  5) Retrieval of final statistical outcomes in the form of a CSV file.

  ![Workflow](Workflow.png)

  ## Requirements

  - Rhino software (Any version)
  - Python 3.6 or higher
 
  ## Usage

  Steps to run the scripts in the 'Analysis_Scripts' folder.
  - Begin by installing Rhino software.
  - Open the 3d model (.3dm file) from the **'Sample_Rhinofile'** folder in Rhino.
  - Examine the layers in the model and identify the Original Map and Sketch Map layer names that you wish to analyze.
  - Access the **'Tools'** option in the top menu and select **'PythonScript > Edit'**.
  - This will open the Python editor. Load the **'Generalization.py'** and **'Connection_info.py'** files within the editor.
  - For scenarios with numerous layers where you want to delete specific attributes, consider using the **'Delete_floors.py'** script.
  - Note that there is no prescribed order for running the scripts; each one can be executed independently.
  - If you choose to run the **'Generalization.py'** script, it will prompt you in the Rhino UI to specify the BaseLayer and SketchLayer names. Once you enter these layer names, the script will generate a .json file containing alignment, generalization, and statistical data.
  - Running the **'Connection_info.py'** script differs from the previous one. It will prompt you for a single layer name. As a result, it will produce another .json file containing connection details such as point connections, cuboid connections, surface connections, and connection types (indicating whether they share an edge, point, or surface). You can input the layer name separately to obtain results for both the sketch map and base map.
  - Lastly, **'Final_Statistics.py'** is a script designed to consolidate statistical information from the generalization results and transform it into a CSV file. This script is useful when you have multiple generalization inputs.

  ## Reference

  - "VResin: Scaffolding the Externalization of Spatial Memory in 3D Sketching" by Xiao et al. (under review) 


