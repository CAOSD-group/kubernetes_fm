# Script to simplify and adapt a feature model for compatibility with Flamapy
# (also removes constraints)

import re

fm_original = 'variability_model/KubernetesFM.uvl'
fm_simplified = 'variability_model/KubernetesFM_simple.uvl'

# Words or characters to remove (comment out those you don't want to remove)
words_to_delete = ['String ', 'Integer ', 'Boolean ', 'cardinality', '[1..*]']  
#words_to_delete = [] 

# Characters to remove from the restrictions (comment out those you don't want to remove)
characters_to_delete = [' < ', ' > ', ' <=> ', ' == ', '//']
#characters_to_delete = ['//']

# Function to simplify the constraints
def simplified_constraints(restrictions):
    # Remove the constraints that are not currently supported by Flamapy
    lines_restrictions = restrictions.split('\n')
    simplified_restrictions = []
    for line in lines_restrictions:
        if any(c in line for c in characters_to_delete):
            continue
        else:
            simplified_restrictions.append(line)
    return simplified_restrictions

# Function to process the text
def generate_fm_simplified(fm_original, fm_simplified, palabras_a_eliminar):
    # Read the original file
    with open(fm_original, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove and replace the specified words or characters
    for palabra in palabras_a_eliminar:
        text = text.replace(palabra, '')
    
    # Replace all periods with underscores
    text = text.replace('.', '_')

    # Replace '[1__]' with '[1..]'
    text = text.replace('[1__*]', '[1..*]')
    
    # Separate the feature model into two parts: the features and the constraints
    tree = re.split(r'^\s*constraints', text, maxsplit=1, flags=re.MULTILINE)[0]
    restrictions = re.split(r'^\s*constraints', text, maxsplit=1, flags=re.MULTILINE)[1]

    # Simplify the constraints (Comment this line if you don't want to simplify the constraints)
    restrictions = simplified_constraints(restrictions)
    

    # Save the modified text in a new file
    with open(fm_simplified, 'w', encoding='utf-8') as f:
        f.write(tree)
        f.write('constraints')
        for i, line in enumerate(restrictions):
            f.write(line)
            if i < len(restrictions) - 1:
                f.write('\n')

# Call the function to process the files
generate_fm_simplified(fm_original, fm_simplified, words_to_delete)

print(f"The processed file has been saved as {fm_simplified}")
