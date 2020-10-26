# Script to generate the codelist for physicsl equation types.
# how to run interactively: python3 -i pe_types_vcl.py
# owlready2 module is needed. I am its using version 0.13 with python 3.5.

# NB: In the first part, I use Owlready2 methods, in the last one basically work with strings.
# The aim of the first part of this script is to create the list of classes I need.
# Then, this list is used to create the "pe-types-vcl.ttl" file, as a text file.

from owlready2 import *

# loading
osmoonto = get_ontology("osmo.owl") # uses the owl version of OSMO, can be generated via Protege
osmoonto.load()

pe_type_class = IRIS["https://purl.vimmp.eu/semantics/osmo/osmo.ttl#physical_equation_type"]
pe_type_co = IRIS["https://purl.vimmp.eu/semantics/osmo/osmo.ttl#pe_type_continuum"]
pe_type_a = IRIS["https://purl.vimmp.eu/semantics/osmo/osmo.ttl#pe_type_atomistic"]
pe_type_el = IRIS["https://purl.vimmp.eu/semantics/osmo/osmo.ttl#pe_type_electronic"]
pe_type_m = IRIS["https://purl.vimmp.eu/semantics/osmo/osmo.ttl#pe_type_mesoscopic"]

all_pe_types_list = list(pe_type_class.descendants())
all_pe_types_list.remove(pe_type_class)
all_pe_types_list.remove(pe_type_el)
all_pe_types_list.remove(pe_type_a)
all_pe_types_list.remove(pe_type_m)
all_pe_types_list.remove(pe_type_co)

print(len(all_pe_types_list))

# ordering by descriptor
def des_fun(x):
    return x.has_pe_type_descriptor

all_pe_types_list.sort(key=des_fun)

# # Creating an output file with some info

# outfile = open("outfile_pe.txt","w")

# for el in all_pe_types_list:
#     siri= (el.iri).rsplit('#')[-1]
#     des=el.has_pe_type_descriptor
#     des_id=(des[0]).rsplit(':')[0]
#     s= siri + ',  ' + des[0] + ', ' +  des_id  + "\n" 
#     outfile.write(s)
    
# outfile.close()

# Creating a .ttl with the individuals needed for the code-list
# They are sorted (by their descriptor) alphabetically

vclfile = open("pe-types-vcl.ttl","w")

header='@prefix osmo: <https://purl.vimmp.eu/semantics/osmo/osmo.ttl#>.'+ "\n"+'@prefix xs: <http://www.w3.org/2001/XMLSchema#>.'+ "\n"+'@prefix skos: <http://www.w3.org/2004/02/skos/core#>.'+ "\n"+'@prefix vcl: <https://purl.vimmp.eu/semantics/alignment/vcl.ttl#>.'+ "\n"+ "\n"

vclfile.write(header)

for el in all_pe_types_list:
    siri= (el.iri).rsplit('#')[-1] # splits IRI using '#' as separator, and takes the last part of the resulting list
    des=el.has_pe_type_descriptor # takes the value of the property pe type descriptor
    des_id=(des[0]).rsplit(':')[0] # takes its part before ":"
    lab_nw = des_id.replace(' ','_') # label with no white spaces (nw)
    lab_nw = lab_nw.upper() # made all upper case
    l1 = 'osmo:INDIVIDUAL_OF_'+lab_nw+' a osmo:physical_equation_type, vcl:codelist_pe_type, osmo:'+siri+";"+ "\n" 
    l2 = '  skos:inScheme vcl:CL_PE_TYPE;' + "\n"
    l3 = '  skos:notation "'+lab_nw+'"^^xs:string, "'+lab_nw+'"@en;' + "\n" 
    l4 = '  skos:prefLabel "'+des[0]+'"^^xs:string.' + "\n" + "\n" 
    vclfile.write(l1)
    vclfile.write(l2)
    vclfile.write(l3)
    vclfile.write(l4)

vclfile.close()

