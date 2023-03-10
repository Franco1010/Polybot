class CodeforcesApiError:
    """Base class for all API related errors."""
    def __init__(self, message=None):
        super().__init__(message or 'Polygon API error')


class TrueApiError(CodeforcesApiError):
    """An error originating from a valid response of the API."""
    def __init__(self, comment, message=None):
        super().__init__(message)
        self.comment = comment


class ClientError(CodeforcesApiError):
    """An error caused by a request to the API failing."""
    def __init__(self):
        super().__init__('Error connecting to Codeforces API')


class CallLimitExceededError(TrueApiError):
    def __init__(self, comment):
        super().__init__(comment, 'Polygon API call limit exceeded')


