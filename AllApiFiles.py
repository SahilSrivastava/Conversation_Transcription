import IdentificationServiceHttpClientHelper
import sys

locale = 'en-us'

def create_profile(subscription_key, locale):
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)
    creation_response = helper.create_profile(locale)
    return creation_response


def delete_profile(subscription_key, profile_id):
		""" Deletes a profile from the server

		Arguments:
    		profile_id -- the profile ID string of user to delete
		"""
		helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)
		helper.delete_profile(profile_id)


def enroll_profile(subscription_key, profile_id, file_path, force_short_audio):
    """Enrolls a profile on the server.

    Arguments:
        subscription_key -- the subscription key string
        profile_id -- the profile ID of the profile to enroll
        file_path -- the path of the file to use for enrollment
        force_short_audio -- waive the recommended minimum audio limit needed for enrollment
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    enrollment_response = helper.enroll_profile(
        profile_id,
        file_path,
        force_short_audio.lower() == "true")
    return enrollment_response


def get_profile(subscription_key, profile_id):
    """Get a speaker's profile with given profile ID

    Arguments:
        subscription_key -- the subscription key string
        profile_id -- the profile ID of the profile to resets
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    profile = helper.get_profile(profile_id)
    return profile


def print_all_profiles(subscription_key):
    """Print all the profiles for the given subscription key.

    Arguments:
        subscription_key -- the subscription key string
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    profiles = helper.get_all_profiles()

    return profiles


def reset_enrollments(subscription_key, profile_id):
    """Reset enrollments of a given profile from the server

    Arguments:
        subscription_key -- the subscription key string
        profile_id -- the profile ID of the profile to reset
    """

    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    helper.reset_enrollments(profile_id)

    print('Profile {0} has been successfully reset.'.format(profile_id))


def identify_file(subscription_key, file_path, force_short_audio, profile_ids):
    """Identify an audio file on the server.

    Arguments:
        subscription_key -- the subscription key string
        file_path -- the audio file path for identification
        profile_ids -- an array of test profile IDs strings
        force_short_audio -- waive the recommended minimum audio limit needed for enrollment
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    identification_response = helper.identify_file(
        file_path, profile_ids,
        force_short_audio.lower() == "true")
    return identification_response
