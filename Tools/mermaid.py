# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:40:53 2023

@author: Flores Bakker

The Mermaid Vocabulary.

With the script mermaid.py one can transform OWL into Mermaid diagrams.

Usage: 

1. Place an arbitrary ontology (as turtle file) in the input folder.
2. In the command prompt, run 'python mermaid.py'
3. Go to the output folder and grab your enriched turtle file, now including Mermaid labels.
4. Copypaste Mermaid labels in your html file and use the Mermaid javascript library (see documentation on the Mermaid site)


"""
import os
import pyshacl
import rdflib 
from rdflib import Namespace

# Set the path to the desired standard directory. 
directory_path = "C:/Users/Administrator/Documents/Branches/"

# namespace declaration
mermaid = Namespace("https://data.rijksfinancien.nl/mermaid/model/def/")

# Function to read a graph (as a string) from a file 
def readGraphFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

# Function to write a graph to a file
def writeGraph(graph):
    graph.serialize(destination="C:/Users/Administrator/Documents/Branches/mermaid/Tools/Output/"+filename_stem+"-mermaid.ttl", format="turtle")

# Function to call the PyShacl engine so that a RDF model of an HTML document can be serialized to HTML-code.
def iteratePyShacl(mermaid_generator, serializable_graph):
        
        # call PyShacl engine and apply the HTML vocabulary to the serializable HTML document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=mermaid_generator,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, #rather than setting this to true, it is better to do the iteration in the script as PyShacl seems to have some buggy behavior around iteration.
        debug=False,
        )
        
        resultquery = serializable_graph.query('''
            
prefix mermaid: <https://data.rijksfinancien.nl/mermaid/model/def/>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix sh: <http://www.w3.org/ns/shacl#>

SELECT (GROUP_CONCAT(?label; separator="\\n") AS ?concatenatedLabels)
WHERE {
  ?element mermaid:label ?label.

}

        ''')   

        # Check whether another iteration is needed. If every OWL and RDFS construct contains a mermaid:syntax statement, the processing is considered done.
        for result in resultquery:
            mermaidlabels = result["concatenatedLabels"]
            print("BEGIN")
            print(mermaidlabels)
            print("EIND")
            output_file_path = "C:/Users/Administrator/Documents/Branches/mermaid/Tools/Output/concatenated_labels.txt"
            with open(output_file_path, "w") as file:
              file.write(mermaidlabels)
            writeGraph(serializable_graph)
            iteratePyShacl(mermaid_generator, serializable_graph)
            

# loop through any turtle files in the input directory
for filename in os.listdir(directory_path+"mermaid/Tools/Input"):
    if filename.endswith(".ttl"):
        file_path = os.path.join(directory_path+"mermaid/Tools/Input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]
        
        # Get the manchester syntax vocabulary and place it in a string
        mermaid_generator = readGraphFromFile("C:/Users/Administrator/Documents/Branches/mermaid/Specification/mermaid.ttl")
        
        # Get some ontology to be transformed from OWL to Manchester Syntax. The ontology needs to be placed in the input directory.
        ontology_graph = readGraphFromFile(file_path)   
        
        
        # Join the manchester syntax and the ontology to be transformed into one big string.
        serializable_graph_string = ontology_graph
        
        # Create a graph of the string consisting of the manchester syntax and the ontology to be transformed 
        serializable_graph = rdflib.Graph().parse(data=serializable_graph_string , format="ttl")
        serializable_graph.bind("mermaid", mermaid)
        
        # Inform user
        print ('Creating Mermaid diagram labels...')
        
        # Call the shacl engine with the HTML vocabulary and the document to be serialized
        iteratePyShacl(mermaid_generator, serializable_graph)
        
        # Inform user
        print ('Done.')
