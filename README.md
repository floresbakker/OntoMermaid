# About

A RDF-based vocabulary to express OWL ontologies into Mermaid diagram language.

## Abstract

The RDF-based vocabulary Mermaid serves as a bridge between the expressive power of OWL (Web Ontology Language) and the visual clarity of Mermaid diagrams. This vocabulary enables the representation of OWL ontologies in a structured and visual manner using the Mermaid diagram language. By doing so, it facilitates the understanding and communication of complex ontological structures, making them more accessible to a wider audience. The RDF-based approach leverages the capabilities of the Semantic Web to enrich the diagrams with metadata, fostering data interoperability and semantic annotation. This readme outlines the development and application of this novel ontology, opening new possibilities for ontology representation and visualization.

## Introduction
Ontologies play a vital role in knowledge representation and reasoning within various domains. OWL, a standard ontology language, offers a powerful and expressive framework for defining ontological structures. However, the complexity of OWL ontologies can be a barrier to comprehension for many stakeholders, especially those without a deep understanding of formal logic or ontology engineering. This challenge has inspired the development of an RDF-based vocabulary that translates OWL ontologies into Mermaid diagrams, known for their intuitive and visually appealing representation of complex relationships. In this readme, we introduce this innovative approach and discuss its potential to bridge the gap between ontology experts and non-experts, making ontological knowledge more accessible and comprehensible.

## Background
The development of ontologies has grown in significance across diverse fields, from bioinformatics to the semantic web, due to their capacity to model and organize complex knowledge structures. OWL, as a semantic web standard, offers a robust framework for defining ontological concepts, relationships, and axioms. On the other hand, Mermaid is a versatile diagramming language renowned for its capacity to create visually engaging and easily interpretable diagrams. The fusion of these two paradigms aims to harness the formal power of OWL for ontology engineering while making it more user-friendly through visualization in Mermaid diagrams. This innovation stands at the intersection of knowledge representation, ontology engineering, and visual communication, promising to enhance the efficiency and accessibility of ontology development and application.

## Objective
The primary objective of this RDF-based vocabulary is to facilitate the translation of OWL ontologies into Mermaid diagrams, resulting in a visually comprehensible representation of complex knowledge structures. By doing so, it aims to address the challenge of making ontological knowledge accessible to a broader audience, including domain experts, decision-makers, and non-experts. Furthermore, this vocabulary seeks to enhance the semantic richness of Mermaid diagrams by embedding RDF metadata, thus enabling semantic annotation and enabling the integration of ontological knowledge with the broader Semantic Web ecosystem. This research endeavors to promote efficient ontology representation, fostering knowledge sharing, and supporting various applications where ontologies play a crucial role.

## Audience
This work is intended for a diverse audience, encompassing ontology engineers, domain experts, data scientists, knowledge managers, and anyone interested in knowledge representation and visualization. Ontology engineers will find in this vocabulary a novel tool for translating complex ontological structures into visually intuitive diagrams. Domain experts and decision-makers will benefit from the enhanced accessibility and clarity of knowledge representations, aiding in informed decision-making. Data scientists and knowledge managers can use this approach to bridge the gap between domain-specific ontologies and data visualization, improving data integration and interpretation. In summary, this research addresses a wide range of stakeholders and contributes to the democratization of ontology usage and understanding across different fields.



## Ontology of Mermaid

The ontology of Mermaid consists of shapes according to the SHACL-format. 

It has NodeShapes for the following class constructs:

1. An atomic class (owl:Class or rdfs:Class);
2. A restriction class with the property owl:allValuesFrom
3. A restriction class with the property owl:someValuesFrom
4. A restriction class with the property owl:hasValue
5. A restriction class with the property owl:cardinality
6. A restriction class with the property owl:maxCardinality
7. A restriction class with the property owl:cardinality
8. A restriction class with the property owl:minCardinality
9. A subclass of some other class (rdfs:SubClassOf)
10. An equivalent class of some other class (owl:equivalentClass)
11. A class that is the union of other classes (owl:unionOf)
12. A class that is the intersection of other classes (owl:intersectionOf)
13. A class that consists of the enumeration of individuals (owl:oneOf)
14. A class that is the complement of another class (owl:complementOf)
14. A property that is an object property (owl:ObjectProperty)
14. A property that is a datatype property (owl:DatatypeProperty)
16. A property that is a subPropertyOf another property (rdfs:subPropertyOf)
17. A property that is an equivalentProperty to another property (owl:equivalentProperty)

