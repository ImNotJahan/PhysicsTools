from .antlr_build.ExprParser import ExprParser
from .antlr_build.ExprVisitor import ExprVisitor

from physics_utils import MeasuredData

from .statements  import handle_statement
from .expressions import handle_expression
from .block       import handle_block
from .control     import handle_control
from .datatypes   import make_list, make_number, make_string, make_symbol, make_package
from .environment import Environment, default_environment


class VisitorInterpreter(ExprVisitor):
    output_expr = False
    env = default_environment

    def add_env(self, new_env: dict) -> None:
        new_env = Environment(values=new_env)
        new_env.parent = self.env
        self.env = new_env

    def pop_env(self) -> None:
        self.env = self.env.parent

    def visitNum(self, ctx: ExprParser.NumContext) -> MeasuredData:
        return make_number(ctx)

    def visitList(self, ctx: ExprParser.ListContext) -> list:
        return make_list(self, ctx)

    def visitVar(self, ctx: ExprParser.VarContext):
        return self.env.get(ctx.getText())

    def visitExpr(self, ctx: ExprParser.ExprContext):
        return handle_expression(self, ctx)

    def visitStr(self, ctx: ExprParser.StrContext):
        return make_string(ctx)

    def visitSymbol(self, ctx: ExprParser.SymbolContext):
        return make_symbol(ctx)

    def visitPackage(self, ctx: ExprParser.PackageContext):
        return make_package(ctx)

    def visitStat(self, ctx: ExprParser.StatContext):
        return handle_statement(self, ctx)

    def visitCtrl(self, ctx: ExprParser.CtrlContext):
        return handle_control(self, ctx)

    def visitBlock(self, ctx: ExprParser.BlockContext):
        return handle_block(self, ctx, self.output_expr)

    def visitProg(self, ctx: ExprParser.ProgContext):
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))