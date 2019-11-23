import _plotly_utils.basevalidators


class MarkerValidator(_plotly_utils.basevalidators.CompoundValidator):
    def __init__(
        self, plotly_name="marker", parent_name="waterfall.increasing", **kwargs
    ):
        super(MarkerValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop("data_class_str", "Marker"),
            data_docs=kwargs.pop(
                "data_docs",
                """
            color
                Sets the marker color of all increasing values.
            line
                plotly_study.graph_objects.waterfall.increasing.marke
                r.Line instance or dict with compatible
                properties
""",
            ),
            **kwargs
        )
