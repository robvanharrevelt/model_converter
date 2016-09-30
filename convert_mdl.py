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

    print("Number of endogenous variables: %d\n" % len(modeldef.endo_dict))
    print("Number of exogenous variables: %d\n" % len(modeldef.exo_dict))
    print("Number of lags: %d\n" % len(modeldef.lag_dict))
    print("Number of frmls: %d\n" % len(modeldef.frmls))
    print("Number of params: %d\n" % len(modeldef.par_dict))

if __name__ == "__main__":
    main()
