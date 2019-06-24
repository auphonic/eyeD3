import unittest
import os
from .. import DATA_D
import eyed3
from eyed3.id3.tag import Tag
from tempfile import mktemp
import shutil
import base64


# this can be any dummy MP3 file, doesn't matter which one!
# (the file won't be changed)
MP3_TESTFILE = os.path.join(DATA_D, "test.mp3")

# base64 encoded test image (PNG)
IMAGE_TESTFILE = b"iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAAK1AAACtQGtywvYAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAo5QTFRF////AAAAAAAAVVVVQEBAMzMzKysrJCQkQEBAOTk5MzMzLi4uKysrOzs7Nzc3MzMzMDAwPDw8OTk5NjY2MzMzMTExOjo6Nzc3MzMzMTExOTk5Nzc3NTU1MzMzMTExODg4NjY2NTU1MzMzMjIyNzc3NjY2NDQ0MzMzODg4Nzc3NTU1Nzc3NjY2NTU1MzMzNzc3NjY2NDQ0MzMzNzc3NjY2NTU1NDQ0MzMzNjY2NTU1NTU1NDQ0Nzc3NTU1NDQ0Nzc3NjY2NTU1NDQ0NDQ0NjY2NjY2NDQ0NDQ0NjY2NjY2NTU1NDQ0NTU1NDQ0NDQ0NjY2NTU1NDQ0NjY2NTU1NTU1NDQ0NjY2NTU1NTU1NjY2NTU1NTU1NDQ0NDQ0NjY2NTU1NTU1NDQ0NjY2NTU1NTU1NDQ0NjY2NTU1NTU1NDQ0NTU1NDQ0NTU1NTU1NTU1NDQ0NjY2NTU1NTU1NTU1NDQ0NjY2NTU1NTU1NDQ0NjY2NTU1NTU1NTU1NjY2NTU1NTU1NTU1NDQ0NjY2NTU1NTU1NDQ0NTU1NTU1NTU1NDQ0NTU1NTU1NTU1NjY2NTU1NTU1NTU1NjY2NTU1NTU1NDQ0NjY2NTU1NjY2NTU1NDQ0NTU1NTU1NTU1NTU1NDQ0NTU1NTU1NTU1NjY2NTU1NTU1NTU1NjY2NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NDQ0NTU1NTU1NTU1NTU1NjY2NTU1NTU1NTU1NTU1NjY2NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NjY2NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1NTU1b+n5DwAAANl0Uk5TAAECAwQFBgcICQoLDA0ODxAREhMUFRYXGRobHB0eHyAhIiMkJSYnKCkqKy4vMDIzNDY3ODk6Ozw9Pj9AQUNFRkdISUpLTE5PUFFSU1dYWVpbXV9gYWJjZWZoaWprbG1ub3Byc3R1d3h5en5/gYKDhIWGh4iJiouMjY6PkJGTlJWWl5iam5yen6Cho6Slpqepqqutrq+wsrW3ubq7vL2+v8DCw8TGx8jJysvMzc7P0NLT1NXW19jZ2tvc3d7f4OHi5Obo6err7O3u7/Dx8vP09fb3+Pn6+/z9/uoCY0kAAAP4SURBVBgZ7cGLV5NlAAfg34BNhDGuk9ZEKaApmIBYEJaBZVJCBBMEb7XUlmU3g7KUzAJbVHZRorJwmZqZDEMtIrULIoORyQDd77+p93u/jYHDy/F0Tp3D82DKlH+bPmNR+fony+5Jj8aNm7Vu358M8Hy26lbcgMzNLl7h6DMWXJ+UZh9DurzLjGuLe8XLSV18yYBrqOnjVfVacTXat3lNDRGYlPFrXoevEjCJeWcY7PiWquKsJOO8JdV1JxisOxMhzfVwzLe22xAkfWM7x7jTEUJ8FwM6H8JEmtIuBpw04Arh++jXWxWOELRrPPRrDcNE2+n3QyomMedn+tVhglL6tRoQJDoKQRL3028Zxpl2hqp3w6CKf+zDU4PkwMndpQaotHuo6tIi2HqqDuggpTaPMmC4yQwp6ihVaxAkro/SaSMUuq3DHGfoZS0Upt8o9cRgTB2l0SwojAd4hbYEKHIuUdqMgMQhSm9CMfM0Q+i6BYpdlC4Y4FdJ6UIyhOh2hnRkOgTzEKVS+O2l9BwUeziJD6Cop7Qbqul/UTGaAOFBBpz/Ykv9l24G3Ach+TIVHh2kZZTaIIR1UOUuh6JygKrvNBAOUiqC9A6lJyCUULXfBNXMb6gqhvAUpZ2Q2inNhtBM6fd4BBjPUWqEYKF0CFIPFb9CiHBTegBBHqH0RxiEc1SchSLCR8VBCNmUDmMcF6VMCMeoGNZAMFP6BMIySm9gnCZKRRBaKSVByKXUAGEVpSqMs5rSCgiNlLIgFLqklRBqXFIOxilwSZUQ1rqkPPy36Wofxk2J42FcJ31OWgSQNHsaYJqFWBOi0wDE8zCMcRC0aQYAuljAGA5oIrUANGY9VHt8ZPccOJgHuLywjzhH2LMYCfT8wktOPXR1w2Tb7bDy/S72b0IeHYjcMkh2zIeiaEn266yHg3lAhxd2flxS1zuSlUh3w9pj3IDn+b31PXZEWNnV8KzHN2shHXiNPz5d2ZgAlXkhf4KDecBxL+ysBTbRnkQnsIiNmkGmAC7ea6UN2Mmld9GhG7lkRMAL3SQH4GAe0OmFnbVAPluS6AQs3GtiJ4CtrLbSBthYczcdmTyEgDv56YI7evuxncXACS/srAXWsclIJ2BhS5hnKAr4nAVW2gAbV+bTMYP9Ovg9yh3T0jwDsLE1f7XbCzsbjEWdLJlBJ2BhCz7ituSK4b5IK22AjdUFdOAIX03WZGsg6E7R13++H6Y+kue9sPMfvm1IphOwsAUxh0i658NKG2DjikI6MPcsRy+yEFLu/dr0fCB2aUWmaTHs3Li83ALoinMBfckCIDz38WI9kLI8A8goSzWWLQBiKl7ckI+Q7LTiphS9tRBTpvzf/A2EZL5vEPHvbAAAAABJRU5ErkJggg=="


