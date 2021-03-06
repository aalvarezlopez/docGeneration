import argparse

class umlGenerator():
    """
    Open the source file, header file and scope database and generate
    and UMLet file with the class diagram of this component.
    """
    def __init__(self, name, path):
        """Initialization of the class

        Open the source file, header fila and scope database and generate
        and UMLet file with the class diagram of this component.

        Args:
            name: This is the name of the SWC. Both source and header file shall
            have this name.
            path: Relative or absolute path to where the components files and
                ctags files are.

        Returns:
            Nothing

        Raises:
            Nothing
        """
        self.swcName = name
        self.swcPath = path
        self.privateAttributes = []
        self.publicAttributes = []
        self.privateMethods = []
        self.publicMethods = []

    def parse_ctags(self):
        """Read and parse ctags file

        CTags file will be read looking for all the symbols that are related to
        this specific software component.

        Raise:
            Error in case of not valid ctags file was found
        """
        try:
            fctags = open(self.swcPath + '/tags', 'r')
        except:
            print "Not valid ctags file found. Please generate it"
            raise
        for f in fctags:
            if self.swcName+'.h' in f and len(f.split('\t')) > 3:
                if f.split('\t')[3] == 'p':
                    self.publicMethods.append([])
                    self.publicMethods[-1].append(f.split('\t')[0])
                    self.publicMethods[-1].append(f.split('\t')[2].split(' ')[0][2:])
                    self.publicMethods[-1].append(f.split('\t')[4].split('(')[1].split(')')[0])
        fctags.seek(0)
        for f in fctags:
            if self.swcName+'.c' in f and len(f.split('\t')) >= 3:
                if f.split('\t')[3].replace('\n','') == 'f' and f.split('\t')[0] not in self.publicMethods:
                    self.privateMethods.append([])
                    self.privateMethods[-1].append(f.split('\t')[0])
                    self.privateMethods[-1].append(f.split('\t')[2].split(' ')[0][2:])
                    self.privateMethods[-1].append(f.split('\t')[4].split('(')[1].split(')')[0])
                if f.split('\t')[3].replace('\n','') == 'v':
                    self.privateAttributes.append([])
                    self.privateAttributes[-1].append(f.split('\t')[0])
                    self.privateAttributes[-1].append(f.split('\t')[2].split(' ')[0][2:])

        fctags.close()

    def generate_uml_file(self):
        """Generate a umlet format file

        This will generate a UMLet readable file with the class diagram of the
        software component that was already parse
        """
        fin = open('./classTemplate.uxf', 'r')
        fout = open('./%sClassDgm.uxf'%self.swcName, 'w')
        for line in fin:
            if "#ATTRIBUTES#" in line:
                for method in self.publicAttributes:
                    fout.write("+ %s: %s\n"%(method[0], method[1]))
                for method in self.privateAttributes:
                    fout.write("- %s: %s\n"%(method[0], method[1]))
            elif "#METHODS#" in line:
                for method in self.publicMethods:
                    fout.write("+ %s(%s): %s\n"%(method[0], method[2], method[1]))
                for method in self.privateMethods:
                    fout.write("- %s(%s): %s\n"%(method[0], method[2], method[1]))
            elif "#NAME#" in line:
                fout.write(line.replace("#NAME#", self.swcName))
            elif "<h>" in line:
                fout.write("<h>%d</h>"%((4\
                        + len(self.privateMethods)\
                        + len(self.privateAttributes)\
                        + len(self.publicMethods)\
                        + len(self.publicAttributes)) * 15 + 10))
            else:
                fout.write(line)

        fout.write('#Date:%d %d %d - GIT release: %s'%(3, 10, 2017, 'r01ase'))

        fin.close()
        fout.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create UML from SW component')
    parser.add_argument('name', metavar='N', type=str,
                    help='Name of the sowfware component that will be parse')
    parser.add_argument('path', metavar='N', type=str,
                    help='Path to the component location')
    args = parser.parse_args()
    umlGen = umlGenerator(args.name, args.path)

    umlGen.parse_ctags()
    umlGen.generate_uml_file()

