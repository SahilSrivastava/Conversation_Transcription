
class IdentificationProfile:
    """This class encapsulates a user profile."""

    _PROFILE_ID = 'identificationProfileId'
    _LOCALE = 'locale'
    _ENROLLMENT_SPEECH_TIME = 'enrollmentSpeechTime'
    _REMAINING_ENROLLMENT_TIME = 'remainingEnrollmentSpeechTime'
    _CREATED_DATE_TIME = 'createdDateTime'
    _LAST_ACTION_DATE_TIME = 'lastActionDateTime'
    _ENROLLMENT_STATUS = 'enrollmentStatus'

    def __init__(self, response):
        """Constructor of the IdentificationProfile class.

        Arguments:
        response -- the dictionary of the deserialized python response
        """
        self._profile_id = response.get(self._PROFILE_ID, None)
        self._locale = response.get(self._LOCALE, None)
        self._enrollment_speech_time = response.get(self._ENROLLMENT_SPEECH_TIME, None)
        self._remaining_enrollment_time = response.get(self._REMAINING_ENROLLMENT_TIME, None)
        self._created_date_time = response.get(self._CREATED_DATE_TIME, None)
        self._last_action_date_time = response.get(self._LAST_ACTION_DATE_TIME, None)
        self._enrollment_status = response.get(self._ENROLLMENT_STATUS, None)

    def get_profile_id(self):
        """Returns the profile ID of the user"""
        return self._profile_id

    def get_locale(self):
        """Returns the locale of the user"""
        return self._locale

    def get_enrollment_speech_time(self):
        """Returns the total enrollment speech time of the user"""
        return self._enrollment_speech_time

    def get_remaining_enrollment_time(self):
        """Returns the remaining enrollment speech time of the user"""
        return self._remaining_enrollment_time

    def get_created_date_time(self):
        """Returns the creation date time of the user"""
        return self._created_date_time

    def get_last_action_date_time(self):
        """Returns the last action date time of the user"""
        return self._last_action_date_time

    def get_enrollment_status(self):
        """Returns the enrollment status of the user"""
        return self._enrollment_status
