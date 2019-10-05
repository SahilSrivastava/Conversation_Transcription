class IdentificationResponse:
    """This class encapsulates the identification response."""

    _IDENTIFIED_PROFILE_ID = 'identifiedProfileId'
    _CONFIDENCE = 'confidence'

    def __init__(self, response):
        """Constructor of the IdentificationResponse class.

        Arguments:
        response -- the dictionary of the deserialized python response
        """
        self._identified_profile_id = response.get(self._IDENTIFIED_PROFILE_ID, None)
        self._confidence = response.get(self._CONFIDENCE, None)

    def get_identified_profile_id(self):
        """Returns the identified profile ID"""
        return self._identified_profile_id

    def get_confidence(self):
        """Returns the identification confidence"""
        return self._confidence
