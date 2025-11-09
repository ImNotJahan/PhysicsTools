import sys
from antlr4 import CommonTokenStream, FileStream, InputStream
from .antlr_build.ExprLexer import ExprLexer
from .antlr_build.ExprParser import ExprParser
from .visitor_interpreter import VisitorInterpreter
import logging

def parse_stream(parser: ExprParser, stream: FileStream | InputStream) -> ExprParser.ProgContext:
    parser.setInputStream(CommonTokenStream(ExprLexer(stream)))
    return parser.block()

def main(argv):
    logger = logging.getLogger(__name__)

    parser = ExprParser(None)
    interp = VisitorInterpreter()

    reading_file = len(argv) > 1
    interp.output_expr = not reading_file

    if reading_file:
        tree = parse_stream(parser, FileStream(argv[1]))

    while True:
        if not reading_file:
            tree = parse_stream(parser, InputStream(input(">>> ")))

        if parser.getNumberOfSyntaxErrors() > 0:
            logger.error("Syntax Error: Parsing failed")
        else:
            try:
                interp.visit(tree)
            except Exception as e:
                logger.error("Runtime Error: {}".format(e))

        if reading_file: break

if __name__ == "__main__":
    main(sys.argv)

