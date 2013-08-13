from atom import Atom
import cvxpy.expressions.types as types
from cvxpy.expressions.variable import Variable
from cvxpy.constraints.second_order import SOC
from cvxpy.constraints.affine import AffEqConstraint, AffLeqConstraint
import cvxpy.utilities as u
import cvxpy.interface.matrix_utilities as intf
import vstack

class geo_mean(Atom):
    """ Geometric mean of two scalars """
    def __init__(self, x, y):
        super(geo_mean, self).__init__(x, y)

    # The shape is the common width and the sum of the heights.
    def set_shape(self):
        self.validate_arguments()
        self._shape = u.Shape(1,1)

    @property
    def sign(self):
        return u.Sign.UNKNOWN
        
    # Default curvature.
    def base_curvature(self):
        return u.Curvature.CONCAVE

    def monotonicity(self):
        return len(self.args)*[u.Monotonicity.INCREASING]

    # Any argument size is valid.
    def validate_arguments(self):
        if not self.args[0].is_scalar() or not self.args[1].is_scalar():
            raise TypeError("The arguments to geo_mean must resolve to scalars." )

    def graph_implementation(self, var_args):
        v = Variable(*self.size)
        x = var_args[0]
        y = var_args[1]

        constraints = SOC(x + y, vstack.vstack(y - x, 2*v)).canonicalize()[1]
        constraints += [AffLeqConstraint(0, x),
                        AffLeqConstraint(0, y)]
        return (v, constraints)