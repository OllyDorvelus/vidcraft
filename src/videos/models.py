from django.db import models
from accounts.validators import validate_file_extension

from django.utils import timezone
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.db.models.signals import post_save
import string
import random

from django.db.utils import IntegrityError
from django.db       import models, transaction
from django.db       import transaction
# Create your models here.


# class RandomPrimaryIdModel(models.Model):
#     KEYPREFIX         = ""
#     KEYSUFFIX         = ""
#     CRYPT_KEY_LEN_MIN = 5
#     CRYPT_KEY_LEN_MAX = 9
#     _FIRSTIDCHAR      = string.ascii_letters                  # First char: Always a letter
#     _IDCHARS          = string.digits + string.ascii_letters  # Letters and digits for the rest
#
#     """ Our new ID field """
#     newid = models.CharField(db_index    = True,
#                           primary_key = True,
#                           max_length  = CRYPT_KEY_LEN_MAX+1+len(KEYPREFIX)+len(KEYSUFFIX),
#                           unique      = True)
#
#     def __str__(self, *args, **kwargs):
#         """
#         Nothing to do but to call the super class' __init__ method and initialize a few vars.
#         """
#         super(RandomPrimaryIdModel, self).__str__(*args, **kwargs)
#         self._retry_count = 0    # used for testing and debugging, nothing else
#
#     def _make_random_key(self, key_len):
#         """
#         Produce a new unique primary key.
#         This ID always starts with a letter, but can then have numbers
#         or letters in the remaining positions.
#         Whatever is specified in KEYPREFIX or KEYSUFFIX is pre/appended
#         to the generated key.
#         """
#         return self.KEYPREFIX + random.choice(self._FIRSTIDCHAR) + \
#                ''.join([ random.choice(self._IDCHARS) for dummy in range(0, key_len-1) ]) + \
#                self.KEYSUFFIX
#
#     def save(self, *args, **kwargs):
#         """
#         Modified save() function, which selects a special unique ID if necessary.
#         Calls the save() method of the first model.Models base class it can find
#         in the base-class list.
#         """
#         if self.id:
#             # Apparently, we know our ID already, so we don't have to
#             # do anything special here.
#             super(RandomPrimaryIdModel, self).save(*args, **kwargs)
#             return
#
#         try_key_len                     = self.CRYPT_KEY_LEN_MIN
#         try_since_last_key_len_increase = 0
#         while try_key_len <= self.CRYPT_KEY_LEN_MAX:
#             # Randomly choose a new unique key
#             _id = self._make_random_key(try_key_len)
#             sid = transaction.savepoint()       # Needed for Postgres, doesn't harm the others
#             try:
#                 if kwargs is None:
#                     kwargs = dict()
#                 kwargs['force_insert'] = True           # If force_insert is already present in
#                                                         # kwargs, we want to make sure it's
#                                                         # overwritten. Also, by putting it here
#                                                         # we can be sure we don't accidentally
#                                                         # specify it twice.
#                 self.id = _id
#                 super(RandomPrimaryIdModel, self).save(*args, **kwargs)
#                 break                                   # This was a success, so we are done here
#
#             except IntegrityError as e:                   # Apparently, this key is already in use
#                 # Only way to differentiate between different IntegrityErrors is to look
#                 # into the message string. Too bad. But I need to make sure I only catch
#                 # the ones for the 'id' column.
#                 #
#                 # Sadly, error messages from different databases look different and Django does
#                 # not normalize them. So I need to run more than one test. One of these days, I
#                 # could probably just examine the database settings, figure out which DB we use
#                 # and then do just a single correct test.
#                 #
#                 # Just to complicates things a bit, the actual error message is not always in
#                 # e.message, but may be in the args of the exception. The args list can vary
#                 # in length, but so far it seems that the message is always the last one in
#                 # the args list. So, that's where I get the message string from. Then I do my
#                 # DB specific tests on the message string.
#                 #
#                 msg = e.args[-1]
#                 if msg.endswith("for key 'PRIMARY'") or msg == "column id is not unique" or \
#                         "Key (id)=" in msg:
#                     transaction.savepoint_rollback(sid) # Needs to be done for Postgres, since
#                                                         # otherwise the whole transaction is
#                                                         # cancelled, if this is part of a larger
#                                                         # transaction.
#
#                     self._retry_count += 1              # Maintained for debugging/testing purposes
#                     try_since_last_key_len_increase += 1
#                     if try_since_last_key_len_increase == try_key_len:
#                         # Every key-len tries, we increase the key length by 1.
#                         # This means we only try a few times at the start, but then try more
#                         # and more for larger key sizes.
#                         try_key_len += 1
#                         try_since_last_key_len_increase = 0
#                 else:
#                     # Some other IntegrityError? Need to re-raise it...
#                     raise e
#
#         else:
#             # while ... else (just as a reminder): Execute 'else' if while loop is exited normally.
#             # In our case, this only happens if we finally run out of attempts to find a key.
#             self.id = None
#             raise IntegrityError("Could not produce unique ID for model of type %s" % type(self))
#
#     class Meta:
#         abstract = True







class VideoModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='videos')
    #user = models.ManyToOneRel(settings.AUTH_USER_MODEL, related_name='profile')
    #following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    #thumbnail = models.FileField(validators=[validate_file_extension], default="vidcraftavatar.png")
    video = models.FileField(upload_to="mp4video")
    title = models.CharField(max_length=115, blank=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    description = models.TextField(blank=True)
    added_date = models.DateField(auto_now=False, auto_now_add=True)
    last_edited = models.DateField(auto_now=True, auto_now_add=False)
    #objects = VideModelManager()

    def __str__(self):
        return self.title + '-' + self.user.username



    # def get_absolute_url(self):
    #     return reverse('accounts:profile_detail', kwargs={'username': self.user.username})

# subprocess.check_call(
#             ['ffmpeg', '-v', '-8', '-i', input_video, '-vf', 'scale=-2:480', '-preset', 'slow',
#              '-c:v', 'libx264', '-strict', 'experimental', '-c:a', 'aac', '-crf', '20', '-maxrate', '500k',
#              '-bufsize', '500k', '-r', '25', '-f', 'mp4', output_video_mp4, '-y'])