# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:40:53 2023

@author: Flores Bakker

The Mermaid Vocabulary.

With the script OntoMermaid.py one can transform OWL into Mermaid diagrams.

Usage: 

1. Place an arbitrary ontology (as turtle file *.ttl) in the input folder.
2. In the command prompt, run 'python mermaid.py'
3. Go to the output folder and grab your enriched turtle file, now including Mermaid labels.
4. Copypaste Mermaid labels in your html file and use the Mermaid javascript library (see documentation on the Mermaid site)


"""
import os
import pyshacl
import rdflib 
from rdflib import Namespace

# Get the current working directory in which the OntoMermaid.py file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir))

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
    graph.serialize(destination=directory_path+"/tools/output/"+filename_stem+"-mermaid.trig", format="trig")

# Function to call the PyShacl engine so that a RDF model of an HTML document can be serialized to HTML-code.
def iteratePyShacl(mermaid_generator, serializable_graph):
        
        # call PyShacl engine and apply the HTML vocabulary to the serializable HTML document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=mermaid_generator,
        data_graph_format="trig",
        shacl_graph_format="trig",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, #rather than setting this to true, it is better to do the iteration in the script as PyShacl seems to have some buggy behavior around iteration.
        debug=False,
        )
        
       
        statusquery = serializable_graph.query('''
            
prefix mermaid: <https://mermaid.org/ontomermaid/model/def/>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix sh: <http://www.w3.org/ns/shacl#>
ASK
WHERE {
  # Any OWL or RDFS entity that is not yet described in terms of the manchester syntax
  {
    $this a owl:Class.
  }  
  UNION
  {
    $this a rdfs:Class.
  }
  UNION
  {
    $this rdfs:subClassOf []
  }
  UNION
  {
    $this owl:equivalentClass []
  }
  UNION
  {
    $this owl:unionOf []
  }
  UNION
  {
    $this owl:intersectionOf []
  }
  UNION
  {
    $this owl:complementOf []
  }
  UNION
  {
    $this owl:oneOf []
  }
  UNION
  {
    $this owl:allValuesFrom []
  }
  UNION
  {
    $this owl:someValuesFrom []
  }
  UNION
  {
    $this owl:hasValue []
  }
  UNION
  {
    $this owl:cardinality []
  }
  UNION
  {
    $this owl:maxCardinality []
  }
  UNION
  {
    $this owl:minCardinality []
  }  
  UNION
  {
   $this rdf:type rdf:Property
  }
  UNION
  {
    $this rdf:type owl:DatatypeProperty.
  }
  UNION
  {
    $this rdf:type owl:ObjectProperty.
  }
  UNION
  {
    $this rdfs:subPropertyOf []
    FILTER NOT EXISTS {$this rdf:type owl:AnnotationProperty}.
    FILTER NOT EXISTS {$this rdf:type owl:InverseFunctionalProperty}
    FILTER NOT EXISTS {$this rdf:type owl:FunctionalProperty}
  }
  UNION
  {
    $this owl:equivalentProperty [].
  }
  filter not exists {
    $this mermaid:syntax 'CLASS'.
  }
  filter not exists {
    $this mermaid:syntax 'CLASS'.
  }
  filter not exists {
    $this mermaid:syntax 'SUBCLASSOF'.
  }
  filter not exists {
    $this mermaid:syntax 'EQUIVALENTTO'.
  }
  filter not exists {
    $this mermaid:syntax 'OR'.
  }
  filter not exists {
    $this mermaid:syntax 'AND'.
  }
  filter not exists {
    $this mermaid:syntax 'NOT'.
  }
  filter not exists {
    $this mermaid:syntax '{}'.
  }
  filter not exists {
    $this mermaid:syntax 'ONLY'.
  }
  filter not exists {
    $this mermaid:syntax 'SOME'.
  }
  filter not exists {
    $this mermaid:syntax 'VALUE'.
  }
  filter not exists {
    $this mermaid:syntax 'EXACTLY'.
  }
  filter not exists {
    $this mermaid:syntax 'MAX'.
  }
  filter not exists {
    $this mermaid:syntax 'MIN'.
  }
  filter not exists {
    $this mermaid:syntax 'RDF_PROPERTY'.
  }
  filter not exists {
    $this mermaid:syntax 'DATATYPEPROPERTY'.
  }
  filter not exists {
    $this mermaid:syntax 'OBJECTPROPERTY'.
  }
  filter not exists {
    $this mermaid:syntax 'SUBPROPERTYOF'.
  }
  filter not exists {
    $this mermaid:syntax 'EQUIVALENTPROPERTY'.
  }
  filter not exists {
    $this mermaid:syntax 'OR-DATATYPE'.
  }
  filter not exists {
    $this mermaid:syntax 'AND-DATATYPE'.
  }
  filter not exists {
    $this mermaid:syntax 'NOT-DATATYPE'.
  }
  filter not exists {
    $this mermaid:syntax '{}-DATATYPE'.
  }
  filter not exists {
    $this mermaid:syntax 'EXACTLYQUALIFIED'.
  }
  filter not exists {
    $this mermaid:syntax 'MAXQUALIFIED'.
  }
  filter not exists {
    $this mermaid:syntax 'MINQUALIFIED'.
  }
}
        ''')   

        resultquery = serializable_graph.query('''
            
prefix owl:  <http://www.w3.org/2002/07/owl#>
prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix sh:   <http://www.w3.org/ns/shacl#>
prefix :     <https://mermaid.org/ontomermaid/model/def/>

SELECT (GROUP_CONCAT(?label; separator="\\n") AS ?mermaid_code)
WHERE {
  ?element :label ?label.
  
}
ORDER BY ?mermaid_code
        ''')   

        # Check whether another iteration is needed. If every OWL and RDFS construct contains a mermaid:syntax statement, the processing is considered done.
        for status in statusquery:
            if status == True:
                writeGraph(serializable_graph)
                iteratePyShacl(mermaid_generator, serializable_graph)
            else: 
                 print ("File " + filename_stem+"-mermaid.trig" + " created in output folder.")
                 writeGraph(serializable_graph)
        
                 for result in resultquery:
                    mermaid_code = result["mermaid_code"]
                    output_file_path = directory_path+"/tools/output/"+filename_stem+"-mermaid.html"
                    # Create the HTML content with the Mermaid code
                    html_start =  '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                    </head>
                    <body>
                    <div><pre class="mermaid">
                    %%{
                    init: {
                    "flowchart":{
                    "useMaxWidth": 0
                    }
                    }
                    }%%
                    graph TB
                    classDef Datatype fill:#9c6,stroke:#9c6;                    
                    '''
                    
                    html_graph = f'''
                  
                    {mermaid_code}
                    
                    ''' 
                    
                    html_end = '''
                    </pre>
                    <script type="module">
                      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                      mermaid.initialize({ startOnLoad: true, maxTextSize : 99999999, maxElements : 99999999 });
                    </script>
                    </div>
                    </body>
                    </html>
                    '''
                    
                    html_content = html_start + html_graph + html_end
                    
                    # Write the HTML content to the output file
                    with open(output_file_path, "w", encoding="utf-8") as file:
                        file.write(html_content)
                    print ("File " + filename_stem+"-mermaid.html" + " created in output folder.")

                 
# loop through any turtle files in the input directory
for filename in os.listdir(directory_path+"/tools/input"):
    if filename.endswith(".trig" or ".ttl" ):
        file_path = os.path.join(directory_path+"/tools/input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]
        
        # Get the manchester syntax vocabulary and place it in a string
        mermaid_generator = readGraphFromFile(directory_path+"/specification/mermaid.trig")
        
        # Get some ontology to be transformed from OWL to Manchester Syntax. The ontology needs to be placed in the input directory.
        ontology_graph = readGraphFromFile(file_path)   
        
        
        # Join the manchester syntax and the ontology to be transformed into one big string.
        serializable_graph_string = ontology_graph
        
        # Create a graph of the string consisting of the manchester syntax and the ontology to be transformed 
        serializable_graph = rdflib.Graph().parse(data=serializable_graph_string , format="trig")
        serializable_graph.bind("mermaid", mermaid)
        
        # Inform user
        print ('\nCreating Mermaid diagram labels for file',filename, '...')
        
        # Call the shacl engine with the HTML vocabulary and the document to be serialized
        iteratePyShacl(mermaid_generator, serializable_graph)
        
        # Inform user
        print ('Done.')
