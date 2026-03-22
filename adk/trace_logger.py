class TraceLogger:

    def __init__(self):
        self.traces = []

    def log(self, step, event, data):

        self.traces.append({
            "step": step,
            "event": event,
            "data": data
        })

    def get_traces(self):

        return self.traces


trace_logger = TraceLogger()