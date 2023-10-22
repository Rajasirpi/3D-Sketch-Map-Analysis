# 3D-Sketch-Map-Analysis

  ## Background
  As a part of my master's program in Geoinformatics and Spatial Data Science  at the University of Münster, I started my internship within a collaborative project between IFGI and ETH Zurich research institute at Switzerland, spanning from 1st April 2023 to 30th September 2023. This internship revolved around the “3D Sketch Maps” project.

  ## SketchMap Creation
  To enhance the assessment of the sketch maps, we expanded upon an existing approach for analyzing 2D sketch maps and integrated it with the formalized technique of portraying buildings as a collection of convex spaces, as established in the architectural framework of Space Syntax. Our method involved two primary steps. Initially, we redrew both the sketch map and the ground-truth building model within Rhino using a standardized set of geometric shapes: cuboids to represent rooms and planes to represent staircases. Subsequently, we manually linked/aligned each cuboid and plane in the ground truth to a corresponding object in the sketch map.

  ## Spatial Analysis
  After acquiring the annotated maps, I have proceeded to examine various spatial relationships within these sketch maps. Initially, focused on extracting connectivity information, specifically between each cuboid-cuboid, cuboid-plane, and plane-plane pairs. To achieve this, a few custom function has been developed and seamlessly integrated into the Rhino software using Python. These custom function served the purpose of retrieving connectivity information, such as identifying the types of connections between cuboids and planes. It determined whether they shared an edge, surface, or point.  Additionally, the function will also gathered topological information, discerning relationships like "inside" and "outside." For instance, it determined which plane, such as a staircase, was positioned inside or outside a particular cuboid, such as a room. In this manner, our script systematically collected comprehensive information from each cuboid and plane featured in the annotated sketch maps

  ## Completeness and Generalization:
  We systematically identified and quantified specific scenarios during which a participant exhibited the following behaviors:
    (a) Failure to depict an object from the ground truth in the sketch map, which represents a case of incompleteness.
    (b) Depiction of multiple objects (e.g., several rooms or cuboids) as a single object (cuboid) in the sketch map, illustrating a common instance of generalization in sketch map drawing.
 

  Prepare a README explaining:
  - the background: that this is part of the 3d sketch map project, that this work was carried on by you at both institutes, etc..
  - what this code does
  - what aspects of a 3d sketch map are calculated
  - what input is required
  - what is the structure of the output
  - what is the structure of the code (I remember it is in two separate files, right? what does each file do? Do they need to be run in a specific order?)
  - how to run the code in Rhino - describe what needs to be done step by step, using a demo example (see point 3 below).
  - what versions of Rhino and python you have used when developing the code
  Hint: a lot of this text you can simply copy from the report! Use screenshots to explain the workflow 
