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
from rdflib import Namespace, Dataset

try:
    # Command prompt execution: current directory is based on location of OntoMermaid.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.abspath(os.path.join(current_dir, '..'))

except NameError:
    # Python IDE exectution: current directory is based on the IDE working directory in Spyder, Jupyter or iPython.
    # PLEASE NOTE: Set working directory in IDE to OntoMermaid root dir.
    current_dir = os.getcwd()
    directory_path  = os.path.abspath(os.path.join(current_dir))

# namespace declaration
rdf      = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs     = Namespace("http://www.w3.org/2000/01/rdf-schema#")
dct      = Namespace("http://purl.org/dc/terms/")
mermaid  = Namespace('https://mermaid.org/ontomermaid/model/def/')

# Function to read a graph (as a string) from a file 
def readStringFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

mermaid_vocabulary    = readStringFromFile(directory_path + "/specification/mermaid.trig")
mermaid_status_query  = readStringFromFile(directory_path + "/tools/playground/static/mermaidStatusQuery.rq")
mermaid_result_query  = readStringFromFile(directory_path + "/tools/playground/static/mermaidResultQuery.rq")
ontology_query        = readStringFromFile(directory_path + "/tools/playground/static/ontologyQuery.rq")

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
       
        statusquery = serializable_graph.query(mermaid_status_query)
        resultquery = serializable_graph.query(mermaid_result_query) 

        # Check whether another iteration is needed. If every OWL and RDFS construct contains a mermaid:syntax statement, the processing is considered done.
        for status in statusquery:
            if status == True:
                writeGraph(serializable_graph)
                iteratePyShacl(mermaid_generator, serializable_graph)
            else: 
                 print ("File " + filename_stem+"-mermaid.trig" + " created in output folder.")
                 writeGraph(serializable_graph)
        
                 for result in resultquery:
                    mermaid_code = result["mermaidFragment"]
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
                
        # Get some ontology to be transformed from OWL to Manchester Syntax. The ontology needs to be placed in the input directory.
        ontology_graph = readStringFromFile(file_path)   
        
        # Join the manchester syntax and the ontology to be transformed into one big string.
        serializable_graph_string = ontology_graph
        
        # Create a graph of the string consisting of the manchester syntax and the ontology to be transformed 
        serializable_graph = Dataset(default_union=True)
        serializable_graph.parse(data=serializable_graph_string , format="trig")
        serializable_graph.bind("mermaid", mermaid)
        
        # Inform user
        print ('\nCreating Mermaid diagram labels for file',filename, '...')
        
        # Call the shacl engine with the HTML vocabulary and the document to be serialized
        iteratePyShacl(mermaid_vocabulary, serializable_graph)
        
        # Inform user
        print ('Done.')
