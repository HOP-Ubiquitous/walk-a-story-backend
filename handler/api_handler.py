import colorlog
import json
from flask import request, Blueprint

from analyzer.IA_service import IAService

logger = colorlog.getLogger('API REST Event Handler')
IA_service: IAService = None

app = Blueprint('analyzer', __name__)


@app.route('/event', methods=['POST'])
def event():
    logger.info("Notification received: " + request.data.decode("utf-8"))
    #
    # notification = json.loads(request.data)
    # # TODO
