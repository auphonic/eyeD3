import unittest
import os
from .. import DATA_D
import eyed3
from eyed3.id3.tag import Tag
from tempfile import mktemp
import shutil


# this can be any dummy MP3 file, doesn't matter which one!
# (the file won't be changed)
MP3_TESTFILE = os.path.join(DATA_D, "test.mp3")


class TmpMP3File:
    """ Helper function to get a temporary MP3 file for testing.
    """

    def __enter__(self):
        self.tmpfile = mktemp(".mp3")
        shutil.copy2(MP3_TESTFILE, self.tmpfile)
        return self.tmpfile

    def __exit__(self, type, value, traceback):
        os.remove(self.tmpfile)


@unittest.skipIf(not os.path.exists(MP3_TESTFILE), "test requires data files")
def test_chapter_title():
    """ Test chapter titles.
    """
    TITLE = "Main title"

    # chapter start+endtimes in sec and titles
    CHAPTERS = [
        [0, 10, "First Chapter"],
        [10, 15, "Second Chapter"],
    ]

    with TmpMP3File() as filename:
        audiofile = eyed3.load(filename)
        tag = Tag()
        tag.version = (2, 3, 0)
        audiofile.tag = tag

        # set a general title
        tag.title = TITLE

        # insert table of content frame
        # toc = eyed3_tag.setContentTableFrame()
        toc = tag.table_of_contents.set(
            "toc", toplevel=True,
            description=u"toplevel toc"
        )

        # insert chapters
        for i, data in enumerate(CHAPTERS):
            start_ms, stop_ms = data[0] * 1000, data[1] * 1000
            chap = tag.chapters.set("chp%d" % (i + 1), (start_ms, stop_ms))
            toc.child_ids.append(chap.element_id)

            # HACK to set the current id3 version in chapter marks for
            # rendering of sub frames
            chap.version = tag.header.version

            chap.title = data[2]

        # save audio file
        audiofile.tag.save(filename)

        # open file again for reading
        audiofile2 = eyed3.load(filename)
        tag2 = audiofile2.tag
        assert tag2.title == TITLE

        # TODO: check MP3 chapters !!!!!!!
