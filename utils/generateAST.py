import sys
from pathlib import Path

def main():
    outputDir = sys.argv[1]
    grammar = [     "Binary   :  left, operator, right",
                    "Grouping : expression",
                    "Literal  : value",
                    "Unary    :  operator, right" ]
    defineAst(outputDir, "Expr", grammar)

def defineAst(outputDir, baseName, types):
    root = Path(outputDir)
    path =  baseName + ".py"
    f = open(root / path , "a")
    defineVisitor(f, baseName, types)
    f.write("class " + baseName + ":\n")
    f.write("\tdef accpet(visitor):\n")
    f.write("\t\tpass\n")
    for t in types:
        className = t.split(":")[0].strip()
        fields = t.split(":")[1].strip()
        defineType(f, baseName, className, fields)

def defineVisitor(f, baseName, types):
    f.write("Class Visitor:\n")
    for t in types:
        typeName = t.split(":")[0].strip()
        f.write("\tdef visit"+ typeName + baseName + "(" + baseName.lower() + "):\n")
        f.write("\t\tpass\n")


def defineType(f, baseName, className, fieldList):
    f.write("class " + className + "(" + baseName + "):\n")
    f.write("\tdef __init__(self, " + fieldList + "):\n")
    fields = fieldList.split(", ")
    for field in fields :
        #name = field.split(" ")[1]
        name = field
        f.write("\t\t" "self." + name + "= " + name + "\n")
    f.write("\tdef accept(visitor):\n")
    f.write("\t\treturn visitor.visit" + className + baseName + "()\n")

main()



