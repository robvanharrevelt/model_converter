from optparse import OptionParser
from model_definition import ModelDefinition

def main():
    usage = """
         %prog MDL_FILE
         Examples:

         %prog sa4.mdl

    """
    parser = OptionParser(usage)
    parser.add_option("--output-type", dest = "output_type", default = "Python",
                       help = "Output type (C, Python, R...)") 
    (options, args) = parser.parse_args()

    if len(args) < 1: parser.error("Incorrect number of arguments")
    mdl_file = args[0]
    modeldef = ModelDefinition(mdl_file, options.output_type)
    
if __name__ == "__main__":
    main()
