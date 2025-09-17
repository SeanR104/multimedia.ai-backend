from flask import Blueprint

from utilities.utils import utils

options_bp = Blueprint('options_bp', __name__)


@options_bp.route('/test', methods=['POST'])
def test():

    return utils.ok({})
