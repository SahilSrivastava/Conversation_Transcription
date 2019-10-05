class EnrollmentResponse:
    """This class encapsulates the enrollment response."""

    _TOTAL_SPEECH_TIME = 'enrollmentSpeechTime'
    _REMAINING_SPEECH_TIME = 'remainingEnrollmentSpeechTime'
    _SPEECH_TIME = 'speechTime'
    _ENROLLMENT_STATUS = 'enrollmentStatus'

    def __init__(self, response):
        """Constructor of the EnrollmentResponse class.

        Arguments:
        response -- the dictionary of the deserialized python response
        """
        self._total_speech_time = response.get(self._TOTAL_SPEECH_TIME, None)
        self._remaining_speech_time = response.get(self._REMAINING_SPEECH_TIME, None)
        self._speech_time = response.get(self._SPEECH_TIME, None)
        self._enrollment_status = response.get(self._ENROLLMENT_STATUS, None)

    def get_total_speech_time(self):
        """Returns the total enrollment speech time"""
        return self._total_speech_time

    def get_remaining_speech_time(self):
        """Returns the remaining enrollment speech time"""
        return self._remaining_speech_time

    def get_speech_time(self):
        """Returns the speech time for this enrollment"""
        return self._speech_time

    def get_enrollment_status(self):
        """Returns the enrollment status"""
        return self._enrollment_status
