import io
import time
import flask
import requests
import numpy
import cv2
import base64

from soonerface.face import soonerize


IMG_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])


main = flask.Blueprint('main', __name__)


@main.route('/')
def index():
    return flask.render_template('index.html')


@main.route('/process', methods=['POST'])
def process():
    try:
        image = _get_image('image', None)
    except ValueError, e:
        flask.flash(e.message, category='error')
        return flask.redirect(flask.url_for('main.index'))

    if image is None:
        flask.flash('No image found', category='error')
        return flask.redirect(flask.url_for('main.index'))

    image = numpy.asarray(bytearray(image.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    result = soonerize(image, pil=True)
    fobj = io.BytesIO()
    result.save(fobj, format='png')
    fobj.seek(0)
    b64 = base64.b64encode(fobj.getvalue())

    return flask.render_template('view.html', image=b64)


def allowed_file(filename):
    filename = filename.lower()
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in IMG_EXTENSIONS


def _download_with_max(r, max_size, timeout=5.0):
    result = io.BytesIO()

    size = 0
    start = time.time()

    for chunk in r.iter_content(1024):
        if time.time() - start > timeout:
            raise ValueError('Timeout reached')

        size += len(chunk)
        if size > max_size:
            raise ValueError('Image too large')

        result.write(chunk)

    return result


def _get_image(field, default=None):
    # did we get an image?
    fobj = flask.request.files.get(field)
    if fobj is not None:
        if not allowed_file(fobj.filename):
            raise ValueError('File not allowed')

        return fobj

    # did we get an url?
    url = flask.request.form.get(field)
    if url is not None:
        # try to download the file
        max_size = flask.current_app.config['MAX_CONTENT_LENGTH']

        r = requests.get(url, stream=True, timeout=3.0)
        r.raise_for_status()
        if int(r.headers.get('Content-Length')) > max_size:
            raise ValueError('Image too large')

        return _download_with_max(r, max_size, timeout=3.0)

    return default