class TmpMP3File:
    """ Helper function to get a temporary MP3 file for testing.
    """

    def __enter__(self):
        self.tmpfile = mktemp(".mp3")
        shutil.copy2(MP3_TESTFILE, self.tmpfile)
        return self.tmpfile

    def __exit__(self, type, value, traceback):
        os.remove(self.tmpfile)


class TmpPNGFile:
    """ Helper function to get a temporary PNG image file for testing.
    """

    def __enter__(self):
        self.tmpfile = mktemp(".png")

        # write base64 encoded image for testing
        f = open(self.tmpfile, 'wb')
        f.write(base64.decodebytes(IMAGE_TESTFILE))
        f.close()

        return self.tmpfile

    def __exit__(self, type, value, traceback):
        os.remove(self.tmpfile)


@unittest.skipIf(not os.path.exists(MP3_TESTFILE), "test requires data files")
def test_chapter_marks():
    """ Test chapter mark titles, URLs and images.
    """
    TITLE = "Main title"

    # chapter start+endtimes in sec, title, chapter URL, chapter image
    CHAPTERS = [
        [0, 2, "First Chapter", None, None],
        [2, 3, 'Begrüßung', None, None],
        [3, 4, "third marks – Unicode", "http://auphonic.com/test", None],
        [4, 5, "Fourth", None, IMAGE_TESTFILE],
        [5, 6, "Fifth", "de.wikipedia.org/wiki/%C3%9Cberfall_%28Milit%C3%A4r%29", None],
        [6, 6.5, "Sixth", "http://www.youtube.com/watch?v=zvCBSSwgtg4&feature=endscreen&NR=1", None],
        [6.5, 6.80, "No Title", "https://alpha.app.net/friolz/post/6394826", IMAGE_TESTFILE],
        [6.8, 7.08, "", u"https://alpha.app.net/friolz/post/6378645426", None],
    ]

    with TmpMP3File() as filename:
        audiofile = eyed3.load(filename)
        tag = Tag()
        tag.version = (2, 3, 0)  # set ID3 version (2.3 here)
        audiofile.tag = tag

        # set a general title
        tag.title = TITLE

        # insert table of content frame
        # toc = eyed3_tag.setContentTableFrame()
        toc = tag.table_of_contents.set(
            "toc", toplevel=True, description="toplevel toc"
        )

        # insert chapters
        for i, data in enumerate(CHAPTERS):
            start_ms, stop_ms = data[0] * 1000, data[1] * 1000
            chap = tag.chapters.set("chp%d" % (i + 1), (start_ms, stop_ms))
            toc.child_ids.append(chap.element_id)

            # HACK to set the current id3 version in chapter marks for
            # rendering of sub frames
            chap.version = tag.header.version

            # add chapter title
            chap.title = data[2]

            # add chapter URL if we have one
            if data[3]:
                chap.user_url = data[3]

            # add chapter image if we have one
            if data[4]:
                with TmpPNGFile() as image_file:
                    chap.chapter_image = image_file

        # save audio file
        audiofile.tag.save(filename)

        # open file again for reading
        audiofile2 = eyed3.load(filename)
        tag2 = audiofile2.tag
        assert tag2.title == TITLE

        # read back chapters for testing
        sorted_chap = sorted([c for c in tag2.chapters], key=lambda ch: ch.times.start)
        for i, chap in enumerate(sorted_chap):
            assert chap.times.start == CHAPTERS[i][0] * 1000
            assert chap.times.end == CHAPTERS[i][1] * 1000
            assert chap.title == CHAPTERS[i][2]
            assert chap.user_url == CHAPTERS[i][3]

            # compare chapter image to IMAGE_TESTFILE (base64 encoded)
            if CHAPTERS[i][4]:
                test_image = base64.decodebytes(IMAGE_TESTFILE)
                assert test_image == chap.chapter_image
