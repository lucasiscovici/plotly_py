import base64
import sys
import json

import pytest
import numpy as np

from plotly import io as pio
import plotly.graph_objs as go

from plotly.offline.offline import _get_jconfig

if sys.version_info.major == 3 and sys.version_info.minor >= 3:
    import unittest.mock as mock
else:
    import mock

plotly_mimetype = "application/vnd.plotly.v1+json"


# fixtures
# --------
@pytest.fixture
def fig1(request):
    return go.Figure(
        data=[
            {
                "type": "scatter",
                "marker": {"color": "green"},
                "y": np.array([2, 1, 3, 2, 4, 2]),
            }
        ],
        layout={"title": {"text": "Figure title"}},
    )


def test_png_renderer_mimetype(fig1):
    pio.renderers.default = "png"

    # Configure renderer so that we can use the same parameters
    # to build expected image below
    pio.renderers["png"].width = 400
    pio.renderers["png"].height = 500
    pio.renderers["png"].scale = 1

    image_bytes = pio.to_image(fig1, width=400, height=500, scale=1)
    image_str = base64.b64encode(image_bytes).decode("utf8")

    expected = {"image/png": image_str}

    pio.renderers.render_on_display = False

    with mock.patch("IPython.display.display") as mock_display:
        fig1._ipython_display_()

    # assert fig1._repr_mimebundle_(None, None) is None
    mock_display.assert_not_called()

    pio.renderers.render_on_display = True
    with mock.patch("IPython.display.display") as mock_display:
        fig1._ipython_display_()

    mock_display.assert_called_once_with(expected, raw=True)


def test_svg_renderer_show(fig1):
    pio.renderers.default = "svg"
    pio.renderers["svg"].width = 400
    pio.renderers["svg"].height = 500
    pio.renderers["svg"].scale = 1

    with mock.patch("IPython.display.display") as mock_display:
        pio.show(fig1)

    # Check call args.
    # SVGs generated by orca are currently not reproducible so we just
    # check the mime type and that the resulting string is an SVG with the
    # expected size
    mock_call_args = mock_display.call_args

    mock_arg1 = mock_call_args[0][0]
    assert list(mock_arg1) == ["image/svg+xml"]
    assert mock_arg1["image/svg+xml"].startswith(
        '<svg class="main-svg" xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="400" height="500"'
    )

    mock_kwargs = mock_call_args[1]
    assert mock_kwargs == {"raw": True}


def test_pdf_renderer_show_override(fig1):
    pio.renderers.default = None

    # Configure renderer so that we can use the same parameters
    # to build expected image below
    pio.renderers["png"].width = 400
    pio.renderers["png"].height = 500
    pio.renderers["png"].scale = 1

    image_bytes_png = pio.to_image(fig1, format="png", width=400, height=500, scale=1)

    image_str_png = base64.b64encode(image_bytes_png).decode("utf8")

    with mock.patch("IPython.display.display") as mock_display:
        pio.show(fig1, renderer="png")

    expected_bundle = {"image/png": image_str_png}

    mock_display.assert_called_once_with(expected_bundle, raw=True)


# Combination
# -----------
def test_mimetype_combination(fig1):
    pio.renderers.default = "png+jupyterlab"

    # Configure renderer so that we can use the same parameters
    # to build expected image below
    pio.renderers["png"].width = 400
    pio.renderers["png"].height = 500
    pio.renderers["png"].scale = 1

    # pdf
    image_bytes = pio.to_image(fig1, format="png", width=400, height=500, scale=1)

    image_str = base64.b64encode(image_bytes).decode("utf8")

    # plotly mimetype
    plotly_mimetype_dict = json.loads(pio.to_json(fig1, remove_uids=False))

    plotly_mimetype_dict["config"] = {
        "plotlyServerURL": _get_jconfig()["plotlyServerURL"]
    }

    # Build expected bundle
    expected = {"image/png": image_str, plotly_mimetype: plotly_mimetype_dict}

    pio.renderers.render_on_display = False

    with mock.patch("IPython.display.display") as mock_display:
        fig1._ipython_display_()

    # assert fig1._repr_mimebundle_(None, None) is None
    mock_display.assert_not_called()

    pio.renderers.render_on_display = True
    with mock.patch("IPython.display.display") as mock_display:
        fig1._ipython_display_()

    mock_display.assert_called_once_with(expected, raw=True)
