from flask import Flask, request, render_template, url_for
from rdflib import Graph, Namespace, Literal, RDF, URIRef, XSD, Dataset
import pyshacl
import datetime
import os

app = Flask(__name__, template_folder='tools/playground/templates', static_folder='tools/playground/static')

# Get the current working directory in which the Playground.py file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir))

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


# Function to write a graph to a file
def writeGraph(graph, name):
    graph.serialize(destination=directory_path + "/tools/playground/static/" + name + ".trig", format="trig")


# Get the ReSpec vocabulary and place it in a string

mermaid_vocabulary    = readStringFromFile(directory_path + "/specification/mermaid.trig")
mermaid_status_query  = readStringFromFile(directory_path + "/tools/playground/static/mermaidStatusQuery.rq")
mermaid_result_query  = readStringFromFile(directory_path + "/tools/playground/static/mermaidResultQuery.rq")
ontology_query        = readStringFromFile(directory_path + "/tools/playground/static/ontologyQuery.rq")

def generateDiagram(mermaid_generator, serializable_graph):
        
        print ("iteration run Diagram")
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
        writeGraph(serializable_graph, 'diagram')
        # Check whether another iteration is needed. If every OWL and RDFS construct contains a mermaid:syntax statement, the processing is considered done.
        for status in statusquery:
            if status == True:
                generateDiagram(mermaid_generator, serializable_graph)
            else:     
                 for result in resultquery:
                    mermaidFragment = result["mermaidFragment"]
                    output_file_path = directory_path+"/tools/playground/static/diagram.html"
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
                    classDef Scheme fill:#FFFF00,stroke:#FFFF00;
                    classDef Concept fill:#FFFFcc,stroke:#FFFFCC;
                    
                    '''
                    
                    html_graph = f'''
                  
                    {mermaidFragment}
                    
                    ''' 
                    
                    html_end = '''
                    </pre>
                    <script type="module">
                      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                      mermaid.initialize({ startOnLoad: true, maxTextSize : 99999999 });
                    </script>
                    </div>
                    </body>
                    </html>
                    '''
                    
                    html_content = html_start + html_graph + html_end
                    
                    # Write the HTML content to the output file
                    with open(output_file_path, "w", encoding="utf-8") as file:
                        file.write(html_content) 

@app.route('/runOntoMermaid', methods=['POST'])
def runOntoMermaid():
    print("Starting generation of the Mermaid diagram")
    
    #1 Retrieve content from user
    ontology = request.form['ontology']
    documentNamespace = request.form['documentNamespace']
    
    #2 Retrieve which components of the ontology need to be specified in the document
    conceptSchemes = request.form.get('conceptSchemes') == 'true'
    concepts = request.form.get('concepts') == 'true'
    classes = request.form.get('classes') == 'true'
    objectProperties = request.form.get('objectProperties') == 'true'
    datatypeProperties = request.form.get('datatypeProperties') == 'true'
    rdfProperties = request.form.get('rdfProperties') == 'true'
    subProperties = request.form.get('subProperties') == 'true'
    equivalentProperties = request.form.get('equivalentProperties') == 'true'
    datatypes = request.form.get('datatypes') == 'true'    
    nodeshapes = request.form.get('nodeshapes') == 'true'
    namedIndividuals = request.form.get('namedIndividuals') == 'true'
    
    # Write ontology to file
    ontology_filepath = directory_path + "/tools/playground/static/ontology.trig"
    with open(ontology_filepath, 'w', encoding='utf-8') as file:
       file.write(str(ontology))

    # Initialize graph
    generation_iri = hash(ontology + str(datetime.datetime.now()))
    generationGraph = Dataset(default_union=True)
    doc = Namespace(documentNamespace)    
    generationGraph.bind("mermaid", mermaid)    
    generationGraph.bind("doc", doc)    
    
    # Add triples to be able to kickstart the SHACL engine later.
    
    #1 Add content from user
    generationGraph.add((doc[generation_iri], RDF.type, mermaid.Generation))
   
    #2 Establish which components of the ontology need to be specified in the document
    if conceptSchemes:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("conceptschemes")))
    
    if concepts:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("concepts")))
    
    if classes:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("classes")))
    
    if objectProperties:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("objectproperties")))
    
    if datatypeProperties:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("datatypeproperties")))
    
    if rdfProperties:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("rdfproperties")))
        
    if subProperties:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("subproperties")))

    if equivalentProperties:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("equivalentproperties")))        
    
    if datatypes:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("datatypes")))
        
    if nodeshapes:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("nodeshapes")))
    
    if namedIndividuals:
        generationGraph.add((doc[generation_iri], mermaid.include, Literal("namedindividuals")))

    # Let us establish which ontology needs to be documented in ReSpec
    try:
       generationGraph.parse(data=ontology , format="trig")
    except Exception as e:
        error_message = str(e)
        return render_template('index.html', 
                               ontology=ontology, 
                               conceptSchemes = conceptSchemes,
                               concepts = concepts,
                               classes = classes,
                               objectProperties = objectProperties,
                               datatypeProperties = datatypeProperties,
                               rdfProperties = rdfProperties,
                               nodeshapes = nodeshapes,
                               namedIndividuals = namedIndividuals,
                               status='Error: Unable to parse the ontology {}'.format(error_message))

    # Establishing ontology to be visualised
    ontologyQuery = generationGraph.query(ontology_query) 
    for result in ontologyQuery:
        generationGraph.add((doc[generation_iri], dct.subject, URIRef(result.ontology)))
        
    # Generating Mermaid diagram 
    print("Step #1. Creating Mermaid diagram...")
    generateDiagram(mermaid_vocabulary, generationGraph)
    writeGraph(generationGraph, 'diagram')
    
    src_filepath = url_for('static', filename='diagram.html')
    
    return render_template('index.html', htmlOutput='<iframe src='+ src_filepath + ' width="100%" height="600"></iframe>',
                           ontology=ontology, 
                           conceptSchemes = conceptSchemes,
                           concepts = concepts,
                           classes = classes,
                           objectProperties = objectProperties,
                           datatypeProperties = datatypeProperties,
                           rdfProperties = rdfProperties,
                           nodeshapes = nodeshapes,
                           namedIndividuals = namedIndividuals,
                           subProperties = subProperties,
                           equivalentProperties = equivalentProperties,
                           datatypes = datatypes, 
                           status ='Ready'
                           )

@app.route('/')
def index():
    return render_template('index.html', 
                           ontology='Place your ontology in turtle code here', 
                           conceptSchemes=True,
                           concepts=True,
                           classes=True,
                           objectProperties=True,
                           datatypeProperties=True,
                           rdfProperties=True,
                           nodeshapes=True,
                           namedIndividuals=True,
                           subProperties = True,
                           equivalentProperties = True,
                           datatypes = True, 
                           status='Ready'
                           )

if __name__ == '__main__':
    app.run()