Still to do:
18. AnnotationProperty
19. owl:Axiom
20. NodeShape

### Example

Using the tool in this repository we can transform any ontology into a diagram. Let us take the [Organization ontology](https://www.w3.org/TR/vocab-org/) of W3C as an example. For reasons of brevity and clarity, let's zoom in on some aspects of the model:


```
org:Organization a owl:Class, rdfs:Class;
    rdfs:subClassOf  foaf:Agent;
    owl:equivalentClass foaf:Organization;
    rdfs:label "Organization"@en;
    owl:hasKey (org:identifier).

org:Site a owl:Class, rdfs:Class;
    rdfs:label "Site"@en.

org:OrganizationalCollaboration a owl:Class, rdfs:Class;

    rdfs:subClassOf  org:Organization;
    owl:equivalentClass
         [ a  owl:Class ;
           owl:intersectionOf (
               org:Organization 
               [a  owl:Restriction ;
                   owl:allValuesFrom org:Organization ;
                   owl:onProperty org:hasMember
               ]
           )
         ]; 
    rdfs:label "Endeavour"@en.

org:basedAt a owl:ObjectProperty, rdf:Property;
    rdfs:label "based At"@en;
    rdfs:domain foaf:Person;
    rdfs:range  org:Site.

org:location a owl:DatatypeProperty, rdf:Property;
    rdfs:label "location"@en;
    rdfs:domain foaf:Person;
    rdfs:range  xsd:string.

org:hasMember a owl:ObjectProperty, rdf:Property;
    rdfs:label "has member"@en;
    rdfs:domain org:Organization;
    rdfs:range  foaf:Agent.
```

This translates to the following Mermaid diagram:

```
graph TB
classDef DatatypeProperty fill:#9c6,stroke:#9c6;

http://www.w3.org/ns/org#OrganizationalCollaboration((Endeavour)) -- subClassOf --> http://www.w3.org/ns/org#Organization((Organization))
http://www.w3.org/ns/org#OrganizationalCollaboration((Endeavour)) -- equivalentTo --> n94d6c1568eec4188bd883caaf0b9c353b20

subgraph n94d6c1568eec4188bd883caaf0b9c353b20[Intersection &cap;]
n94d6c1568eec4188bd883caaf0b9c353b20http://www.w3.org/ns/org#Organization((Organization)) -- and --- n94d6c1568eec4188bd883caaf0b9c353b21
end

subgraph n94d6c1568eec4188bd883caaf0b9c353b21[Restriction &forall;]
n94d6c1568eec4188bd883caaf0b9c353b21thing((thing)) -- has member only --> n94d6c1568eec4188bd883caaf0b9c353b21http://www.w3.org/ns/org#Organization((Organization))
end

http://www.w3.org/ns/org#Site((Site))
http://xmlns.com/foaf/0.1/Person -- based At --> http://www.w3.org/ns/org#Site
http://xmlns.com/foaf/0.1/Person -- location --> http://www.w3.org/2001/XMLSchema#string:::DatatypeProperty
http://www.w3.org/ns/org#Site -- site Of --> http://www.w3.org/ns/org#Organization


```
This Mermaid code is generated by the tool mermaid.py using the Mermaid Vocabulary as described in this repository. For your comfort, the tool outputs an HTML file that contains this diagram code and which can be rendered by just opening the file in any browser. Here is the example result:

![An example of a Mermaid diagram of an owl ontology](/Examples/ExampleMermaid.JPG)


In the examples folder there are more generated HTML files with diagrams of existing W3C ontologies like the [Organization ontology](https://www.w3.org/TR/vocab-org/) and the [Provenance ontology](https://www.w3.org/TR/prov-o/).

# Tools and dependencies

This repository comes with a, fairly primitive, Python-based tool to transform OWL into Mermaid.

1. mermaid.py

## mermaid.py

The tool mermaid.py is used to read OWL ontologies and express them in the Mermaid diagram language.

### How to use mermaid.py

A. Install all necessary libraries:

	1. pip install os
	1. pip install pyshacl
	2. pip install rdflib

B. Place one or more OWL-ontologies in the input folder in \mermaid\Tools\Input. 

C. Run the script in the command prompt by typing: 

```
python mermaid.py
```

D. Go to the output folder in \mermaid\Tools\Output and grab your generated HTML (*.html) and Turtle-file(s) (*.ttl). 

