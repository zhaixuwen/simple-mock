import configs
import logging
from flask import Flask

logging.basicConfig(filename='mocker.log',
                    level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
app.config.from_object(configs)
